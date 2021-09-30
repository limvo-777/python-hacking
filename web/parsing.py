import requests
from bs4 import BeautifulSoup

login_url = "http://192.168.10.4/gnu/bbs/login_check.php"

session = requests.session()

params = dict()
params['mb_id'] = 'admin'
params['mb_password'] = 'qwer1234'
res = session.post(login_url, data=params)

res = session.get("http://192.168.10.4/gnu/bbs/board.php?bo_table=free")

soup = BeautifulSoup(res.content,"html.parser")

result = soup.find_all("b", class_="sound_only")


for x in result:
    print(x.get_text())
