import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 使用cookie实现自动登录airbnb.cn并自动订房

cookies = [{'domain': '.airbnb.cn', 'expiry': 1672304737, 'httpOnly': False, 'name': '_abck', 'path': '/', 'secure': True, 'value': '321FF26EC03D9479A687B0CB69567F76~-1~YAAQDoyUG4R2U5p9AQAALxdwBQdaIWufcleKyYfyU8u6iOdI9kJ7SWXOwjfn/v6F2JDDk3rbAw6PswofHDMpszOeix3v/sEt9s8WMtayN/Xsh5WtDI5QD8HzzpDqMx7Uyk2hbdKJcbd0FEUProeM5QvMztb2AqKZJaSLXXmVAkYeTptmG5blyOOJ3JYktW/Ds95yvo4LdI195VFrBP8fRjPxhF6l4LMZC0nS9CXy1Wxv9v1YO95TbZBXzHgkrlIR7QH0X2km73eQqfKF7qot8lex/Fd9iZLf1cl5/FRBHuhzTcp4MrtBDXlh++ytjgkljKya41MuSSbFjOExY71lxPyre304PslVngq3vkjfwjoM5Etmc0ySUQ7Gbb8YeOyhpHC1NN1cbxlCYb4YBKEIhX2jQTp8BQ0=~0~-1~-1'}, {'domain': '.airbnb.cn', 'expiry': 1645952732, 'httpOnly': False, 'name': 'cdn_exp_edb50325b473721a8', 'path': '/', 'secure': False, 'value': 'treatment'}, {'domain': '.airbnb.cn', 'httpOnly': False, 'name': '_csrf_token', 'path': '/', 'secure': True, 'value': 'V4%24.airbnb.cn%24-q0BK41KXcw%24ot0pWDJpRpl-UfxwTITAaEu_JzGP4TiYVu-zG2d5kww%3D'}, {'domain': '.airbnb.cn', 'expiry': 1703840736, 'httpOnly': False, 'name': '_user_attributes', 'path': '/', 'secure': True, 'value': '%7B%22curr%22%3A%22CNY%22%2C%22guest_exchange%22%3A6.369785%2C%22device_profiling_session_id%22%3A%221640768699--acc054a10bbdf458471810db%22%2C%22giftcard_profiling_session_id%22%3A%221640768699--4f957758634e7ddb379d8ae2%22%2C%22reservation_profiling_session_id%22%3A%221640768699--30099087c185417744eb70ed%22%2C%22id%22%3A437967605%2C%22hash_user_id%22%3A%22d2caf30c1d07e55537a1b2862e60feeb2dd061db%22%2C%22eid%22%3A%22X3SdoVY_u6osZnCTpweuMQ%3D%3D%22%2C%22num_h%22%3A0%2C%22num_trip_notif%22%3A0%2C%22name%22%3A%22%E6%B1%A0%E9%B1%BC%22%2C%22num_action%22%3A0%2C%22is_admin%22%3Afalse%2C%22can_access_photography%22%3Afalse%2C%22travel_credit_status%22%3Anull%2C%22referrals_info%22%3A%7B%22receiver_max_savings%22%3A%22%EF%BF%A5178%22%2C%22receiver_savings_percent%22%3A0%2C%22receiver_signup%22%3A%22%EF%BF%A50%22%2C%22referrer_guest%22%3A%22%EF%BF%A530%22%2C%22terms_and_conditions_link%22%3A%22%2Fhelp%2Farticle%2F2269%22%2C%22wechat_link%22%3A%22https%3A%2F%2Fwww.airbnb.cn%2Fc%2Fc8c0da3%3Fcurrency%3DCNY%26s%3D11%22%2C%22offer_discount_type%22%3A%22tiered_savings%22%7D%7D'}, {'domain': 'www.airbnb.cn', 'expiry': 1640772331, 'httpOnly': False, 'name': 'alfc', 'path': '/', 'secure': False, 'value': '0'}, {'domain': 'www.airbnb.cn', 'expiry': 1640772331, 'httpOnly': False, 'name': 'alfces', 'path': '/', 'secure': False, 'value': '0'}, {'domain': '.airbnb.cn', 'httpOnly': False, 'name': 'roles', 'path': '/', 'secure': True, 'value': '0'}, {'domain': '.airbnb.cn', 'expiry': 1703840731, 'httpOnly': False, 'name': 'abb_fa2', 'path': '/', 'secure': True, 'value': '%7B%22user_id%22%3A%2258%7C1%7CFDYOX1fXuJLXjB%2BNP71UVBltwSn1NtG3Lx9Dpg0uFJhpLUGQvaxmwdk%3D%22%7D'}, {'domain': '.airbnb.cn', 'expiry': 1645952732, 'httpOnly': False, 'name': 'cdn_exp_37bbb1cafa653df39', 'path': '/', 'secure': False, 'value': 'treatment'}, {'domain': '.airbnb.cn', 'expiry': 1727082318, 'httpOnly': False, 'name': 'frmfctr', 'path': '/', 'secure': False, 'value': 'wide'}, {'domain': 'www.airbnb.cn', 'httpOnly': False, 'name': 'auth_jitney_session_id', 'path': '/', 'secure': False, 'value': 'e4b81ac8-94c0-44da-8877-313864af1821'}, {'domain': '.airbnb.cn', 'expiry': 1727082335, 'httpOnly': False, 'name': 'cbkp', 'path': '/', 'secure': False, 'value': '3'}, {'domain': '.airbnb.cn', 'expiry': 1727082302, 'httpOnly': False, 'name': 'cfrmfctr', 'path': '/', 'secure': False, 'value': 'DESKTOP'}, {'domain': '.airbnb.cn', 'expiry': 1640775896, 'httpOnly': True, 'name': 'ak_bmsc', 'path': '/', 'secure': False, 'value': '3F8A5ABF30A3EF5C51C57D6C36C150B9~000000000000000000000000000000~YAAQDoyUG+BwU5p9AQAAOolvBQ6/u/QarUaQaq0geG1h3dDBy3es04GZXV4HZnhY4AfbrUKQPlo/kTVbEaVtrBa3Qbik+6TzLgMjsjAS+oIM67UUexyNgEofG1v3qU2HWmXure3BxG44LBu/cqU+O8uyRolOa2Y0DCpI86LZYN3sYDgy3/xkOt5aXSQ0x/Vvb7G4ZyJEnNoQKG01joIyxqeCVOCGMi2lPwAEvbyDRwSpCHrdyAghe9CV7Y1ySWnoD5DLD2w7SJnIQz2UXF69WhaxejgguB4mj1mOvgBLxioj9JN/y6ZHgl/Iu4zOAWy9ZtjWvEV4MwEAooNiox1zH3+omid7oXDanwRMSwPSELNitjEqrc2yb89KTlsO0R6jwkWkYwNUOG4JXOXqqy22CtOwD1298gzzo0HsxRq9GvKePhiySjisr18Y4xuXwMJlGalmFbjyKGq3h4XSpE2VJXakrm0Le6avSu2jdgJYkJLtIc2y1650C4fI4Z3CPC0u/gcNzQv4fMo3E+VD9uRRL6fLiVIsocNczPaB6no='}, {'domain': 'www.airbnb.cn', 'httpOnly': False, 'name': 'currency', 'path': '/', 'secure': False, 'value': 'CNY'}, {'domain': '.airbnb.cn', 'expiry': 1640855135, 'httpOnly': False, 'name': 'jitney_client_session_updated_at', 'path': '/', 'secure': True, 'value': '1640768737'}, {'domain': '.airbnb.cn', 'httpOnly': False, 'name': 'OptanonAlertBoxClosed', 'path': '/', 'secure': False, 'value': 'NR'}, {'domain': '.airbnb.cn', 'expiry': 1703840737, 'httpOnly': True, 'name': '_airbed_session_id', 'path': '/', 'secure': True, 'value': '2f0c66dbef9436e780070b964062067d'}, {'domain': '.airbnb.cn', 'expiry': 1640775901, 'httpOnly': True, 'name': 'bm_sv', 'path': '/', 'secure': False, 'value': 'AB5D8B382145BED018621067C16985C4~PfyVXgxW6eY/uC5jMAjNGwkDaFgwTYsfCyjrIphrDQLrYGCOaL0Al8g2HSDlGuR3hGAGRM5CUsrGDBTwMwrSolwwJavt09YriQ6AH623DmfHRnlc52CNxdQL7+SWfNzYRc6Yb0BixNBrHjeHFm2ItHMgvD0U8OSg+w2S0iEQn9E='}, {'domain': '.airbnb.cn', 'expiry': 1703840731, 'httpOnly': True, 'name': '_aat', 'path': '/', 'secure': True, 'value': '0%7CwME%2Bh4Up4bdkyqzetPNqs%2BWv1Nw0MgFqwoM%2BxHJyWfwbCJ5baHQQnJqZsj3%2Bo6qG'}, {'domain': '.airbnb.cn', 'expiry': 1703840735, 'httpOnly': False, 'name': 'bev', 'path': '/', 'secure': True, 'value': '1640768698_NDRkNTM4ZTllYWRm'}, {'domain': '.airbnb.cn', 'expiry': 1640783096, 'httpOnly': False, 'name': 'bm_sz', 'path': '/', 'secure': False, 'value': 'A921AEC6F5E189480E7FE37BD8E73495~YAAQDoyUG/JvU5p9AQAABHlvBQ5dN5r+bPLWdYDj0zy0z9q2f1MADxPKSWs0nJy7Jt+9RW2ySiGoSUwdB2QiCTlxMi6RyukMKctmCewbvqpRZ/RftqrjEcBje1OiWJKk/hIdnO1iM76VWUn5qLbPN4ARx1nsyHjBjDtBC8sJuNjHlYs9gvvPs1+5uQ3uHqXXQkjxfOOJovWfbnzMrJQwQpuRFFlyhKFZoPc1GgxLyzhzkS5QF/ve58b13iRE8qqtryUMCCtnkjkmtc+utgqQY17Qq2I+lWPH/oBkmwpIVoOxTg==~3293747~4273977'}, {'domain': '.airbnb.cn', 'httpOnly': False, 'name': 'flags', 'path': '/', 'secure': True, 'value': '0'}, {'domain': '.airbnb.cn', 'expiry': 1640855097, 'httpOnly': False, 'name': 'jitney_client_session_created_at', 'path': '/', 'secure': True, 'value': '1640768699'}, {'domain': '.airbnb.cn', 'expiry': 1640855097, 'httpOnly': False, 'name': 'jitney_client_session_id', 'path': '/', 'secure': True, 'value': '90259bc9-8ed9-4cf3-a6f7-a161ad7505fc'}]

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
# 打开网页
driver.get('https://www.airbnb.cn/')
time.sleep(5)
# 设置cookie实现免登录
driver.delete_all_cookies()
for item in cookies:
    driver.add_cookie(item)
# 重新打开网页
driver.get('https://www.airbnb.cn/')
time.sleep(5)
# 在输入框输入长沙并回车
driver.find_element_by_name('query').send_keys('长沙')
driver.find_element_by_name('query').send_keys(Keys.ENTER)
# 选择日期
driver.find_element_by_id('menuItemButton-date_picker').click()
driver.find_element_by_class_name('_16zigr23').click()
# 选择人数
driver.find_element_by_id('menuItemButton-guest_picker').click()
driver.find_element_by_class_name('_1a72ixey').click()
driver.find_element_by_class_name('_dae0b4e').click()
# 点击一个住宅
time.sleep(5)
driver.find_element_by_xpath("//div[@itemprop='itemListElement']").click()
time.sleep(10)
# 切换到新标签页
driver.switch_to.window(driver.window_handles[1])
# 点击预订
driver.find_element_by_class_name('_ptje086').click()
time.sleep(10)
driver.quit()
