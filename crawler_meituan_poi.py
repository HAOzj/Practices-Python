# -*- coding:utf-8 -*-
"""
Created on Julio 01 2022

@author : woshihaozhaojun@sina.com
"""
import requests
import json


url = "https://i.waimai.meituan.com/openh5/homepage/poilist"
headers = {
"Host": "i.waimai.meituan.com",
"Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh-Hans;q=0.9",
"Content-Type": "application/x-www-form-urlencoded",
"Origin": "https://h5.waimai.meituan.com",
"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
"Connection": "keep-alive",
"Referer": "htts://h5.waimai.meituan.com/",
"Content-Length": "1805",
"mtgsig": '{"a1":"1.0","a2":1654090486594,"a3":"65893xyv31z7595316548x0188ux4vzy8188u3734809795849y1v5xx","a4":"d0adaae15a288581e1aaadd08185285aa379d4cf22fcfc95","a5":"ZcNaSjLgrlT8jBe/GH4jix5RNKG4BPma9xTdMiGm7psYbcGhggXaq3xueruHCikOnFQx0fum0VuUu2fFyfr=","a6":"h1.0CqYlsb1xzW5AozM3C8cpXW1srvImIxU0QQoAm5lsJ+GUwaL9wgBreGKEk9EE7r2NJekgXq0jpoqGSfePXdqdKxBbRKRAE/'
}
cookies_str = """_lxsdk_s=1811f62603f-021-0ed-879%7C%7C306; isIframe=false; openh5_uuid=87703994715DD356BD762167FAFE3CDFCBE66B2226967A3AF927FFEEDDD935B5; terminal=i; w_token=1Yc33kTDc2BiLCu40yJuKNiNToMAAAAABRIAADdoeYSWMcDHlOkBu69wTloLQVzVmlNG8llz5o_kI61zrkDf7QSgBmVmrsRP-F9wjg; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; WEBDFPID=65893xyv31z7595316548x0188ux4vzy8188u3734809795849y1v5xx-1654175351135-1654088948573GOOAGKS868c0ee73ab28e1d0b03bc83148500061296; openh5_uuid=87703994715DD356BD762167FAFE3CDFCBE66B2226967A3AF927FFEEDDD935B5; uuid=87703994715DD356BD762167FAFE3CDFCBE66B2226967A3AF927FFEEDDD935B5; au_trace_key_net=default; cssVersion=b876f7c4; request_source=openh5; channelType={%22mtib%22:%220%22}; mt_c_token=1Yc33kTDc2BiLCu40yJuKNiNToMAAAAABRIAADdoeYSWMcDHlOkBu69wTloLQVzVmlNG8llz5o_kI61zrkDf7QSgBmVmrsRP-F9wjg; oops=1Yc33kTDc2BiLCu40yJuKNiNToMAAAAABRIAADdoeYSWMcDHlOkBu69wTloLQVzVmlNG8llz5o_kI61zrkDf7QSgBmVmrsRP-F9wjg; token=1Yc33kTDc2BiLCu40yJuKNiNToMAAAAABRIAADdoeYSWMcDHlOkBu69wTloLQVzVmlNG8llz5o_kI61zrkDf7QSgBmVmrsRP-F9wjg; userId=1708151683; iuuid=87703994715DD356BD762167FAFE3CDFCBE66B2226967A3AF927FFEEDDD935B5; w_visitid=26956b9c-33e5-4724-b01d-07b75ad2207e; _lx_utm=utm_source%3D60030; utm_source=60030; wm_order_channel=mtib; __utma=74597006.435720927.1654084536.1654084536.1654084536.1; __utmz=74597006.1654084536.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); i_extend=C_b1Gimthomepagecategory1394H__a; ci=1; cityname=%E5%8C%97%E4%BA%AC; latlng=22.740035,113.938228,1654084536273; _lxsdk=87703994715DD356BD762167FAFE3CDFCBE66B2226967A3AF927FFEEDDD935B5; _lxsdk_cuid=1811f1ef536c8-04d09d6c4e3ac48-7d7b3762-3d10d-1811f1ef536c8"""
params = {
    "_": "1654090486593"
}
data_list = """startIndex=0&sortId=0&multiFilterIds=&sliderSelectCode=&sliderSelectMin=&sliderSelectMax=&geoType=2&rankTraceId=&uuid=87703994715DD356BD762167FAFE3CDFCBE66B2226967A3AF927FFEEDDD935B5&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fhome&riskLevel=71&optimusCode=10&firstcategoryid=0&wm_latitude=39992806&wm_longitude=116311006&wm_actual_latitude=22737056&wm_actual_longitude=113943117&wmUuidDeregistration=0&wmUserIdDeregistration=0&openh5_uuid=87703994715DD356BD762167FAFE3CDFCBE66B2226967A3AF927FFEEDDD935B5&_token=eJyVlHuLq0YYxr%2BLcPrPDqvjXF1Yip5ssuZ6dnMxm3IouRijiSYajcbS794ZNUkLpVAQ%2FM3r816eGfUPJbE3ygvUINMgUC5uorwo8Fl7pgpQ0rN4QgnWuEE4IgwBZX2PGRrmlBgaUFbJrKW8%2FIYYAQSTnzLwKdZVgFL2EzwI6eKSClsIlF2ans4vqrojz%2FnSD5f%2Bc%2Bj6abaMntfHUK1DauhHG7dQd8fQFSP9d8rh6PnRr9tjsnZf0yRzf1kt1%2Fvfs%2BTwWuV9Q%2BY3vS2uf80W8ToooG5ag6uIgcOJHJgiQCASYyBIBRFBFAtgAqABm5Au3HIMpYwCjCRgCpDBJSABuhQhArAuaxEGiI5lBW40tYQcs6oPEyJDyjnQWdUYwKoQ5ByQqjYUIshhVdMAtJJROZ48QqRjQKEuLeylBXFf%2Fs0KaNmzh51mVVtqFo2tZiWtiWO%2FpQlXVAN9%2B%2B6weVC7vOUIp5DAWlabvdWuDd%2BSKICQ1zJhSed6zZV1YN%2FN35OrDQDWdDIZDR%2F7AOxBp9kLSG8Gq%2F24uxUDENFarsR%2BpNV%2BEAR0IgaVM0pkD%2BQPNP5HFD8Q1YgFwhqJQK1GCnTcVBCucVPBuCOF%2F8BbXfFFcXZHfK9LGbl1u0flO1BrxXHpuG5MRQu9bsz4HbmYl9YC8b0jpteIAeINyoOmd0EzOuUAQTmZfMEG4h8iYmffiwS53Wu6H7Sz%2FGp%2BfP54OliYFt5n4I93pa93v87pch2SPFh0ikvbMx083tKnUbcTp6O4%2BNQX4cYI0PrQH%2B3gV4f2dBZP6T42XXbRNO%2F7sF922uO08L5ndFWYG88uF4MNCZL9kFyjIS%2Fn784sGgfW9LDIP8p5qCZ%2BxnruYTMNLOftrftVXuL5auS7PImzuD%2FI1ov91DnkzmHBnsr3D39tZ%2Bk04aUVOLb9te1dxpPuPsbp1InjmbWbhcvZMoXrQ2ucfFzfZ9dJ7pzMPZpYnjVMhrZ2jXrlxPPtqJxHl4WZDrvEmqiXvBOVZi84vW1nH9vM1BbHnCFjp9pZwvjbYtn15o7njFrs7RyuTsFRVc35%2B6fFuNk%2Ft60EFfnA3yX4cjoWtq2S3vBsY7Xo9J6GXyO7vXtv9TScG66x0lrFMAhjfiqiorhoW%2F%2BARtexy4MS7p29HvXmCTYDP87b%2Beur8udfX5KPBQ%3D%3D""".split("&")
data = {}
for ele in data_list:
    kv = ele.split("=")
    data[kv[0]] = kv[-1]
