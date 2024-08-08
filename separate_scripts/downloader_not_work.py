import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def extract_last_two_digits(filename):
    digits = re.findall(r'\d+', filename)
    if digits:
        return digits[-1][-2:]
    return None

def download_image(img_url, folder):
    img_name = os.path.join(folder, os.path.basename(img_url))
    try:
        with open(img_name, 'wb') as f:
            f.write(requests.get(img_url).content)
        print(f"Downloaded: {img_name}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

def download_images_from_webpage(url, folder, scroll_duration=15):
    # Налаштування веб-драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # Натиснення кнопки "Читати розділ"
    try:
        read_button = driver.find_element(By.XPATH, "//a[b[text()='Читати розділ']]")
        read_button.click()
        print("Clicked on 'Читати розділ' button.")
    except NoSuchElementException:
        print("Button 'Читати розділ' not found.")
        driver.quit()
        return

    # Зачекати 5 секунд після натискання кнопки
    time.sleep(5)

    # Прокручування сторінки протягом вказаного часу
    end_time = time.time() + scroll_duration
    while time.time() < end_time:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Зачекати, поки сторінка завантажиться

    # Отримати всі зображення
    img_tags = driver.find_elements(By.TAG_NAME, "img")
    img_urls = [img.get_attribute('src') for img in img_tags if img.get_attribute('src') and re.match(r'.*_\d{2}\.jpg$', img.get_attribute('src'))]

    if not os.path.exists(folder):
        os.makedirs(folder)

    for img_url in img_urls:
        download_image(img_url, folder)

    driver.quit()

# Використання
url = 'https://manga.in.ua/chapters/2280-berserk-tom-2-rozdil-004.html'
image_folder = 'images'

download_images_from_webpage(url, image_folder)
