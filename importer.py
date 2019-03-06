from cookiespool.db import RedisClient


def scan():
    set_name = input('请输入账号对应网站名称')
    conn = RedisClient('accounts', set_name)
    print('请输入账号密码组(以username:格式输入) 输入exit退出读入')
    while True:
        account = input()
        if account == 'exit':
            break
        username, password = account.split(':')
        result = conn.set(username, password)
        print('账号', username, '密码', password, '录入成功' if result else '录入失败')


if __name__ == '__main__':
    scan()
