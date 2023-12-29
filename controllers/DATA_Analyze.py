import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# CSV 파일 경로 설정
csv_path = '/content/drive/MyDrive/P_Pro/food_db.csv'

# CSV 파일을 데이터프레임으로 읽어오기
df = pd.read_csv(csv_path)

# '식품상세분류' 별로 행의 개수 확인
count_by_category = df['식품상세분류'].value_counts()

# 결과를 확인해보니 '기타 빵류', '기타 음료류', '커피류' 가 압도적으로 많은 수치를 기록
# 추천하는 과정에서 위 식품분류만 편향적으로 추천할수도 있기에 각각 30%씩 랜덤하게 삭제
# '식품상세분류'가 '기타 빵류', '기타 음료류', '커피류' 중 하나인 경우에 30%의 확률로 삭제
mask = df['식품상세분류'].isin(['기타 빵류', '기타 음료류', '커피류'])
df['삭제'] = np.random.rand(len(df)) < 0.3
df = df[~(mask & df['삭제'])].drop(columns=['삭제'])

#최초 DB 결측치, 이상치 처리

# 채우는 방식은 2가지
# 1. 100g 당 탄수화물과 지질의 수치를 입력해 1회제공량을 기반으로 비율에 따라 결측치 처리
# 2. 특정 식품명 혹은 식품상세분류에 대해 모두 동일한 수치로 결측치 처리

# 식품상세분류가 '아이스크림'에 해당하는 행 중에서 탄수화물이나 지질에 결측치가 있는 경우
# 100g 당으로 처리 탄수화물은 25g, 지질은 10.5g 으로 채우기
condition = (df['식품상세분류'] == '아이스크림류') & (df['탄수화물(g)'].isnull() | df['지질(g)'].isnull())
df.loc[condition, '탄수화물(g)'] = df.loc[condition, '1회제공량'] * 25 / 100
df.loc[condition, '지질(g)'] = df.loc[condition, '1회제공량'] * 10.5 / 100

# 식품명에 '베이글'이 포함되는 행 중에서 탄수화물이나 지질에 결측치가 있는 경우
# 모두 탄수화물은 53g, 지질은 1.5g 으로 채우기
mask = (df['식품명'].str.contains('베이글', na=False)) & (df['지질(g)'].isnull()) & (df['탄수화물(g)'].isnull())
df.loc[mask, '지질(g)'] = 1.5
df.loc[mask, '탄수화물(g)'] = 53

#['식품상세분류'] == '과일.채소음료류'
condition = (df['식품상세분류'] == '과일.채소음료류') & (df['탄수화물(g)'].isnull() | df['지질(g)'].isnull())
df.loc[condition, '탄수화물(g)'] = df.loc[condition, '1회제공량'] * 10 / 100
df.loc[condition, '지질(g)'] = df.loc[condition, '1회제공량'] * 0.5 / 100

