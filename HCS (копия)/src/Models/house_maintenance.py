from enum import EnumMeta
from src.Models.house import House

from src.Models.BaseModel import *


class House_maintenance(BaseModel):
    maintenance_id = PrimaryKeyField()
    house_id = ForeignKeyField(House)
    service_type = CharField()
    maintenance_date = DateTimeField()
    status = CharField()
    notes = TextField()