cookies = {}
for ele in cookies_str.split(";"):
    kv = ele.split("=")
    cookies[kv[0]] = kv[-1].strip()

# response = requests.post(url,
#                              headers=headers,
#                              cookies=cookies,
#                              params=params,
#                              data=data
#                          )
# shops = json.loads(response.text)["data"]["shopList"]
# for k, v in shops[0]["poi_tags"][0].items():
#     print(k)


def get_shop(page, file="meituan_poi_for_su.txt"):
    data["startIndex"] = str(page)
    response = requests.post(url,
                             headers=headers,
                             cookies=cookies,
                             params=params,
                             data=data
                             )
    shop_list = json.loads(response.text)["data"]["shopList"]
    with open(file, "a") as fp:
        for ind, shop in enumerate(shop_list):
            shop_name = shop["shopName"]
            address = shop["address"]
            tags = []
            for sub_tags in shop["poi_tags"]:
                for sub_tag in sub_tags["sub_tags"]:
                    if "text" in sub_tag:
                        tags.append(sub_tag["text"])
            tag_str = ";".join(tags)
            fp.write(f"{page},{ind},{shop_name},{address},{tag_str}\n")


def main():
    for page in range(10000):
        print(page)
        get_shop(page)


if __name__ == "__main__":
    main()

