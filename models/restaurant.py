from models.base_model import BaseModel
import peewee as pw

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
