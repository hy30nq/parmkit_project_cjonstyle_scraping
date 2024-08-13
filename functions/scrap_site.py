from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def scrape_product_data(url):
    # Chrome 옵션 설정
    options = Options()
    options.headless = True

    # WebDriver 서비스 설정
    service = Service(ChromeDriverManager().install())

    # WebDriver 객체 생성
    driver = webdriver.Chrome(service=service, options=options)
    data = {}

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)  # 10초 동안 기다릴 수 있도록 설정

        # 요소 로드 대기
        name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#content > div.prd_wrap > div.prd_detail_cont > div.prd_info_wrap > div.prd_content_wrap > div.prd_info > h3')))
        category = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#content > div.u_breadcrumbs_wrap > ul > li:nth-child(2) > a')))
        
        # 할인 전 가격이 있으면 추출
        try:
            orig_price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#content > div.prd_wrap > div.prd_detail_cont > div.prd_info_wrap > div.prd_content_wrap > div.prd_info > div.price_area > span > span.txt_del > strong')))
            data['orig_price'] = orig_price.text
        except:
            data['orig_price'] = "가격 정보 없음"
        
        discount_price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#content > div.prd_wrap > div.prd_detail_cont > div.prd_info_wrap > div.prd_content_wrap > div.prd_info > div.price_area > span > strong')))

        # 기본 정보 저장
        data['name'] = name.text
        data['discount_price'] = discount_price.text
        data['category'] = category.text
        data['product_info'] = {}

        # 상세 정보 저장
        for i in range(1, 11):
            try:
                pro_info_name = driver.find_element(By.CSS_SELECTOR, f'#_INFO > div:nth-child(3) > table > tbody > tr:nth-child({i}) > th')
                pro_info_des = driver.find_element(By.CSS_SELECTOR, f'#_INFO > div:nth-child(3) > table > tbody > tr:nth-child({i}) > td')
                data['product_info'][pro_info_name.text] = pro_info_des.text
            except:
                break
    
    finally:
        driver.quit()

    return json.dumps(data, ensure_ascii=False, indent=4)

def url_info_json(url):
    result = scrape_product_data(url)
    return result
