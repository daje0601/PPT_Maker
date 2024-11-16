from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def download_responsive_reading(reading_number, driver, wait):
    try:
        # 구글 검색
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(f"성시교독 {reading_number}번 ppt")
        search_box.send_keys(Keys.RETURN)
        
        # 블로그 링크 찾기
        blog_link = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href, 'getwater.tistory.com')]")))
        blog_link.click()
        
        # 페이지의 2/3 지점까지 스크롤
        time.sleep(2)
        total_height = driver.execute_script("return document.body.scrollHeight")
        scroll_height = int(total_height * 2/3)
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        time.sleep(2)
        
        # 파일 링크 찾기 (수정된 XPath)
        download_link = wait.until(EC.presence_of_element_located((
            By.XPATH, 
            "//figure[contains(@class, 'fileblock')]/a"
        )))
        
        # 현재 창의 핸들 저장
        main_window = driver.current_window_handle
        
        # JavaScript로 직접 클릭 실행
        driver.execute_script("arguments[0].click();", download_link)
        time.sleep(2)  # 팝업이 뜰 때까지 대기
        
        # 모든 창 핸들 가져오기
        all_windows = driver.window_handles
        
        # 팝업 창 찾기 및 처리
        for window in all_windows:
            if window != main_window:
                # 팝업 창으로 전환
                driver.switch_to.window(window)
                try:
                    # 닫기 버튼 찾기 시도 (여러 가능한 선택자 시도)
                    close_button = driver.find_element(By.CSS_SELECTOR, "button.close") or \
                                 driver.find_element(By.CLASS_NAME, "close") or \
                                 driver.find_element(By.XPATH, "//button[contains(@class, 'close')]") or \
                                 driver.find_element(By.XPATH, "//div[contains(@class, 'close')]")
                    close_button.click()
                except:
                    # 닫기 버튼을 찾지 못하면 창 자체를 닫기
                    driver.close()
                
                # 메인 창으로 돌아가기
                driver.switch_to.window(main_window)
        
        # 다시 다운로드 링크 클릭
        time.sleep(1)
        driver.execute_script("arguments[0].click();", download_link)
        print(f"성시교독 {reading_number}번 PPT 다운로드를 시작했습니다.")
        time.sleep(5)  # 다운로드 완료 대기
        return True
        
    except Exception as e:
        print(f"성시교독 {reading_number}번 다운로드 중 에러 발생: {str(e)}")
        return False

def batch_download_responsive_readings(reading_numbers):
    # Chrome 드라이버 설정 - 화면 표시 모드
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("prefs", {
        "download.default_directory": "C:\\Downloads",
        "download.prompt_for_download": False,
    })
    options.add_argument('--headless')  # 백그라운드 실행
    options.add_argument('--disable-gpu')  # GPU 사용 안함
    options.add_argument('--no-sandbox')  # 샌드박스 비활성화
    options.add_argument('--disable-dev-shm-usage')  # 공유 메모리 제한 해제
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        successful_downloads = []
        failed_downloads = []
        
        for reading_number in reading_numbers:
            print(f"\n{'='*50}")
            print(f"성시교독 {reading_number}번 다운로드 시도 중...")
            
            if download_responsive_reading(reading_number, driver, wait):
                successful_downloads.append(reading_number)
            else:
                failed_downloads.append(reading_number)
                
        # 최종 결과 출력
        print(f"\n{'='*50}")
        print("다운로드 완료 보고서:")
        print(f"성공한 다운로드: {successful_downloads}")
        print(f"실패한 다운로드: {failed_downloads}")
        
    finally:
        driver.quit()

# 사용 예시
