# Redis数据库地址
REDIS_HOST = '10.42.1.74'

# Redis端口
REDIS_PORT = 6179

# Redis密码，如无填None
REDIS_PASSWORD = 'foobared'

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'
BROWSER_EXECUTABLE_PATH = 'D:\chromedriver_win32\chromedriver.exe'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'rmhnair': 'RmHnairCookiesGenerator',
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'rmhnair': 'RmHnairValidTester',
}

# 产生器和验证器循环周期
CYCLE = 120

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5000

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = True
