from src.Models.BaseModel import *


class Services(BaseModel):
    service_id = PrimaryKeyField()
    service_name = CharField()
    description = TextField()
    cost = DecimalField()

