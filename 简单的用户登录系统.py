# 使用Python制作简单的用户登录系统

# 使用列表存储用户名与密码
users = ['root', 'westos']
passwd = ['123', '456']

# 初始化用户登录机会数，用户在列表中的位置，以及登录是否成功标志
print('****用户登录系统****')
chance = 3
index = -1
succeed = False
# 判断用户名是否存在
while chance > 0:
    try:
        userName = input("请输入用户名：")
        index = users.index(userName)
        # 用户名存在，重置尝试次数，检查密码
        chance = 3
        while chance > 0:
            if passwd[index] == input('请输入密码：'):
                print('登陆成功！！！')
                succeed = True
                break
            else:
                print('密码错误！！！')
                chance -= 1
        if succeed:
            break
    except ValueError:
        print('用户不存在！！！')
        chance -= 1
# 根据用户登录是否成功，输出语句
if succeed:
    print('{}，欢迎'.format(userName))
else:
    print('您的登录尝试次数已用尽，请稍后重试。')
