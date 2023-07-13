#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "C:\Program Files\PostgreSQL\15\include\libpq-fe.h"

#define LEARNING_RATE 0.01
#define MAX_ITERATIONS 1000

// 선형 회귀 모델의 가중치와 편향
double weights[4];
double bias;

// 손실 함수: 평균 제곱 오차
double calculate_loss(double *features, double *labels, int num_samples) {
    double loss = 0.0;
    for (int i = 0; i < num_samples; i++) {
        double prediction = bias;
        for (int j = 0; j < 4; j++) {
            prediction += weights[j] * features[i * 4 + j];
        }
        double error = prediction - labels[i];
        loss += error * error;
    }
    loss /= num_samples;
    return loss;
}

// 경사 하강법을 사용하여 모델 학습
void train_model(double *features, double *labels, int num_samples) {
    for (int i = 0; i < MAX_ITERATIONS; i++) {
        double prediction, error;

        // 가중치와 편향을 업데이트
        for (int j = 0; j < num_samples; j++) {
            prediction = bias;
            for (int k = 0; k < 4; k++) {
                prediction += weights[k] * features[j * 4 + k];
            }
            error = prediction - labels[j];
            bias -= LEARNING_RATE * error;
            for (int k = 0; k < 4; k++) {
                weights[k] -= LEARNING_RATE * error * features[j * 4 + k];
            }
        }

        // 학습 과정 출력
        if (i % 100 == 0) {
            double loss = calculate_loss(features, labels, num_samples);
            printf("Iteration %d - Loss: %.4f\n", i, loss);
        }
    }
}

// 새로운 데이터에 대한 예측
double predict(double *features) {
    double prediction = bias;
    for (int i = 0; i < 4; i++) {
        prediction += weights[i] * features[i];
    }
    return prediction;
}

int main() {
    // PostgreSQL 연결 설정
    PGconn *conn;
    conn = PQconnectdb("host=localhost port=5432 dbname=Rldata user=postgres password=iesllink30!");
    if (PQstatus(conn) != CONNECTION_OK) {
        fprintf(stderr, "Connection to database failed: %s", PQerrorMessage(conn));
        PQfinish(conn);
        exit(1);
    }

    // 쿼리 실행
    const char *query = "SELECT r_month, r_hour, r_dofw, us_rate, dong, dong_index FROM usage_rate";
    PGresult *result = PQexec(conn, query);
    if (PQresultStatus(result) != PGRES_TUPLES_OK) {
        fprintf(stderr, "Query execution failed: %s", PQresultErrorMessage(result));
        PQclear(result);
        PQfinish(conn);
        exit(1);
    }

    // 학습 데이터
    int num_samples = PQntuples(result);
    double *features = (double *)malloc(num_samples * 4 * sizeof(double));
    double *labels = (double *)malloc(num_samples * sizeof(double));

    for (int i = 0; i < num_samples; i++) {
        double r_month = atof(PQgetvalue(result, i, 0));
        double r_hour = atof(PQgetvalue(result, i, 1));
        double r_dofw = atof(PQgetvalue(result, i, 2));
        double us_rate = atof(PQgetvalue(result, i, 3));
        const char *dong_str = PQgetvalue(result, i, 4);
        int dong_index = atoi(PQgetvalue(result, i, 5));

        features[i * 4] = r_month;
        features[i * 4 + 1] = r_hour;
        features[i * 4 + 2] = r_dofw;
        features[i * 4 + 3] = dong_index;
        labels[i] = us_rate;

        printf("Data %d - Dong: %s, Dong Index: %d\n", i, dong_str, dong_index);
    }

    // 모델 초기화
    for (int i = 0; i < 4; i++) {
        weights[i] = 0.0;
    }
    bias = 0.0;

    // 모델 학습
    train_model(features, labels, num_samples);

    // 새로운 데이터에 대한 예측
    double new_features[] = {
        // r_month, r_hour, r_dofw, dong_index
        7, 10, 1, 31,
        // ...
    };
    double prediction = predict(new_features);
    printf("Prediction: %.4f\n", prediction);

    // 리소스 해제
    PQclear(result);
    PQfinish(conn);
    free(features);
    free(labels);

    return 0;
}
