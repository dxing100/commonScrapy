import pickle

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class LoginCookie:

    session_file = 'session.pkl'

    def __init__(self):
        self.session = self.load_session()

    def login(self, url, suc_tag):
        if not self.session:
            # 使用selenium模拟登陆，获取并返回cookie
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome()
            driver.get(url)
            # 定义等待条件：等待页面上出现特定元素（例如，表示扫描成功的元素）
            WebDriverWait(driver, 60)  # 设置最大等待时间为60秒

            # 如果扫描成功元素出现，表示二维码已被扫描
            while True:  # 不断循环，直到条件满足或超时
                try:
                    # "ttbar-login"
                    scan_result = driver.find_element(By.ID, suc_tag)
                    if scan_result:
                        print("扫描登陆成功！")
                        break  # 条件满足，跳出循环
                except:  # 如果出现异常（例如，页面未加载完成），则继续等待
                    pass
                time.sleep(1)  # 等待1秒后再次检查条件
            self.session = driver.get_cookies()
            # 保存session
            self.save_session()
            # 退出浏览器
            driver.quit()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in self.session}
        return cookies_dict

    def save_session(self):
        with open(self.session_file, 'wb') as file:
            pickle.dump(self.session, file)

    # 从本地文件加载session
    def load_session(self):
        # 从文件中加载会话对象
        try:
            with open(self.session_file, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None
