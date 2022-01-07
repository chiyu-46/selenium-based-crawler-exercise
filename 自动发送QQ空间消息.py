import time
from selenium import webdriver

# 实现自动发送QQ空间消息

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.implicitly_wait(60)
# 打开网页
driver.get('https://qzone.qq.com/')
# 转到登录区域的iframe
iframe = driver.find_element_by_xpath('//*[@id="login_frame"]')
driver.switch_to.frame(iframe)
# 点击头像
driver.find_element_by_xpath('//*[@id="img_out_434481283"]').click()
time.sleep(10)
# 点击说说链接
driver.find_element_by_xpath('//*[@id="menuContainer"]/div/ul/li[5]/a').click()
time.sleep(5)
# 转到登录区域的iframe
iframe = driver.find_element_by_xpath('//*[@id="app_container"]/iframe')
driver.switch_to.frame(iframe)
# 点击输入框（div）
webdriver.ActionChains(driver).double_click(driver.find_element_by_xpath('//*[@id="$1_substitutor_content"]')).perform()
# 重新登录（二次登录，仅会出现一次）
# 输入内容
driver.find_element_by_xpath('//*[@id="$1_content_content"]').send_keys('这是一条测试信息')
# 点击发表
driver.find_element_by_xpath('//*[@id="QM_Mood_Poster_Container"]/div/div[4]/div[4]').click()
time.sleep(5)
driver.quit()


# # 重新登录（二次登录，就为了发条说说，腾讯是不是有什么大病）
# # 转到登录区域的iframe
# iframe = driver.find_element_by_xpath('//*[@id="dialog_content_1"]/iframe')
# driver.switch_to.frame(iframe)
# # 点击头像
# driver.find_element_by_xpath('//*[@id="img_out_434481283"]').click()
# time.sleep(10)
# # 再次点击输入框（div）
# webdriver.ActionChains(driver).double_click(driver.find_element_by_xpath('//*[@id="$1_content_content"]')).perform()
