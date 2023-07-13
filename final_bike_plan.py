import numpy as np
import psycopg2

LEARNING_RATE = 0.01
MAX_ITERATIONS = 1000

# PostgreSQL에 연결
conn = psycopg2.connect(
    host="localhost",
    database="Rldata",
    user="postgres",
    password="iesllink30!"
)

# 커서 생성
cursor = conn.cursor()

# 쿼리 실행
query = "SELECT r_month, r_hour, r_dofw, us_rate, dong, dong_index FROM usage_rate"
cursor.execute(query)

# 결과 가져오기
results = cursor.fetchall()

# 학습 데이터
features = []
labels = []

for row in results:
    r_month, r_hour, r_dofw, us_rate, dong_str, dong_index = row
    features.append([r_month, r_hour, r_dofw, dong_index])
    labels.append(us_rate)

    print(f"Data {len(features) - 1} - Dong: {dong_str}, Dong Index: {dong_index}")

# 모델 초기화
global bias, weights

weights = [0.0, 0.0, 0.0, 0.0]
bias = 0.0

# 모델 학습
# 선형 회귀 모델의 가중치와 편향

# 손실 함수: 평균 제곱 오차
def calculate_loss(features, labels):
    global bias, weights
    num_samples = len(features)
    loss = sum((bias + sum(w * f for w, f in zip(weights, feat)) - label) ** 2 for feat, label in zip(features, labels))
    loss /= num_samples
    return loss

# 경사 하강법을 사용하여 모델 학습
def train_model(features, labels):
    global bias, weights
    num_samples = len(features)
    for i in range(MAX_ITERATIONS):
        for j in range(num_samples):
            prediction = bias + sum(w * f for w, f in zip(weights, features[j]))
            error = prediction - labels[j]
            bias -= LEARNING_RATE * error
            weights = [w - LEARNING_RATE * error * f for w, f in zip(weights, features[j])]
        
        # 학습 과정 출력
        if i % 100 == 0:
            loss = calculate_loss(features, labels)
            print(f"Iteration {i} - Loss: {loss:.4f}")

# 새로운 데이터에 대한 예측
def predict(features):
    global bias, weights
    prediction = bias + sum(w * f for w, f in zip(weights, features))
    return prediction

train_model(features, labels)

# 새로운 데이터에 대한 예측
new_features = [
    # r_month, r_hour, r_dofw, dong_index
    [7, 10, 1, 31],
    # ...
]
prediction = predict(new_features)
print(f"Prediction: {prediction:.4f}")

# 리소스 해제
cursor.close()
conn.close()
