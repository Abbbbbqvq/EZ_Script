import subprocess
import re
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# 忽略InsecureRequestWarning类型的警告
warnings.simplefilter('ignore', InsecureRequestWarning)

black_list = ["网站防火墙"]
black_path = [".js", ".jsx", ".coffee", ".ts", ".css", ".less", ".sass", ".scss", ".jpg", ".png", ".gif", ".bmp", ".svg", ".svg", ".ttf", ".eot", ".woff", ".woff2", ".ejs", ".jade", ".vue"]
url_http_cache = set()
url_https_cache = set()

def crawlergo_run():
    with open('targets.txt', 'r', encoding='utf-8') as f:
        for line in f:
            #print(line, end="")
            line = line.replace('\n', '')
            commond = './crawlergo -t 20 -f smart --fuzz-path --output-mode json ' + line
            output = subprocess.run(commond, shell=True, capture_output=True, text=True, encoding='utf-8')
            body = str(output)
            t = re.compile('"url":"(.*?)",')
            r = t.findall(body)
            #print(r)
            domain = open("./sub_domains.txt", "r", encoding='utf-8')
            for url in r:
                no_black_path_flag = 1
                for check_black_path in black_path:
                    if check_black_path in url:
                        no_black_path_flag = 0
                        break
                if no_black_path_flag == 0:
                    print("该路径为资源文件路径，忽略当前url")
                    continue
                domain_in_url_flag = 0
                if domain_in_url_flag != 1:
                    for sub_domain in domain.readlines():
                        sub_domain = sub_domain.replace('\n', '')
                        if sub_domain in url:
                            domain_in_url_flag = 1
                            break
                if domain_in_url_flag == 1:
                    #print(url)
                    if "https" in url:
                        path = r'https?://[^/]+/'
                        find_path = re.search(path, url)
                        #print('2：' + find_path.group())
                        domains = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
                        find_domains = re.search(domains, url)
                        s = find_domains.group() + '/' + url.replace(find_path.group(), '')
                        if s not in url_https_cache:
                            url_https_cache.add(s)
                            #print(url_https_cache)
                        else:
                            continue
                    elif "http" in url:
                        path = r'http?://[^/]+/'
                        find_path = re.search(path, url)
                        #print('1：' + find_path.group())
                        domains = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
                        find_domains = re.search(domains, url)
                        # print('asdasd：' + url.replace(find_path.group(),''))
                        s = find_domains.group() + '/' + url.replace(find_path.group(), '')
                        if s not in url_http_cache:
                            url_http_cache.add(s)
                            #print(url_http_cache)
                        else:
                            continue

                    url_is_on_live_flag = url_to_ez(url)
                    #print(url_is_on_live_flag)
                    if url_is_on_live_flag == 1:
                        continue
                domain.seek(0)

def url_to_ez(url):
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    # 使用代理访问URL
    try:
        print("正在请求：" + url)
        response = requests.get(url, proxies=proxies, verify=False, timeout=10)
        for i in black_list:
            if i in response.text:
                print("检测到防火墙，忽略该条url")
                return 1
        return 0
    except requests.exceptions.RequestException as e:
        #print(f'访问 {url} 时发生错误: {e}')
        print("访问超时，执行下一条url")
        return 1
    except requests.exceptions.Timeout:
        return 1

crawlergo_run()
