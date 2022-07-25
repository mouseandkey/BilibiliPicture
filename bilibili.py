import requests
import time
import json
import os
from bs4 import BeautifulSoup as bs

def download_pic(url, uname,name):
    path = f"E://bilibili//{uname}//{name}.jpg"
    restart = 1
    while restart < 10:
        resp = requests.get(url)
        if resp.status_code == 200:
            with open(path, "wb") as fp:
                fp.write(resp.content)
            break
        restart += 1
    print(path)

def dynamic(uid, uname, dynamic_id):
    # PATH = "E://bilibili//秋风笑里有明哲//"
    PATH = f"E://bilibili//{uname}//"
    next_offset = ""
    page = 1
    dynamic_new = 0
    # uid = 194846269
    # uid = 424692353

    # 上线发动态时间统计
    # try:
    #     with open(f".//{uname}.json", "r") as fp:
    #          desc_list = json.load(fp)
    # except FileNotFoundError:
    #     desc_list = []

    desc = {}
    desc_ = ["type", "rid", "dynamic_id", "timestamp"]
    while True:
        URL = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?_device=android&channel=bili&from=space&host_uid={uid}&https_url_req=0&mobi_app=android&need_top=1&offset_dynamic_id={next_offset}&page={page}&platform=android&qn=32&src=bili&visitor_uid=229027149"
        resp = requests.get(URL)
        json_ = resp.json()
        #
        for card in json_['data']['cards']:
            if card['extra']['is_space_top']:
                continue
            desc = {}
            for key in desc_:
                desc[key] = card['desc'][key]

            if desc['dynamic_id'] == dynamic_id:
                break
            # desc_list.append(desc)
            card_ = json.loads(card['card'])
            if len(card_.keys()) == 2:
                try:
                    pictures = card_['item']['pictures']
                except KeyError:
                    print(desc['dynamic_id'], "有问题")
                    continue
                if dynamic_new == 0:
                    dynamic_new = desc['dynamic_id']
                download_pic(pictures[0]['img_src'], uname, desc['dynamic_id'])
                if len(pictures) > 1:
                    print(desc['dynamic_id'], "多图")
                    for i in range(1, len(pictures)):
                        download_pic(pictures[i]['img_src'], uname, str(desc['dynamic_id']) + "_" + str(i))
        print("page:", page)
        print(len(json_['data']['cards']))

        #
        next_offset = json_['data']['next_offset']
        if desc['dynamic_id'] == dynamic_id or json_['data']["has_more"] != True :
            print(uname, "动态历史爬取完毕！")
            break
        page += 1


    # with open(f".//{uname}.json", "w") as fp:
    #     json.dump(desc_list, fp)
    if dynamic_new == 0:
        dynamic_new = desc['dynamic_id']

    return dynamic_new

if __name__ == '__main__':
    with open(".//dynamic.json", "r") as fp:
        dynamic_id_list = json.load(fp)
    for dynamic_id in dynamic_id_list:
        print(dynamic_id)
        dynamic_id['dynamic_id'] = dynamic(dynamic_id['uid'], dynamic_id['uname'], dynamic_id['dynamic_id'])
        with open(".//dynamic.json", "w") as fp:
            json.dump(dynamic_id_list, fp)
	
    input()
