import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class OpenChromeGetToken(object):

    def __init__(self):
        self.info = "任务开始"

    def run(self):
        print(self.info)

        # 设置 Chrome 的选项
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")  # 禁用“Chrome 正在受到自动化软件的控制”的信息栏
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 隐藏“正在受自动化软件控制”信息
        chrome_options.add_experimental_option('useAutomationExtension', False)
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
            time.sleep(3)  # 每 3 秒检查一次
            try:
                data = driver.page_source
                # print(data)
                if "写轮眼上报" in data:
                    found_target_element = True

                    # print("找到目标元素：邮箱首页")
                    cookies = driver.get_cookies()
                    # print("获取的 Cookies：")
                    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

                    # 跳转新页面
                    driver.get("about:blank")

                    # 构建新的 HTML 内容
                    html_content = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Token</title>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                background-color: #f5f5f5;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                justify-content: center;
                                height: 40vh;
                                margin: 0;
                            }}
                    
                          .content-container {{
                                text-align: center;
                                background-color: #fff;
                                padding: 20px;
                                padding-bottom: 20px;
                                margin: 10px;
                                margin-bottom: 20px;
                                border-radius: 10px;
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                width: 60%;
                                overflow: hidden;
                            }}
                    
                          .token-content {{
                                word-wrap: break-word;
                                overflow: hidden;
                                text-overflow: ellipsis;
                            }}
                    
                          .animated-button {{
                                padding: 15px 30px;
                                background-color: #4CAF50;
                                color: white;
                                border: none;
                                border-radius: 10px;
                                cursor: pointer;
                                transition: all 0.3s ease;
                                margin-top: 6px;
                            }}
                    
                          .animated-button:active {{
                                transform: scale(0.95);
                                background-color: #45a049;
                            }}
                        </style>
                    </head>
                    
                    <body>
                        <h3 style="text-align: center">token</h3>
                        <div class="content-container">
                            <p class="token-content">{cookie_str}</p>
                        </div>
                        <button class="animated-button" onclick="copyToken()">点击复制</button>
                        <script>
                            function copyToken() {{
                                const textToCopy = '{cookie_str}';
                                const textArea = document.createElement('textarea');
                                textArea.value = textToCopy;
                                document.body.appendChild(textArea);
                                textArea.select();
                                document.execCommand('copy');
                                document.body.removeChild(textArea);
                                alert('复制成功!');
                            }}
                        </script>
                    </body>
                    
                    </html>
                    """

                    # 执行 JavaScript 设置页面内容
                    driver.execute_script(f"document.write(`{html_content}`);")

                    # print("关闭浏览器")
                    # time.sleep(40)
                    input('输入任意字符关闭插件: ')
                    driver.quit()

                    print(cookie_str)
                    return cookie_str
            except Exception as e:
                print(f"未找到目标元素，继续检查... 错误：{e}")


def main():
    # 获取 token
    get_token = OpenChromeGetToken()
    get_token.run()


if __name__ == '__main__':
    main()
