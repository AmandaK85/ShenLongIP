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
from driver_utils import setup_chrome_driver

def wait_for_personal_center(driver, timeout=30):
    """
    Wait for the personal center page to be fully loaded and ready.
    
    Args:
        driver: Selenium WebDriver instance
        timeout: Maximum time to wait in seconds (default: 30)
    
    Returns:
        bool: True if personal center page is loaded successfully, False otherwise
    """
    print("🔄 Waiting for personal center page to load...")
    
    try:
        # Wait for URL to change to personal center
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.current_url == "https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter"
        )
        print("✅ URL successfully redirected to personal center")
        
        # Wait for page to fully load (wait for body or main content)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Additional wait for any dynamic content to load
        time.sleep(2)
        
        # Try to verify the page content by looking for common elements
        try:
            # Look for the main heading or title
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), '一站式国内网络解决方案')]"))
            )
            print("✅ Personal center page content verified")
        except:
            # If specific content not found, just verify page is loaded
            print("ℹ️ Page loaded, content verification skipped")
        
        print("✅ SUCCESS! Personal center page is fully loaded and ready.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to load personal center page: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        return False

def login_shenlong(driver):
    """Login to ShenLong using the provided driver instance"""
    print("Starting login process...")
    
    try:
        # Navigate to login page
        print("Navigating to login page...")
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/login")
        
        # Wait for page to load
        print("Waiting for page to load...")
        time.sleep(3)
        
        # Click on verification code login/register
        print("Clicking on verification code login option...")
        verification_login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '验证码登录/注册')]"))
        )
        verification_login.click()
        
        print("✅ Successfully clicked on verification code login/register option!")
        
        # Wait for the phone number input to appear and enter the phone number
        print("Waiting for phone number input field...")
        try:
            phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.el-input__inner[placeholder='请输入手机号']"))
            )
            print("✅ Phone number input found by CSS selector!")
        except Exception as e:
            print("❌ Could not find phone number input by CSS selector, trying alternative selector...")
            phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "el-id-1024-168"))
            )
            print("✅ Phone number input found by ID!")
        
        phone_input.click()
        phone_input.clear()
        phone_input.send_keys("14562485478")
        print("✅ Phone number entered successfully!")
        
        # Wait for the verification code input to appear and enter the code
        print("Waiting for verification code input field...")
        try:
            code_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.el-input__inner[placeholder='请输入验证码']"))
            )
            print("✅ Verification code input found by CSS selector!")
        except Exception as e:
            print("❌ Could not find verification code input by CSS selector, trying alternative selector...")
            code_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @maxlength='6']"))
            )
            print("✅ Verification code input found by alternative selector!")
        
        code_input.click()
        code_input.clear()
        code_input.send_keys("999999")
        print("✅ Verification code entered successfully!")
        
        # Tick the checkbox for user agreement
        print("Ticking the user agreement checkbox...")
        try:
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'el-checkbox__input')]"))
            )
            print("✅ User agreement checkbox found!")
        except Exception as e:
            print("❌ Could not find checkbox by class, trying alternative selector...")
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[contains(., '我已阅读并同意')]//span"))
            )
            print("✅ User agreement checkbox found by alternative selector!")
        
        checkbox.click()
        print("✅ User agreement checkbox ticked!")
        
        # Wait for manual button click
        print("⏳ Waiting for manual click on '首次登录即注册' button...")
        print("Please click the registration button manually when ready.")
        
        # Wait for redirection after manual click
        print("Waiting for redirection after manual click...")
        
        # Use the new wait function for personal center
        login_success = wait_for_personal_center(driver, timeout=40)
        
        if login_success:
            print("✅ SUCCESS! Login successful - redirected to personal center.")
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
    test_no_balance_scenario() 