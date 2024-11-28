from src.Models.BaseModel import *


class Payments(BaseModel):
    id = PrimaryKeyField()
    residents_id = IntegerField()
    services_id = IntegerField()
    payment_date = DateTimeField()
    amount = DecimalField()
    status = CharField()