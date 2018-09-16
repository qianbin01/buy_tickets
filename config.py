from urllib.parse import quote

stations = {}


def init_doc():
    with open('station_name.txt', 'r', encoding='utf-8') as f:
        locations = f.readlines()
        for loc in locations:
            if loc:
                stations[loc.split(' ')[0]] = quote(','.join([i.strip() for i in loc.split(' ')]))


init_doc()

username = 'xxxxxx'  # 12306用户名
password = 'xxxxxx'  # 12306密码
passengers = ['张三', '李四']  # 乘客名,可多个
dtime = '2018-10-02'  # 出发日期
starts = stations['杭州东']  # 鳌江
ends = stations['鳌江']  # 杭州东
order_begin = 10  # 最早发车时间
order_end = 18  # 最晚发车时间
business_allow = False  # 是否接受商务座
first_allow = False  # 是否接受一等座
mail_host = "smtp.qq.com"  # SMTP服务器
mail_user = "xxxx@qq.com"  # 邮箱用户名
mail_pass = "xxxxxx"  # 邮箱密码
from_e = 'xxxx@qq.com'  # 发件人邮箱(最好写全, 不然会失败)
to_e = 'xxxxx@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
content = '当你收到这封邮件的时候，代表你神奇的爬虫帮你抢到了票'
title = '火车票事件'  # 邮件主题
