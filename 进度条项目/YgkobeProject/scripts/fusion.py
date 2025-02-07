import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class OpenChromeGetToken(object):

    def run(self):
        # 设置 Chrome 的选项
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")  # 禁用“Chrome正在受到自动化软件的控制”的信息栏
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

                    # 跳转新页面
                    driver.get("about:blank")
                    # 使用 JavaScript 创建新内容
                    js_code_show_content = f"""
                    const contentDiv = document.createElement('div');
                    contentDiv.style.margin = '10px';
                    contentDiv.textContent = `{cookie_str}`;
                    """

                    js_code_button_head = """
                    const buttonDiv = document.createElement('div');
                    const button = document.createElement('button');
                    button.textContent = '点击复制token';
                    button.style.backgroundColor = '#4CAF50'; // 绿色背景
                    button.style.color = 'white';
                    button.style.margin = '10px';
                    button.style.padding = '12px 24px';
                    button.style.borderRadius = '5px';
                    button.style.border = 'none';
                    button.style.cursor = 'pointer';
                    button.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
                    button.onclick = function() {
                        this.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            this.style.transform = 'scale(1)';
                        }, 100);

                    """

                    js_code_copy_content = f"""
                    const textToCopy = `{cookie_str}`;
                    """

                    js_code_button_bottom = """
                        const textArea = document.createElement('textarea');
                        textArea.value = textToCopy;
                        document.body.appendChild(textArea);
                        textArea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textArea);
                        alert('复制token成功!');
                    };
                    buttonDiv.appendChild(button);

                    document.body.appendChild(contentDiv);
                    document.body.appendChild(buttonDiv);

                    const style = document.createElement('style');
                    style.textContent = `
                        button:hover {
                            background-color: #45a049;
                        }
                    `;
                    document.head.appendChild(style);
                    """

                    # 合并 JavaScript 代码
                    js_code_fusion = js_code_show_content + js_code_button_head + js_code_copy_content + js_code_button_bottom

                    # 执行 JavaScript 代码
                    driver.execute_script(js_code_fusion)

                    # print("关闭浏览器")
                    # time.sleep(40)
                    input('关闭插件: ')
                    driver.quit()

                    print(cookie_str)
                    return cookie_str
            except Exception as e:
                print(f"未找到目标元素，继续检查... 错误：{e}")




def main():
    # 获取token
    open = OpenChromeGetToken()
    token = open.run()
    pass




if __name__ == '__main__':
    main()

