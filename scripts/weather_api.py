# 기상청 단기예보 (구 동네예보) 조회서비스
# https://www.data.go.kr/data/15084084/openapi.do#/tab_layer_detail_function

# 대한민국 행정구역별 위경도 좌표
# https://skyseven73.tistory.com/23

from urllib.parse import unquote
from datetime import datetime, date, timedelta
from scripts import config, convert_latlon
import requests
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# 기상청 초단기예보 조회서비스
url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

# API 키
key = unquote(config.api_key, 'UTF-8')

# 어제 날짜
today = datetime.today().strftime("%Y%m%d")
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%Y%m%d")

# 서울 읍면동 단위 위경도 데이터
out_df = pd.DataFrame()
df = pd.read_excel('scripts/korea_latlon.xlsx', sheet_name=None)
df = pd.concat(df.values())
df = out_df.append(df,ignore_index=True)
df = df.loc[~pd.isnull(df['읍면동/구'])]

# 읍면동/구 까지의 파라미터 입력 시 조회일의 기상 예보 정보 반환
def api_call(loc1, loc2, loc3, loc4=None):
    # 위경도 조회 및 좌표 변환
    if loc4:
        df_row = df.loc[
            (df['시도'] == loc1) &
            (df['시군구'] == loc2) &
            (df['읍면동/구'] == loc3) &
            (df['읍/면/리/동'] == loc4)
        ]
    else:
        df_row = df.loc[
            (df['시도'] == loc1) &
            (df['시군구'] == loc2) &
            (df['읍면동/구'] == loc3)
        ]
    lat, lon = df_row['위도'].values[0], df_row['경도'].values[0]
    x, y = convert_latlon.mapToGrid(lat, lon)

    # API 파라미터
    params = {
        'serviceKey' : key, 
        'pageNo' : '1', 
        'numOfRows' : '1000', 
        'dataType' : 'JSON', 
        'base_date' : yesterday, 
        'base_time' : '2300', 
        'nx' : x, 
        'ny' : y
    }

    response = requests.get(url, params=params)
    items = response.json().get('response').get('body').get('items')

    weather_data = {
        'rain' : []
    }

    # 정보 취합 & 반환
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

    return weather_data