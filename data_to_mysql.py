import pymysql
import csv
import codecs


def get_conn():
    db = pymysql.connect(host="localhost",port=3306,
                   user="root",password="886886",
                   db="search",charset="utf8")
    return db


def insert(cur, sql, args):
    try:
        cur.execute(sql, args)
    except Exception as e:
        print(e)
        # db.rollback()


def read_csv_to_mysql(filename):
    with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        head = next(reader)
        print(head)
        conn = get_conn()
        cur = conn.cursor()
        sql = 'insert into job values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        for item in reader:
            # if item[1] is None or item[1] == '':  # item[1]作为唯一键，不能为null
            #     continue
            args = tuple(item)
            print(args)
            insert(cur, sql=sql, args=args)
            print("成功")
        conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    read_csv_to_mysql(r"qcwy_pre1.csv")
