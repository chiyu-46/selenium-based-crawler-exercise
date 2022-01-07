from selenium import webdriver

# 抓取B站入站必刷的信息数据：标题、up主、播放量、弹幕量、一句话评论

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.implicitly_wait(30)
# 打开网页
driver.get('https://www.bilibili.com/v/popular/history')
# 找到视频卡片列表
cardList = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/ul/div').find_elements_by_tag_name('div')
# 遍历列表
for i in range(0, len(cardList), 5):
    infoList = cardList[i].text.splitlines()
    print('标题：{}'.format(infoList[0]))
    print('up主：{}'.format(infoList[1]))
    print('播放量：{}'.format(infoList[2]))
    print('弹幕量：{}'.format(infoList[3]))
    print('一句话评论：{}'.format(infoList[4]))
    print()
driver.quit()
