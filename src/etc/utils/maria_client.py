import json
import pymysql


def get_connection(config_path):
    conn = None
    with open(config_path, encoding="UTF-8") as file_:
        db_config = json.loads(file_.read())['test']
        conn = pymysql.connect(host=db_config['host'], port=db_config['port'],
                               user=db_config['user'], password=db_config['password'],
                               db=db_config['database'], charset=db_config['charset'])
    return conn


if __name__ == '__main__':
    conn = get_connection('/srv/stock/config/config.json')
    with conn.cursor() as curs:
        rs = curs.execute("SELECT 1")
        print(f'test rs : {rs}')
    conn.close()
