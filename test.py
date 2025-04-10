import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup

# 从环境变量读取 123pan 登录 cookie
COOKIE = os.environ.get("PAN_COOKIE")
DOWNLOAD_DIR = "spotify_apks"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": COOKIE,  # 使用从 GitHub Secrets 获取的 cookie
}

def fetch_versions():
    url = "https://spotify.en.uptodown.com/android/versions"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    links = []
    for a in soup.select("div.version div.more-info > a"):
        href = a.get("href")
        if href:
            links.append("https://spotify.en.uptodown.com" + href)
    return links

def download_apk(url):
    print(f"Downloading: {url}")
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    name = url.strip("/").split("/")[-1] + ".apk"
    path = os.path.join(DOWNLOAD_DIR, name)
    with open(path, "wb") as f:
        f.write(r.content)
    print(f"Saved to: {path}")
    return path

def upload_to_123pan(file_path):
    print(f"Uploading {file_path} to 123 Pan")
    
    # 设置 ChromeOptions
    options = Options()
    options.add_argument("--headless")  # 无头浏览器，不弹出 UI

    # 设置 ChromeDriver 路径
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=options)
    
    # 登录页面
    driver.get("https://www.123pan.com/")
    sleep(3)

    # 模拟登录（假设你已经有了 cookie，可以直接设置）
    driver.add_cookie({"name": "token", "value": COOKIE})  # 使用 GitHub Secrets 中的 cookie
    driver.get("https://www.123pan.com/")
    sleep(3)

    # 上传文件
    upload_button = driver.find_element(By.ID, "upload-btn")  # 根据网页元素修改
    upload_button.click()
    sleep(2)

    # 模拟选择文件上传
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(file_path)  # 选择要上传的文件路径
    sleep(5)  # 等待文件上传

    print(f"Uploaded: {file_path} to 123 Pan")

    driver.quit()

def main():
    versions = fetch_versions()
    for link in versions[:3]:  # 限制下载数量为前 3 个
        try:
            # 下载 APK
            path = download_apk(link)
            
            # 上传文件到 123pan
            upload_to_123pan(path)
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
