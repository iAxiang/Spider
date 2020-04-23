import json
import time
import requests


def data_search(query):
    # 获取链接
    # 打开json文件
    dataJson = open('other.json', encoding='utf-8')
    # 将json文件转换成python对象
    data = json.load(dataJson)
    data_list = []

    url = 'http://api.map.baidu.com/place/v2/search?'
    outType = 'json'
    # ak = 'h0g4UwgMKfYgqRETP8tbSgbtLNWoj2s1'
    ak = 'G3jGAbY2QpIX4wZAjmEnH9Ow9FXIk4y2'

    for i in data:
        # 经度
        longitude = str(i['Longitude'])
        # 纬度
        latitude = str(i['Latitude'])
        # http://api.map.baidu.com/place/v2/search?query=银行&location=39.915,116.404&radius=2000&output=xml&ak=您的密钥 //GET请求
        iurl = url + 'query=' + query + '&location=' + latitude + ',' + longitude + '&radius=2000&output=' + outType + '&ak=' + ak
        data_dict = {
            'city' : i['City'],
            'longitude':i['Longitude'],
            'latitude':i['Latitude'],
            'url' : iurl
        }
        data_list.append(data_dict)

    with open('storeInfo.comments', 'a+', encoding='utf-8') as f:
        f.write(
            'longitude' + ',' + 'latitude' + ',' + 'city' + ',' + 'area' + ',' + 'name' + ',' + 'lng' + ',' + 'lat' + ',' + 'address' + ',' + 'telephone' + '\n')
    for i in data_list:
        time.sleep(10)
        req = requests.get(i['url'])
        req_dict = req.json()
        print(i['longitude'], i['latitude'])
        print(req_dict)
        if req_dict['status'] == 401:
            continue
        else:
            for j in req_dict['results']:
                loc_list = []
                loc_list.append(j['location'])
                for k in loc_list:
                    ads_list = j.get('address', 'null').split(',')
                    ads = ''.join(ads_list)
                    phone_list = j.get('telephone', 'null').split(',')
                    phone = ' '.join(phone_list)
                    print(j.get('city', 'null') + ',' + j.get('area', 'null')  + ',' + j.get('name', 'null') + ',' + str(k.get('lng', 'null')) + ',' + str(k.get('lat', 'null')) + ',' + ads + ',' + phone + '\n')
                    with open('storeInfo.comments', 'a+', encoding='utf-8') as f:
                       f.write(str(i['longitude']) + ',' + str(i['latitude']) + ',' + j.get('city', 'null') + ',' + j.get('area', 'null') + ',' + j.get('name', 'null') + ',' + str(k.get('lng', 'null')) + ',' + str(k.get('lat', 'null')) + ',' + ads + ',' + phone + '\n')

if __name__ == '__main__':
    data_search('美食')
