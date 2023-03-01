# Yscan_v1.0

**Yscan是一款域名解析、端口扫描、子域名挖掘为一体的信息收集工具。**

**一、安装说明**

- 工具使用python3开发，请确保您的电脑上已经安装了python3环境。

- 工具的端口扫描功能调用了nmap接口，请确保您的电脑已安装nmap。

- 首次使用请使用 **python3 -m pip install -r requirements.txt** 命令，来安装必要的外部依赖包。

- 本机未安装pip工具的请使用如下命令来进行安装：
![1](https://user-images.githubusercontent.com/71480339/222026628-69c7cfed-f2ed-4425-9174-052e7023eb0c.png)

**二、使用说明**
**1.-u 获取网站基本信息**
```
$ python3 searchmap.py -u 192.168.0.132
```
![2](https://user-images.githubusercontent.com/71480339/222026056-bc738df4-617b-40a5-b0f4-650cbff1b3e6.png)

**2.-p 使用nmap进行隐式端口扫描**
```
$ python3 searchmap.py -u 192.168.0.132 -p
```
![3](https://user-images.githubusercontent.com/71480339/222026067-1271d9eb-6f61-42ca-8a5a-a9650f52be91.png)

**3.-r 批量扫描网站基本信息**
```
$ python3 searchmap.py -r url.txt
```
![4](https://user-images.githubusercontent.com/71480339/222026071-7e389a94-8ebd-4cae-902b-4c4ccf0d81e5.png)

**4.-s 对输入域名的进行子域名爆破**
```
需要注册securitytrails注册API
$ python3 searchmap.py -u baidu.com -s
```
![5](https://user-images.githubusercontent.com/71480339/222026076-83a9a142-8162-4a5a-bf03-06c02edb7003.png)

****************************

本工具仅面向合法授权的企业安全建设行为，如您需要测试本工具的可用性，请自行搭建靶机环境。 在使用本工具进行检测时，您应确保该行为符合当地的法律法规，并且已经取得了足够的授权。请勿对非授权目标进行扫描。如果发现上述禁止行为，我们将保留追究您法律责任的权利。 如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。 在安装并使用本工具前，请您务必审慎阅读、充分理解各条款内容，限制、免责条款或者其他涉及您重大权益的条款。除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要安装并使用本工具。 您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。 程序仅提供对漏洞点的判断，并不存在恶意操作!若检测到程序发出危险流量请及时联系作者进行删除，程序内的所有Payload来源于网络.
