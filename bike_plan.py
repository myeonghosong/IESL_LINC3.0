import psycopg2
from datetime import datetime

def get_and_analyze_data(month, dow, hour):
    # PostgreSQL 연결 정보 설정
    connection = psycopg2.connect(
        host="localhost",
        database="Rldata",
        user="postgres",
        password="iesllink30!"
    )

    # PostgreSQL 쿼리 실행
    query = f"""
        SELECT city, gu, dong, dong_index, r_year, r_month, r_day, r_dofw, r_hour, us_rate
        FROM usage_rate
        WHERE r_month = {month} AND r_dofw = {dow} AND r_hour = {hour}
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    # gu를 기준으로 데이터 그룹화
    gu_data = {}
    for row in data:
        city, gu, dong, dong_index, r_year, r_month, r_day, r_dofw, r_hour, us_rate = row
        if gu not in gu_data:
            gu_data[gu] = []
        gu_data[gu].append((dong, us_rate))

    # 각 gu의 dong별 사용율 출력 및 동별 사용율 평균 계산
    for gu, dong_data in gu_data.items():
        print(f"Gu: {gu}")
        dong_avg_rates = {}  # 각 동별 사용율의 총합과 개수를 저장하는 딕셔너리

        for dong, us_rate in dong_data:
            print(f"  Dong: {dong}, Usage Rate: {us_rate}")

            # 각 동별 사용율의 총합과 개수를 업데이트
            if dong not in dong_avg_rates:
                dong_avg_rates[dong] = {'sum': 0, 'count': 0}
            dong_avg_rates[dong]['sum'] += us_rate
            dong_avg_rates[dong]['count'] += 1

        for dong, rates in dong_avg_rates.items():
            avg_rate = rates['sum'] / rates['count']
            print(f"{dong} Avg Usage Rate : {avg_rate:.2f}")

        min_usage_dong = min(dong_avg_rates, key=lambda x: dong_avg_rates[x]['sum'] / dong_avg_rates[x]['count'])
        min_avg_rate = dong_avg_rates[min_usage_dong]['sum'] / dong_avg_rates[min_usage_dong]['count']

        max_usage_dong = max(dong_avg_rates, key=lambda x: dong_avg_rates[x]['sum'] / dong_avg_rates[x]['count'])
        max_avg_rate = dong_avg_rates[max_usage_dong]['sum'] / dong_avg_rates[max_usage_dong]['count']

        print(f"  Lowest Usage Dong: {min_usage_dong}, Avg Usage Rate: {min_avg_rate:.2f}")
        print(f"  Highest Usage Dong: {max_usage_dong}, Avg Usage Rate: {max_avg_rate:.2f}")

    # 연결 종료
    connection.close()

# 현재 시간 정보를 얻어옴
now = datetime.now()
current_month = now.month
current_day_of_week = now.weekday()  # 월요일: 0, 일요일: 6 (요일 순서를 변경하여 저장)
current_hour = now.hour

# 토요일은 6으로 저장되므로, 일요일은 0으로, 토요일은 6으로 변환
if current_day_of_week == 6:
    current_day_of_week = 0
else:
    current_day_of_week += 1

# 현재 시간 정보를 함수에 전달
print("현재 ->",current_month,"월", current_day_of_week, current_hour,"시간 대")
get_and_analyze_data(current_month, current_day_of_week, current_hour)
