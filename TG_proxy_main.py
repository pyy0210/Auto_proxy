# coding=utf-8
import base64
import requests
import re
import time
import os

#文件路径
update_path = "./sub/"
#所有的clash订阅链接
end_list_clash = []
#所有的v2ray订阅链接
end_list_v2ray = []
#所有的节点明文信息
end_bas64 = []
#获得格式化后的链接
new_list = []
#永久订阅
e_sub = ['https://openit.daycat.space/long','http://file.52nfw.cn/word/obtain.php?user=111111&id=1','https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub','https://raw.githubusercontent.com/kxswa/k/k/v2ray','https://www.prop.cf/?name=paimon&client=base64','https://gitlab.com/univstar1/v2ray/-/raw/main/data/v2ray/general.txt']
#频道
urls =["https://t.me/s/masco899","https://t.me/s/nice16688","https://t.me/s/airproxies","https://t.me/s/jokerbphome","https://t.me/s/kxswa","https://t.me/s/BaiPiao166","https://t.me/s/beiyiwangdeguodu","https://t.me/s/baipiaoi","https://t.me/s/dingyue_Center","https://t.me/s/fffffx2","https://t.me/s/xuanyizero"]



#获取群组聊天中的HTTP链接
def get_channel_http(url):
    headers = {
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://t.me/s/wbnet',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.post(
        url, headers=headers)
    #print(response.text)
    pattren = re.compile(r'"https+:[^\s]*"')
    url_lst = pattren.findall(response.text)
    return url_lst


#对bs64解密
def jiemi_base64(data):  # 解密base64
    # data= '''{'aa':'bb'}'''
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return base64.b64decode(data).decode('ascii')
    #print(type(base64.b64decode(data)))
    #b"{'name':'kkk','age':22}"
    #<class 'bytes'>


#判读是否为订阅链接
def get_content(url_lst):
    #对链接进行格式化
    for i in url_lst:
        result = i.replace("\\", "").replace('"', "")
        if result not in new_list:
            new_list.append(result)
    #print(new_list)
    #print("共获得", len(new_list), "条链接")
    #获取单个订阅链接进行判断
    i = 1
    try:
        new_list_down = new_list[-20::]
    except:
        new_list_down = new_list[len(new_list) * 2 // 3::]
    print("共获得", len(new_list_down), "条链接")
    for o in new_list_down:
        try:
            res = requests.get(o)
            #判断是否为clash
            try:
                skuid = re.findall('proxies:', res.text)[0]
                if skuid == "proxies:":
                    print(i, ".这是个clash订阅", o)
                    end_list_clash.append(o)
            except:
                #判断是否为v2
                try:
                    #解密base64
                    peoxy = jiemi_base64(res.text)
                    print(i, ".这是个v2ray订阅", o)
                    end_list_v2ray.append(o)
                    end_bas64.extend(peoxy.splitlines())
                    
                #均不是则非订阅链接
                except:
                    print(i, ".非订阅链接")
        except:
            print("第", i, "个链接获取失败跳过！")
        i += 1
    return end_bas64


def write_document():
    if end_list_v2ray == [] or end_list_clash == []:
        #print("https://oss.v2rayse.com/proxies/data/2022-07-08/cvSBda.yaml")
        return "https://oss.v2rayse.com/proxies/data/2022-07-08/cvSBda.yaml"
    else:
        #永久订阅
        em = 1
        for e in e_sub:
            try:
                res = requests.get(e)
                proxys=jiemi_base64(res.text)
                end_bas64.extend(proxys.splitlines())
            except:
                print("第",em,"永久订阅出现错误❌跳过")
            em += 1
        print('永久订阅更新完毕')
        
        #去重
        end_bas64_A = list(set(end_bas64))
        print("去重完毕！！去除",len(end_bas64) - len(end_bas64_A),"个重复节点")
        bas64 = '\n'.join(end_bas64_A).replace('\n\n', "\n").replace('\n\n', "\n").replace('\n\n', "\n")
        
        #获取时间，给文档命名用
        t = time.localtime()
        date = time.strftime('%y%m', t)
        date_day = time.strftime('%y%m%d', t)
        #创建文件路径
        try:
            os.mkdir(f'{update_path}{date}')
        except FileExistsError:
            pass
        txt_dir = update_path + date + '/' + date_day + '.txt'
        #写入时间订阅
        file = open(txt_dir, 'w', encoding='utf-8')
        file.write(bas64)
        file.close()       
        
        #减少获取的个数
        r = 1
        length = len(end_bas64_A)  # 总长
        m = 8  # 切分成多少份
        step = int(length / m) + 1  # 每份的长度
        for i in range(0, length, step):
            print("起",i,"始",i+step)
            zhengli = '\n'.join(end_bas64_A[i: i + step]).replace('\n\n', "\n").replace('\n\n', "\n").replace('\n\n', "\n")
            #将获得的节点变成base64加密，为了长期订阅
            obj = base64.b64encode(zhengli.encode())
            plaintext_result = obj.decode()
            #写入长期订阅
            file_L = open("Long_term_subscription"+str(r), 'w', encoding='utf-8')
            file_L.write(plaintext_result)
            r += 1
        #写入总长期订阅
        obj = base64.b64encode(bas64.encode())
        plaintext_result = obj.decode()
        file_L = open("Long_term_subscription_num", 'w', encoding='utf-8')
        file_L.write(plaintext_result)
        print("订阅写入完成✅")
        try:
            numbers =sum(1 for _ in open(txt_dir))
            print("共获取到",numbers,"节点")
        except:
            print("出现错误！")
        
    return

#获取clash订阅
def get_yaml():
    print("开始获取clsah订阅")
    urls = ["https://suo.yt/AmwsC4c",
            "https://v1.mk/y5kPoHm", "https://v1.mk/6mm8aPR"]
    n = 1
    for i in urls:
        response = requests.get(i)
        #print(response.text)
        file_L = open("Long_term_subscription" + str(n) +".yaml", 'w', encoding='utf-8')
        file_L.write(response.text)
        file_L.close()
        n += 1
    print("clash订阅获取完成！")


if __name__ == '__main__':
    for url in urls:
        resp = get_content(get_channel_http(url))
        print(url, "获取完毕！！")
    res = write_document()
    clash_sub = get_yaml()
    print("执行完毕！！")
