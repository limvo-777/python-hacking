import requests
from bs4 import BeautifulSoup

login_url = "http://192.168.10.4/gnu/bbs/login_check.php"

session = requests.session()

params = dict()
params['mb_id'] = 'admin'
params['mb_password'] = 'qwer1234'
res = session.post(login_url, data=params)


url ="http://192.168.10.4/gnu/bbs/board.php?bo_table=free"
for i in range(1,4):

    free = url+"&wr_id="+str(i)
    res = session.get(free)

    soup = BeautifulSoup(res.content,"html.parser")
    result = soup.find("div", id="bo_v_con")
    print(result.text)



