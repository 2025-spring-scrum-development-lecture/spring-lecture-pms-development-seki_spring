import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(to, subject, body):
    """
    メール送信関数
    
    Parameters:
    to (str): 送信先メールアドレス
    subject (str): メールの件名
    body (str): メール本文（HTML形式）
    """
    ID = 'a.seki.sys24@morijyobi.ac.jp'
    PASS = os.environ['MAIL_PASS']
    HOST = 'smtp.gmail.com'
    PORT = 587
    
    msg = MIMEMultipart()
    
    msg.attach(MIMEText(body, 'html'))
    
    msg['Subject'] = subject
    msg['From'] = ID
    msg['To'] = to  # 引数で受け取ったメールアドレスを使用
    
    server = SMTP(HOST, PORT)
    server.starttls()
    server.login(ID, PASS)
    
    server.send_message(msg)
    server.quit()
