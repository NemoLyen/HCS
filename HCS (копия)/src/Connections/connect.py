from peewee import *
mysql_db = MySQLDatabase('SamE1234_HCS', user ='SamE1234_NEMO', password = 'gadzila555', host = '10.11.13.118', port = 3306)

if __name__ == "__main__":
    mysql_db.connect()