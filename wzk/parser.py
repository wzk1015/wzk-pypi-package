from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from email.header import Header
from time import sleep, ctime
from requests import get

from wzk.utils import diff_compare


class MailSender:
    def __init__(self, host, mail_addr, password):
        self.mail_host = host  #设置SMTP服务器，如smtp.qq.com
        self.mail_user = mail_addr  #发送邮箱的用户名，如xxxxxx@qq.com
        self.mail_pass = password  #发送邮箱的密码（注：QQ邮箱需要开启SMTP服务后在此填写授权码）
        self.sender = mail_addr  #发件邮箱，如xxxxxx@qq.com

    def send_mail(self, title, content, receiver=None):
        if receiver is None:
            receiver = self.mail_user
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header(self.sender, 'utf-8')  #发件人
        message['To'] = Header(receiver, 'utf-8')  #收件人
        subject = title  #主题
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = SMTP()
            smtpObj.connect(self.mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, receiver, str(message))
            print("邮件发送成功")
        except SMTPException:
            print("ERROR：无法发送邮件")


class WebPageUpdateChecker:
    def __init__(self, host, mail_addr, password, cookies=None):
        self.mail_sender = MailSender(host, mail_addr, password)
        if cookies is None:
            self.cookies = {}
        else:
            self.cookies = cookies

    def check(self, url, message="爷爷，爷爷你订阅的网站更新啦",
              interval=60, init_send=False):
        html_content = ""
        if not url.startswith("http://"):
            url = "http://" + url
        while True:
            print(ctime())
            try:
                r = get(url, headers={'User-agent': 'Mozilla 5.10'}, cookies=self.cookies)
            except:
                print("网络连接错误")
                sleep(interval)
                continue
            r.encoding = 'utf8'
            new_content = r.text.encode('gbk', 'ignore').decode('gbk')
            if new_content != html_content:
                if init_send:
                    content = message + ": " + url + "\n以下为对比内容：\n" \
                              + diff_compare(html_content, new_content)
                    self.mail_sender.send_mail(message, content)
                else:
                    print("initial check")
                init_send = True
                html_content = new_content
            else:
                print("no update")
            sleep(interval)


if __name__ == '__main__':
    pass

    # sender = MailSender(mail_host, mail_user, mail_pass)
    # sender.send_mail("title", diff_compare(
    #     "this is good \n but i don't like it\nhahaha\n666",
    #     "this isn't good \n but i don't like it\n666\nyeah~"
    # ))
    # checker = WebPageUpdateChecker(mail_host, mail_user, mail_pass)
    # checker.check("www.baidu.com", interval=10)