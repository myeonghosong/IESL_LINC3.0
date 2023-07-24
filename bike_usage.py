import psycopg2

def get_data_and_average(month, dow, hour, dong_index):
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
        WHERE r_month = {month} AND r_dofw = {dow} AND r_hour = {hour} AND dong_index = {dong_index}
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    # 데이터 출력
    for row in data:
        city, gu, dong, dong_index, r_year, r_month, r_day, r_dofw, r_hour, us_rate = row
        print(f"City: {city}, Gu: {gu}, Dong: {dong}, Dong Index: {dong_index}, "
              f"Year: {r_year}, Month: {r_month}, Day: {r_day}, Day of Week: {r_dofw}, "
              f"Hour: {r_hour}, Usage Rate: {us_rate}")

    # 사용율 평균 계산 및 출력
    if data:
        average_usage_rate = sum(row[-1] for row in data) / len(data)
        print(f"Average Usage Rate: {average_usage_rate:.2f}")

    # 연결 종료
    connection.close()

# 예시 데이터 입력 (월, 요일, 시간대, 동번호)
get_data_and_average(3, 1, 12, 44)
