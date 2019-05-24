"""
    上传文本词典到数据库dict
"""
import pymysql
import re

fd = open('dict.txt')
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='123456',
                     database='dict',
                     charset='utf8', )
cur = db.cursor()
sql = "insert into words values (%s,%s,%s)"
n = 1
for line in fd:
    # 获取匹配内容元组 (word,mean)
    tup = re.findall(r'(\w+)\s+(.*)', line)[0]
    try:
        cur.execute(sql, [n, tup[0], tup[1]])
        db.commit()
    except Exception:
        db.rollback()
    n += 1
fd.close()
cur.close()
db.close()
