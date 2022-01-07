from sqlalchemy import *
from sqlalchemy.engine import URL
import pyodbc
from sqlalchemy.orm import declarative_base, relationship, Session

# 将在前程无忧网站爬取到的已经存入数据库的招聘信息：
# 岗位名称、日期、薪资、地区、经验年限、学历、招聘人数、公司名称
# 进行处理，存入新表中

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


class PositionNew(Base):
    """改后的岗位数据库"""
    __tablename__ = 'position_new'
    id = Column(Integer, primary_key=True)
    job_title = Column(String(100))
    month = Column(Integer)
    day = Column(Integer)
    max_salary = Column(Integer)
    min_salary = Column(Integer)
    area = Column(String(20))
    district = Column(String(20))
    max_experience = Column(Integer)
    min_experience = Column(Integer)
    education = Column(String(20))
    number_of_recruits = Column(Integer)
    company_name = Column(String(100))


# 将 DDL 发送到数据库,创建对应数据库（只需要运行一次）
Base.metadata.create_all(engine)


# 生成与数据库的会话。
session = Session(engine)
i = 0
while True:
    i += 1
    print(i)
    # 处理源数据库中的数据到新数据库中
    positionItem = session.get(Position, i)
    if positionItem is None:
        break
    positionItemNew = PositionNew()
    # 处理岗位名称
    positionItemNew.job_title = positionItem.job_title
    # 处理发布日期
    temp = positionItem.posting_date[:-2].split('-')
    positionItemNew.month = temp[0]
    positionItemNew.day = temp[1]
    # 处理薪资（统一按月计算）
    minSalary = 0
    maxSalary = 0
    # 获得基础薪资数字
    if '以' in positionItem.salary:
        # 如果工资为以上以下之类，扔掉数据
        continue
    if '-' in positionItem.salary[:-3]:
        temp = positionItem.salary[:-3].split('-')
        minSalary = float(temp[0])
        maxSalary = float(temp[1])
    else:
        minSalary = float(positionItem.salary[:-3])
        maxSalary = float(positionItem.salary[:-3])
    # 获取薪资单位
    if positionItem.salary[-3] == '千':
        # 如果按月计算薪资
        minSalary *= 1000
        maxSalary *= 1000
    elif positionItem.salary[-3] == '万':
        # 如果按月计算薪资
        minSalary *= 10000
        maxSalary *= 10000
    # 判断年月日
    if positionItem.salary[-1] == '天':
        # 如果按月计算薪资
        minSalary *= 30
        maxSalary *= 30
    elif positionItem.salary[-1] == '年':
        # 如果按年计算薪资
        minSalary /= 12
        maxSalary /= 12
    positionItemNew.min_salary = minSalary
    positionItemNew.max_salary = maxSalary
    # 处理地区
    if '-' in positionItem.region:
        temp = positionItem.region.split('-')
        positionItemNew.area = temp[0]
        positionItemNew.district = temp[1]
    else:
        positionItemNew.area = positionItem.region
    # 处理工作经验
    temp = positionItem.years_of_experience[:-3]
    if positionItem.years_of_experience == '在校生/应届生' or positionItem.years_of_experience == '无需经验':
        positionItemNew.max_experience = 0
        positionItemNew.min_experience = 0
    elif '以' == temp[-1]:
        positionItemNew.min_experience = temp[:-2]
    elif '-' in temp:
        temp = temp.split('-')
        positionItemNew.max_experience = temp[1]
        positionItemNew.min_experience = temp[0]
    else:
        positionItemNew.max_experience = temp
        positionItemNew.min_experience = temp
    # 处理学历
    positionItemNew.education = positionItem.education
    # 处理招聘人数
    temp = positionItem.number_of_recruits[1:-1]
    if temp != '若干':
        positionItemNew.number_of_recruits = positionItem.number_of_recruits[1:-1]
    else:
        # 如果写“招若干人”，扔掉数据
        continue
    # 处理公司名称
    positionItemNew.company_name = positionItem.company_name
    # 提交到数据库
    session.add(positionItemNew)
    session.commit()
# 关闭与数据库的会话
session.close()
