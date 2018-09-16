from selenium import webdriver
from time import sleep
import smtplib
from email.mime.text import MIMEText
import config


class Buy_Tickets(object):
    def __init__(self,
                 username,
                 password,
                 order_begin,
                 order_end,
                 passengers,
                 dtime,
                 starts,
                 ends,
                 business_allow=False,
                 first_allow=False,
                 mail_host='',
                 mail_user='',
                 mail_pass='',
                 from_e='',
                 to_e='',
                 title='',
                 content=''):
        self.username = username
        self.password = password
        self.order_begin = order_begin
        self.order_end = order_end
        self.passengers = passengers
        self.starts = starts
        self.ends = ends
        self.dtime = dtime
        self.business_allow = business_allow
        self.first_allow = first_allow
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.executable_path = 'chromedriver'

        # email setting
        self.mail_host = mail_host  # SMTP服务器
        self.mail_user = mail_user  # 用户名
        self.mail_pass = mail_pass  # 密码
        self.sender = from_e  # 发件人邮箱(最好写全, 不然会失败)
        self.receivers = to_e  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        self.content = content
        self.message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        self.message['From'] = from_e
        self.message['To'] = to_e
        self.message['Subject'] = title

    # 登录功能实现
    def login(self):
        self.driver.get(self.login_url)
        self.driver.find_element_by_id('username').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        print('请输入验证码...')
        while True:
            if self.driver.current_url != self.initMy_url:
                sleep(1)
            else:
                break

    # 买票功能实现
    def start_buy(self):
        self.driver = webdriver.Chrome(executable_path=self.executable_path)
        self.login()
        self.driver.get(self.ticket_url)
        try:
            print('开始购票...')
            # 加载查询信息
            self.driver.add_cookie(
                {"name": "_jc_save_fromStation", "value": self.starts})
            self.driver.add_cookie(
                {"name": "_jc_save_toStation", "value": self.ends})
            self.driver.add_cookie(
                {"name": "_jc_save_fromDate", "value": self.dtime})
            self.driver.refresh()
            count = 0
            while self.driver.current_url == self.ticket_url:
                count += 1
                print('第%d次点击查询...' % count)
                try:
                    self.driver.find_element_by_link_text('查询').click()
                    sleep(1)
                    table = self.driver.find_element_by_id('queryLeftTable')
                    trs = table.find_elements_by_tag_name('tr')
                    for index, tr in enumerate(trs):
                        if index % 2 == 0:
                            try:
                                tds = tr.find_elements_by_tag_name('td')
                                first_seat = tds[2]
                                second_seat = tds[3]
                                order = tr.find_element_by_class_name('no-br')
                                train = tr.find_element_by_class_name('ticket-info')
                                order.find_element_by_tag_name('a')
                                train_time = train.find_element_by_class_name('cds')
                                start_time = int(train_time.find_elements_by_tag_name('strong')[0].text.split(':')[0])
                                if self.order_begin <= start_time <= self.order_end:
                                    print(start_time)
                                    print(self.business_allow, self.first_allow)
                                    if self.business_allow:
                                        order.find_element_by_tag_name('a').click()
                                    elif not self.business_allow and self.first_allow and '无' not in first_seat.text:
                                        order.find_element_by_tag_name('a').click()
                                    elif not self.business_allow and not self.first_allow and '无' not in second_seat.text:
                                        order.find_element_by_tag_name('a').click()
                            except:
                                continue

                except Exception as e:
                    sleep(1)
                    print(e)
                    print('预订失败...')
                    continue
            print('开始预订...')
            sleep(1)
            print('开始选择用户...')
            ul_passengers = self.driver.find_element_by_id('normal_passenger_id')
            lis = ul_passengers.find_elements_by_tag_name('li')
            for li in lis:
                if li.text.strip() in self.passengers:
                    li.find_element_by_tag_name('label').click()
            print('提交订单...')
            self.driver.find_element_by_id('submitOrder_id').click()
            sleep(1)
            print('确认选座...')
            self.driver.find_element_by_id('qr_submit_id').click()
            print('预订成功...')
            try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(self.mail_host, 25)
                smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
                smtpObj.sendmail(self.sender, self.receivers, self.message.as_string())  # 发送
                print("mail has been send successfully.")
            except smtplib.SMTPException as e:
                print(e)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    Buy_Tickets(config.username,
                config.password,
                config.order_begin,
                config.order_end,
                config.passengers,
                config.dtime,
                config.starts,
                config.ends,
                config.business_allow,
                config.first_allow,
                config.mail_host,
                config.mail_user,
                config.mail_pass,
                config.from_e,
                config.to_e,
                config.title,
                config.content).start_buy()
