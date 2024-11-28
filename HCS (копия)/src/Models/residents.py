from src.Models.BaseModel import *


class Residents(BaseModel):
    resident_id = PrimaryKeyField()
    surname = CharField()
    name = CharField()
    birthdate = DateTimeField()
    apartment_number = CharField()
    telephone = CharField()
    roles_id = CharField()
    login = CharField()
    password = CharField()