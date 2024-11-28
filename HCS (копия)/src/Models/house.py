from src.Models.BaseModel import *


class House(BaseModel):
    id = PrimaryKeyField()
    address = CharField()
    number_apartments = IntegerField()
    house_type = CharField()


