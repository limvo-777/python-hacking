import requests

login_url = "http://192.168.10.4/gnu/bbs/login_check.php"

session = requests.session()

params = dict()
params['mb_id'] = 'admin'
params['mb_password'] = 'qwer1234'
res = session.post(login_url, data=params)

res = session.get("http://192.168.10.4/gnu/bbs/board.php?bo_table=free")

print(res.text)
