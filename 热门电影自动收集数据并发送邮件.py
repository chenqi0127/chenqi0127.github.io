import smtplib
import requests
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from email.utils import parseaddr,formataddr
from email.header import Header
import schedule
import time
sender = input('请输入邮箱地址：')
psw = input('请输入密码：')
recevier = input('请输入收件人邮箱地址：')
index = 0
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr))
def get_movie():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    url = 'https://movie.douban.com/chart'
    res = requests.get('https://movie.douban.com/chart',headers=headers)
    bs_res = BeautifulSoup(res.text,'html.parser')
    movie_info = bs_res.find_all('div', class_='pl2')
    list_all = []
    for movie in movie_info:
        name_tag = movie.find('a')
        name = name_tag.text.replace(' ','').replace('\n','')
        url_tag = name_tag['href']
        info_tag = movie.find('p',class_='pl')
        info = info_tag.text.replace(' ','').replace('\n','')
        rate_tag = movie.find('div',class_='star clearfix')
        rate = rate_tag.text.replace(' ','').replace('\n','')
        list_all.append(name+url_tag+info+rate+'\n')
    return list_all
def send_email(movie_list,sender,psw,recevier):
    mailhost = 'smtp.qq.com'
    qqmail = smtplib.SMTP()
    qqmail.connect(mailhost,25)
    qqmail.login(sender,psw)
    content = '\n'.join(movie_list)
    message = MIMEText(content,'plain','utf-8')
    message['From'] = _format_addr(sender)
    message['To'] = _format_addr(recevier)
    subject = '热门电影'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        qqmail.sendmail(sender, recevier, message.as_string())
        return True
    except:
        return False
    qqmail.quit()

def job():
    global index
    print('开始一次发送任务')
    movie_list =get_movie()
    success_mail = send_email(movie_list,sender,psw,recevier)
    while success_mail is False:
        print('发送失败，正在尝试重新发送！')
        success_mail = send_email(movie_list, sender, psw, recevier)
    else:
        print('发送成功')
    index +=1

schedule.every().second.do(job)
while index !=2:
    schedule.run_pending()
    time.sleep(2)
