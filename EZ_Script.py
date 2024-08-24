import subprocess
import re
import requests

black_list = ["网站防火墙"]

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
                domain_in_url_flag = 0
                for sub_domain in domain.readlines():
                    sub_domain = sub_domain.replace('\n', '')
                    if sub_domain in url:
                        domain_in_url_flag = 1
                        break
                if domain_in_url_flag == 1:
                    #print(url)
                    url_is_on_live_flag = url_to_ez(url)
                    print(url_is_on_live_flag)
                    if url_is_on_live_flag == 1:
                        break
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
                return 1
        return 0
    except requests.exceptions.RequestException as e:
        print(f'访问 {url} 时发生错误: {e}')
        return 1
    except requests.exceptions.Timeout:
        return 1

crawlergo_run()
