import subprocess
import re
import requests

def crawlergo_run():
    with open('targets.txt', 'r', encoding='utf-8') as f:
        for line in f:
            print(line, end="")
            line = line.replace('\n', '')
            commond = './crawlergo -t 20 -f smart --fuzz-path --output-mode json ' + line
            output = subprocess.run(commond, shell=True, capture_output=True, text=True, encoding='utf-8')
            body = str(output)
            t = re.compile('"url":"(.*?)",')
            r = t.findall(body)
            print(r)
            domain = open("./sub_domains.txt", "r", encoding='utf-8')
            for url in r:
                flag = 0
                for sub_domain in domain.readlines():
                    sub_domain = sub_domain.replace('\n', '')
                    if sub_domain in url:
                        flag = 1
                        break
                if flag == 1:
                    print(url)
                    url_to_ez(url)
                domain.seek(0)

def url_to_ez(url):
    proxies = {
        'http': 'http://127.0.0.1:2222',
        'https': 'http://127.0.0.1:2222',
    }
    # 使用代理访问URL
    response = requests.get(url, proxies=proxies, verify=False)
    print(response.text)

crawlergo_run()