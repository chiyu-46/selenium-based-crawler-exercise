from sqlalchemy import *
from sqlalchemy.engine import URL
import pyodbc
from sqlalchemy.orm import declarative_base, Session


class Helper:
    """海关数据爬虫项目的数据库操作辅助类。"""
    # 声明映射类基类
    Base = declarative_base()

    # 声明映射类
    class Category(Base):
        """部分国家(地区)进口商品类章金额信息表的映射类。"""
        __tablename__ = 'category'
        # 大类别：类比代码 * 100； 小类别：对应代码
        category_id = Column(Integer, primary_key=True)
        # 类别文字描述
        description = Column(String(50))
        # 类别的父类别，如果是父类，此值为空
        parent_id = Column(Integer)

    class ImportAmount(Base):
        """部分国家(地区)进口商品类章金额信息表的映射类。"""
        __tablename__ = 'import_amount'
        id = Column(Integer, primary_key=True)
        # 商品种类（年度总值：10000； 大类别：类比代码 * 100； 小类别：对应代码）
        category = Column(Integer)
        '''
            统计的所有国家列表：缅甸 中国香港 印度 印度尼西亚 伊朗 日本 中国澳门 马来西亚 阿曼 巴基斯坦 菲律宾 沙特阿拉伯  新加坡 韩国 泰国 
            土耳其 阿拉伯联合酋长国 越南 中国台湾 哈萨克斯坦 南非 欧洲联盟 比利时 丹麦 英国 德国 法国 意大利 荷兰 西班牙 奥地利 芬兰 瑞典 
            罗马尼亚 瑞士 俄罗斯联邦 乌克兰 阿根廷 巴西 智  利 加拿大 美国 澳大利亚 新西兰
        '''
        Myanmar = Column(Integer)
        China_Hong_Kong = Column(Integer)
        India = Column(Integer)
        Indonesia = Column(Integer)
        Iran = Column(Integer)
        Japan = Column(Integer)
        China_Macau = Column(Integer)
        Malaysia = Column(Integer)
        Oman = Column(Integer)
        Pakistan = Column(Integer)
        Philippines = Column(Integer)
        Saudi_Arabia = Column(Integer)
        Singapore = Column(Integer)
        Korea = Column(Integer)
        Thailand = Column(Integer)
        Turkey = Column(Integer)
        United_Arab_Emirates = Column(Integer)
        Vietnam = Column(Integer)
        China_Taiwan = Column(Integer)
        Kazakhstan = Column(Integer)
        South_Africa = Column(Integer)
        European_Union = Column(Integer)
        Belgium = Column(Integer)
        Denmark = Column(Integer)
        United_Kingdom = Column(Integer)
        Germany = Column(Integer)
        France = Column(Integer)
        Italy = Column(Integer)
        Netherlands = Column(Integer)
        Spain = Column(Integer)
        Austria = Column(Integer)
        Finland = Column(Integer)
        Sweden = Column(Integer)
        Romania = Column(Integer)
        Switzerland = Column(Integer)
        Russian_Federation = Column(Integer)
        Ukraine = Column(Integer)
        Argentina = Column(Integer)
        Brazil = Column(Integer)
        Chile = Column(Integer)
        Canada = Column(Integer)
        United_States = Column(Integer)
        Australia = Column(Integer)
        New_Zealand = Column(Integer)
        # 对应年份
        year = Column(Integer)

    class ExportAmount(Base):
        """部分国家(地区)出口商品类章金额信息表的映射类。"""
        __tablename__ = 'export_amount'
        id = Column(Integer, primary_key=True)
        # 商品种类（年度总值：10000； 大类别：类比代码 * 100； 小类别：对应代码）
        category = Column(Integer)
        '''
            统计的所有国家列表：缅甸 中国香港 印度 印度尼西亚 伊朗 日本 中国澳门 马来西亚 阿曼 巴基斯坦 菲律宾 沙特阿拉伯  新加坡 韩国 泰国 
            土耳其 阿拉伯联合酋长国 越南 中国台湾 哈萨克斯坦 南非 欧洲联盟 比利时 丹麦 英国 德国 法国 意大利 荷兰 西班牙 奥地利 芬兰 瑞典 
            罗马尼亚 瑞士 俄罗斯联邦 乌克兰 阿根廷 巴西 智  利 加拿大 美国 澳大利亚 新西兰
        '''
        Myanmar = Column(Integer)
        China_Hong_Kong = Column(Integer)
        India = Column(Integer)
        Indonesia = Column(Integer)
        Iran = Column(Integer)
        Japan = Column(Integer)
        China_Macau = Column(Integer)
        Malaysia = Column(Integer)
        Oman = Column(Integer)
        Pakistan = Column(Integer)
        Philippines = Column(Integer)
        Saudi_Arabia = Column(Integer)
        Singapore = Column(Integer)
        Korea = Column(Integer)
        Thailand = Column(Integer)
        Turkey = Column(Integer)
        United_Arab_Emirates = Column(Integer)
        Vietnam = Column(Integer)
        China_Taiwan = Column(Integer)
        Kazakhstan = Column(Integer)
        South_Africa = Column(Integer)
        European_Union = Column(Integer)
        Belgium = Column(Integer)
        Denmark = Column(Integer)
        United_Kingdom = Column(Integer)
        Germany = Column(Integer)
        France = Column(Integer)
        Italy = Column(Integer)
        Netherlands = Column(Integer)
        Spain = Column(Integer)
        Austria = Column(Integer)
        Finland = Column(Integer)
        Sweden = Column(Integer)
        Romania = Column(Integer)
        Switzerland = Column(Integer)
        Russian_Federation = Column(Integer)
        Ukraine = Column(Integer)
        Argentina = Column(Integer)
        Brazil = Column(Integer)
        Chile = Column(Integer)
        Canada = Column(Integer)
        United_States = Column(Integer)
        Australia = Column(Integer)
        New_Zealand = Column(Integer)
        # 对应年份
        year = Column(Integer)

    def __init__(self):
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
        self.engine = create_engine(connection_url)
        # 将 DDL 发送到数据库,创建对应数据库（只需要运行一次）
        self.Base.metadata.create_all(self.engine)
        # 生成与数据库的会话。
        self.session = Session(self.engine)

    def get_session(self):
        """获取与数据库的会话。"""
        return self.session

    def close_session(self):
        """关闭与数据库的会话。"""
        self.session.close()

    def add_export_amount_from_list(self, info_list, year, is_thread=False):
        """向出口表中添加数据。"""
        temp = self.ExportAmount()
        if is_thread:
            self.__add_item_to_database_for_thread(temp, info_list, year)
        else:
            self.__add_item_to_database(temp, info_list, year)

    def add_import_amount_from_list(self, info_list, year, is_thread=False):
        """向进口表中添加数据。"""
        temp = self.ImportAmount()
        if is_thread:
            self.__add_item_to_database_for_thread(temp, info_list, year)
        else:
            self.__add_item_to_database(temp, info_list, year)

    def __add_item_to_database(self, temp, info_list, year):
        """向数据库表中添加数据。具体表由temp的数据类型决定。"""
        temp = self.split_info_list(temp, info_list)
        # 对应年份
        temp.year = year

        # 添加此向数据到数据库（准备提交）
        self.session.add(temp)
        # 提交到数据库
        self.session.commit()

    def __add_item_to_database_for_thread(self, temp, info_list, year):
        """向数据库表中添加数据。具体表由temp的数据类型决定。用于多线程操作。"""
        temp = self.split_info_list(temp, info_list)
        # 对应年份
        temp.year = year

        # 添加此向数据到数据库（准备提交）
        self.session.add(temp)

    def split_info_list(self, temp, info_list):
        temp.category = info_list[0]
        temp.Myanmar = info_list[1]
        temp.China_Hong_Kong = info_list[2]
        temp.India = info_list[3]
        temp.Indonesia = info_list[4]
        temp.Iran = info_list[5]
        temp.Japan = info_list[6]
        temp.China_Macau = info_list[7]
        temp.Malaysia = info_list[8]
        temp.Oman = info_list[9]
        temp.Pakistan = info_list[10]
        temp.Philippines = info_list[11]
        temp.Saudi_Arabia = info_list[12]
        temp.Singapore = info_list[13]
        temp.Korea = info_list[14]
        temp.Thailand = info_list[15]
        temp.Turkey = info_list[16]
        temp.United_Arab_Emirates = info_list[17]
        temp.Vietnam = info_list[18]
        temp.China_Taiwan = info_list[19]
        temp.Kazakhstan = info_list[20]
        temp.South_Africa = info_list[21]
        temp.European_Union = info_list[22]
        temp.Belgium = info_list[23]
        temp.Denmark = info_list[24]
        temp.United_Kingdom = info_list[25]
        temp.Germany = info_list[26]
        temp.France = info_list[27]
        temp.Italy = info_list[28]
        temp.Netherlands = info_list[29]
        temp.Spain = info_list[30]
        temp.Austria = info_list[31]
        temp.Finland = info_list[32]
        temp.Sweden = info_list[33]
        temp.Romania = info_list[34]
        temp.Switzerland = info_list[35]
        temp.Russian_Federation = info_list[36]
        temp.Ukraine = info_list[37]
        temp.Argentina = info_list[38]
        temp.Brazil = info_list[39]
        temp.Chile = info_list[40]
        temp.Canada = info_list[41]
        temp.United_States = info_list[42]
        temp.Australia = info_list[43]
        temp.New_Zealand = info_list[44]
        return temp

    def add_category(self, category_id, description, parent_id, is_thread=False):
        """添加商品种类数据。"""
        temp = self.Category()
        temp.category_id = category_id
        temp.description = description
        temp.parent_id = parent_id
        # 添加此向数据到数据库（准备提交）
        self.session.add(temp)
        if not is_thread:
            # 提交到数据库
            self.session.commit()

    def commit(self):
        self.session.commit()
