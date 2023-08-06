from django.db.models.sql.query import Query
from django.core import checks

__all__ = ['CheckConstraint']


class CheckConstraint:

    def __init__(self, constraint, name):
        self.constraint = constraint
        self.name = name

    def constraint_sql(self, model, schema_editor):
        query = Query(model)
        where = query.build_where(self.constraint)
        connection = schema_editor.connection
        compiler = connection.ops.compiler('SQLCompiler')(query, connection, 'default')
        sql, params = where.as_sql(compiler, connection)
        params = tuple(schema_editor.quote_value(p) for p in params)
        return schema_editor.sql_check % {
            'name': schema_editor.quote_name(self.name),
            'check': sql % params,
        }

    def create_sql(self, model, schema_editor):
        sql = self.constraint_sql(model, schema_editor)
        return schema_editor.sql_create_check % {
            'table': schema_editor.quote_name(model._meta.db_table),
            'check': sql,
        }

    def remove_sql(self, model, schema_editor):
        quote_name = schema_editor.quote_name
        return schema_editor.sql_delete_check % {
            'table': quote_name(model._meta.db_table),
            'name': quote_name(self.name),
        }

    def __repr__(self):
        return "<%s: constraint='%s' name='%s'>" % (self.__class__.__name__, self.constraint, self.name)

    def __eq__(self, other):
        return (
            isinstance(other, CheckConstraint) and
            self.name == other.name and
            self.constraint == other.constraint
        )

    def deconstruct(self):
        path = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        path = path.replace('django.db.models.constraints', 'django.db.models')
        return (path, (), {'constraint': self.constraint, 'name': self.name})

    def clone(self):
        _, args, kwargs = self.deconstruct()
        return self.__class__(*args, **kwargs)


class CheckKaratFields:

    def __init__(self, cls):
        self.cls = cls
        self.karat_table = cls._meta.karat_table
        self.karat_fields = cls._meta.karat_fields
        self.model_fields = cls._meta.get_fields()
        self.model_fields_names = [field.name for field in self.model_fields]

    def check_karat_table(self):
        errors = []
        if not self.karat_table and self.karat_fields:
            errors.append(
                checks.Error(
                    'missing field `karat_table` in Meta',
                    hint="add field `karat_table` to Meta or remove field `karat_fields`",
                    obj=self.cls,
                    id='karat.E001'
                )
            )
        elif not isinstance(self.karat_table, str):
            errors.append(
                checks.Error(
                    'field `karat_table` must be string',
                    obj=self.cls,
                    id='karat.E002'
                )
            )
        if self.karat_table and not self.karat_fields:
            errors.append(
                checks.Warning(
                    'missing field `karat_fields` in Meta',
                    hint="if not added all fields be used to karat_fields similiar to `__all__`",
                    obj=self.cls,
                    id='karat.W001'
                )
            )
        return errors

    def check_karat_fields(self):
        errors = []
        if (
            (isinstance(self.karat_fields, str) and self.karat_fields != '__all__')
            or not isinstance(self.karat_fields, (str, dict, list))
        ):
            errors.append(
                checks.Error(
                    'field `karat_fields` has to be `__all__`, list or dict',
                    hint="change field to correct type",
                    obj=self.cls,
                    id='karat.E003'
                )
            )
        if self.karat_fields and not '__all__':
            for field in self.karat_fields:
                if not field in model_fields:
                    errors.append(
                        checks.Error(
                            "doesn't have field {}".format(field),
                            hint="Correct typo in model",
                            obj=self.cls,
                            id='karat.E004'
                        )
                    )
        elif isinstance(self.karat_fields, dict):
            has_unique_id = False
            for field, karat_field in self.karat_fields.items():
                if not field in self.model_fields_names:
                    errors.append(
                        checks.Error(
                            "doesn't have field {}".format(field),
                            hint="Correct typo in model key",
                            obj=self.cls,
                            id='karat.E004'
                        )
                    )

        return errors

    def check_uniqueness(self):
        errors = []
        unique = False
        for field in self.model_fields:
            if unique:
                break

            if field.get_internal_type() != 'OneToOneField':
                if field.get_internal_type() == 'ForeignKey' or not field.unique:
                    continue

            if isinstance(self.karat_fields, dict):
                if field.name in self.karat_fields.keys():
                    unique = True
            else:
                if field.name in self.karat_fields:
                    unique = True

        if not unique:
            errors.append(
                checks.Error(
                    "class doesn't have unique in `karat_fields` used to connect dbs",
                    hint="Add unique field for id from karat db",
                    obj=self.cls,
                    id='karat.E004'
                )
            )

        return errors
