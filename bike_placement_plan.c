#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "C:\Program Files\PostgreSQL\15\include\libpq-fe.h"

double slope, intercept;

// 예측 모델에 필요한 데이터 구조체
struct Data {
    int time;       // 시간대
    char dong[50];  // 동
    char gu[50];    // 구
    char city[50];  // 시
    double usage;   // 사용율
};

// 예측 모델을 학습시키는 함수
void trainModel(struct Data* data, int numSamples) {
    // 회귀 분석 알고리즘 등을 활용하여 모델을 학습시킵니다.
    // 예시로 선형 회귀를 사용합니다.
    
    double sumX = 0.0;
    double sumY = 0.0;
    double sumXY = 0.0;
    double sumXX = 0.0;
    
    for (int i = 0; i < numSamples; i++) {
        sumX += data[i].time;
        sumY += data[i].usage;
        sumXY += data[i].time * data[i].usage;
        sumXX += data[i].time * data[i].time;
    }
    
    slope = (numSamples * sumXY - sumX * sumY) / (numSamples * sumXX - sumX * sumX);
    intercept = (sumY - slope * sumX) / numSamples;
    
    printf("학습 완료! 회귀식: y = %.2f * x + %.2f\n", slope, intercept);
}

// 동별 구별 시별 시간대 사용율을 예측하는 함수
double predictUsage(struct Data* data, int numSamples, int time, const char* dong, const char* gu, const char* city) {
    // 예측 모델을 활용하여 동별 구별 시별 시간대 사용율을 예측합니다.
    // 회귀 모델에 따라 예측 결과를 계산하고 반환합니다.
    
    double predictedUsage = slope * time + intercept;
    
    printf("%s, %s, %s, %d시 사용율 예측: %.2f\n", dong, gu, city, time, predictedUsage);
    
    return predictedUsage;
}

int main() {
    // postgreSQL DB에 연결
    PGconn *conn;
    PGresult *res;
    const char *conninfo = "host=localhost port=5432 dbname=Rldata user=postgres password=iesllink30!";

    conn = PQconnectdb(conninfo);

    if (PQstatus(conn) != CONNECTION_OK) {
        fprintf(stderr, "DB 연결 실패: %s\n", PQerrorMessage(conn));
        PQfinish(conn);
        return 1;
    }
    
    // postgreSQL DB에서 데이터 가져오기
    const char *query = "SELECT time, dong, gu, city, usage FROM your_table";
    res = PQexec(conn, query);
    if (PQresultStatus(res) != PGRES_TUPLES_OK) {
        fprintf(stderr, "쿼리 실행 실패: %s\n", PQerrorMessage(conn));
        PQclear(res);
        PQfinish(conn);
        return 1;
    }
    
    int numSamples = PQntuples(res);
    struct Data* usageData = (struct Data*)malloc(numSamples * sizeof(struct Data));
    
    // 데이터를 배열에 저장
    for (int i = 0; i < numSamples; i++) {
        usageData[i].time = atoi(PQgetvalue(res, i, 0));
        strcpy(usageData[i].dong, PQgetvalue(res, i, 1));
        strcpy(usageData[i].gu, PQgetvalue(res, i, 2));
        strcpy(usageData[i].city, PQgetvalue(res, i, 3));
        usageData[i].usage = atof(PQgetvalue(res, i, 4));
    }
    
    // 예측 모델 학습
    trainModel(usageData, numSamples);
    
    // 실시간으로 동별 구별 시별 시간대 사용율 예측 및 바이크 배치 계획 수립
    int currentTime = 12;  // 현재 시간대 (예시)
    const char* currentDong = "동이름";  // 현재 동 (예시)
    const char* currentGu = "구이름";  // 현재 구 (예시)
    const char* currentCity = "시이름";  // 현재 시 (예시)
    
    double predictedUsage = predictUsage(usageData, numSamples, currentTime, currentDong, currentGu, currentCity);
    
    // 적절한 알고리즘을 활용하여 바이크의 배치 계획을 수립합니다.
    // 예시로서 사용율이 일정 임계값을 넘으면 해당 지역에 바이크를 추가로 배치하는 방식으로 구현합니다.
    if (predictedUsage > 0.8) {
        printf("바이크를 추가 배치해야 합니다.\n");
    } else {
        printf("추가적인 배치 필요 없음.\n");
    }
    
    // 메모리 해제 및 연결 종료
    free(usageData);
    PQclear(res);
    PQfinish(conn);
    
    return 0;
}
