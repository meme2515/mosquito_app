# 기상청 단기예보 (구 동네예보) 조회서비스
# https://www.data.go.kr/data/15084084/openapi.do#/tab_layer_detail_function

from urllib.parse import unquote
from datetime import datetime, date, timedelta
import requests
import config
import numpy as np

# API 키
key = unquote(config.api_key, 'UTF-8')

# 어제 날짜
today = datetime.today().strftime("%Y%m%d")
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%Y%m%d")

# 기상청 초단기예보 조회서비스
url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

# API 파라미터
params = {
    'serviceKey' : key, 
    'pageNo' : '1', 
    'numOfRows' : '1000', 
    'dataType' : 'JSON', 
    'base_date' : yesterday, 
    'base_time' : '2300', 
    'nx' : '55', 
    'ny' : '127' 
}

response = requests.get(url, params=params)
items = response.json().get('response').get('body').get('items')

weather_data = {
    'rain' : []
}

for item in items['item']:
    # 최저기온
    if (item['category'] == "TMN") & (item['fcstDate'] == today):
        weather_data['min_temp'] = float(item['fcstValue'])
    # 최고기온
    elif (item['category'] == "TMX") & (item['fcstDate'] == today):
        weather_data['max_temp'] = float(item['fcstValue'])
    # 강수량 (시간단위 강수량의 평균)
    elif (item['category'] == "PCP") & (item['fcstDate'] == today):
        if item['fcstValue'] == '강수없음':
            weather_data['rain'].append(0.0)
        else:
            weather_data['rain'].append(float(item['fcstValue']))
weather_data['rain'] = np.mean(weather_data['rain'])

print(weather_data)