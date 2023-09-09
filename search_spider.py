import base64
import os
import time
from datetime import datetime
from io import BytesIO

from PIL import Image
from selenium import webdriver


class SpiderImages:
    keyword = ''
    url = ''
    c_time = ''

    def __init__(self):
        print('START: ', datetime.now())
        self.keyword = input("Enter the keyword of the image you want to search for: ")
        self.url = 'https://www.google.com/search?q=' + self.keyword + '&tbm=isch&sclient=img'

    def temp_browser(self):
        driver = webdriver.Chrome('I:\dev\chromedriver-win64\chromedriver.exe')
        driver.get(self.url)
        driver.maximize_window()
        return driver

    def download(self, b, p):
        img_path = './result_images'
        if not os.path.exists(img_path):
            os.makedirs(img_path)

        f = open(self.keyword + ".txt", "a", encoding="utf-8")

        position = 0
        for i in range(p):
            position += 500
            b_js = 'var q = document.documentElement.scrollTop=' + str(position)
            b.execute_script(b_js)
            time.sleep(2)

            img_elements = b.find_elements_by_tag_name('img')
            for img_element in img_elements:
                try:
                    img_url = img_element.get_attribute('src')
                    if img_url is None:
                        print('None: ', img_url)
                        continue
                    print(img_url)
                    f.write("".join(img_url) + '\n')
                except Exception as e:
                    with open('exception.txt', 'w') as f:
                        f.write('异常信息:[ ' + str(e) + ' ]  ' + str(datetime.now()) + '\n')
            time.sleep(2)

    def get_picture(self):
        keyword_file = self.keyword + '.txt'
        count = 0
        with open(keyword_file, 'r', encoding='utf-8') as f:
            for b_url in f:
                if b_url.startswith('data'):
                    if "data:image/jpeg" in b_url:
                        image_data = b_url.split(',')[1]
                        decode_data = base64.b64decode(image_data)
                        image = Image.open(BytesIO(decode_data))
                        image_name = f"./result_images/{self.keyword}_{count}.jpg"
                        image.save(image_name)
                        count += 1

    def run(self):
        print('搜索链接:[ ' + self.url + ' ]')
        browser = self.temp_browser()
        self.download(b=browser, p=2)
        browser.close()
        self.get_picture()
        print('END: ', datetime.now())


if __name__ == '__main__':
    spider = SpiderImages()
    spider.run()
