print('=== Script started ===')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime

def setup_chrome_driver():
    """
    Setup and configure Chrome WebDriver with optimized settings.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance or None if failed
    """
    try:
        # Configure Chrome options
        chrome_options = Options()
        
        # Performance optimizations
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--memory-pressure-off')
        chrome_options.add_argument('--max_old_space_size=2048')
        chrome_options.add_argument('--aggressive-cache-discard')
        chrome_options.add_argument('--disable-cache')
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument('--disable-offline-load-stale-cache')
        chrome_options.add_argument('--disk-cache-size=0')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Anti-detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        print('=== Chrome driver created ===')
        
        # Configure driver settings
        driver.set_page_load_timeout(15)
        driver.implicitly_wait(2)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.maximize_window()
        
        print("✅ Chrome WebDriver initialized successfully")
        return driver
        
    except Exception as e:
        print(f"❌ Failed to initialize Chrome WebDriver: {str(e)}")
        return None

def wait_for_personal_center(driver, timeout=30):
    """
    Wait for the personal center page to be fully loaded and ready.
    Accepts the page as loaded if the URL contains '/personalCenter', even if isGuide=true is present.
    """
    print("🔄 Waiting for personal center page to load...")
    try:
        # Wait for URL to contain personal center
        WebDriverWait(driver, timeout).until(
            lambda driver: "/personalCenter" in driver.current_url
        )
        print("✅ URL successfully redirected to personal center")
        # Wait for page to fully load (wait for body or main content)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # Additional wait for any dynamic content to load
        time.sleep(2)
        print("✅ SUCCESS! Personal center page is fully loaded and ready.")
        return True
    except Exception as e:
        print(f"❌ Failed to load personal center page: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        return False

def login_shenlong(driver):
    """Login to ShenLong using cookies and tokens"""
    print("Starting login process with cookies...")
    
    try:
        # Navigate to the main domain first to set cookies
        print("Navigating to main domain to set cookies...")
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net")
        time.sleep(2)
        
        # Add authentication cookies
        print("Adding authentication cookies...")
        cookies = [
            {'name': 'Hm_lpvt_ab97e0528cd8a1945e66aee550b54522', 'value': '1751509230', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'Hm_lpvt_b697afe6e9c7d29cd1db7fa7b477f2f6', 'value': '1751509230', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'Hm_lvt_ab97e0528cd8a1945e66aee550b54522', 'value': '1751348297,1751349468,1751439990,1751506933', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'Hm_lvt_b697afe6e9c7d29cd1db7fa7b477f2f6', 'value': '1751348297,1751349468,1751439990,1751506933', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'HMACCOUNT', 'value': '30F199DAD7C59D55', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'token', 'value': 'z7PFxmh3SZngVpqpfaUckeVK6dcqvHeaeTiZPebp5j8=', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'User_Info', 'value': '%7B%22_id%22%3A%226848ec1665510850cc139ec5%22%2C%22id%22%3A10621%2C%22username%22%3A%2214562485478%22%2C%22realMoney%22%3A1%2C%22balance%22%3A0%2C%22phone%22%3A%2214562485478%22%2C%22state%22%3A1%2C%22createTime%22%3A1749609493%2C%22isNewUser%22%3Atrue%2C%22registIP%22%3A%22120.240.163.164%22%2C%22creator%22%3A10616%2C%22parent%22%3A%5B8948%2C10616%5D%2C%22appointSellerTime%22%3A1749611980%2C%22source%22%3A%22register%22%2C%22keyword%22%3Anull%2C%22brand%22%3A1%2C%22roles%22%3A%5B300%5D%2C%22testLimitAccess%22%3Afalse%2C%22testLimit%22%3A1%2C%22testCount%22%3A0%2C%22registFingerPrint%22%3A%221cb3b2bdbae44e7c77615a01d626fe77%22%2C%22dailyActive%22%3A13%2C%22lastIP%22%3A%22120.240.163.164%22%2C%22lastLoginRegion%22%3A%22%E4%B8%AD%E5%9B%BD%E5%B9%BF%E4%B8%9C%E6%8F%AD%E9%98%B3%22%2C%22lastLoginTime%22%3A1751421394%2C%22loginTime%22%3A1751502908%2C%22userLevel%22%3A40%2C%22lastCreator%22%3A6839%2C%22thirdPayAccCount%22%3A1%2C%22regionLimit%22%3Afalse%2C%22token%22%3A%22z7PFxmh3SZngVpqpfaUckeVK6dcqvHeaeTiZPebp5j8%3D%22%2C%22registered%22%3Atrue%7D', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'balance', 'value': '0', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'gdxidpyhxdE', 'value': 'i6txcKzzcafBs1sm%2BewYNTu4UpN143O0J%2B8M98GL8iek3Y%2BtQZ8muYvYgkNtYotpt6Kb%2Fl75tym2lg6T21R%5C%2FBYOBZ60RhdMvD6ZVbdXNSASOGEOoUGdCZpI9epYfV%2F9wno322p4tTrHpsQt5zXz2qi5vbE6ZEtj%2BabowMLqKiuSM5M6%3A1751509633322', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'}
        ]
        
        success_count = 0
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
                success_count += 1
                print(f"✅ Added cookie: {cookie['name']}")
            except Exception as e:
                print(f"⚠️ Failed to add cookie {cookie['name']}: {e}")
        
        print(f"✅ Successfully added {success_count}/{len(cookies)} cookies")
        
        # Navigate to personal center to verify login
        print("Navigating to personal center to verify login...")
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter")
        time.sleep(3)
        
        # Use the wait function for personal center
        login_success = wait_for_personal_center(driver, timeout=30)
        
        if login_success:
            print("✅ SUCCESS! Login successful using cookies - redirected to personal center.")
            return True
        else:
            print(f"❌ Login verification failed. Current URL: {driver.current_url}")
            return False
            
    except Exception as e:
        print(f"❌ Login error occurred: {str(e)}")
        return False

def test_no_balance_scenario():
    """Test scenarios where user has insufficient balance"""
    print("Starting NO Balance test scenario...")
    print("=" * 50)
    print("1. Dynamic Advance Package (动态高级套餐)")
    print("=" * 50)
    
    # Initialize the Chrome driver once
    driver = setup_chrome_driver()
    if not driver:
        print("❌ Failed to initialize Chrome driver. Cannot proceed.")
        return False
    
    try:
        # First, perform login using the same driver
        login_success = login_shenlong(driver)
        
        if not login_success:
            print("❌ Login failed. Cannot proceed with no balance test.")
            return False
        
        print("✅ Login successful! Proceeding with no balance test...")
        
        # Navigate to the dynamic advanced package page
        print("Navigating to Dynamic Advanced Package page...")
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=0")
        
        # Wait for page to load
        print("Waiting for page to load...")
        time.sleep(5)
        
        # Find and click on "动态高级套餐-7天" (Dynamic Advanced Package - 7 days)
        print("Looking for 7-day package...")
        try:
            # Try to find the 7-day package by text content
            seven_day_package = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '动态高级套餐-7天')]"))
            )
            print("✅ Found 7-day package!")
        except Exception as e:
            print("❌ Could not find 7-day package by text, trying alternative selectors...")
            # Try alternative selectors
            try:
                seven_day_package = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'package-item') and contains(., '7天')]"))
                )
                print("✅ Found 7-day package by class!")
            except Exception as e2:
                print("❌ Could not find 7-day package by class, trying price selector...")
                seven_day_package = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(., '￥1') and contains(., '7天')]"))
                )
                print("✅ Found 7-day package by price!")
        
        # Click on "立即购买" (Buy Now) button using specific XPath
        print("Looking for '立即购买' button...")
        try:
            buy_now_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
            )
            print("✅ Found '立即购买' button using specific XPath!")
        except Exception as e:
            print("❌ Could not find '立即购买' button with specific XPath, trying alternative selectors...")
            try:
                buy_now_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '立即购买')]"))
                )
                print("✅ Found '立即购买' button with text selector!")
            except Exception as e2:
                print("❌ Could not find '立即购买' button, trying any button with text...")
                buy_now_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., '购买')]"))
                )
                print("✅ Found button with '购买' text!")
        
        # Click the buy now button
        print("Clicking '立即购买' button...")
        buy_now_button.click()
        print("✅ Clicked '立即购买' button!")
        
        # Wait for popup to appear
        print("Waiting for popup to appear...")
        time.sleep(3)
        
        # Look for and click "立即支付" (Pay Now) button in the popup
        print("Looking for '立即支付' button in popup...")
        try:
            pay_now_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
            )
            print("✅ Found '立即支付' button using specific XPath!")
        except Exception as e:
            print("❌ Could not find '立即支付' button with specific XPath, trying alternative selectors...")
            try:
                pay_now_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '立即支付')]"))
                )
                print("✅ Found '立即支付' button with text selector!")
            except Exception as e2:
                print("❌ Could not find payment button in modal, trying any payment button...")
                pay_now_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '支付')]"))
                )
                print("✅ Found payment button!")
        
        # Click the pay now button
        print("Clicking '立即支付' button...")
        pay_now_button.click()
        print("✅ Clicked '立即支付' button!")
        
        # Wait for redirection to recharge page
        print("Waiting for redirection to recharge page...")
        time.sleep(10)  # Wait 10 seconds to ensure redirect happens
        
        # Check if redirected to recharge page
        try:
            WebDriverWait(driver, 10).until(
                lambda driver: driver.current_url == "https://test-ip-shenlong.cd.xiaoxigroup.net/recharge"
            )
            print("✅ SUCCESS! Successfully redirected to recharge page!")
            
            # Start 2. Dedicated Dynamic Package (动态独享套餐)
            print("=" * 50)
            print("2. Dedicated Dynamic Package (动态独享套餐)")
            print("=" * 50)
            
            # Navigate to the dedicated dynamic package page
            print("Navigating to Dedicated Dynamic Package page...")
            driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=1")
            
            # Wait for page to load
            print("Waiting for page to load...")
            time.sleep(5)
            
            # Find and click on "动态独享套餐-7天" (Dedicated Dynamic Package - 7 days)
            print("Looking for 7-day dedicated package...")
            try:
                # Try to find the 7-day dedicated package by text content
                seven_day_dedicated_package = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '动态独享套餐-7天')]"))
                )
                print("✅ Found 7-day dedicated package!")
            except Exception as e:
                print("❌ Could not find 7-day dedicated package by text, trying alternative selectors...")
                # Try alternative selectors
                try:
                    seven_day_dedicated_package = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'package-item') and contains(., '7天')]"))
                    )
                    print("✅ Found 7-day dedicated package by class!")
                except Exception as e2:
                    print("❌ Could not find 7-day dedicated package by class, trying price selector...")
                    seven_day_dedicated_package = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(., '￥60') and contains(., '7天')]"))
                    )
                    print("✅ Found 7-day dedicated package by price!")
            
            # Click on "立即购买" (Buy Now) button using specific XPath
            print("Looking for '立即购买' button for dedicated package...")
            try:
                buy_now_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
                )
                print("✅ Found '立即购买' button using specific XPath!")
            except Exception as e:
                print("❌ Could not find '立即购买' button with specific XPath, trying alternative selectors...")
                try:
                    buy_now_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '立即购买')]"))
                    )
                    print("✅ Found '立即购买' button with text selector!")
                except Exception as e2:
                    print("❌ Could not find '立即购买' button, trying any button with text...")
                    buy_now_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., '购买')]"))
                    )
                    print("✅ Found button with '购买' text!")
            
            # Click the buy now button
            print("Clicking '立即购买' button for dedicated package...")
            buy_now_button.click()
            print("✅ Clicked '立即购买' button!")
            
            # Wait for popup to appear
            print("Waiting for popup to appear...")
            time.sleep(3)
            
            # Look for and click "立即支付" (Pay Now) button in the popup
            print("Looking for '立即支付' button in popup...")
            try:
                pay_now_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
                )
                print("✅ Found '立即支付' button using specific XPath!")
            except Exception as e:
                print("❌ Could not find '立即支付' button with specific XPath, trying alternative selectors...")
                try:
                    pay_now_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '立即支付')]"))
                    )
                    print("✅ Found '立即支付' button with text selector!")
                except Exception as e2:
                    print("❌ Could not find payment button in modal, trying any payment button...")
                    pay_now_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '支付')]"))
                    )
                    print("✅ Found payment button!")
            
            # Click the pay now button
            print("Clicking '立即支付' button...")
            pay_now_button.click()
            print("✅ Clicked '立即支付' button!")
            
            # Wait for redirection to recharge page
            print("Waiting for redirection to recharge page...")
            time.sleep(10)  # Wait 10 seconds to ensure redirect happens
            
            # Check if redirected to recharge page
            try:
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.current_url == "https://test-ip-shenlong.cd.xiaoxigroup.net/recharge"
                )
                print("✅ SUCCESS! Successfully redirected to recharge page for dedicated package!")
                print("🎉 ALL TEST SCENARIOS COMPLETED SUCCESSFULLY!")
                print("=" * 60)
                print("✅ 1. Dynamic Advance Package - PASSED")
                print("✅ 2. Dedicated Dynamic Package - PASSED") 
                return True
            except Exception as e:
                print(f"❌ Failed to redirect to recharge page. Current URL: {driver.current_url}")
                return False
            
        except Exception as e:
            print(f"❌ Failed to redirect to recharge page. Current URL: {driver.current_url}")
            return False
            
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        return False
        
    finally:
        # Wait for 5 seconds to see the result
        print("Waiting 5 seconds to see the result...")
        time.sleep(5)
        # Close the browser
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    try:
        print('=== Entering main ===')
        test_no_balance_scenario()
        print('=== Script finished ===')
    except Exception as e:
        print(f'=== Unhandled exception: {e} ===') 