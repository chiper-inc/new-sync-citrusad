import mysql.connector

from configs.mysql_config import MYSQL_CONFIG

print("conectandose a la base de datos")
mysql_client = mysql.connector.connect(user =MYSQL_CONFIG['USER_MYSQL'],
                                       password= MYSQL_CONFIG['PASSWORD_MYSQL'],
                                       host= MYSQL_CONFIG['HOST_MYSQL'],
                                       database= MYSQL_CONFIG['NAME_MYSQL'])
print("base de datos conectado")