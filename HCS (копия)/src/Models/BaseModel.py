from src.Connections.connect import *

class BaseModel(Model):
    class Meta:
        database = mysql_db