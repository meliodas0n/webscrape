from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
import time
from PIL import Image

PATH = "/home/meliodas/WebScrape/chromedriver"
DOWNLOAD_PATH = "/home/meliodas/WebScrape/images/"
wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    url = "https://www.google.com/search?q=4k+wallaper+for+pc&hl=en&tbm=isch&sxsrf=AOaemvL115dYbtkTQa8njixpRfU2GdYj8w%3A1635600496994&source=hp&biw=1207&bih=1160&ei=cEh9YZavOYfN1sQP-cGHwA4&iflsig=ALs-wAMAAAAAYX1WgLqQuxIpZ14KzoyHCwjUTpe1KnMJ&oq=4k+walla&gs_lcp=CgNpbWcQAxgBMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoKCCMQ7wMQ6gIQJzoICAAQgAQQsQM6CwgAEIAEELEDEIMBULQsWJwyYPM8aAFwAHgAgAGkAYgBhAmSAQMwLjiYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img#imgrc=Bhiq4tQ1HaxkYM"
    wd.get(url)
    image_urls = set()
    while len(image_urls) < max_images:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
        for thumbnail in thumbnails[len(image_urls) : max_images]:
            try:
                thumbnail.click()
                time.sleep(delay)
            except:
                continue
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    continue
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found image! {len(image_urls)}")
    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, 'wb') as f:
            image.save(f, "JPEG")
        
        print("succes")
    except Exception as e:
        print(f'FAILED {e}')

urls = get_images_from_google(wd, 0.5, 5)
for i, url in enumerate(urls):
    download_image(DOWNLOAD_PATH, url, f'{i}.jpg')
wd.quit()