from selenium import webdriver


class WebdriverHelper:
    """用于获取webdriver的辅助类。"""
    # 创建浏览器启动选项
    options = webdriver.ChromeOptions()
    # 不使用GPU硬件加速，避免显示错误
    options.add_argument('--disable-gpu')
    # 避免网站发现正在使用webdriver
    options.add_argument("--disable-blink-features=AutomationControlled")
    # 设置开发者模式启动
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    def get_webdriver(self):
        """获取具有伪装的webdriver"""
        return webdriver.Chrome(executable_path='./chromedriver.exe', options=self.options)
