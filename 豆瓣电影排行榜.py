import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from sqlalchemy import *
from sqlalchemy.engine import URL
import pyodbc
from sqlalchemy.orm import declarative_base, relationship, Session

# 爬取豆瓣电影 Top 250信息：
# 电影名称(取第一个)、导演、主演、时间、类型、评分、评论人数、电影描述
# 将爬取到的电影数据存储数据到mysql表中

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
class Movie(Base):
    """电影250排行榜数据库的映射类。
    """
    __tablename__ = 'movie_top250'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    director = Column(String(50))
    starring = Column(String(50))
    time = Column(String(20))
    genre = Column(String(50))
    rating = Column(DECIMAL)
    number_of_reviews = Column(Integer)
    description = Column(String(100))

    def __repr__(self):
        """展示数据。"""
        return f"名称={self.name!r}, 导演={self.director!r}, 主演={self.starring!r}, 时间={self.time!r}, " \
               f"类型={self.genre!r}, 评分={self.rating!r}, 评论人数={self.number_of_reviews!r}, " \
               f"描述={self.description!r} "


# 将 DDL 发送到数据库,创建对应数据库（只需要运行一次）
Base.metadata.create_all(engine)


# 生成与数据库的会话。
session = Session(engine)

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.implicitly_wait(30)
# 打开网页
driver.get('https://movie.douban.com/top250')
# 声明一个标志，如果因等待时间太短而需要重新获取positionList，则置为True。
reload = False
# 每次循环点击下一页
while True:
    # 等待页面加载
    time.sleep(2)
    # 获取职位列表
    positionList = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/ol') \
        .find_elements_by_tag_name('li')
    for i in positionList:
        try:
            # 声明一个空的能存储一条电影信息的变量（因为向数据库保存后，将自动得到主键id，所以存储下一条数据前，需要创建新对象）
            movie = Movie()
            infoList = i.text.splitlines()
            print('名称：{}'.format(infoList[1].split('  ', 1)[0]))
            movie.name = infoList[1].split('  ', 1)[0]
            # print('导演：{}'.format(infoList[2].split(' ', 2)[1]))
            movie.director = infoList[2].split(' ', 2)[1]
            if '主演: ' in infoList[2]:
                starring = infoList[2].split('主演: ')[-1]
                if ' ' in starring:
                    starring = starring.split(' ')[0]
                    # print('主演：{}'.format(starring))
                    movie.starring = starring
            infoList1 = infoList[3].split(' / ')
            # print('时间：{}'.format(infoList1[0]))
            movie.time = infoList1[0]
            # print('类型：{}'.format(infoList1[2]))
            movie.genre = infoList1[-1]
            infoList2 = infoList[4].split(' ')
            # print('评分：{}'.format(infoList2[0]))
            movie.rating = infoList2[0]
            # print('评论人数：{}'.format(infoList2[1][:-3]))
            movie.number_of_reviews = infoList2[1][:-3]
            try:
                # print('描述：{}'.format(infoList[5]))
                movie.description = infoList[5]
            except IndexError:
                # 这个电影没有描述，直接忽略这个错误
                pass
            print('**********************************************')
            # 向数据库保存得到的一条信息。
            session.add(movie)
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
