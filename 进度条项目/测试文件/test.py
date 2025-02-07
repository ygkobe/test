import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from PIL import Image as PILImage
import io

# 初始化Chrome浏览器
chrome_options = Options()
# chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

# 创建浏览器驱动
driver = webdriver.Chrome(options=chrome_options)

try:
    # 打开目标网页
    url = "https://yiyan.baidu.com/"
    driver.get(url)

    # 截图并保存到内存
    screenshot = driver.get_screenshot_as_png()
    image = PILImage.open(io.BytesIO(screenshot))

    # 将截图保存到内存中的字节流
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # 重置流位置

    # 使用 openpyxl 将内存中的图片插入到 Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Webpage Screenshot"

    # 设置图片大小
    img = Image(img_byte_arr)
    img.width, img.height = 800, 600  # 这里设置图片大小（宽度800，高度600）
    sheet.add_image(img, "A1")

    # 保存 Excel 文件
    excel_path = "webpage_screenshot.xlsx"
    workbook.save(excel_path)
    print(f"Screenshot saved to {excel_path}")

finally:
    # 关闭浏览器
    # time.sleep(10)
    driver.quit()
