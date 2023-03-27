# :bug: 모기 활동 지수 예측기

<p align="center">
  <img src=img1.png width="400"/>
</p>

본 사이트는 서울시에서 운영 중인 [모기 활동 지수](https://news.seoul.go.kr/welfare/mosquito) 데이터를 기반으로 학습된 모델을 웹 어플리케이션 형태로 제공합니다. 읍면동 까지의 예측 위치 선택시 [기상청 단기예보 API](https://www.data.go.kr/data/15084084/openapi.do) 를 통해 당일 기상 정보를 조회한 후, 이를 회귀 모델의 인풋으로 활용해 0~10 사이의 모기 활동 지수를 예측하는 구조를 가지고 있습니다.

프로젝트 관련 블로그 글 : https://meme2515.github.io/projects/mosquito