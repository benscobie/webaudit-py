import pymysql.cursors
import configparser

_connection = None

def get_connection():
    global _connection
    if not _connection:
        config = configparser.ConfigParser()
        config.read('config.ini')
        _connection = pymysql.connect(host=config['DATABASE']['Server'],user=config['DATABASE']['Username'],passwd=config['DATABASE']['Password'],db=config['DATABASE']['Database'])
    return _connection