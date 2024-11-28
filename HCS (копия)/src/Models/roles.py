from src.Models.BaseModel import *


class Roles(BaseModel):
    role_id = PrimaryKeyField()
    role_name = CharField()
