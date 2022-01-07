import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from sqlalchemy import *
from sqlalchemy.engine import URL
import pyodbc
from sqlalchemy.orm import declarative_base, relationship, Session

# 在前程无忧网站爬取招聘信息：
# 岗位名称、日期、薪资、地区、经验年限、学历、招聘人数、公司名称
# 将数据存储到数据库表中

# 关闭 pyodbc 默认连接池
pyodbc.pooling = False
# 创建连接字符串
connection_url = URL.create(
    "mssql+pyodbc",
    username="sa",
    password="123456",
    host="localhost",
    port=1433,
    database="ForTraining",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
    },
)
# 创建数据库引擎（隐藏显示执行的sql）
engine = create_engine(connection_url)

# 声明基类
Base = declarative_base()


# 声明映射类
class Position(Base):
    """岗位数据库的映射类。
    """
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    job_title = Column(String(100))
    posting_date = Column(String(20))
    salary = Column(String(20))
    region = Column(String(20))
    years_of_experience = Column(String(20))
    education = Column(String(20))
    number_of_recruits = Column(String(20))
    company_name = Column(String(100))

    def __repr__(self):
        """展示数据。"""
        return f"岗位名称={self.job_title!r}, 日期={self.posting_date!r}, 薪资={self.salary!r}, 地区={self.region!r}, " \
               f"经验年限={self.years_of_experience!r}, 学历={self.education!r}, 招聘人数={self.number_of_recruits!r}, " \
               f"公司名称={self.company_name!r} "


# 将 DDL 发送到数据库,创建对应数据库（只需要运行一次）
Base.metadata.create_all(engine)


# 生成与数据库的会话。
session = Session(engine)

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.implicitly_wait(30)
# 打开网页
driver.get('https://search.51job.com/list/020000%252c010000%252c030200,000000,0000,00,9,99,'
           '%25E8%25BD%25AF%25E4%25BB%25B6%25E6%25B5%258B%25E8%25AF%2595,2,'
           '1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0'
           '&dibiaoid=0&line=&welfare=')
# 声明一个标志，如果因等待时间太短而需要重新获取positionList，则置为True。
reload = False
# 每次循环点击下一页
while True:
    # 等待页面加载
    time.sleep(5)
    # 获取职位列表
    positionList = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div[4]/div[1]') \
        .find_elements_by_tag_name('div')
    for i in range(0, len(positionList), 3):
        try:
            # 声明一个空的能存储一条岗位信息的变量（因为向数据库保存后，将自动得到主键id，所以存储下一条数据前，需要创建新对象）
            positionItem = Position()
            infoList = positionList[i].text.splitlines()
            # print('岗位名称：{}'.format(infoList[0]))
            positionItem.job_title = infoList[0]
            # print('日期：{}'.format(infoList[1]))
            positionItem.posting_date = infoList[1]
            # print('薪资：{}'.format(infoList[2]))
            positionItem.salary = infoList[2]
            infoList2 = infoList[3].split(' | ')
            # print('地区：{}'.format(infoList2[0]))
            positionItem.region = infoList2[0]
            # print('经验年限：{}'.format(infoList2[1]))
            positionItem.years_of_experience = infoList2[1]
            # print('学历：{}'.format(infoList2[2]))
            positionItem.education = infoList2[2]
            # print('招聘人数：{}'.format(infoList2[3]))
            positionItem.number_of_recruits = infoList2[3]
            print('公司名称：{}'.format(infoList[-3]))
            positionItem.company_name = infoList[-3]
            print('**********************************************')
            # 向数据库保存得到的一条岗位信息。
            session.add(positionItem)
        except IndexError:
            try:
                # 输出获取的源信息
                print(positionList[i].text)
            except StaleElementReferenceException:
                # 得到此错误，说明得到时间不足，需要重新获取positionList
                reload = True
            # 如果得到此异常，说明当前行缺少部分数据，应当跳过
            continue
        except StaleElementReferenceException:
            # 得到此错误，说明得到时间不足，需要重新获取positionList
            reload = True
    # 因等待时间太短而重新获取positionList，不进入下一页
    if reload:
        reload = False
        continue
    # 保存此页获取到的数据
    session.commit()

    try:
        # 点击下一页
        driver.find_element_by_class_name('next').find_elements_by_tag_name('a')[0].click()
    except IndexError:
        # 发生此异常，说明已经到最后一页，跳出循环
        break

# 退出浏览器
driver.quit()
# 关闭与数据库的会话
session.close()
