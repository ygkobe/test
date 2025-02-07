import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class OpenChromeGetToken(object):

    def run(self):
        # 设置 Chrome 的选项
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--lang=en-US")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

        # 创建 Chrome WebDriver 对象
        driver = webdriver.Chrome(options=chrome_options)

        # 打开目标页面
        driver.get('https://mail.qq.com/')

        # 循环检查页面内容
        found_target_element = False
        while not found_target_element:
            time.sleep(3)  # 每3秒检查一次
            try:
                data = driver.page_source
                # print(data)
                if "写轮眼上报" in data:
                    found_target_element = True

                    # print("找到目标元素：邮箱首页")
                    cookies = driver.get_cookies()
                    # print("获取的 Cookies：")
                    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

                    print("关闭浏览器")
                    # time.sleep(40)

                    driver.quit()

                    print(cookie_str)
                    return cookie_str
            except Exception as e:
                print(f"未找到目标元素，继续检查... 错误：{e}")


class StylishWindow(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token  # 保存传入的 token 值
        self.initUI()

    def initUI(self):
        # 设置窗口大小和标题
        self.setWindowTitle('token')
        self.setFixedSize(600, 380)  # 设置窗口宽度为500，高度为330

        # 设置布局
        layout = QVBoxLayout()

        # 添加标题标签
        self.title = QLabel(self.token)  # 使用传入的 token 值
        self.title.setFont(QFont('Arial', 14))  # 调整字体大小以适应自动换行
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: black; background-color: white;")  # 设置黑色字体和白色背景
        self.title.setWordWrap(True)  # 启用自动换行
        self.title.setMaximumWidth(580)  # 限制最大宽度以控制换行
        layout.addWidget(self.title)

        # 添加按钮
        btn = QPushButton('点击复制')
        btn.setFont(QFont('Arial', 14))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #72A545;
                border-radius: 15px;
                color: white;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
            QPushButton:pressed {
                background-color: #bfbfbf;
            }
        """)
        btn.clicked.connect(self.copyTextToClipboard)  # 连接按钮点击事件到方法
        layout.addWidget(btn)

        # 将布局添加到窗口中
        self.setLayout(layout)

        # 显示窗口
        self.show()

    def copyTextToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.title.text())  # 复制标签文本到剪贴板

        QMessageBox.information(self, 'Success', 'Token 已复制到剪贴板！', QMessageBox.Ok)


def main():
    # 获取token
    # open = OpenChromeGetToken()
    # token = open.run()

    app = QApplication(sys.argv)

    token = "wqè2211221122112"
    # 示例 token 值，可以替换为实际的 token
    StylishWindow(token)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

