from splinter.browser import Browser
from time import sleep
import smtplib
from email.mime.text import MIMEText
from config import get_stations


class Buy_Tickets(object):
    # 定义实例属性，初始化
    def __init__(self, username, passwd, order, passengers, dtime, starts, ends,
                 mail_host='', mail_user='', mail_pass='', from_e='', to_e='', title='', content=''):
        self.username = username
        self.passwd = passwd
        # 车次，0代表所有车次，依次从上到下，1代表所有车次，依次类推
        self.order = order
        # 乘客名
        self.passengers = passengers
        # 起始地和终点
        self.starts = starts
        self.ends = ends
        # 日期
        self.dtime = dtime
        # self.xb = xb
        # self.pz = pz
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver_name = 'chrome'
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
        self.driver.visit(self.login_url)
        self.driver.fill('loginUserDTO.user_name', self.username)
        # sleep(1)
        self.driver.fill('userDTO.password', self.passwd)
        # sleep(1)
        print('请输入验证码...')
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break

    # 买票功能实现
    def start_buy(self):
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        # 窗口大小的操作
        self.driver.driver.set_window_size(700, 500)
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            print('开始购票...')
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
            self.driver.reload()
            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        self.driver.find_by_text('预订')[self.order - 1].click()
                        sleep(1.5)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        for i in self.driver.find_by_text('预订'):
                            i.click()
                            sleep(1)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            print('开始预订...')
            sleep(1)
            print('开始选择用户...')
            for p in self.passengers:

                self.driver.find_by_text(p).last.click()
                sleep(0.5)
                if p[-1] == ')':
                    self.driver.find_by_id('dialog_xsertcj_ok').click()
            print('提交订单...')
            # sleep(1)
            # self.driver.find_by_text(self.pz).click()
            # sleep(1)
            # self.driver.find_by_text(self.xb).click()
            # sleep(1)
            self.driver.find_by_id('submitOrder_id').click()
            sleep(2)
            print('确认选座...')
            self.driver.find_by_id('qr_submit_id').click()
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
    username = 'xxxx'  # 用户名
    password = 'xxxxx'  # 密码
    order = 2  # 车次选择，0代表所有车次
    # 乘客名，比如passengers = ['丁小红', '丁小明']
    # 学生票需注明，注明方式为：passengers = ['丁小红(学生)', '丁小明']
    passengers = ['xxx']
    dtime = '2018-02-22'  # 日期，格式为：'2018-01-20'

    # 出发地(需填写cookie值)
    starts = get_stations()['出发地']  # 鳌江
    # 目的地(需填写cookie值)
    ends = get_stations()['目的地']  # 杭州东

    # xb =['硬座座']
    # pz=['成人票']

    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "xxxx@163.com"  # 邮箱用户名
    mail_pass = "xxxxxx"  # 邮箱密码
    from_e = 'xxxxx'  # 发件人邮箱(最好写全, 不然会失败)
    to_e = 'xxxxx'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    content = '当你收到这封邮件的时候，代表你神奇的爬虫帮你抢到了票'
    title = '火车票事件'  # 邮件主题
    Buy_Tickets(username, password, order, passengers, dtime, starts, ends, mail_host, mail_user, mail_pass, from_e,
                to_e, title, content).start_buy()
