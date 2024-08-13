from functions.scrap_site import url_info_json
import json
import csv
import os

# os.system('pipenv run python ./functions/get_url_specific_category_product.py')
os.system('python3 ./functions/get_url_specific_category_product.py')


for category_num in range(1, 16):
    file_name = f'./href_values_{category_num}.csv'

    # 파일을 열고 각 줄을 읽어 출력합니다.
    with open(file_name, 'r') as file:
        for line in file:
            res = url_info_json(line.strip())
            print(res)

            data = json.loads(res)
            
            # CSV 파일 이름
            csv_file_name = 'product_results.csv'

            # CSV 파일이 존재하지 않으면 새로 생성하고, 존재하면 데이터를 추가
            try:
                # 파일을 append 모드로 열기
                with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    
                    # 파일이 비어있는지 확인하고, 헤더를 작성
                    file.seek(0, 2)  # 파일 끝으로 이동
                    if file.tell() == 0:  # 파일이 비어있다면
                        writer.writerow(['name', 'orig_price', 'discount_price', 'category', 'product_info'])

                    # product_info를 JSON 문자열로 변환하여 저장
                    product_info_str = json.dumps(data['product_info'], ensure_ascii=False)
                    writer.writerow([data['name'], data['orig_price'], data['discount_price'], data['category'], product_info_str])

            except Exception as e:
                print(f"An error occurred: {e}")


