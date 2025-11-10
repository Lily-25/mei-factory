from operator import index

import requests
import os
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
import pandas as pd

def extract_date_from_element(element):
    """
    从元素中提取日期信息
    """
    # 方法1: 直接在当前元素中查找日期
    date_patterns = [
        #r'(\d{4}-\d{1,2}-\d{1,2})',
        #r'(\d{4}\.\d{1,2}\.\d{1,2})',
        #r'(\d{4}/\d{1,2}/\d{1,2})',
        r'(\d{4}年\d{1,2}月\d{1,2}日)'
    ]

    # 检查元素文本
    element_text = element.get_text().strip()
    for pattern in date_patterns:
        match = re.search(pattern, element_text)
        if match:
            return match.group(1)

    # 方法2: 在相邻元素中查找日期
    parent = element.parent
    if parent:
        parent_text = parent.get_text().strip()
        for pattern in date_patterns:
            match = re.search(pattern, parent_text)
            if match:
                return match.group(1)

    # 方法3: 在父元素的相邻元素中查找
    if parent and parent.parent:
        siblings = parent.parent.find_all(recursive=False)
        for sibling in siblings:
            sibling_text = sibling.get_text().strip()
            for pattern in date_patterns:
                match = re.search(pattern, sibling_text)
                if match:
                    return match.group(1)

    # 方法4: 在class或id包含date/time的元素中查找
    date_elements = element.find_parent().find_all(class_=re.compile(r'date|time|日期|时间'))
    for date_elem in date_elements:
        date_text = date_elem.get_text().strip()
        for pattern in date_patterns:
            match = re.search(pattern, date_text)
            if match:
                return match.group(1)

    return 'unknown'

def parse_links_from_html(html_content):
    """
    从HTML内容中解析以"奇瑞"或"iCAR"开头的超链接
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有超链接
    all_links = soup.find_all('a', href=True)

    # 定义匹配模式
    pattern_奇瑞 = re.compile(r'^奇瑞')
    pattern_iCAR = re.compile(r'^iCAR', re.IGNORECASE)

    matched_links = []

    for link in all_links:
        link_text = link.get_text().strip()

        # 检查链接文本是否以"奇瑞"或"iCAR"开头
        if link_text and (pattern_奇瑞.match(link_text) or pattern_iCAR.match(link_text)):
            # 获取完整的URL
            href = link.get('href')
            if href and not href.startswith('javascript:'):

                #过滤产品介绍
                if link_text == '奇瑞iCAR 03T13.98-16.58万':
                    continue

                date = extract_date_from_element(link)
                matched_links.append({
                    'text': link_text,
                    'full_url': href if href.startswith('http') else f"https://12365auto.com{href}" if href.startswith(
                        '/') else href,
                    'date': date
                })

    return matched_links

def download_webpage(url, save_path=None, headers=None):
    """
    下载网页并保存到本地

    参数:
        url: 要下载的网页URL
        save_path: 保存路径（可选）
        headers: 请求头（可选）
    """
    # 设置默认请求头
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    try:
        # 发送GET请求[citation:4][citation:9]
        response = requests.get(url, headers=headers, timeout=30)

        # 检查请求是否成功[citation:4]
        if response.status_code == 200:
            # 如果没有指定保存路径，自动生成
            if save_path is None:
                parsed_url = urlparse(url)
                filename = f"webpage_{parsed_url.netloc}_{int(time.time())}.html"
                save_path = filename

            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            html_content = response.text
            matched_links = parse_links_from_html(html_content)
            print(matched_links)

            # 保存网页内容[citation:9]
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(html_content)

            print(f"网页已成功下载到: {save_path}")
            return True, matched_links
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return False, []

    except requests.exceptions.RequestException as e:
        print(f"下载过程中出现错误: {e}")
        return False, []


def download_multiple_pages(base_url, start_page=1, end_page=10, save_dir="downloaded_pages"):
    """
    下载多个页码的网页

    参数:
        base_url: 基础URL（包含{page}占位符）
        start_page: 起始页码
        end_page: 结束页码
        save_dir: 保存目录
    """
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    matched_links = []

    for page in range(start_page, end_page + 1):
        # 替换URL中的页码
        current_url = base_url.replace("{page}", str(page))

        # 生成保存路径
        filename = f"page_{page}.html"
        save_path = os.path.join(save_dir, filename)

        print(f"正在下载第 {page} 页: {current_url}")

        # 下载网页
        success, links = download_webpage(current_url,save_path)

        if success:
            print(f"第 {page} 页下载完成")
            matched_links = matched_links + links
        else:
            print(f"第 {page} 页下载失败")

        # 添加延迟，避免请求过于频繁
        time.sleep(1)

    return matched_links


def main():
    """
    主函数 - 下载指定网站的所有相关页面
    """
    print("开始下载网页...")

    # 如果需要下载多个页面，可以使用下面的代码
    # 注意：需要先了解网站的分页规则
    base_url = "https://12365auto.com/search/search.aspx?page={page}&search=%E5%A5%87%E7%91%9E+iCAR&t=2"
    matched_links = download_multiple_pages(
        base_url=base_url,
        start_page=1,
        end_page=21,  # 根据实际页数调整
        save_dir="iCAR_Complaints"
    )

    df = pd.DataFrame(matched_links)

    df.to_csv("data/mid/statics.csv", index=False)

    """
    for item in matched_links:
        print(item)
        save_dir = "iCAR_Complaints/details/"
        filename = f"{item['text']}.html"
        save_path = os.path.join(save_dir, filename)
        download_webpage(item['full_url'], save_path)
    """

if __name__ == "__main__":
    main()