#['식품명']=마카롱
mask = df['식품명'].str.contains('마카롱', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.16
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.695

##['식품명']=초코롱
mask = df['식품명'].str.contains('초코롱', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.16
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.695

#['식품명']=핫도그
mask = df['식품명'].str.contains('핫도그', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.15
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.185

#['식품명']=치즈볼
mask = df['식품명'].str.contains('치즈볼', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.06
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.08

#['식품명']=치즈 스틱
mask = df['식품명'].str.contains('치즈 스틱', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.18
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.24

#['식품상세분류'] == '리조또.그라탕류'
condition = (df['식품상세분류'] == '리조또.그라탕류') & (df['탄수화물(g)'].isnull() | df['지질(g)'].isnull())
df.loc[condition, '탄수화물(g)'] = df.loc[condition, '1회제공량'] * 22.5 / 100
df.loc[condition, '지질(g)'] = df.loc[condition, '1회제공량'] * 7.5 / 100

#['식품상세분류'] == '샌드위치류'
condition = (df['식품상세분류'] == '샌드위치류') & (df['탄수화물(g)'].isnull() | df['지질(g)'].isnull())
df.loc[condition, '탄수화물(g)'] = df.loc[condition, '1회제공량'] * 48 / 350
df.loc[condition, '지질(g)'] = df.loc[condition, '1회제공량'] * 17 / 350

#['식품상세분류'] == '샐러드'
condition = (df['식품상세분류'] == '샐러드') & (df['탄수화물(g)'].isnull() | df['지질(g)'].isnull())
df.loc[condition, '탄수화물(g)'] = df.loc[condition, '1회제공량'] * 2 / 100
df.loc[condition, '지질(g)'] = df.loc[condition, '1회제공량'] * 15 / 100

#['식품상세분류'] == '앙금빵류'
condition = (df['식품상세분류'] == '앙금빵류') & (df['탄수화물(g)'].isnull() | df['지질(g)'].isnull())
df.loc[condition, '탄수화물(g)'] = df.loc[condition, '1회제공량'] * 52 / 100
df.loc[condition, '지질(g)'] = df.loc[condition, '1회제공량'] * 4 / 100

#['식품상세분류'] == '채소류튀김'
condition = (df['식품상세분류'] == '채소류튀김') & (df['탄수화물(g)'].isnull() | df['지질(g)'].isnull())
df.loc[condition, '탄수화물(g)'] = df.loc[condition, '1회제공량'] * 35.5 / 100
df.loc[condition, '지질(g)'] = df.loc[condition, '1회제공량'] * 14 / 100

# ['식품상세분류'] == '초콜릿류'
condition = (df['식품상세분류'] == '초콜릿류') & (df['탄수화물(g)'].isnull() | df['지질(g)'].isnull())
df.loc[condition, '탄수화물(g)'] = df.loc[condition, '1회제공량'] * 60 / 100
df.loc[condition, '지질(g)'] = df.loc[condition, '1회제공량'] * 30 / 100

# '식품명' = '바닐라 라떼' 포함
mask = df['식품명'].str.contains('바닐라 라떼', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.07
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.255

#식품명에 '와플'이 들어가는 식품 중 지방과 탄수화물이 결측치인 행에 대해
mask = df['식품명'].str.contains('와플', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

# '1회 제공량' 100g 당 지방은 10, 탄수화물은 50으로 '1회 제공량'을 기반으로 지방과 탄수화물 계산하여 결측치 채우기
df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.10
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.50

#['식품명']=스콘
mask = df['식품명'].str.contains('스콘', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.15
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.455

#['식품명']=핫초코
mask = df['식품명'].str.contains('핫초코', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.1
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.8

#['식품명']=초콜릿
mask = df['식품명'].str.contains('초콜릿', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.03
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.07

#['식품명']=고구마
mask = df['식품명'].str.contains('고구마', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.02
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.19

#['식품명']=카페모카
mask = df['식품명'].str.contains('카페 모카', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.01
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.08

#['식품명']=타르트
mask = df['식품명'].str.contains('타르트', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.11
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.41

#['식품명']=맘모스
mask = df['식품명'].str.contains('맘모스', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.2
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.4

#['식품명']=버블티
mask = df['식품명'].str.contains('버블티', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.01
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.2

#['식품명']=그린티
mask = df['식품명'].str.contains('그린티', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.03
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.13

#['식품명']=카푸치노
mask = df['식품명'].str.contains('카푸치노', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.016
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.025

#['식품명']=콜드브루 라떼
mask = df['식품명'].str.contains('콜드브루 라떼', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.02

#['식품명']=초코
mask = df['식품명'].str.contains('초코', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.048
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.137

#['식품명']=바게트
mask = df['식품명'].str.contains('바게트', na=False, case=False) & \
       df['1회제공량'].notnull() & \
       df['지질(g)'].isnull() & df['탄수화물(g)'].isnull()

df.loc[mask, '지질(g)'] = df.loc[mask, '1회제공량'] * 0.22
df.loc[mask, '탄수화물(g)'] = df.loc[mask, '1회제공량'] * 0.37

# 기존에 존재하는 '기타 빵류'들의 평균값으로 남은 '기타 빵류'들의 결측치를 처리
for category in df[df['식품상세분류'] == '기타 빵류']['식품상세분류'].unique():
    category_rows = df[df['식품상세분류'] == category]
    avg_fat = category_rows['지질(g)'].mean()
    avg_carbs = category_rows['탄수화물(g)'].mean()

    mask = (df['식품상세분류'] == category) & (df['지질(g)'].isnull() | df['탄수화물(g)'].isnull())

    df.loc[mask, '지질(g)'] = df.loc[mask, '지질(g)'].fillna(avg_fat)
    df.loc[mask, '탄수화물(g)'] = df.loc[mask, '탄수화물(g)'].fillna(avg_carbs)

# 기존에 존재하는 '기타 음료류'들의 평균값으로 남은 '기타 음료류'들의 결측치를 처리
for category in df[df['식품상세분류'] == '기타 음료류']['식품상세분류'].unique():
    category_rows = df[df['식품상세분류'] == category]
    avg_fat = category_rows['지질(g)'].mean()
    avg_carbs = category_rows['탄수화물(g)'].mean()

    mask = (df['식품상세분류'] == category) & (df['지질(g)'].isnull() | df['탄수화물(g)'].isnull())

    df.loc[mask, '지질(g)'] = df.loc[mask, '지질(g)'].fillna(avg_fat)
    df.loc[mask, '탄수화물(g)'] = df.loc[mask, '탄수화물(g)'].fillna(avg_carbs)

# 기존에 존재하는 '케이크류'들의 평균값으로 남은 '케이크류'들의 결측치를 처리
for category in df[df['식품상세분류'] == '케이크류']['식품상세분류'].unique():
    category_rows = df[df['식품상세분류'] == category]
    avg_fat = category_rows['지질(g)'].mean()
    avg_carbs = category_rows['탄수화물(g)'].mean()

    mask = (df['식품상세분류'] == category) & (df['지질(g)'].isnull() | df['탄수화물(g)'].isnull())

    df.loc[mask, '지질(g)'] = df.loc[mask, '지질(g)'].fillna(avg_fat)
    df.loc[mask, '탄수화물(g)'] = df.loc[mask, '탄수화물(g)'].fillna(avg_carbs)

#이상치 처리
# '1회제공량'이 2000을 초과하는 행 삭제
df = df[df['1회제공량'] <= 2000].dropna()

# '칼로리'가 1500을 초과하는 행 삭제
df = df[df['1회제공량'] <= 1500].dropna()

# 결측치, 이상치 처리 이후 최종적으로 탄수화물과 지질의 평균 파악
# 예상대로 결과가 나왔는지 혹은 튀는 값은 없는지 확인
plt.rc('font', family='NanumBarunGothic')
# GROUP_NAME에 따른 칼로리의 평균 계산
average_nutr_cont1 = df_end.groupby('GROUP_NAME')['NUTR_CONT2'].mean().reset_index()
# seaborn을 사용하여 그래프 그리기
plt.figure(figsize=(30, 6))
sns.barplot(x='GROUP_NAME', y='NUTR_CONT2', data=average_nutr_cont1)
plt.title('GROUP_NAME & Carbo_MEAN')
plt.xlabel('GROUP_NAME')
plt.ylabel('Carbo')
plt.show()

# 최종 데이터 저장
df.to_csv('/content/drive/MyDrive/food_db_final.csv', index=False)

# 추가 범주형 데이터 라벨링
# 완성된 DB에 chatGPT API 를 활용해 맛(단맛, 짠맛, 매운맛, 신맛, 담백한맛),주재료, 부재료,
# 조리 방법(굽기, 찌기, 끓이기, 튀기기, 볶기, 무치기, 저미기, 로스팅, 훈제, 회), 알레르기 유발 재료를 자동으로 라벨링

import openai
from concurrent.futures import ThreadPoolExecutor
from tqdm.notebook import tqdm

# OpenAI API 키 설정
openai.api_key = “REAL_API_KEY”

def get_label_for_food(food_name, attribute):
    try:
        # 맛에 대한 질문
        if attribute == 'taste':
            question = f"음식 '{food_name}'의 맛이 단맛, 짠맛, 매운맛, 신맛, 담백한맛 중에서 해당 단어 답해 하나로만 답해주세요. 부가적인 설명은 필요없습니다."
        # 주재료에 대한 질문
        elif attribute == 'mainIngredient':
            question = f"음식 '{food_name}'의 주된 재료는 무엇인가요? 단일 단어로 답해주세요."
        # 부재료에 대한 질문
        elif attribute == 'secondaryIngredient':
            question = f"음식 '{food_name}'에 들어가는 부재료 중 하나를 구체적으로 말해주세요. 단일 단어로 답해주세요."
        # 조리 방법에 대한 질문
        elif attribute == 'cookingMethod':
            question = f"음식 '{food_name}'는 어떻게 조리하나요? 굽기, 찌기, 끓이기, 튀기기, 볶기, 무치기, 저미기, 로스팅, 훈제, 회 중에 단일 단어 하나로만 답해주세요."
        # 알레르기 유발 재료에 대한 질문
        elif attribute == 'allergens':
            question = f"음식 '{food_name}'에 알레르기를 유발할 수 있는 재료가 있습니까? 단일 단어로 답해주세요. 알 수 없거나 없으면 '없음'이라고 답해주세요."

        # GPT 챗 모델을 사용하여 질문에 대한 답변 생성
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": question}]
        )
        answer = response.choices[0].message["content"].strip()

        return answer
    except Exception as e:
        print(f"Error processing {food_name}: {e}")
        return ''

attributes = ['taste', 'mainIngredient', 'secondaryIngredient', 'cookMethod', 'allergens']

# 병렬 처리를 위한 함수
def process_row(row):
    result = row.copy()
    for attribute in attributes:
        result[attribute] = get_label_for_food(row['name'], attribute)
    return result

# 데이터셋 로드
file_path = 'food_db_final.csv'  # 파일 경로 설정
df = pd.read_csv(file_path)

# ThreadPoolExecutor를 사용하여 병렬 처리
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(tqdm(executor.map(process_row, df.to_dict('records')), total=len(df)))

# 결과를 데이터프레임으로 변환
df_result = pd.DataFrame(results)

# 데이터셋 저장 또는 출력
df_result.to_csv('food_db_result.csv', index=False)
print(df_result.head())

# 파일 로드
df = pd.read_csv('food_db_result5.csv')

# 'allergens' 열의 데이터 길이가 10 이상인 경우 '알 수 없음'으로 변경
df['taste'] = df['taste'].apply(lambda x: '알 수 없음' if len(str(x)) >= 10 else x)

# 변경된 데이터를 저장
df.to_csv('food_db_result_fianl.csv', index=False)

# 하지만 chatGPT API로 라벨링한 데이터는 문제가 존재
# 주재료에 오류가 너무 많다. 예를 들어 모두 주재료가 말차인 음식이지만 녹차,그린티,그린 티,말차 등으로 나눠져 학습에 혼란과 과소적합을 가져옴
# 또한 너무 세세하게 분류되어있어 범주형 데이터로써의 역할을 하지 못한다.
# 따라서 겹치는 주재료들은 하나로 합치고, 전체 주분류의 종류(개수)를 줄이는 일이 필요해보인다.
# 부재료도 당연히 위와 같은 오류가 나타난다. 하지만 학습 시, 부재료는 주재료보다 중요도가 낮기에 따로 수정은 하지 않기로 한다.
# 조리 방법도 약간의 수정이 필요하다. EX) 로스팅과 로스티드 모두 존재 -> 하나로 합칠 예정

# 위 문제들 해결하기
file_path = '/content/drive/MyDrive/food_db_result_final.csv'
df = pd.read_csv(file_path)

# 같은 '주재료'이지만 다른 어감으로 나눠진 '주재료'를 하나로 합침
# '주재료'에 '닭'이라는 단어가 포함된 모든 행의 '주재료'를 '닭'으로 변경
df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('닭'), '닭', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('사과'), '사과', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('초콜릿'), '초콜릿', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('돼지'), '돼지', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('소고기'), '소고기', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('베이컨'), '베이컨', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('치즈'), '치즈', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('고구마'), '고구마', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('우유'), '우유', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('딸기'), '딸기', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('빵'), '빵', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('초코'), '초코', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('치킨'), '닭', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('호두', '아몬드'), '견과류', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('트러플'), '트러플', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('라면'), '라면', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('삼겹'), '돼지', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('조개', '조갯'), '조개', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('새우'), '새우', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('두부'), '두부', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('바닐라'), '바닐라', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('미역'), '미역', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('바질'), '바질', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('레몬'), '레몬', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('키위'), '키위', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('바나나'), '바나나', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('자두'), '자두', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('옥수수'), '옥수수', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('회'), '회', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('땅콩'), '땅콩', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('나물'), '나물', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('복숭아'), '복숭아', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('메론', '멜론'), '메론', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('오렌지'), '오렌지', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('망고'), '망고', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('유자'), '유자', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('피자'), '피자', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('파인애플'), '파인애플', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('코코넛'), '코코넛', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('햄버거'), '햄버거', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('햄버거'), '햄버거', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('터키'), '터키', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('케익'), '케이크', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('고기'), '고기', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('콩'), '콩', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('햄,'), '햄', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('쉬림프', '새우'), '새우', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('아몬드', '알몬드'), '아몬드', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('뼈'), '뼈', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('스트로베리'), '딸기', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('베리'), '베리', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('쏘시지'), '소세지', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('쑥'), '쑥', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('쌀'), '쌀', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('밀가루'), '밀가루', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('쿠키'), '쿠키', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('잡채'), '잡채', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('마카다미아'), '마카다미아', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('버섯'), '버섯', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('도토리'), '도토리', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('요거트'), '요거트', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('달걀', '계란'), '계란', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('야채', '채소'), '채소', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('쇠'), '소', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('대추'), '대추', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('허니', '꿀'), '꿀', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('레모네이드', '레몬'), '레몬', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('레드빈', '단팥'), '팥', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('오징어'), '오징어', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('아구'), '아귀', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('스테이크'), '소', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('장어'), '장어', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('꿀'), '꿀', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('미트'), '육류', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('멸치'), '멸치', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('고추'), '고추', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('머스캣'), '포도', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('포도'), '포도', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('블랙빈'), '검은콩', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('밀크'), '우유', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('갈비'), '갈비', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('떡'), '떡', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('녹차'), '녹차', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('바게트'), '바게트', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('알몬드'), '아몬드', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('와플'), '와플', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('바비큐'), '육류', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('자몽'), '자몽', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('상추'), '야채', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('땡초'), '고추', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('에스프레소'), '커피', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('커피'), '커피', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('라떼'), '커피', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('그린테이', '그린티'), '그린티', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('그린티'), '녹차', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('말차'), '녹차', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('얼그레이'), '얼그레이', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('후랑크'), '소세지', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('피자'), '밀가루', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('핫도그'), '밀가루', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('통밀'), '밀가루', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('토스트'), '밀가루', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('팝콘'), '옥수수', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('눈꽃빙수'), '우유', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('연근'), '연근', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('마라'), '마라', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('마늘'), '마늘', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('마카롱'), '마카롱', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('포테이토'), '감자', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('감자, 맛살'), '감자', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('우리밀'), '밀가루', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('유부'), '유부', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('짜장'), '춘장', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('피넛'), '땅콩', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('어묵', '오뎅'), '어묵', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('에그', '알'), '계란', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('토마토'), '토마토', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('오트밀'), '오트밀', df['mainIngredient'])

df['mainIngredient'] = np.where(df['mainIngredient'].str.contains('순대'), '순대', df['mainIngredient'])


# 너무 세세하게 분류된 주재료의 개수를 줄이는 작업
# 예를 들어 아몬드,마카다미아,피스타치오는 모두 견과류로 변경
veggie_list = [ '견과류', '아몬드', '마카다미아', '피스타치오']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '견과류'

veggie_list = ['가오리', '가자미', '게', '광어', '꽃게', '낙지', '농어', '무생채', '문어', '미꾸라지', '방어', '벤자메', '뱅어포', '산낙지', '산마', '살몬',
               '새우', '송어', '숭어', '아귀', '연어', '우럭', '우렁', '우렁이', '장어', '조기', '주꾸미', '짱뚱어', '해물', '해파리', '홍합', '추어']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '해산물'

veggie_list = ['명란', '크랩', '한치', '홍어', '황태', '튜나', '참치', '코다리', '해초', '톳', '소라', '백합']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '해산물'

veggie_list = ['갈치', '건갈치', '게살', '고등어', '골뱅이', '김', '']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '해산물'

veggie_list = ['가지', '갈릭', '감자', '고구마', '고추', '고춧잎', '김치', '깻잎', '당근', '치커리', '얼갈이배추', '호박', '후박', '열무', '샐러드', '배추',
               '생강', '근대', '무', '무시레기', '부추', '시래기', '씀바귀', '쑥', '애호박', '야채', '양배추', '양파', '양파와 감자']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '채소류'

veggie_list = ['대구', '대합', '생선', '동태', '멍게', '메기', '병어', '북어', '북어채', '붕어', '삼치', '씨푸드']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '해산물'

veggie_list = ['고들빼기', '고사리', '곤드레', '나물', '냉', '더덕', '도라지', '도라지, 오이', '두릅', '미나리', '시금치', '아욱']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '나물류'

veggie_list = ['꽃', '꽃잎']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '꽃'

veggie_list = ['깔라만시', '레몬', '딸기', '망고', '바나나', '메론', '멜론', '모과', '배', '베리', '복숭아', '수박', '아마레나 체리', '애플', '오렌지',
               '워터멜론', '윈터멜론', '자두', '자몽', '천혜향', '청귤', '체리', '코코넛', '키위', '파인애플', '한라봉', '홍시']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '과일류'

veggie_list = ['다시마', '미역', '매생이']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '해조류'

veggie_list = ['냉이', '달래']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '나물류'

veggie_list = ['로즈마리', '로즈자스민', '로즈힙']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '로즈마리'

veggie_list = ['한라봉, 스콘믹스', '프렛즐', '프레즐', '토르티야', '타코', '타르트, 티라미수', '크루아상', '크로와상', '크레이프', '크레페', '쿠키', '케이크믹스',
               '케이크', '와플', '브리오슈', '부기브레드', '바게트', '밀', '도우', '도넛']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '밀가루'

veggie_list = ['파래']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '해조류'

veggie_list = ['가루']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '밀가루'

veggie_list = ['달고나', '흑당']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '설탕'

veggie_list = ['감귤']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '과일류'

veggie_list = ['파이도우', '파이반죽', '파이생지', '라면', '빵', '마카롱', '머핀믹스', '베이글', '브라우니']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '밀가루'

veggie_list = ['소세지', '소시지', '소시지, 김치']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '소세지'

veggie_list = ['오레오', '쇼콜라']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '초콜릿'

veggie_list = ['한우', '와규', '안심', '소곱창', '소꼬리']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '소'

veggie_list = ['비프', '우육', '차돌박이, 숙주']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '소'

veggie_list = ['피치', '피치플럼', '포도', '사과', '석류']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '과일류'

veggie_list = ['제육', '베이컨', '돈까스', '돈사골', '돈육', ]
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '돼지'

veggie_list = ['페파로니', '페퍼로니', '페페로니']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '페페로니'

veggie_list = ['재첩', '전복', '조개', '조갯살', '오징어', '꼬막', '꽁치']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '해산물'

veggie_list = ['풀드포크', '프로슈토']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '돼지'

veggie_list = ['파마산', '모짜렐라', '마스카포네', '리코타, 과일']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '치즈'

veggie_list = ['초코', '카카오', '코코아']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '초콜릿'

veggie_list = ['회']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '해산물'

veggie_list = ['밀푀유', '감자', '호박잎', '마늘', '새싹채소', '브로콜리', '우엉', '우거지', '오이', '구마', '단무지', '단호박', '락교', '민들레잎', '숙주',
               '콜라비', '파', '토마토', '토란', '채소', '비타민', '연근', '옥수수', '올리브', '알로에', '아보카도', '밤', '도토리']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '채소류'

veggie_list = ['냉면', '당면', '스파게티', '파스타', '펜네', '우동면', '국수', '잡채']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '면'

veggie_list = ['곰', '멸치', '바지락', '쥐포', '달팽이', '굴', '굴비', '임연수', '어묵', '올갱이', '양미리', '알', '맛살', '오뎅', '꽃맛살', '참치, 김치']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '해산물'

veggie_list = ['호박오가리', '무시래기', '토란대', '노각', '머위', '비름', '치피']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '나물류'

veggie_list = ['현무암', '라디코니', '라우겐', '레즌', '로만밀', '비스킷', '효모', '맘모스']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '밀가루'

veggie_list = ['유자', '라임', '과일', '대추']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '과일류'

veggie_list = ['와인', '맥아']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '알코올'

veggie_list = ['가금류']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '커피'

veggie_list = ['메추리알', '목초란']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '계란'

veggie_list = ['밥', '김밥', '떡', '인절미']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '쌀'

veggie_list = ['검은콩', '녹두', '기장', '미숫가루', '현미', '흑미', '흑임자', '팥', '통곡물', '퀴노아', '잡곡', '보리', '오트밀', '콩', '메밀', '녹말',
               '둘깨', '들깨', '단팥', '참깨', '완두', '오곡', '부꾸미', '수수', '깨']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '곡물'

veggie_list = ['단백질', '버터', '미크스', '반하나', '요거트', '우유', '아이스크림', '생크림', '연유', '빙수', '크림', '얼음']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '유제품'

veggie_list = ['레드벨벳', '머스카포네']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '치즈'

veggie_list = ['헤이즐넛', '피칸', '잣', '땅콩']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '견과류'

veggie_list = ['춘장', '된장', '미소시루', '청국장']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '장류'

veggie_list = ['녹차', '라벤더', '로즈마리', '루이보스', '마차', '마테', '우롱차', '자스민', '차', '차나무', '차엽', '차이티', '차잎', '카모마일', '캐모마일',
               '타로', '티', '페퍼민트', '허브', '홍차', '히비스커스', '얼그레이', '꽃', '시트러스', '아이스티']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '차류'

veggie_list = ['머쉬룸', '트러플', '버섯']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '버섯류'

veggie_list = ['곤약', '도토리묵', '메밀묵', '묵', '청포묵', ]
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '묵류'

veggie_list = ['사골', '선지', '수육', '햄버거', '버거', '버거패티', '도가니', '곱창']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '소'

veggie_list = ['순대', '햄', '페페로니', '살라미']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '돼지'

veggie_list = ['덕', '부대찌개']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '소세지'

veggie_list = ['민트', '바닐라', '바질', '시나몬']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '향신료'

veggie_list = ['솜사탕', '꿀', '비스코프', '소다', '카라멜', '설탕']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '당류'

veggie_list = ['타피오카']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '커피'

veggie_list = ['닭', '모래집', '꿩', '터키', '오리']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '가금류'

veggie_list = ['유부', '비지']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '두부'

veggie_list = ['고기', '갈비', '내장', '뼈', '만두피', '만두', '돼지', '소', '브리또', '소세지', '육류']
df.loc[df['mainIngredient'].isin(veggie_list), 'mainIngredient'] = '가금류 이외 육류'


# 조리 방법도 역시 같지만 다르게 표현된 단어들을 하나로 합침
veggie_list = ['블렌디드', '블렌딩']
df.loc[df['cookingMethod'].isin(veggie_list), 'cookingMethod'] = '블렌딩'

veggie_list = ['부치기', '부침기']
df.loc[df['cookingMethod'].isin(veggie_list), 'cookingMethod'] = '부치기'

veggie_list = ['믹서기', '믹싱']
df.loc[df['cookingMethod'].isin(veggie_list), 'cookingMethod'] = '믹싱'


# 저장
df.to_csv('/content/drive/MyDrive/final_DB_really.csv', index=False)





