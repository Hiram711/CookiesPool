from io import BytesIO
from PIL import Image
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
import tesserocr


class RmHnairCookies():
    def __init__(self, username, password, browser):
        self.url = 'http://rm.hnair.com'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.delete_all_cookies()
        self.browser.get(self.url)

    def submit(self, captcha):
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        rand = self.wait.until(EC.presence_of_element_located((By.ID, 'rand')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        rand.send_keys(captcha)
        self.browser.execute_script("jQuery('#fm1').submit();")

    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'btnLoginOut'))))
        except UnexpectedAlertPresentException:
            self.browser.switch_to_alert().dismiss()
            print('登录失败：无法识别验证码')
            return False
        except TimeoutException:
            print('登录失败：超时')
            return False

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """

        img = self.wait.until(EC.presence_of_element_located((By.ID, 'code')))
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        return captcha

    def clear_image(self, image):
        image = image.convert('L')
        threshold = 127
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, '1')
        return image

    def detect_image(self, image):
        result = tesserocr.image_to_text(image)
        print('验证码识别为', result)
        return str(result)

    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()

    def main(self):
        """
        破解入口
        :return:
        """
        self.open()
        tag = False
        retry = 0
        while not tag and retry < 3:
            image = self.get_image()
            image = self.clear_image(image)
            numbers = self.detect_image(image)
            self.submit(numbers)
            tag = self.login_successfully()
            retry += 1
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        else:
            return {
                'status': 3,
                'content': '登录失败'
            }


if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
    result = RmHnairCookies('jie.zhang8', 'Zj930711', driver).main()
    print(result)
