import os
from time import sleep
try:
	from selenium import webdriver
	from selenium.webdriver.support import expected_conditions as EC
except:
	print('检测到有未安装的支持库，正在安装')
	os.system('pip3 install selenium')
	sleep(1)
	from selenium import webdriver
	from selenium.webdriver.support import expected_conditions as EC

print('初始化浏览器')
config = open('配置.ini')
DRIVERKIND = config.readline().split('"')[1]
DRIVERPATH = config.readline().split('"')[1]
USERNAME   = config.readline().split('"')[1]
PASSWORD   = config.readline().split('"')[1]
config.close()
driver = None
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 MicroMessenger/6.3.27 NetType/WIFI Language/zh_CN'
if DRIVERKIND == 'edge':
	try:
		from msedge.selenium_tools import Edge, EdgeOptions
	except:
		print('检测到有未安装的支持库，正在安装')
		os.system('pip3 install msedge.selenium_tools')
		sleep(1)
		from msedge.selenium_tools import Edge, EdgeOptions
	option = EdgeOptions()
	option.use_chromium = True
	option.add_argument('user-agent='+ua)
	option.add_argument('headless')
	try:
		driver = Edge(executable_path = DRIVERPATH, options = option)
	except:
		print('driver无效，请检查设置')
		exit(1)
elif DRIVERKIND == 'chrome':
	option = webdriver.ChromeOptions()
	option.add_argument("--headless")
	option.add_argument('user-agent='+ua)
	try:
		driver = webdriver.Chrome(executable_path= DRIVERPATH, options = option)
	except:
		print('driver无效，请检查设置')
		exit(1)
else:
	print('不支持的浏览器类型')
	exit(2)
print('正在上报')
driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange')
driver.execute_script('tongyishenfen();')
driver.find_element_by_id('mobileUsername').send_keys(USERNAME)
driver.find_element_by_id('mobilePassword').send_keys(PASSWORD)
driver.find_element_by_id('load').click()
driver.find_element_by_id('mrsb').click()
driver.find_element_by_class_name('right_btn').click()
sleep(1)
alert = EC.alert_is_present()(driver)
if alert:
	alert.accept()
	driver.find_element_by_id('center').find_elements_by_tag_name('div')[5].click()
driver.find_element_by_id('txfscheckbox').click()
driver.execute_script('save();')
driver.quit()
print('上报完成')