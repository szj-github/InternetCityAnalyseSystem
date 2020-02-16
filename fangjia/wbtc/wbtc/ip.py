import requests
url = 'https://qd.58.com/'
proxies_list = [
		'https://184.105.143.66:3128'
		
	]
ip_list = []
 
for proxy_ip in proxies_list:
	print (proxy_ip)
	# print(proxies_list)
	headers = {
            'user-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400"
        } 
	proxies = {'https': proxy_ip}
	try:
		wb_data = requests.get(url=url,,proxies=proxies,headers=headers,timeout=8)
		if wb_data.status_code == 200:
			flag = True
		else:
			proxies_list.remove(proxies['https'])
			flag = False
			print("无效ip")
	except:
		flag = False
		print("无效ip")
	if flag:
		ip_list.append(proxies['https'])
print (ip_list)
