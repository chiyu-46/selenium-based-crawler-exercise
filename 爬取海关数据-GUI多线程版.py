import PySimpleGUI as sg
import threading
import time
from webdriverHelper.CommonWebdriverHelper import WebdriverHelper
from DBHelper.DBHelperForCustoms import Helper

# 爬取海关部分国家(地区)进出口商品类章金额信息，使用多线程和GUI界面

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


def get_tr_list(url):
    """获取网页中的表格的行列表"""
    # 获取浏览器驱动
    driver = WebdriverHelper().get_webdriver()
    driver.get(url)
    time.sleep(10)
    # 获取此年对应出口数据的所有行列表
    tr_list = driver.find_element_by_xpath('//*[@id="easysiteText"]/table/tbody').find_elements_by_tag_name('tr')
    return tr_list, driver


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


def export_data_access(window, url, year):
    """获取出口数据。"""
    temp = get_tr_list(url)
    tr_list = temp[0]
    driver = temp[1]
    # 遍历每一行
    for i in range(3, len(tr_list)):
        info_list = data_processing(tr_list[i])
        # 查看获取到的数据
        window.write_event_value('info', f'-出口数据年份：{year}，商品章类序号{info_list[0]}-')
        # 保存出口信息到数据库
        db_helper.add_export_amount_from_list(info_list, year, True)
    driver.quit()
    window.write_event_value('info', f'-出口数据年份：{year}，数据爬取完成。-')


def import_data_access(window, url, year):
    """获取进口数据。"""
    temp = get_tr_list(url)
    tr_list = temp[0]
    driver = temp[1]
    # 遍历每一行
    for i in range(3, len(tr_list)):
        info_list = data_processing(tr_list[i])
        # 查看获取到的数据
        window.write_event_value('info', f'-进口数据年份：{year}，商品章类序号{info_list[0]}-')
        # 保存进口信息到数据库
        db_helper.add_import_amount_from_list(info_list, year, True)
    driver.quit()
    window.write_event_value('info', f'-进口数据年份：{year}，数据爬取完成。-')


def get_category(window, url):
    """获取商品类型数据。"""
    temp = get_tr_list(url)
    tr_list = temp[0]
    driver = temp[1]
    # 定义父种类id
    parent_id = -1
    # 遍历每一行
    for i in range(3, len(tr_list)):
        # 获取每个的商品种类数据（字符串）
        td_of_category = tr_list[i].find_elements_by_tag_name('td')[0].text
        # 用于判断是否为类（章的父级）
        temp = td_of_category[2]
        if temp == ' ':
            # 总值(不存入数据库)
            pass
        elif temp == '类':
            # 是类，值为一位数
            db_helper.add_category(int(td_of_category[1]) * 100, td_of_category.split(' ')[1], None, True)
            parent_id = int(td_of_category[1]) * 100
        elif td_of_category[3] == '类':
            # 是类，值为二位数
            db_helper.add_category(int(td_of_category[1:3]) * 100, td_of_category.split(' ')[1], None, True)
            parent_id = int(td_of_category[1:3]) * 100
        else:
            # 是章
            db_helper.add_category(int(td_of_category[0:2]), td_of_category.split(' ')[1], parent_id, True)
    driver.quit()
    window.write_event_value('info', '商品类型数据表信息获取完成！')


def thread_starter(value_for_switch):
    """根据传入参数启动线程。传入0则启动出口线程；传入1则启动进口线程。"""
    db_helper.commit()
    if value_for_switch == 0:
        year = 2021
        # 获取出口数据
        for url in export_url_list:
            if url == '':
                continue
            year -= 1
            threading.Thread(target=export_data_access, args=(window, url, year), daemon=True).start()
        threading.Thread(target=get_category, args=(window, export_url_list[0]), daemon=True).start()
    else:
        year = 2021
        # 获取进口数据
        for url in import_url_list:
            if url == '':
                continue
            year -= 1
            threading.Thread(target=import_data_access, args=(window, url, year), daemon=True).start()


# 以下是工作窗口
layout = [[sg.Output(size=(100, 10))],
          [sg.Button('开始爬取出口数据'), sg.Button('开始爬取入口数据'), sg.Button('退出')]]
window = sg.Window('海关进出口数据爬虫程序', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '退出':
        db_helper.commit()
        break
    if event == '开始爬取出口数据':
        print('开始爬取出口数据...')
        thread_starter(0)
    elif event == '开始爬取入口数据':
        print('开始爬取入口数据...')
        thread_starter(1)
    else:
        print(values)
window.close()

# 关闭数据库连接
db_helper.close_session()
