import re
import os
import sys
import nmap
import json
import zlib
import random
import socket
import argparse
import requests
from bs4 import BeautifulSoup

def logo():
    print("""\033[36m
██╗   ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
╚██╗ ██╔╝██╔════╝██╔════╝██╔══██╗████╗  ██║
 ╚████╔╝ ███████╗██║     ███████║██╔██╗ ██║
  ╚██╔╝  ╚════██║██║     ██╔══██║██║╚██╗██║
   ██║   ███████║╚██████╗██║  ██║██║ ╚████║
   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                        v1.0
    \033[0m""")

# 请求头库
def headers_lib():
    lib = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:57.0) Gecko/20100101 Firefox/57.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:57.0) Gecko/20100101 Firefox/57.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 OPR/50.0.2762.58",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"]
    headers = {
        "User-Agent": random.choice(lib)}
    return headers

# 判断输入是IP还是域名
def isIP(str):
    try:
        check_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if check_ip.match(str):
            return True
        else:
            return False
    except:
        return False

# 格式化url
def get_domain(url):
    if "https://" in url or "http://" in url:
        url = url.replace("https://", "").replace("http://", "")
    domain = "{}".format(url).split("/")[0]
    return domain


# ----------------------------------------------------------------------------------------------------------------------
def Subscan(domain):# 主要子域名模块，需要注册securitytrails领取API
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?children_only=false&include_inactive=true"
    headers = {
        "accept": "application/json",
        "APIKEY": "2mPhSbIp3TB1WSpbleu978heR52TkIhT"
    }
    response = requests.get(url, headers=headers)
    result_json = json.loads(response.text)
    sub_domains = [i + '.' + domain for i in result_json['subdomains']] #输出结果
    current_dir = os.getcwd() #获取当前文件路径

    for i in sub_domains:
        filename = "子域名.txt"
        with open(os.path.join(current_dir, filename), 'a') as f:
            url = check_head(i)
            try:
                res = requests.get(url=url, headers=headers, allow_redirects=True, timeout=5)
                output = f"{i} {Status_code(url)} {title(res)}"
                print(output)
                output = re.sub(r'\x1b\[[0-9;]*m', '', output) #处理写入中的ascii颜色代码
                f.write(f"{output}\n")
            except Exception as e: #返回无法连接的站点
                print(f"{i} 无回应")
                f.write(f"{i} 无回应\n")
    print(f"\033[1;32m[Subdomain]:\033[1;0m \033[96m{current_dir}\{filename}\033[0m") #文件


def Status_code(domain): #获取网页状态码并加以判断
    response = requests.get(url = domain, headers = headers_lib(), allow_redirects = False)
    try:
        if str(response) == '<Response [404]>':
            return ("\033[91m[404]\033[0m")
        if str(response) == '<Response [200]>':
            return ("\033[92m[200]\033[0m")
        if str(response) == '<Response [302]>':
            return ("\033[93m[302]\033[0m")
    except NameError:
        pass
    else: #识别不了未知状态码返回
        return ([response.status_code])

def title(response): #获取网页title接口
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    return (f"\033[96m[{title}]\033[0m")

#----------------------------------------------------------------------------------------------------------------------
# 获取ip地址所属位置
def check_ip(ip):
    ip_list = []
    for i in ip:
        url = f"https://ip.cn/ip/{i}.html"
        res = requests.get(url = url, timeout = 10, headers = headers_lib())
        html = res.text
        site = re.findall('<div id="tab0_address">(.*?)</div>', html, re.S)[0]
        result = f"{i}-{site}".replace(" ", "-")
        ip_list.append(result)
    return ip_list

# 获取网页标题
def get_title(url):
    try:
        res = requests.get(url = url, headers=headers_lib(), verify=False, timeout=3)
        res.encoding = res.apparent_encoding
        html = res.text
        title = re.findall("<title>(.*?)</title>", html, re.S)[0]
    except:
        title = "None"
    return title.replace(" ", "").replace("\r", "").replace("\n", "")

# 检测http头是否缺失
def check_head(url):
    if url[:4] == "http":
        return url
    else:
        head = "https://"
        fix_url = head + url
        try:
            res = requests.get(url=url, headers=headers_lib(), verify=False)
            if res.status_code == 200:
                return fix_url
            else:
                return "http://" + url
        except:
            return "http://" + url

