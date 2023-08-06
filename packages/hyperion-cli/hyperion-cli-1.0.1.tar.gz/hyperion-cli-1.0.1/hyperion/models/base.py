from peewee import Model, SqliteDatabase, Proxy
from playhouse.shortcuts import model_to_dict

database_proxy = Proxy()


class BaseModel(Model):
    """
    Defines some base properties for a model.
    """

    def serialize(self):
        return model_to_dict(self)

    class Meta:
        database: SqliteDatabase = database_proxy
