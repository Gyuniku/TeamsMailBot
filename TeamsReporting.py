import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../python-3.7.1-embed-win32\Lib\site-packages'))
from datetime import datetime
import ReportingCommon
import TeamsUtil
from prettytable import PrettyTable


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), ''))
    # 設定ファイル読み込み
    reporting_common = ReportingCommon.ReportingCommon()
    config = reporting_common.load_config()
    # SQLファイル読み込み
    purchase_sql = reporting_common.load_today_purchase_status_sql()
    duplicated_sql = reporting_common.load_duplicated_purchase_sql()
    members_sql = reporting_common.load_members_sql()
    # DBに接続
    conn = reporting_common.setup_db(config)

    # 現在日時
    now_str_in_sql = datetime.now().strftime(reporting_common.DATETIME_FORMAT_IN_SQL)
    now_str_in_text = datetime.now().strftime(reporting_common.DATETIME_FORMAT_IN_TEXT)
    now_str_file = datetime.now().strftime(reporting_common.DATETIME_FORMAT_FILENAME)

    # SQLを発行
    try:
        with conn.cursor() as cursor:
            cursor.execute(purchase_sql, {'date': now_str_in_sql})
            ticket_status = cursor.fetchall()
            cursor.execute(duplicated_sql)
            duplicated_purchase = cursor.fetchall()
            cursor.execute(members_sql)
            members = cursor.fetchall()
    finally:
        conn.close()

    # Teamsの本文を作成
    message = ''
    message += '【購入状況】<br>'
    if not ticket_status:
        message += '本日列車運行なし'
    else:
        # 購入情報の表を作成
        purchases_table = PrettyTable()
        # 表ヘッダを作成
        purchases_labels = ['列1', '列2', '列3', '列4', '列5', '列6', '列7', '列8', '列9', '列10', '列11', '列12', '列13']
        purchases_table.field_names = purchases_labels

        # 表データを作成
        for dic in ticket_status:
            row = []
            for value in dic.values():
                row.append(value)
            purchases_table.add_row(row)

        message += str(purchases_table)

    # 重複購入者情報を追加
    message += '<br><br>【重複購入者情報】<br>'
    # 重複があるかの情報を本文に追加
    if not duplicated_purchase:
        message += '重複購入者：なし<br>'
    else:
        message += '重複購入者(購入ID)：' + str(duplicated_purchase) + '<br>'

    # 会員情報を追加
    message += '<br>【会員登録情報】<br>'
    members_table = PrettyTable()
    members_labels = []
    for key in members[0].keys():
        members_labels.append(key)
    members_table.field_names = members_labels

    for dic in members:
        row = []
        for value in dic.values():
            row.append(value)
        members_table.add_row(row)

    message += str(members_table)

    # 表のAAがTeams上で崩れてしまうことを防ぐ
    message = message.replace('\n', '<br>')
    message = message.replace(' ', '   ')
    message = message.replace('-', '. ')

    # Teamsに投稿
    teams = TeamsUtil.TeamsUtil()
    title = now_str_in_text + ' ' + config['teams']['title']
    teams.post_to_teams(title, message, config['teams']['uri'])


if __name__ == '__main__':
    main()