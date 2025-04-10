import os
import requests
from bs4 import BeautifulSoup
import time

# 保存路径
DOWNLOAD_DIR = "spotify_apks"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 获取所有版本页面
BASE_URL = "https://spotify.en.uptodown.com/android/versions"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_versions():
    response = requests.get(BASE_URL, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    version_links = []
    for tag in soup.select("div.version div.more-info > a"):
        href = tag.get("href")
        if href and href.startswith("/android/download/"):
            full_url = "https://spotify.en.uptodown.com" + href
            version_links.append(full_url)

    return version_links

def download_apk(download_url):
    print(f"正在下载: {download_url}")
    resp = requests.get(download_url, headers=headers, allow_redirects=True)
    resp.raise_for_status()

    # 自动跟随跳转并获取最终文件
    filename = download_url.strip("/").split("/")[-1] + ".apk"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(resp.content)
    print(f"已保存: {filepath}")

def main():
    versions = fetch_versions()
    print(f"共找到 {len(versions)} 个版本")

    for url in versions[:5]:  # 可调试先下载前5个
        try:
            download_apk(url)
            time.sleep(2)  # 避免请求太快被封
        except Exception as e:
            print(f"下载失败: {e}")

if __name__ == "__main__":
    main()
