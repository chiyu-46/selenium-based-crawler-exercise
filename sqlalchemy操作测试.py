from sqlalchemy import *
from sqlalchemy.engine import URL
import pyodbc
from sqlalchemy.orm import declarative_base, relationship, Session

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

# 创建数据库引擎（显示执行的sql）
engine = create_engine(connection_url, echo=True)

# 创建数据库连接
# with engine.connect() as conn:
#     # 执行一条 SQL 语句
#     result = conn.execute(text("select * from books"))
#     # 输出执行结果
#     print(result.all())

# 声明基类
Base = declarative_base()

# 声明映射类
class User(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# 将 DDL 发送到数据库
# Base.metadata.create_all(engine)
# 使用 ORM 插入行（自动生成的主键属性）
squidward = User()
squidward.name = 'abc'
squidward.fullname = 'abcdef'
# krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
# 目前，我们上面的两个对象被称为处于一种称为瞬态的状态 ——它们不与任何数据库状态相关联，并且尚未与Session可以为它们生成 INSERT 语句的对象相关联。
session = Session(engine)
session.add(squidward)
# session.add(krabs)
session.commit()
print(squidward.id)
session.close()

# stmt = select(user_table).where(user_table.c.name == 'spongebob')
# 输出上面的方法的SQL语句形式
# print(stmt)

# ****************************************Core********************************************************
# 创建数据库（手动提交事务）
# with engine.connect() as conn:
#     conn.execute(text("CREATE TABLE some_table (x int, y int)"))
#     conn.execute(
#     text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
#     )
#     conn.commit()
# 向数据库插入数据（自动提交事务begin）（发送带参数SQL‘：x’，如果只有一条信息，不使用列表，只使用字典）
# with engine.begin() as conn:
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
#     )

# ****************************************ORM********************************************************
# 使用ORM执行事务（stmt绑定数据）
# stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
# with Session(engine) as session:
#     result = session.execute(stmt)
# 使用ORM执行事务（更新数据）
# with Session(engine) as session:
#     result = session.execute(
#         text("UPDATE some_table SET y=:y WHERE x=:x"),
#         [{"x": 9, "y":11}, {"x": 13, "y": 15}]
#     )
#     session.commit()
# 使用ORM选择行
# stmt = select(User).where(User.name == 'spongebob')
# with Session(engine) as session:
#     for row in session.execute(stmt):
#         print(row)
# 使用 ORM 选择指定列
# print(select(User.name, User.fullname))
# 声明基类
# Base = declarative_base()
# 声明映射类
# class User(Base):
#     __tablename__ = 'user_account'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(30))
#     fullname = Column(String)
#     addresses = relationship("Address", back_populates="user")
#     def __repr__(self):
#        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
#
# class Address(Base):
#     __tablename__ = 'address'
#     id = Column(Integer, primary_key=True)
#     email_address = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey('user_account.id'))
#     user = relationship("User", back_populates="addresses")
#     def __repr__(self):
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
# 将 DDL 发送到数据库
# Base.metadata.create_all(engine)
# 使用 ORM 插入行（自动生成的主键属性）
# squidward = User(name="squidward", fullname="Squidward Tentacles")
# krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
# 目前，我们上面的两个对象被称为处于一种称为瞬态的状态 ——它们不与任何数据库状态相关联，并且尚未与Session可以为它们生成 INSERT 语句的对象相关联。
# session = Session(engine)
# session.add(squidward)
# session.add(krabs)
# 此时，对象处于挂起状态并且尚未插入
# 当我们有待处理的对象时，我们可以通过查看被Session调用的集合来查看此状态Session.new
# session.new
# 主键标识获取行
# session.get(User, 4)
# 如果我们更改此对象的属性，Session则会跟踪此更改：
# sandy.fullname = "Sandy Squirrel"
# 该对象出现在名为 的集合中Session.dirty，表明该对象是“脏的”
# sandy in session.dirty
# 当下Session一次发出刷新时，将发出 UPDATE 更新数据库中的此值。如前所述，在我们发出任何 SELECT 之前，使用称为autoflush的行为自动发生 刷新。我们可以直接User.fullname从这一行查询列，我们将获得更新后的值
# ORM 的 UPDATE 语句
# session.execute(
#     update(User).
#     where(User.name == "sandy").
#     values(fullname="Sandy Squirrel Extraordinaire")
# )
# 删除 ORM 对象
# session.delete(patrick)
# patrick现在被删除的对象实例不再被视为在 中是持久的Session
# patrick in session
# ORM 的 DELETE 语句
# session.execute(delete(User).where(User.name == "squidward"))
# 关闭会话
# session.close()
