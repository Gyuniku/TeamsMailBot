import smtplib
from email.message import EmailMessage

mine = {'type': 'text', 'subtype': 'comma-separated-values'}


class MailUtil:
    # メールオブジェクトを返します。
    @classmethod
    def create_message(cls, from_addr, to_addr, subject, body, attach_file):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg.set_content(body)
        # 添付ファイルを追加
        file = open(attach_file['path'], 'rb')
        file_read = file.read()
        msg.add_attachment(file_read, maintype=mine['type'], subtype=mine['subtype'], filename=attach_file['name'])
        file.close()
        return msg

    # メールを送信します。
    @classmethod
    def send(cls, from_addr, to_addr, msg, password):
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(from_addr, password)
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        smtpobj.close()
