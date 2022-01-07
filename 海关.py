import time
from webdriverHelper.CommonWebdriverHelper import WebdriverHelper
from DBHelper.DBHelperForCustoms import Helper


# 爬取海关部分国家(地区)进出口商品类章金额信息

def data_processing(tr):
    # 切割获取每行的各项数据
    td_list = tr.find_elements_by_tag_name('td')
    info_list = []
    # 第一项数据是类别，需要单独分析
    temp = td_list[0].text[2]
    if temp == ' ':
        # 总值
        info_list.append(10000)
    elif temp == '类':
        info_list.append(int(td_list[0].text[1]) * 100)
    elif td_list[0].text[3] == '类':
        info_list.append(int(td_list[0].text[1:3]) * 100)
    else:
        info_list.append(int(td_list[0].text[0:2]))
    # 遍历剩下的每个数据项
    for itemIndex in range(2, len(td_list), 2):
        temp = td_list[itemIndex].text
        if temp == '-':
            temp = None
        else:
            temp = temp.replace(',', '').replace(' ', '')
        info_list.append(temp)
    return info_list


# 初始化数据库连接
db_helper = Helper()

# 出口数据来源网页列表
export_url_list = ['http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/3516050/index.html',
                   'http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/2851371/index.html',
                   'http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/2278890/index.html',
                   'http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/1421214/index.html',
                   '',
                   'http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/310686/index.html',
                   '']
# 进口数据来源网页列表
import_url_list = ['http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/3516063/index.html',
                   'http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/2851375/index.html',
                   'http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/2278922/index.html',
                   'http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/1421228/index.html',
                   '',
                   'http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/310687/index.html',
                   'http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/302276/310259/index.html']
year = 2021
# 获取出口数据
for url in export_url_list:
    year -= 1
    if url == '':
        continue
    # 获取浏览器驱动
    driver = WebdriverHelper().get_webdriver()
    driver.get(url)
    time.sleep(10)
    # 获取此年对应出口数据的所有行列表
    trList = driver.find_element_by_xpath('//*[@id="easysiteText"]/table/tbody').find_elements_by_tag_name('tr')
    # 遍历每一行
    for i in range(3, len(trList)):
        infoList = data_processing(trList[i])
        # 查看获取到的数据
        print(infoList)
        # 保存出口信息到数据库
        db_helper.add_export_amount_from_list(infoList, year)
    driver.quit()
year = 2021
# 获取进口数据
for url in import_url_list:
    year -= 1
    if url == '':
        continue
    # 获取浏览器驱动
    driver = WebdriverHelper().get_webdriver()
    driver.get(url)
    time.sleep(10)
    # 获取此年对应出口数据的所有行列表
    trList = driver.find_element_by_xpath('//*[@id="easysiteText"]/table/tbody').find_elements_by_tag_name('tr')
    # 遍历每一行
    for i in range(3, len(trList)):
        infoList = data_processing(trList[i])
        # 查看获取到的数据
        print(infoList)
        # 保存进口信息到数据库
        db_helper.add_import_amount_from_list(infoList, year)
    driver.quit()

# 获取商品类型数据
print('开始完成商品类型数据表.......')
driver = WebdriverHelper().get_webdriver()
driver.get(import_url_list[0])
time.sleep(10)
# 获取此年对应出口数据的所有行列表
trList = driver.find_element_by_xpath('//*[@id="easysiteText"]/table/tbody').find_elements_by_tag_name('tr')
# 定义父种类id
parent_id = -1
# 遍历每一行
for i in range(3, len(trList)):
    # 获取每个的商品种类数据（字符串）
    td_of_category = trList[i].find_elements_by_tag_name('td')[0].text
    # 用于判断是否为类（章的父级）
    temp = td_of_category[2]
    if temp == ' ':
        # 总值(不存入数据库)
        pass
    elif temp == '类':
        # 是类，值为一位数
        db_helper.add_category(int(td_of_category[1]) * 100, td_of_category.split(' ')[1], None)
        parent_id = int(td_of_category[1]) * 100
    elif td_of_category[3] == '类':
        # 是类，值为二位数
        db_helper.add_category(int(td_of_category[1:3]) * 100, td_of_category.split(' ')[1], None)
        parent_id = int(td_of_category[1:3]) * 100
    else:
        # 是章
        db_helper.add_category(int(td_of_category[0:2]), td_of_category.split(' ')[1], parent_id)
driver.quit()
print('商品类型数据表信息获取完成！')

# 关闭数据库连接
db_helper.close_session()
