import time
from selenium import webdriver

# 抓取央视网(CCTV1-CCTV5)节目信息：时间、节目名称

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.implicitly_wait(30)
# 打开网页
driver.get('https://tv.cctv.com/epg/index.shtml?spm=C31267.PFsKSaKh6QQC.EEfEAhEnQFPl.3')
# 获取频道列表
channelList = driver.find_element_by_xpath('//*[@id="jiemudan01"]/div[2]/div[1]/ul').find_elements_by_tag_name('li')
for channelNum in range(5):
    channelList[channelNum].click()
    time.sleep(2)
    # 找到上下午的节目列表
    forenoonList = driver.find_element_by_xpath('//*[@id="shangwu"]').find_elements_by_tag_name('tr')
    afternoonList = driver.find_element_by_xpath('//*[@id="xiawu"]').find_elements_by_tag_name('tr')
    print('*************CCTV{}***************'.format(channelNum + 1))
    # 遍历上午的节目列表
    for i in forenoonList:
        infoList = i.text.splitlines()
        print('时间：{}'.format(infoList[0]))
        print('节目名称：{}'.format(infoList[1]))
        print()
    # 遍历下午的节目列表
    for i in afternoonList:
        infoList = i.text.splitlines()
        print('时间：{}'.format(infoList[0]))
        print('节目名称：{}'.format(infoList[1]))
        print()
driver.quit()
