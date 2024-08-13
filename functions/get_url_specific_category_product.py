import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
actions = ActionChains(driver)
    
count = 0

for category_num in range(1, 16):
    # CSV 파일 초기화
    csv_file = open(f'./href_values_{category_num}.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    save_url = f'https://display.cjonstyle.com/p/category/categoryMain?dpCateId=G00{213+category_num}' # 카테고리 번호별 csv 파일 만들기
    category_url = save_url


    try:
        driver.get(category_url) # 한 카테고리 시작 주소

        while True:
            try:
                # 모든 요소의 href 값을 찾기 위해 num 값을 1부터 48까지 반복
                for num in range(1, 49):  # 1부터 48까지
                    selector = f"#cont_listing0 > div.listing_result.is_preprefix.with_line > ul > li:nth-child({num}) > a"
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    href_value = element.get_attribute('href')
                    csv_writer.writerow([href_value])  # CSV 파일에 쓰기

                # 다음 페이지 버튼
                try:
                    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn_pn_next")))
                    actions.scroll_to_element(next_button).perform()  # 스크롤하여 요소를 화면에 표시
                    next_button.click()
                except ElementClickInterceptedException:
                    # 요소가 클릭 가능할 때까지 js를 사용하여 클릭
                    driver.execute_script("arguments[0].click();", next_button)
                except NoSuchElementException:
                    print("No more pages to navigate.")
                    break

            except StaleElementReferenceException:
                count += 1
                print(f"Encountered a stale element while waiting, retrying...{count}")
            except Exception as e:
                print(f"Error processing element: {e}")

    except TimeoutException:
        print("Timed out waiting for page to load")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        csv_file.close()  # 파일 닫기