# 获取网站的中间件、服务器等版本信息，接口每日可调用1000次
def whatweb(url):
    response = requests.get(url,verify=False)
    whatweb_dict = {"url":response.url,"text":response.text,"headers":dict(response.headers)}
    whatweb_dict = json.dumps(whatweb_dict)
    whatweb_dict = whatweb_dict.encode()
    whatweb_dict = zlib.compress(whatweb_dict)
    data = {"info":whatweb_dict}
    res = requests.post("http://whatweb.bugscaner.com/api.go",files=data)
    whatcms = res.json()
    res_info = dict(whatcms)
    for key in res_info.keys():
        try:
            if res_info[key] is not None:
                isList = True if type(res_info[key]) == list else False
                if isList:
                    print(f"\033[1;32m[{key}]:\033[0m\033[36m{''.join(res_info[key])}\033[0m")
                else:
                    print(f"\033[1;32m[{key}]:\033[0m\033[36m{res_info[key]}\033[0m")
        except Exception as e:
            print(f"\033[1;31m[Error]:{e}\033[0m")

# 获取网站whois等基本信息
def get_base_info(url):
    domain_url = get_domain(url)
    ip = []
    try:
        addrs = socket.getaddrinfo(domain_url, None)
        for item in addrs:
            if item[4][0] not in ip:
                ip.append(item[4][0])
        if len(ip) > 1:
            print(f"\033[1;32m[Ip]:\033[0m\033[36m{check_ip(ip)}\033[0m \033[1;31m PS:CDN may be used\033[0m")

        else:
            print(f"\033[1;32m[Ip]:\033[0m\033[36m{check_ip(ip)[0]}\033[0m")
    except:
        pass
    title = get_title(check_head(url))
    print(f"\033[1;32m[Web_title]:\033[0m\033[36m{title}\033[0m".replace(" ", ""))
    whatweb(check_head(url))
    return ip


# nmap端口扫描模块
def port_scan(ip_list):
    for ip in ip_list:
        arguments = '-sV -sS -T4'
        nm = nmap.PortScanner()
        try:
            nm.scan(hosts=ip, arguments=arguments, sudo=True)
        except:
            nm.scan(hosts=ip, arguments=arguments)
        scan_info = nm[ip]
        tcp = scan_info["tcp"]
        print(f"\033[1;32m[Port_info:{ip}]:\033[0m")
        for i in tcp.keys():
            print(f"\033[1;34m{i} {tcp[i]['state']} {tcp[i]['name']} {tcp[i]['version']}\033[0m")
#-----------------------------------------------------------------------------------------------------------------------
# 读文件，批量扫描功能模块
def bat_scan(filename):
    with open(filename, "r+", encoding="utf-8") as f:
        url_list = f.readlines()
    return url_list

# 程序功能选择模块
def switch(url, port, subscan):

    if port:
        ip = get_base_info(url)
        print('\033[1;31m正在启动端口扫描......\033[0m')
        port_scan(ip)
    if subscan:
        print('\033[1;31m正在启动子域名扫描......\033[0m')
        Subscan(get_domain(url))

if __name__ == '__main__':
    logo()
    requests.packages.urllib3.disable_warnings()
    parser = argparse.ArgumentParser(description="BugMap (An automatic information collection tool for pre penetration testing)")
    parser.add_argument('-u', '--url', help='Scan target banner')
    parser.add_argument('-r', '--read', help='Batch scan target url')
    parser.add_argument('-p', '--port', help='Scan target port', action='store_true')
    parser.add_argument('-n', '--nping', help='Multi-node ping target', action='store_true')
    parser.add_argument('-d', '--dirscan', help='Scan target directory', action='store_true')
    parser.add_argument('-s', '--subscan', help='Scan target subdomain', action='store_true')
    parser.add_argument('-a', '--fullscan', help='Use all options', action='store_true')
    parser.add_argument('-o', '--outlog', help='Output log')
    args = parser.parse_args()
    url = args.url
    filename = args.read
    nping = args.nping
    port = args.port
    dirscan = args.dirscan
    subscan = args.subscan
    fullscan = args.fullscan
    outlog = args.outlog

    if filename is not None:
        url_list = bat_scan(filename)
        print(f"\033[1;32m[Total_task]:\033[0m\033[36m{len(url_list)}\033[0m")
        i = 0
        for url in url_list:
            try:
                i += 1
                url = url.replace("\n", "")
                print(f"\033[1;32m[Task_{i}]:\033[0m\033[36m{url}\033[0m")
                switch(check_head(url),port)
                print()
            except Exception as e:
                print(f"\033[1;31m[Error]:{e}\033[0m")
    else:
        if url:
            print(f"\033[1;32m[Task]:\033[0m\033[36m{url}\033[0m")
            switch(check_head(url), port, subscan)