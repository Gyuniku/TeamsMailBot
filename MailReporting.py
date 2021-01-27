import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../python-3.7.1-embed-win32\Lib\site-packages'))
import csv
import MailUtil
from datetime import datetime
import os
import ReportingCommon


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), ''))
    # 設定ファイル読み込み
    reporting_common = ReportingCommon.ReportingCommon()
    config = reporting_common.load_config()
    # SQLファイル読み込み
    purchase_sql = reporting_common.load_purchase_status_sql()
    duplicated_sql = reporting_common.load_duplicated_purchase_sql()
    members_sql = reporting_common.load_members_sql()
    # DBに接続
    conn = reporting_common.setup_db(config)

    # 現在日時
    now_str_in_text = datetime.now().strftime(reporting_common.DATETIME_FORMAT_IN_TEXT)
    now_str_file = datetime.now().strftime(reporting_common.DATETIME_FORMAT_FILENAME)

    # SQLを発行
    try:
        with conn.cursor() as cursor:
            cursor.execute(purchase_sql)
            ticket_status = cursor.fetchall()
            cursor.execute(duplicated_sql)
            duplicated_purchase = cursor.fetchall()
            cursor.execute(members_sql)
            members = cursor.fetchall()
    finally:
        conn.close()

    # CSVに書き込む
    with open(now_str_file + '_purchases.csv', 'w', newline='') as file:
        header = ['列1', '列2', '列3', '列4', '列5', '列6', '列7', '列8',
                  '列9', '列10', '列11', '列12', '列13']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(ticket_status)

    # メール作成
    mail = MailUtil.MailUtil()
    # タイトルに現在日時を埋め込む
    subject = '【' + now_str_in_text + '】' + config['mail']['base_subject']
    body = config['mail']['base_body'] + '\n算出日時：' + now_str_in_text

    # 重複があるかの情報を本文に追加
    if not duplicated_purchase:
        body += '\n\n重複購入者：なし\n'
    else:
        body += '\n\n重複購入者(購入ID)：' + str(duplicated_purchase) + '\n'

    # 会員情報を本文に追加
    for dic in members:
        body += '\n【会員登録状況】\n' + dic['会員状態'] + '：' + str(dic['件数'])

    # CSVを添付してメール送信
    ATTACH_FILE = {'name': now_str_file + '_purchases.csv', 'path': './' + now_str_file + '_purchases.csv'}
    msg = mail.create_message(config['mail']['from_address'], config['mail']['to_address'], subject, body, ATTACH_FILE)
    mail.send(config['mail']['from_address'], config['mail']['to_address'], msg, config['mail']['password'])

    # CSVファイルを削除
    os.remove(now_str_file + '_purchases.csv')


if __name__ == '__main__':
    main()