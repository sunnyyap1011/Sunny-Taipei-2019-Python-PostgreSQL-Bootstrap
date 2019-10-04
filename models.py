import os
import peewee as pw
import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(os.getenv('DATABASE'))

class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    # def update(self, *args, **kwargs):
    #     self.errors = []

    #     if len(self.errors) == 0:
    #         self.updated_at = datetime.datetime.now()
    #         return super(BaseModel, self).save(*args, **kwargs)
    #     else:
    #         return 0

    class Meta:
        database = db
        legacy_table_names = False

class Restaurant(BaseModel):
    name = pw.CharField(unique=True)
    address = pw.CharField()
    google_map_link = pw.CharField(null=True)
    area_code = pw.CharField(null=True)
    must_try = pw.CharField(null=True)

    def validate(self):
        duplicate_name = Restaurant.get_or_none(Restaurant.name == self.name)
        duplicate_address = Restaurant.get_or_none(Restaurant.address == self.address)

        if not self.id and duplicate_name:
            self.errors.append('Restaurant name not unique')
        if not self.id and duplicate_address:
            self.errors.append('Restaurant address already existed')

# class Warehouse(BaseModel):
#     store = pw.ForeignKeyField(Store, backref='warehouses', unique=True)
#     location = pw.TextField()

#     def validate(self):
#         duplicate_stores_id = Warehouse.get_or_none(Warehouse.store_id == self.store_id)

#         if duplicate_stores_id:
#             self.errors.append('Store id not unique')

# class Product(BaseModel):
#     name = pw.CharField(index=True)
#     description = pw.TextField()
#     warehouse = pw.ForeignKeyField(Warehouse, backref='products')
#     color = pw.CharField(null=True)