import numpy as np
import psycopg2
#test

# 경사 하강법을 사용하여 모델 학습
def train_model(features, labels, bias):
    weights = np.zeros(features.shape[1])
    learning_rate = 0.01
    max_iterations = 1000

    for _ in range(max_iterations):
        predictions = bias + np.dot(features, weights)
        error = predictions - labels
        weights -= learning_rate * np.dot(features.T, error)
        bias -= learning_rate * np.mean(error)

    return weights, bias

# 새로운 데이터에 대한 예측
def predict(features, weights, bias):
    return bias + np.dot(features, weights)

# PostgreSQL 연결 설정
conn = psycopg2.connect(
    host="localhost",
    database="Rldata",
    user="postgres",
    password="iesllink30!"
)
cursor = conn.cursor()

# 쿼리 실행
query = "SELECT r_month, r_hour, r_dofw, us_rate, dong_index FROM usage_rate"
cursor.execute(query)
rows = cursor.fetchall()

# 학습 데이터
num_samples = len(rows)
features = np.zeros((num_samples, 4))
labels = np.zeros(num_samples)

for i, row in enumerate(rows):
    r_month, r_hour, r_dofw, us_rate, dong_index = row
    features[i] = [r_month, r_hour, r_dofw, dong_index]
    labels[i] = us_rate

# 모델 학습
weights, bias = train_model(features, labels, 0)

# 새로운 데이터에 대한 예측
new_features = np.array([
    # r_month, r_hour, r_dofw, dong_index
    [7, 10, 1, 31],
    # ...
])
predictions = predict(new_features, weights, bias)
print("Predictions:", predictions)

# 리소스 해제
cursor.close()
conn.close()
