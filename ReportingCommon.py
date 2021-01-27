import pymysql.cursors
import yaml
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

class ReportingCommon:
    DATETIME_FORMAT_IN_SQL = '%Y-%m-%d'
    DATETIME_FORMAT_IN_TEXT = '%Y/%m/%d %H:%M'
    DATETIME_FORMAT_FILENAME = '%Y%m%d_%H%M'

    # 設定ファイルを読み込んで設定情報を返します。
    @classmethod
    def load_config(cls):
        file = open('config.yml', 'r+', encoding='utf-8')
        config = yaml.load(file)
        file.close()
        return config

    # SQLファイルを読み込んで返します。
    @classmethod
    def load_purchase_status_sql(cls):
        file = open('sql/test.sql', 'r', encoding='utf-8')
        purchase_sql = file.read()
        file.close()
        return purchase_sql

    # DBへの接続を行い、接続用オブジェクトを返します。
    @classmethod
    def setup_db(cls, config):
        conn = pymysql.connect(host=config['db']['host'], user=config['db']['user_name'],
                               password=config['db']['password'],
                               db=config['db']['db_name'], charset=config['db']['charset'],
                               cursorclass=pymysql.cursors.DictCursor)
        return conn
