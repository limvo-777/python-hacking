import requests
from bs4 import BeautifulSoup

login_url = "http://192.168.10.4/gnu/bbs/login_check.php"

session = requests.session()

params = dict()
params['mb_id'] = 'admin'
params['mb_password'] = 'aaaeae'
res = session.post(login_url, data=params)
print(res.text)

# res = session.get("http://192.168.10.4/gnu/bbs/board.php?bo_table=free")
# print(res.text)
# soup = BeautifulSoup(res.content,"html.parser")

# result = soup.find_all("b", class_="sound_only")


# for x in result:
#     print(x.get_text())
