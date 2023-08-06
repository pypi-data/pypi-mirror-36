from . import mysql_base2
from . import MysqlBase


class JavDao(MysqlBase):

    def __init__(self):
        # o class JavDao(mysql_base2.MysqlBase2):
        # x class JavDao(MysqlBase):
        print('abc')

    def __get_sql_select(self):
        sql = 'SELECT id' \
                '  , title, post_date, package, thumbnail ' \
                '  , sell_date, actress, maker, label ' \
                '  , download_links, download_files, url, is_selection ' \
                '  , product_number, rating, is_site, is_parse2 ' \
                '  , makers_id ' \
                '  , created_at, updated_at ' \
                '  FROM jav '

        return sql

    def __get_list(self, rs):

        javs = []
        for row in rs:
            jav = site_data.JavData()
            jav.id = row[0]
            jav.title = row[1]
            jav.postDate = row[2]
            jav.package = row[3]
            jav.thumbnail = row[4]
            jav.sellDate = row[5]
            jav.actress = row[6]
            jav.maker = row[7]
            jav.label = row[8]
            jav.downloadLinks = row[9]
            jav.downloadFiles = row[10]
            jav.url = row[11]
            jav.isSelection = row[12]
            jav.productNumber = row[13]
            jav.rating = row[14]
            jav.isSite = row[15]
            jav.isParse2 = row[16]
            jav.makersId = row[17]
            jav.createdAt = row[18]
            jav.updatedAt = row[19]
            javs.append(jav)

        return javs

