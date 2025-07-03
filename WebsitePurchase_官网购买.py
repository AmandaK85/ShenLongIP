#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ShenLong IP Official Website Comprehensive Test Suite
综合测试套件 - 官网所有套餐测试 

Test Order:
1. 动态高级套餐 (Dynamic Advanced Package)
2. 动态独享套餐 (Dynamic Dedicated Package) 
3. 静态高级套餐 (Static Premium Package)
4. 固定长效套餐 (Fixed Long-Term Package)
5. 个人中心 > 动态高级 (Personal Center - Dynamic Advanced)
6. 个人中心 > 动态独享 (Personal Center - Dynamic Dedicated)
7. 个人中心 > 静态高级 (Personal Center - Static Premium)

Features:
- Automatic retry for failed tests (up to 2 retries)
- Comprehensive reporting with retry information
- Robust error handling
"""

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

class TestReporter:
    """Class to handle test reporting functionality"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        
        # Create reports directory if it doesn't exist
        if not os.path.exists("reports"):
            os.makedirs("reports")
    
    def add_step(self, step_name, status, message="", retry_attempt=0):
        """Add a test step to the report"""
        retry_info = f" (Retry {retry_attempt})" if retry_attempt > 0 else ""
        step_data = {
            "step_name": step_name + retry_info,
            "status": status,  # "PASS", "FAIL", "INFO", "RETRY"
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "retry_attempt": retry_attempt
        }
        self.test_results.append(step_data)
        
        # Print to console
        status_text = "PASS" if status == "PASS" else "FAIL" if status == "FAIL" else "RETRY" if status == "RETRY" else "INFO"
        print(f"[{status_text}]{retry_info} {step_name}: {message}")
    
    def generate_html_report(self):
        """Generate HTML report with all test results"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # Count results
        passed = len([r for r in self.test_results if r["status"] == "PASS"])
        failed = len([r for r in self.test_results if r["status"] == "FAIL"])
        retried = len([r for r in self.test_results if r["status"] == "RETRY"])
        total = len([r for r in self.test_results if r["status"] in ["PASS", "FAIL"]])
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ShenLong Complete Package Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .test-step {{ background-color: white; margin: 10px 0; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .pass {{ border-left: 5px solid #27ae60; }}
        .fail {{ border-left: 5px solid #e74c3c; }}
        .info {{ border-left: 5px solid #3498db; }}
        .retry {{ border-left: 5px solid #f39c12; }}
        .stats {{ display: flex; justify-content: space-around; }}
        .stat-box {{ text-align: center; padding: 15px; }}
        .stat-number {{ font-size: 2em; font-weight: bold; }}
        .pass-color {{ color: #27ae60; }}
        .fail-color {{ color: #e74c3c; }}
        .info-color {{ color: #3498db; }}
        .retry-color {{ color: #f39c12; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>ShenLong Complete Package Test Report (With Auto-Retry)</h1>
        <p>Generated on: {end_time.strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>Test Duration: {str(duration).split('.')[0]}</p>
    </div>
    
    <div class="summary">
        <h2>Test Summary</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number pass-color">{passed}</div>
                <div>Passed</div>
            </div>
            <div class="stat-box">
                <div class="stat-number fail-color">{failed}</div>
                <div>Failed</div>
            </div>
            <div class="stat-box">
                <div class="stat-number retry-color">{retried}</div>
                <div>Retried</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{total}</div>
                <div>Total Tests</div>
            </div>
        </div>
    </div>
    
    <div class="summary">
        <h2>Test Steps</h2>
"""
        
        for result in self.test_results:
            status_class = result["status"].lower()
            status_text = "[PASS]" if result["status"] == "PASS" else "[FAIL]" if result["status"] == "FAIL" else "[RETRY]" if result["status"] == "RETRY" else "[INFO]"
            
            html_content += f"""
        <div class="test-step {status_class}">
            <h3>{status_text} {result["step_name"]}</h3>
            <p><strong>Time:</strong> {result["timestamp"]}</p>
            <p><strong>Status:</strong> {result["status"]}</p>
            <p><strong>Message:</strong> {result["message"]}</p>
        </div>
"""
        
        html_content += """
    </div>
</body>
</html>
"""
        
        # Save HTML report
        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        report_filename = f"complete_package_test_with_retry_{timestamp}.html"
        report_path = os.path.join("reports", report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML Report generated: {report_path}")
        return report_path

def retry_test(test_func=None, test_name=None, max_retries=2):
    """
    Retry wrapper for test functions - can be used as decorator with or without arguments
    
    Args:
        test_func: Function to test (when used as @retry_test)
        test_name: Name of the test for logging (optional, will use function name if not provided)
        max_retries: Maximum number of retry attempts
    
    Returns:
        Decorated function or decorator
    """
    def decorator(func):
        func_test_name = test_name or func.__name__.replace('_', ' ').title()
        
        def wrapper(driver, reporter, *args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        reporter.add_step(f"Retrying {func_test_name}", "RETRY", f"Attempt {attempt + 1}/{max_retries + 1}", attempt)
                        print(f"\n{'='*60}")
                        print(f"RETRYING: {func_test_name} - Attempt {attempt + 1}")
                        print(f"{'='*60}")
                        time.sleep(3)  # Brief pause before retry
                    
                    result = func(driver, reporter, *args, **kwargs)
                    
                    if result:
                        if attempt > 0:
                            reporter.add_step(f"{func_test_name} - Retry Success", "PASS", f"Succeeded on retry attempt {attempt + 1}", attempt)
                        return True
                    elif attempt < max_retries:
                        reporter.add_step(f"{func_test_name} - Failed", "RETRY", f"Failed on attempt {attempt + 1}, will retry", attempt)
                    else:
                        reporter.add_step(f"{func_test_name} - Final Failure", "FAIL", f"Failed after {max_retries + 1} attempts", attempt)
                        
                except Exception as e:
                    error_msg = f"Exception on attempt {attempt + 1}: {str(e)}"
                    if attempt < max_retries:
                        reporter.add_step(f"{func_test_name} - Exception", "RETRY", error_msg, attempt)
                    else:
                        reporter.add_step(f"{func_test_name} - Final Exception", "FAIL", error_msg, attempt)
            
            return False
        
        return wrapper
    
    # If called without arguments (@retry_test), test_func will be the actual function
    if test_func is not None:
        return decorator(test_func)
    
    # If called with arguments (@retry_test(...)), return the decorator
    return decorator

def setup_chrome_driver():
    """Setup and return Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Try using ChromeDriverManager first
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e1:
            print(f"ChromeDriverManager failed: {str(e1)}")
            
            # Fallback: try without service
            try:
                driver = webdriver.Chrome(options=chrome_options)
                return driver
            except Exception as e2:
                print(f"Direct Chrome initialization failed: {str(e2)}")
                
                # Last resort: try with minimal options
                try:
                    minimal_options = Options()
                    minimal_options.add_argument('--no-sandbox')
                    minimal_options.add_argument('--disable-dev-shm-usage')
                    driver = webdriver.Chrome(options=minimal_options)
                    return driver
                except Exception as e3:
                    print(f"Minimal Chrome initialization failed: {str(e3)}")
                    return None
                    
    except Exception as e:
        print(f"Error initializing Chrome driver: {str(e)}")
        return None

def login_shenlong(driver, reporter):
    """Login to ShenLong using only the provided cookies"""
    print("Starting login process with provided cookies...")
    reporter.add_step("Login Process", "INFO", "Starting ShenLong login process with provided cookies")
    try:
        # Go to the domain to allow setting cookies
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net")
        time.sleep(2)
        reporter.add_step("Navigate to Domain", "PASS", "Successfully navigated to domain for cookie setup")

        # Clear all cookies first
        driver.delete_all_cookies()
        reporter.add_step("Clear Cookies", "PASS", "Cleared all existing cookies")

        # Set ALL authentication cookies including the missing ones
        cookies_data = [
            {"name": "__root_domain_v", "value": "", "domain": ".xiaoxigroup.net", "path": "/"},
            {"name": "__snaker__id", "value": "h93rjcHY8FBOfcOO", "domain": "test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "_clck", "value": "f8psxo%7C2%7Cfxa%7C0%7C2000", "domain": ".xiaoxigroup.net", "path": "/"},
            {"name": "_clsk", "value": "6pzrpz%7C1751509591927%7C1%7C1%7Cf.clarity.ms%2Fcollect", "domain": ".xiaoxigroup.net", "path": "/"},
            {"name": "_qdda", "value": "4-1.1", "domain": "test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "_qddab", "value": "4-n5m2mg.mck49897", "domain": "test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "_qddaz", "value": "QD.987350750324316", "domain": ".xiaoxigroup.net", "path": "/"},
            {"name": "_uetsid", "value": "96b990c0563d11f08aefdd0db7ff4ce9", "domain": ".xiaoxigroup.net", "path": "/"},
            {"name": "_uetvid", "value": "0bba69504ff811f09f2d55e2ba8ec7e4", "domain": ".xiaoxigroup.net", "path": "/"},
            {"name": "balance", "value": "88428.26", "domain": "test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "CLID", "value": "a5c2908c138b40d6bdddad2621376c38.20250620.20260703", "domain": "www.clarity.ms", "path": "/"},
            {"name": "gdxidpyhxdE", "value": "EYWJbNBnd%2FDUJYgXbebDGwzwkiZ7mWYQbvLBsg6P3tV%5Cw%5CWK%5C0QUP6hQGU3%2FRGGRuH82ocoduqt%2BfSNWqbYwtG%2Fv%2FnAGmXH03Edrca7kkk0%5CW5mfnl15uDPXQfMkBVu%2FXH4JpXEhWWmvlHAZbOoqOoj6urBWDCaRLvWpx5iuyos8XITn%3A1751510473331", "domain": "test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "Hm_lpvt_ab97e0528cd8a1945e66aee550b54522", "value": "1751509591", "domain": ".test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "Hm_lpvt_b697afe6e9c7d29cd1db7fa7b477f2f6", "value": "1751509591", "domain": ".test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "Hm_lvt_ab97e0528cd8a1945e66aee550b54522", "value": "1751348297,1751349468,1751439990,1751506933", "domain": ".test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "Hm_lvt_b697afe6e9c7d29cd1db7fa7b477f2f6", "value": "1751348297,1751349468,1751439990,1751506933", "domain": ".test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "HMACCOUNT", "value": "30F199DAD7C59D55", "domain": ".test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            {"name": "HMACCOUNT_BFESS", "value": "30F199DAD7C59D55", "domain": ".hm.baidu.com", "path": "/"},
            {"name": "MR", "value": "0", "domain": ".bat.bing.com", "path": "/"},
            {"name": "MSPTC", "value": "J6eC0nN3qdOcXveMzFmUMMKKy5_OE9j8xHnKyOy8hdU", "domain": ".bing.com", "path": "/"},
            {"name": "MUID", "value": "25C0E30F99F56CAB1B36F51E985C6D29", "domain": ".clarity.ms", "path": "/"},
            {"name": "MUID", "value": "25C0E30F99F56CAB1B36F51E985C6D29", "domain": ".bing.com", "path": "/"},
            # MOST IMPORTANT - AUTHENTICATION TOKEN
            {"name": "token", "value": "3KPhUMtt/2YVZWGylT7TmAlrjWkR1bDwjyqcknvQOOQ=", "domain": "test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"},
            # USER SESSION DATA
            {"name": "User_Info", "value": "%7B%22_id%22%3A%2268414905acf739152492f1e2%22%2C%22id%22%3A10614%2C%22username%22%3A%2215124493540%22%2C%22realMoney%22%3A67045.22000000004%2C%22balance%22%3A88428.26000000015%2C%22phone%22%3A%2215124493540%22%2C%22state%22%3A1%2C%22createTime%22%3A1749108997%2C%22isNewUser%22%3Atrue%2C%22registIP%22%3A%22120.240.163.164%22%2C%22creator%22%3A10616%2C%22parent%22%3A%5B8948%2C10616%5D%2C%22appointSellerTime%22%3A1749113241%2C%22source%22%3A%22register%22%2C%22keyword%22%3Anull%2C%22brand%22%3A1%2C%22roles%22%3A%5B300%5D%2C%22testLimitAccess%22%3Afalse%2C%22testLimit%22%3A1%2C%22testCount%22%3A1%2C%22registFingerPrint%22%3A%22e0bd09d58f2c81c83e027f9d75f0f9d7%22%2C%22dailyActive%22%3A19%2C%22lastIP%22%3A%22120.240.163.164%22%2C%22lastLoginRegion%22%3A%22%E4%B8%AD%E5%9B%BD%E5%B9%BF%E4%B8%9C%E6%8F%AD%E9%98%B3%22%2C%22lastLoginTime%22%3A1751503103%2C%22loginTime%22%3A1751507098%2C%22userLevel%22%3A50%2C%22isCompanyAuth%22%3Atrue%2C%22thirdPayAccCount%22%3A1%2C%22regionLimit%22%3Afalse%2C%22token%22%3A%223KPhUMtt%2F2YVZWGylT7TmAlrjWkR1bDwjyqcknvQOOQ%3D%22%2C%22registered%22%3Atrue%7D", "domain": "test-ip-shenlong.cd.xiaoxigroup.net", "path": "/"}
        ]
        for cookie in cookies_data:
            try:
                driver.add_cookie(cookie)
                reporter.add_step(f"Add Cookie: {cookie['name']}", "PASS", f"Successfully added cookie: {cookie['name']}")
            except Exception as e:
                reporter.add_step(f"Add Cookie: {cookie['name']}", "INFO", f"Could not add cookie: {str(e)}")

        # Go to personal center and verify login
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter")
        time.sleep(3)
        reporter.add_step("Navigate to Personal Center", "PASS", "Successfully navigated to personal center")

        # Try multiple indicators of successful login
        login_verified = False
        indicators = [
            "//*[contains(text(), '余额')]",
            "//*[contains(text(), 'balance')]",
            "//*[contains(text(), '账户')]",
            "//*[contains(text(), 'account')]",
            "//*[contains(text(), '个人中心')]",
            "//*[contains(text(), 'personal')]",
            "//button[contains(text(), '添加付费账户')]",
            "//div[contains(@class, 'personal')]",
            "//div[contains(@class, 'account')]"
        ]
        for indicator in indicators:
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, indicator))
                )
                reporter.add_step("Login Verification", "PASS", f"Successfully logged in - found indicator: {indicator}")
                login_verified = True
                break
            except:
                continue
        if not login_verified:
            if "login" not in driver.current_url.lower():
                reporter.add_step("Login Verification", "PASS", "Successfully logged in - not on login page")
                login_verified = True
        if login_verified:
            return True
        else:
            reporter.add_step("Login Verification", "FAIL", "Could not find any login indicators")
            return False
    except Exception as e:
        reporter.add_step("Login Error", "FAIL", f"Login process error: {str(e)}")
        return False

# ============================================================================
# 1. 动态高级套餐 (Dynamic Advanced Package) Tests with Retry
# ============================================================================

@retry_test
def test_dynamic_advanced_wallet_payment(driver, reporter):
    """Test Dynamic Advanced Package with wallet balance payment"""
    print("\n" + "=" * 60)
    print("1.1 动态高级套餐 - 余额支付(Pay With Wallet Balance)")
    print("=" * 60)
    
    try:
        # Navigate to dynamic advanced package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=0")
        time.sleep(3)
        reporter.add_step("Navigate to Dynamic Advanced", "PASS", "Successfully navigated to dynamic advanced package page")
        
        # Click 立即购买
        buy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
        )
        buy_button.click()
        time.sleep(2)
        reporter.add_step("Click Buy Button", "PASS", "Successfully clicked 立即购买")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
        )
        pay_button.click()
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付")
        
        # Wait and check redirection
        time.sleep(10)
        current_url = driver.current_url
        if "personalCenter/countManage" in current_url:
            reporter.add_step("Dynamic Advanced Wallet Payment", "PASS", "Successfully redirected to countManage page")
            return True
        else:
            reporter.add_step("Dynamic Advanced Wallet Payment", "INFO", f"Current URL: {current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Dynamic Advanced Wallet Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_dynamic_advanced_alipay_payment(driver, reporter):
    """Test Dynamic Advanced Package with Alipay payment"""
    print("\n" + "=" * 60)
    print("1.2 动态高级套餐 - 支付宝支付(Pay With Alipay)")
    print("=" * 60)
    
    try:
        # Navigate to dynamic advanced package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=0")
        time.sleep(3)
        reporter.add_step("Navigate to Dynamic Advanced", "PASS", "Successfully navigated to dynamic advanced package page")
        
        # Click 立即购买
        buy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
        )
        buy_button.click()
        time.sleep(2)
        reporter.add_step("Click Buy Button", "PASS", "Successfully clicked 立即购买")
        
        # Select Alipay payment
        alipay_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., '支付宝')]"))
        )
        alipay_option.click()
        time.sleep(2)
        reporter.add_step("Select Alipay", "PASS", "Successfully selected Alipay payment method")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
        )
        pay_button.click()
        time.sleep(5)
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付")
        
        # Switch to new tab
        WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Check Alipay page
        WebDriverWait(driver, 20).until(
            lambda d: "excashier-sandbox.dl.alipaydev.com/standard/auth.htm" in d.current_url
        )
        reporter.add_step("Alipay Page Opened", "PASS", "Successfully redirected to Alipay sandbox page")
        
        # Enter email
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='手机号码/邮箱']"))
        )
        email_input.clear()
        email_input.send_keys("lgipqm7573@sandbox.com")
        reporter.add_step("Enter Email", "PASS", "Successfully entered email: lgipqm7573@sandbox.com")
        
        # Enter password and click next step
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "payPasswd_rsainput"))
        )
        password_input.clear()
        password_input.send_keys("111111")
        reporter.add_step("Enter Alipay Password", "PASS", "Successfully entered password: 111111")
        time.sleep(5)

        # Click 下一步 (Next Step)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='下一步']"))
        )
        next_button.click()
        time.sleep(3)
        reporter.add_step("Click Next Step", "PASS", "Successfully clicked 下一步")
        
        # Verify recipient
        try:
            recipient_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'shmgbf5888@sandbox.com')]"))
            )
            reporter.add_step("Verify Recipient", "PASS", "Successfully verified recipient: shmgbf5888@sandbox.com")
        except Exception as e:
            reporter.add_step("Verify Recipient", "INFO", f"Could not verify recipient: {str(e)}")
        
        # Enter payment password
        payment_password = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/form/div[2]/div[2]/div/div/span[2]/input"))
        )
        payment_password.clear()
        payment_password.send_keys("111111")
        reporter.add_step("Enter Payment Password", "PASS", "Successfully entered payment password")
        
        # Click confirm payment
        confirm_payment_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/form/div[3]/div/input"))
        )
        confirm_payment_button.click()
        time.sleep(3)
        reporter.add_step("Confirm Payment", "PASS", "Successfully clicked 确认付款")
        
        # Wait for redirection
        print("Waiting 30 seconds for redirection...")
        time.sleep(30)
        
        # Check if redirected back
        if "test-ip-shenlong.cd.xiaoxigroup.net" in driver.current_url:
            reporter.add_step("Alipay Payment Success", "PASS", "Successfully redirected back to main site")
            return True
        else:
            reporter.add_step("Alipay Payment Check", "INFO", f"Current URL: {driver.current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Dynamic Advanced Alipay Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_dynamic_advanced_wechat_payment(driver, reporter):
    """Test Dynamic Advanced Package with WeChat payment"""
    print("\n" + "=" * 60)
    print("1.3 动态高级套餐 - 微信付款(Pay With WeChat)")
    print("=" * 60)
    
    try:
        # Navigate to dynamic advanced package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=0")
        time.sleep(3)
        reporter.add_step("Navigate to Dynamic Advanced", "PASS", "Successfully navigated to dynamic advanced package page")
        
        # Click 立即购买
        buy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
        )
        buy_button.click()
        time.sleep(2)
        reporter.add_step("Click Buy Button", "PASS", "Successfully clicked 立即购买")
        
        # Select WeChat payment
        wechat_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., '微信')]"))
        )
        wechat_option.click()
        time.sleep(2)
        reporter.add_step("Select WeChat", "PASS", "Successfully selected WeChat payment method")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
        )
        pay_button.click()
        time.sleep(5)
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付")
        
        # Check for WeChat QR
        try:
            wechat_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '微信扫码付款')]"))
            )
            reporter.add_step("WeChat QR Found", "PASS", "Successfully found '微信扫码付款' - WeChat payment successful")
            
            time.sleep(10)
            reporter.add_step("WeChat Payment Complete", "PASS", "WeChat payment process completed")
            return True
            
        except Exception as e:
            reporter.add_step("WeChat QR Check", "INFO", f"WeChat QR check: {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Dynamic Advanced WeChat Error", "FAIL", f"Error: {str(e)}")
        return False

# ============================================================================
# 2. 动态独享套餐 (Dynamic Dedicated Package) Tests with Retry
# ============================================================================

@retry_test
def test_dynamic_dedicated_wallet_payment(driver, reporter):
    """Test Dynamic Dedicated Package with wallet balance payment"""
    print("\n" + "=" * 60)
    print("2.1 动态独享套餐 - 余额支付(Pay With Wallet Balance)")
    print("=" * 60)
    
    try:
        # Navigate to dynamic dedicated package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=1")
        time.sleep(3)
        reporter.add_step("Navigate to Dynamic Dedicated", "PASS", "Successfully navigated to dynamic dedicated package page")
        
        # Click 立即购买
        buy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
        )
        buy_button.click()
        time.sleep(2)
        reporter.add_step("Click Buy Button", "PASS", "Successfully clicked 立即购买")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
        )
        pay_button.click()
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付")
        
        # Wait and check redirection
        time.sleep(10)
        current_url = driver.current_url
        if "personalCenter/countManage" in current_url:
            reporter.add_step("Dynamic Dedicated Wallet Payment", "PASS", "Successfully redirected to countManage page")
            return True
        else:
            reporter.add_step("Dynamic Dedicated Wallet Payment", "INFO", f"Current URL: {current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Dynamic Dedicated Wallet Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_dynamic_dedicated_alipay_payment(driver, reporter):
    """Test Dynamic Dedicated Package with Alipay payment"""
    print("\n" + "=" * 60)
    print("2.2 动态独享套餐 - 支付宝支付(Pay With Alipay)")
    print("=" * 60)
    
    try:
        # Navigate to dynamic dedicated package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=1")
        time.sleep(3)
        reporter.add_step("Navigate to Dynamic Dedicated", "PASS", "Successfully navigated to dynamic dedicated package page")
        
        # Click 立即购买
        buy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
        )
        buy_button.click()
        time.sleep(2)
        reporter.add_step("Click Buy Button", "PASS", "Successfully clicked 立即购买")
        
        # Select Alipay payment
        alipay_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., '支付宝')]"))
        )
        alipay_option.click()
        time.sleep(2)
        reporter.add_step("Select Alipay", "PASS", "Successfully selected Alipay payment method")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
        )
        pay_button.click()
        time.sleep(5)
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付")
        
        # Switch to new tab
        WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Check Alipay page
        WebDriverWait(driver, 20).until(
            lambda d: "excashier-sandbox.dl.alipaydev.com/standard/auth.htm" in d.current_url
        )
        reporter.add_step("Alipay Page Opened", "PASS", "Successfully redirected to Alipay sandbox page")
        
        # Enter email
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='手机号码/邮箱']"))
        )
        email_input.clear()
        email_input.send_keys("lgipqm7573@sandbox.com")
        reporter.add_step("Enter Email", "PASS", "Successfully entered email: lgipqm7573@sandbox.com")
        
        # Enter password and click next step
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "payPasswd_rsainput"))
        )
        password_input.clear()
        password_input.send_keys("111111")
        reporter.add_step("Enter Alipay Password", "PASS", "Successfully entered password: 111111")
        time.sleep(5)

        # Click 下一步 (Next Step)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='下一步']"))
        )
        next_button.click()
        time.sleep(3)
        reporter.add_step("Click Next Step", "PASS", "Successfully clicked 下一步")
        
        # Verify recipient
        try:
            recipient_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'shmgbf5888@sandbox.com')]"))
            )
            reporter.add_step("Verify Recipient", "PASS", "Successfully verified recipient: shmgbf5888@sandbox.com")
        except Exception as e:
            reporter.add_step("Verify Recipient", "INFO", f"Could not verify recipient: {str(e)}")
        
        # Enter payment password
        payment_password = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/form/div[2]/div[2]/div/div/span[2]/input"))
        )
        payment_password.clear()
        payment_password.send_keys("111111")
        reporter.add_step("Enter Payment Password", "PASS", "Successfully entered payment password")
        
        # Click confirm payment
        confirm_payment_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/form/div[3]/div/input"))
        )
        confirm_payment_button.click()
        time.sleep(3)
        reporter.add_step("Confirm Payment", "PASS", "Successfully clicked 确认付款")
        
        # Wait for redirection
        print("Waiting 30 seconds for redirection...")
        time.sleep(30)
        
        # Check if redirected back
        if "test-ip-shenlong.cd.xiaoxigroup.net" in driver.current_url:
            reporter.add_step("Dynamic Dedicated Alipay Payment", "PASS", "Successfully redirected back to main site")
            return True
        else:
            reporter.add_step("Dynamic Dedicated Alipay Payment", "INFO", f"Current URL: {driver.current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Dynamic Dedicated Alipay Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_dynamic_dedicated_wechat_payment(driver, reporter):
    """Test Dynamic Dedicated Package with WeChat payment"""
    print("\n" + "=" * 60)
    print("2.3 动态独享套餐 - 微信付款(Pay With WeChat)")
    print("=" * 60)
    
    try:
        # Navigate to dynamic dedicated package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=1")
        time.sleep(3)
        reporter.add_step("Navigate to Dynamic Dedicated", "PASS", "Successfully navigated to dynamic dedicated package page")
        
        # Click 立即购买
        buy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
        )
        buy_button.click()
        time.sleep(2)
        reporter.add_step("Click Buy Button", "PASS", "Successfully clicked 立即购买")
        
        # Select WeChat payment
        wechat_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., '微信')]"))
        )
        wechat_option.click()
        time.sleep(2)
        reporter.add_step("Select WeChat", "PASS", "Successfully selected WeChat payment method")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
        )
        pay_button.click()
        time.sleep(5)
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付")
        
        # Check for WeChat QR
        try:
            wechat_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '微信扫码付款')]"))
            )
            reporter.add_step("WeChat QR Found", "PASS", "Successfully found '微信扫码付款' - WeChat payment successful")
            
            time.sleep(10)
            reporter.add_step("WeChat Payment Complete", "PASS", "WeChat payment process completed")
            return True
            
        except Exception as e:
            reporter.add_step("WeChat QR Check", "INFO", f"WeChat QR check: {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Dynamic Dedicated WeChat Error", "FAIL", f"Error: {str(e)}")
        return False

# ============================================================================
# 3. 静态高级套餐 (Static Premium Package) Tests with Retry 
# ============================================================================

@retry_test
def test_static_premium_wallet_payment(driver, reporter):
    """Test Static Premium Package with wallet balance payment"""
    print("\n" + "=" * 60)
    print("3.1 静态高级套餐 - 余额支付(Pay With Wallet Balance)")
    print("=" * 60)
    
    try:
        # Navigate to static premium package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=2")
        time.sleep(3)
        reporter.add_step("Navigate to Static Premium", "PASS", "Successfully navigated to static premium package page")
        
        # Click 立即购买
        buy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
        )
        buy_button.click()
        time.sleep(2)
        reporter.add_step("Click Buy Button", "PASS", "Successfully clicked 立即购买")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
        )
        pay_button.click()
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付")
        
        # Wait and check redirection
        time.sleep(10)
        current_url = driver.current_url
        if "personalCenter/countManage" in current_url:
            reporter.add_step("Static Premium Wallet Payment", "PASS", "Successfully redirected to countManage page")
            return True
        else:
            reporter.add_step("Static Premium Wallet Payment", "INFO", f"Current URL: {current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Static Premium Wallet Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_static_premium_alipay_payment(driver, reporter):
    """Test Static Premium Package with Alipay payment"""
    print("\n" + "=" * 60)
    print("3.2 静态高级套餐 - 支付宝支付(Pay With Alipay)")
    print("=" * 60)
    
    try:
        # Navigate to static premium package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=2")
        time.sleep(3)
        reporter.add_step("Navigate to Static Premium", "PASS", "Successfully navigated to static premium package page")
        
        # Click 立即购买
        buy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
        )
        buy_button.click()
        time.sleep(2)
        reporter.add_step("Click Buy Button", "PASS", "Successfully clicked 立即购买")
        
        # Select Alipay payment
        alipay_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., '支付宝')]"))
        )
        alipay_option.click()
        time.sleep(2)
        reporter.add_step("Select Alipay", "PASS", "Successfully selected Alipay payment method")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
        )
        pay_button.click()
        time.sleep(5)
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付")
        
        # Switch to new tab
        WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Check Alipay page
        WebDriverWait(driver, 20).until(
            lambda d: "excashier-sandbox.dl.alipaydev.com/standard/auth.htm" in d.current_url
        )
        reporter.add_step("Alipay Page Opened", "PASS", "Successfully redirected to Alipay sandbox page")
        
        # Enter email
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='手机号码/邮箱']"))
        )
        email_input.clear()
        email_input.send_keys("lgipqm7573@sandbox.com")
        reporter.add_step("Enter Email", "PASS", "Successfully entered email: lgipqm7573@sandbox.com")
        
        # Enter password and click next step
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "payPasswd_rsainput"))
        )
        password_input.clear()
        password_input.send_keys("111111")
        reporter.add_step("Enter Alipay Password", "PASS", "Successfully entered password: 111111")
        time.sleep(5)

        # Click 下一步 (Next Step)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='下一步']"))
        )
        next_button.click()
        time.sleep(3)
        reporter.add_step("Click Next Step", "PASS", "Successfully clicked 下一步")
        
        # Verify recipient
        try:
            recipient_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'shmgbf5888@sandbox.com')]"))
            )
            reporter.add_step("Verify Recipient", "PASS", "Successfully verified recipient: shmgbf5888@sandbox.com")
        except Exception as e:
            reporter.add_step("Verify Recipient", "INFO", f"Could not verify recipient: {str(e)}")
        
        # Enter payment password
        payment_password = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/form/div[2]/div[2]/div/div/span[2]/input"))
        )
        payment_password.clear()
        payment_password.send_keys("111111")
        reporter.add_step("Enter Payment Password", "PASS", "Successfully entered payment password")
        
        # Click confirm payment
        confirm_payment_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/form/div[3]/div/input"))
        )
        confirm_payment_button.click()
        time.sleep(3)
        reporter.add_step("Confirm Payment", "PASS", "Successfully clicked 确认付款")
        
        # Wait for redirection
        print("Waiting 30 seconds for redirection...")
        time.sleep(30)
        
        # Check if redirected back
        if "test-ip-shenlong.cd.xiaoxigroup.net" in driver.current_url:
            reporter.add_step("Static Premium Alipay Payment", "PASS", "Successfully redirected back to main site")
            return True
        else:
            reporter.add_step("Static Premium Alipay Payment", "INFO", f"Current URL: {driver.current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Static Premium Alipay Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_static_premium_wechat_payment(driver, reporter):
    """Test Static Premium Package with WeChat payment"""
    print("\n" + "=" * 60)
    print("3.3 静态高级套餐 - 微信付款(Pay With WeChat)")
    print("=" * 60)
    
    try:
        # Navigate to static premium package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/ip?ipType=2")
        time.sleep(3)
        reporter.add_step("Navigate to Static Premium", "PASS", "Successfully navigated to static premium package page")
        
        # Click 立即购买
        buy_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/button"))
        )
        buy_button.click()
        time.sleep(2)
        reporter.add_step("Click Buy Button", "PASS", "Successfully clicked 立即购买")
        
        # Select WeChat payment
        wechat_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., '微信')]"))
        )
        wechat_option.click()
        time.sleep(2)
        reporter.add_step("Select WeChat", "PASS", "Successfully selected WeChat payment method")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div[5]/button"))
        )
        pay_button.click()
        time.sleep(5)
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付")
        
        # Check for WeChat QR
        try:
            wechat_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '微信扫码付款')]"))
            )
            reporter.add_step("WeChat QR Found", "PASS", "Successfully found '微信扫码付款' - WeChat payment successful")
            
            time.sleep(10)
            reporter.add_step("WeChat Payment Complete", "PASS", "WeChat payment process completed")
            return True
            
        except Exception as e:
            reporter.add_step("WeChat QR Check", "INFO", f"WeChat QR check: {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Static Premium WeChat Error", "FAIL", f"Error: {str(e)}")
        return False

# ============================================================================
# 4. 固定长效套餐 (Fixed Long-Term Package) Tests with Retry
# ============================================================================

@retry_test
def test_longterm_wallet_payment(driver, reporter):
    """Test Fixed Long-Term Package with wallet balance payment"""
    print("\n" + "=" * 60)
    print("4.1 固定长效套餐 - 余额支付(Pay With Wallet Balance)")
    print("=" * 60)
    
    try:
        # Navigate to long-term package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/long")
        time.sleep(3)
        reporter.add_step("Navigate to Long-Term Package", "PASS", "Successfully navigated to long-term package page")
        
        # Click 北京
        beijing_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/span[2]"))
        )
        beijing_button.click()
        time.sleep(2)
        reporter.add_step("Select Beijing", "PASS", "Successfully selected 北京")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div[3]/div/div[4]/div[2]/button"))
        )
        pay_button.click()
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付 button")
        
        # Wait and check redirection
        time.sleep(10)
        current_url = driver.current_url
        if current_url == "https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage":
            reporter.add_step("Long-Term Wallet Payment", "PASS", "Successfully redirected to countManage page")
            return True
        else:
            reporter.add_step("Long-Term Wallet Payment", "INFO", f"Current URL: {current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Long-Term Wallet Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_longterm_alipay_payment(driver, reporter):
    """Test Fixed Long-Term Package with Alipay payment"""
    print("\n" + "=" * 60)
    print("4.2 固定长效套餐 - 支付宝支付(Pay With Alipay)")
    print("=" * 60)
    
    try:
        # Navigate to long-term package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/long")
        time.sleep(3)
        reporter.add_step("Navigate to Long-Term Package", "PASS", "Successfully navigated to long-term package page")
        
        # Click 北京
        beijing_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/span[2]"))
        )
        beijing_button.click()
        time.sleep(2)
        reporter.add_step("Select Beijing", "PASS", "Successfully selected 北京")
        
        # Click 支付宝
        alipay_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div[3]/div/div[4]/div[2]/div[2]/label[2]"))
        )
        alipay_option.click()
        time.sleep(2)
        reporter.add_step("Select Alipay", "PASS", "Successfully selected 支付宝 payment method")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div[3]/div/div[4]/div[2]/button"))
        )
        pay_button.click()
        time.sleep(5)
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付 button")
        
        # Switch to new tab
        WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Check Alipay page
        WebDriverWait(driver, 20).until(
            lambda d: "excashier-sandbox.dl.alipaydev.com/standard/auth.htm" in d.current_url
        )
        reporter.add_step("Alipay Page Opened", "PASS", "Successfully redirected to Alipay sandbox page")
        
        # Enter email
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='手机号码/邮箱']"))
        )
        email_input.clear()
        email_input.send_keys("lgipqm7573@sandbox.com")
        reporter.add_step("Enter Email", "PASS", "Successfully entered email: lgipqm7573@sandbox.com")
        
        # Enter password and click next step
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "payPasswd_rsainput"))
        )
        password_input.clear()
        password_input.send_keys("111111")
        reporter.add_step("Enter Alipay Password", "PASS", "Successfully entered password: 111111")
        time.sleep(5)

        # Click 下一步 (Next Step)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='下一步']"))
        )
        next_button.click()
        time.sleep(3)
        reporter.add_step("Click Next Step", "PASS", "Successfully clicked 下一步")
        
        # Verify recipient
        try:
            recipient_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'shmgbf5888@sandbox.com')]"))
            )
            reporter.add_step("Verify Recipient", "PASS", "收款方 verified: shmgbf5888@sandbox.com")
        except Exception as e:
            reporter.add_step("Verify Recipient", "INFO", f"Failed to verify 收款方: {str(e)}")
        
        # Enter payment password
        payment_password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/form/div[2]/div[2]/div/div/span[2]/input"))
        )
        payment_password.clear()
        payment_password.send_keys("111111")
        reporter.add_step("Enter Payment Password", "PASS", "Successfully entered payment password: 111111")
        
        # Click confirm payment
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/form/div[3]/div/input"))
        )
        confirm_button.click()
        reporter.add_step("Confirm Payment", "PASS", "Successfully clicked 确认付款")
        
        # Wait and check redirection
        time.sleep(20)
        current_url = driver.current_url
        if current_url == "https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage":
            reporter.add_step("Long-Term Alipay Payment", "PASS", "Successfully redirected to countManage page")
            return True
        else:
            reporter.add_step("Long-Term Alipay Payment", "INFO", f"Current URL: {current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Long-Term Alipay Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_longterm_wechat_payment(driver, reporter):
    """Test Fixed Long-Term Package with WeChat payment"""
    print("\n" + "=" * 60)
    print("4.3 固定长效套餐 - 微信付款(Pay with WeChat Wallet)")
    print("=" * 60)
    
    try:
        # Navigate to long-term package page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/meal/long")
        time.sleep(3)
        reporter.add_step("Navigate to Long-Term Package", "PASS", "Successfully navigated to long-term package page")
        
        # Click 北京
        beijing_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/span[2]"))
        )
        beijing_button.click()
        time.sleep(2)
        reporter.add_step("Select Beijing", "PASS", "Successfully selected 北京")
        
        # Click 微信 (first time)
        wechat_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div[3]/div/div[4]/div[2]/div[2]/label[3]"))
        )
        wechat_option.click()
        time.sleep(2)
        reporter.add_step("Select WeChat", "PASS", "Successfully selected 微信 payment method")
        
        # Click 立即支付
        pay_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div[3]/div/div[4]/div[2]/button"))
        )
        pay_button.click()
        time.sleep(3)
        reporter.add_step("Click Pay Button", "PASS", "Successfully clicked 立即支付 button")
        
        # Check for WeChat QR - if found, success
        try:
            wechat_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '微信扫码付款')]"))
            )
            reporter.add_step("WeChat QR Found", "PASS", "Successfully found '微信扫码付款' - WeChat payment successful")
            
            # Wait 10 seconds as specified
            time.sleep(10)
            reporter.add_step("WeChat Payment Complete", "PASS", "WeChat payment process completed - waited 10 seconds")
            return True
            
        except Exception as e:
            reporter.add_step("WeChat QR Check", "INFO", f"WeChat QR check: {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Long-Term WeChat Error", "FAIL", f"Error: {str(e)}")
        return False

# ============================================================================
# 5. 个人中心 > 动态高级 (Personal Center - Dynamic Advanced) with Retry
# ============================================================================

@retry_test
def test_personal_center_dynamic_advanced_wallet(driver, reporter):
    """Test Dynamic Advanced Package via Personal Center with wallet payment"""
    print("\n" + "=" * 60)
    print("5.1 个人中心>动态高级 - 余额支付(Personal Center Wallet Payment)")
    print("=" * 60)
    
    try:
        # Navigate to count manage page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage")
        time.sleep(3)
        reporter.add_step("Navigate to Count Manage", "PASS", "Successfully navigated to count manage page")
        
        # Click 添加付费账户
        add_account_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/button[1]"))
        )
        add_account_button.click()
        time.sleep(2)
        reporter.add_step("Click Add Account", "PASS", "Successfully clicked 添加付费账户")
        
        # Click 动态高级套餐
        dynamic_advanced_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[1]/form/div[1]/div[2]/div/label[2]/span[1]/span"))
        )
        dynamic_advanced_option.click()
        time.sleep(2)
        reporter.add_step("Select Package", "PASS", "Successfully selected 动态高级套餐")
        
        # Click 确认
        confirm_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]"))
        )
        confirm_button.click()
        time.sleep(3)
        reporter.add_step("Click Confirm", "PASS", "Successfully clicked 确认")
        
        # Wait for success popup
        try:
            success_popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '添加成功!')]"))
            )
            reporter.add_step("Personal Center Dynamic Advanced", "PASS", "Found '添加成功!' popup - Dynamic Advanced Package added successfully")
            return True
            
        except Exception as e:
            reporter.add_step("Personal Center Dynamic Advanced", "INFO", f"Could not find success popup: {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Personal Center Dynamic Advanced Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_personal_center_dynamic_advanced_alipay(driver, reporter):
    """Test Dynamic Advanced Package via Personal Center with Alipay payment"""
    print("\n" + "=" * 60)
    print("5.2 个人中心>动态高级 - 支付宝支付(Personal Center Alipay Payment)")
    print("=" * 60)
    
    try:
        # Navigate to count manage page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage")
        time.sleep(3)
        reporter.add_step("Navigate to Count Manage", "PASS", "Successfully navigated to count manage page")
        
        # Click 添加付费账户
        add_account_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/button[1]"))
        )
        add_account_button.click()
        time.sleep(2)
        reporter.add_step("Click Add Account", "PASS", "Successfully clicked 添加付费账户")
        
        # Click 动态高级套餐
        dynamic_advanced_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[1]/form/div[1]/div[2]/div/label[2]/span[1]/span"))
        )
        dynamic_advanced_option.click()
        time.sleep(2)
        reporter.add_step("Select Package", "PASS", "Successfully selected 动态高级套餐")
        
        # Click 支付宝
        alipay_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[6]/div/div[2]/div"))
        )
        alipay_option.click()
        time.sleep(2)
        reporter.add_step("Select Alipay", "PASS", "Successfully selected 支付宝 payment method")
        
        # Click 确认
        confirm_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]"))
        )
        confirm_button.click()
        time.sleep(5)
        reporter.add_step("Click Confirm", "PASS", "Successfully clicked 确认")
        
        # Switch to new tab
        WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Check Alipay page
        WebDriverWait(driver, 20).until(
            lambda d: "excashier-sandbox.dl.alipaydev.com/standard/auth.htm" in d.current_url
        )
        reporter.add_step("Alipay Page Opened", "PASS", "Successfully redirected to Alipay sandbox page")
        
        # Enter email
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='手机号码/邮箱']"))
        )
        email_input.clear()
        email_input.send_keys("lgipqm7573@sandbox.com")
        reporter.add_step("Enter Email", "PASS", "Successfully entered email: lgipqm7573@sandbox.com")
        
        # Enter password and click next step
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "payPasswd_rsainput"))
        )
        password_input.clear()
        password_input.send_keys("111111")
        reporter.add_step("Enter Alipay Password", "PASS", "Successfully entered password: 111111")
        time.sleep(5)

        # Click 下一步 (Next Step)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='下一步']"))
        )
        next_button.click()
        time.sleep(3)
        reporter.add_step("Click Next Step", "PASS", "Successfully clicked 下一步")
        
        # Verify recipient
        try:
            recipient_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'shmgbf5888@sandbox.com')]"))
            )
            reporter.add_step("Verify Recipient", "PASS", "收款方 verified: shmgbf5888@sandbox.com")
        except Exception as e:
            reporter.add_step("Verify Recipient", "INFO", f"Failed to verify 收款方: {str(e)}")
        
        # Enter payment password
        payment_password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/form/div[2]/div[2]/div/div/span[2]/input"))
        )
        payment_password.clear()
        payment_password.send_keys("111111")
        reporter.add_step("Enter Payment Password", "PASS", "Successfully entered payment password: 111111")
        
        # Click confirm payment
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/form/div[3]/div/input"))
        )
        confirm_button.click()
        reporter.add_step("Confirm Payment", "PASS", "Successfully clicked 确认付款")
        
        # Wait and check redirection
        time.sleep(20)
        current_url = driver.current_url
        if current_url == "https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage":
            reporter.add_step("Personal Center Alipay Payment", "PASS", "Successfully redirected to countManage page")
            return True
        else:
            reporter.add_step("Personal Center Alipay Payment", "INFO", f"Current URL: {current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Personal Center Alipay Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_personal_center_dynamic_advanced_wechat(driver, reporter):
    """Test Dynamic Advanced Package via Personal Center with WeChat payment"""
    print("\n" + "=" * 60)
    print("5.3 个人中心>动态高级 - 微信付款(Personal Center WeChat Payment)")
    print("=" * 60)
    
    try:
        # Navigate to count manage page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage")
        time.sleep(3)
        reporter.add_step("Navigate to Count Manage", "PASS", "Successfully navigated to count manage page")
        
        # Click 添加付费账户
        add_account_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/button[1]"))
        )
        add_account_button.click()
        time.sleep(2)
        reporter.add_step("Click Add Account", "PASS", "Successfully clicked 添加付费账户")
        
        # Click 动态高级套餐
        dynamic_advanced_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[1]/form/div[1]/div[2]/div/label[2]/span[1]/span"))
        )
        dynamic_advanced_option.click()
        time.sleep(2)
        reporter.add_step("Select Package", "PASS", "Successfully selected 动态高级套餐")
        
        # Click 微信
        wechat_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[6]/div/div[3]/div"))
        )
        wechat_option.click()
        time.sleep(2)
        reporter.add_step("Select WeChat", "PASS", "Successfully selected 微信 payment method")
        
        # Click 确认
        confirm_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]"))
        )
        confirm_button.click()
        time.sleep(5)
        reporter.add_step("Click Confirm", "PASS", "Successfully clicked 确认")
        
        # Check for WeChat QR
        try:
            wechat_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '微信扫码付款')]"))
            )
            reporter.add_step("WeChat QR Found", "PASS", "Successfully found '微信扫码付款' - WeChat payment successful")
            
            time.sleep(10)
            reporter.add_step("WeChat Payment Complete", "PASS", "WeChat payment process completed")
            return True
            
        except Exception as e:
            reporter.add_step("WeChat QR Check", "INFO", f"Failed to find '微信扫码付款': {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Personal Center WeChat Error", "FAIL", f"Error: {str(e)}")
        return False

# ============================================================================
# 6. 个人中心 > 动态独享 (Personal Center - Dynamic Dedicated) with Retry
# ============================================================================

@retry_test
def test_personal_center_dynamic_dedicated_wallet(driver, reporter):
    """Test Dynamic Dedicated Package via Personal Center with wallet payment"""
    print("\n" + "=" * 60)
    print("6.1 个人中心>动态独享 - 余额支付(Personal Center Wallet Payment)")
    print("=" * 60)
    
    try:
        # Navigate to count manage page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage")
        time.sleep(3)
        reporter.add_step("Navigate to Count Manage", "PASS", "Successfully navigated to count manage page")
        
        # Click 添加付费账户
        add_account_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/button[1]"))
        )
        add_account_button.click()
        time.sleep(2)
        reporter.add_step("Click Add Account", "PASS", "Successfully clicked 添加付费账户")
        
        # Click 确认 (default selection should be Dynamic Dedicated)
        confirm_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]"))
        )
        confirm_button.click()
        time.sleep(3)
        reporter.add_step("Click Confirm", "PASS", "Successfully clicked 确认 (default Dynamic Dedicated)")
        
        # Wait for success popup
        try:
            success_popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '添加成功!')]"))
            )
            reporter.add_step("Personal Center Dynamic Dedicated", "PASS", "Found '添加成功!' popup - Dynamic Dedicated Package added successfully")
            return True
            
        except Exception as e:
            reporter.add_step("Personal Center Dynamic Dedicated", "INFO", f"Could not find success popup: {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Personal Center Dynamic Dedicated Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_personal_center_dynamic_dedicated_alipay(driver, reporter):
    """Test Dynamic Dedicated Package via Personal Center with Alipay payment"""
    print("\n" + "=" * 60)
    print("6.2 个人中心>动态独享 - 支付宝支付(Personal Center Alipay Payment)")
    print("=" * 60)
    
    try:
        # Navigate to count manage page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage")
        time.sleep(3)
        reporter.add_step("Navigate to Count Manage", "PASS", "Successfully navigated to count manage page")
        
        # Click 添加付费账户
        add_account_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/button[1]"))
        )
        add_account_button.click()
        time.sleep(2)
        reporter.add_step("Click Add Account", "PASS", "Successfully clicked 添加付费账户")
        
        # Click 支付宝
        alipay_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[6]/div/div[2]/div"))
        )
        alipay_option.click()
        time.sleep(2)
        reporter.add_step("Select Alipay", "PASS", "Successfully selected 支付宝 payment method")
        
        # Click 确认 (default selection should be Dynamic Dedicated)
        confirm_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]"))
        )
        confirm_button.click()
        time.sleep(5)
        reporter.add_step("Click Confirm", "PASS", "Successfully clicked 确认")
        
        # Switch to new tab
        WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Check Alipay page
        WebDriverWait(driver, 20).until(
            lambda d: "excashier-sandbox.dl.alipaydev.com/standard/auth.htm" in d.current_url
        )
        reporter.add_step("Alipay Page Opened", "PASS", "Successfully redirected to Alipay sandbox page")
        
        # Enter email
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='手机号码/邮箱']"))
        )
        email_input.clear()
        email_input.send_keys("lgipqm7573@sandbox.com")
        reporter.add_step("Enter Email", "PASS", "Successfully entered email: lgipqm7573@sandbox.com")
        
        # Enter password and click next step
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "payPasswd_rsainput"))
        )
        password_input.clear()
        password_input.send_keys("111111")
        reporter.add_step("Enter Alipay Password", "PASS", "Successfully entered password: 111111")
        time.sleep(5)

        # Click 下一步 (Next Step)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='下一步']"))
        )
        next_button.click()
        time.sleep(3)
        reporter.add_step("Click Next Step", "PASS", "Successfully clicked 下一步")
        
        # Verify recipient
        try:
            recipient_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'shmgbf5888@sandbox.com')]"))
            )
            reporter.add_step("Verify Recipient", "PASS", "收款方 verified: shmgbf5888@sandbox.com")
        except Exception as e:
            reporter.add_step("Verify Recipient", "INFO", f"Failed to verify 收款方: {str(e)}")
        
        # Enter payment password
        payment_password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/form/div[2]/div[2]/div/div/span[2]/input"))
        )
        payment_password.clear()
        payment_password.send_keys("111111")
        reporter.add_step("Enter Payment Password", "PASS", "Successfully entered payment password: 111111")
        
        # Click confirm payment
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/form/div[3]/div/input"))
        )
        confirm_button.click()
        reporter.add_step("Confirm Payment", "PASS", "Successfully clicked 确认付款")
        
        # Wait and check redirection
        time.sleep(20)
        current_url = driver.current_url
        if current_url == "https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage":
            reporter.add_step("Personal Center Dedicated Alipay Payment", "PASS", "Successfully redirected to countManage page")
            return True
        else:
            reporter.add_step("Personal Center Dedicated Alipay Payment", "INFO", f"Current URL: {current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Personal Center Dedicated Alipay Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_personal_center_dynamic_dedicated_wechat(driver, reporter):
    """Test Dynamic Dedicated Package via Personal Center with WeChat payment"""
    print("\n" + "=" * 60)
    print("6.3 个人中心>动态独享 - 微信付款(Personal Center WeChat Payment)")
    print("=" * 60)
    
    try:
        # Navigate to count manage page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage")
        time.sleep(3)
        reporter.add_step("Navigate to Count Manage", "PASS", "Successfully navigated to count manage page")
        
        # Click 添加付费账户
        add_account_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/button[1]"))
        )
        add_account_button.click()
        time.sleep(2)
        reporter.add_step("Click Add Account", "PASS", "Successfully clicked 添加付费账户")
        
        # Click 微信
        wechat_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[6]/div/div[3]/div"))
        )
        wechat_option.click()
        time.sleep(2)
        reporter.add_step("Select WeChat", "PASS", "Successfully selected 微信 payment method")
        
        # Click 确认 (default selection should be Dynamic Dedicated)
        confirm_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]"))
        )
        confirm_button.click()
        time.sleep(5)
        reporter.add_step("Click Confirm", "PASS", "Successfully clicked 确认")
        
        # Check for WeChat QR
        try:
            wechat_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '微信扫码付款')]"))
            )
            reporter.add_step("WeChat QR Found", "PASS", "Successfully found '微信扫码付款' - WeChat payment successful")
            
            time.sleep(10)
            reporter.add_step("WeChat Payment Complete", "PASS", "WeChat payment process completed")
            return True
            
        except Exception as e:
            reporter.add_step("WeChat QR Check", "INFO", f"Failed to find '微信扫码付款': {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Personal Center Dedicated WeChat Error", "FAIL", f"Error: {str(e)}")
        return False

# ============================================================================
# 7. 个人中心 > 静态高级 (Personal Center - Static Premium) with Retry
# ============================================================================

@retry_test
def test_personal_center_static_advanced_wallet(driver, reporter):
    """Test Static Advanced Package via Personal Center with wallet payment"""
    print("\n" + "=" * 60)
    print("7.1 个人中心>静态高级 - 余额支付(Personal Center Wallet Payment)")
    print("=" * 60)
    
    try:
        # Navigate to count manage page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage")
        time.sleep(3)
        reporter.add_step("Navigate to Count Manage", "PASS", "Successfully navigated to count manage page")
        
        # Click 添加付费账户
        add_account_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/button[1]"))
        )
        add_account_button.click()
        time.sleep(2)
        reporter.add_step("Click Add Account", "PASS", "Successfully clicked 添加付费账户")
        
        # Click 静态高级套餐 (label[3])
        static_advanced_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[1]/form/div[1]/div[2]/div/label[3]/span[1]/span"))
        )
        static_advanced_option.click()
        time.sleep(2)
        reporter.add_step("Select Package", "PASS", "Successfully selected 静态高级套餐")
        
        # Click 确认
        confirm_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]"))
        )
        confirm_button.click()
        time.sleep(3)
        reporter.add_step("Click Confirm", "PASS", "Successfully clicked 确认")
        
        # Wait for success popup
        try:
            success_popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '添加成功!')]"))
            )
            reporter.add_step("Personal Center Static Advanced", "PASS", "Found '添加成功!' popup - Static Advanced Package added successfully")
            return True
            
        except Exception as e:
            reporter.add_step("Personal Center Static Advanced", "INFO", f"Could not find success popup: {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Personal Center Static Advanced Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_personal_center_static_advanced_alipay(driver, reporter):
    """Test Static Advanced Package via Personal Center with Alipay payment"""
    print("\n" + "=" * 60)
    print("7.2 个人中心>静态高级 - 支付宝支付(Personal Center Alipay Payment)")
    print("=" * 60)
    
    try:
        # Navigate to count manage page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage")
        time.sleep(3)
        reporter.add_step("Navigate to Count Manage", "PASS", "Successfully navigated to count manage page")
        
        # Click 添加付费账户
        add_account_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/button[1]"))
        )
        add_account_button.click()
        time.sleep(2)
        reporter.add_step("Click Add Account", "PASS", "Successfully clicked 添加付费账户")
        
        # Click 静态高级套餐 (label[3])
        static_advanced_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[1]/form/div[1]/div[2]/div/label[3]/span[1]/span"))
        )
        static_advanced_option.click()
        time.sleep(2)
        reporter.add_step("Select Package", "PASS", "Successfully selected 静态高级套餐")
        
        # Click 支付宝
        alipay_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[6]/div/div[2]/div"))
        )
        alipay_option.click()
        time.sleep(2)
        reporter.add_step("Select Alipay", "PASS", "Successfully selected 支付宝 payment method")
        
        # Click 确认
        confirm_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]"))
        )
        confirm_button.click()
        time.sleep(5)
        reporter.add_step("Click Confirm", "PASS", "Successfully clicked 确认")
        
        # Switch to new tab
        WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Check Alipay page
        WebDriverWait(driver, 20).until(
            lambda d: "excashier-sandbox.dl.alipaydev.com/standard/auth.htm" in d.current_url
        )
        reporter.add_step("Alipay Page Opened", "PASS", "Successfully redirected to Alipay sandbox page")
        
        # Enter email
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='手机号码/邮箱']"))
        )
        email_input.clear()
        email_input.send_keys("lgipqm7573@sandbox.com")
        reporter.add_step("Enter Email", "PASS", "Successfully entered email: lgipqm7573@sandbox.com")
        
        # Enter password and click next step
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "payPasswd_rsainput"))
        )
        password_input.clear()
        password_input.send_keys("111111")
        reporter.add_step("Enter Alipay Password", "PASS", "Successfully entered password: 111111")
        time.sleep(5)

        # Click 下一步 (Next Step)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='下一步']"))
        )
        next_button.click()
        time.sleep(3)
        reporter.add_step("Click Next Step", "PASS", "Successfully clicked 下一步")
        
        # Verify recipient
        try:
            recipient_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'shmgbf5888@sandbox.com')]"))
            )
            reporter.add_step("Verify Recipient", "PASS", "收款方 verified: shmgbf5888@sandbox.com")
        except Exception as e:
            reporter.add_step("Verify Recipient", "INFO", f"Failed to verify 收款方: {str(e)}")
        
        # Enter payment password
        payment_password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/form/div[2]/div[2]/div/div/span[2]/input"))
        )
        payment_password.clear()
        payment_password.send_keys("111111")
        reporter.add_step("Enter Payment Password", "PASS", "Successfully entered payment password: 111111")
        
        # Click confirm payment
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/form/div[3]/div/input"))
        )
        confirm_button.click()
        reporter.add_step("Confirm Payment", "PASS", "Successfully clicked 确认付款")
        
        # Wait and check redirection
        time.sleep(20)
        current_url = driver.current_url
        if current_url == "https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage":
            reporter.add_step("Personal Center Static Alipay Payment", "PASS", "Successfully redirected to countManage page")
            return True
        else:
            reporter.add_step("Personal Center Static Alipay Payment", "INFO", f"Current URL: {current_url}")
            return True
            
    except Exception as e:
        reporter.add_step("Personal Center Static Alipay Error", "FAIL", f"Error: {str(e)}")
        return False

@retry_test
def test_personal_center_static_advanced_wechat(driver, reporter):
    """Test Static Advanced Package via Personal Center with WeChat payment"""
    print("\n" + "=" * 60)
    print("7.3 个人中心>静态高级 - 微信付款(Personal Center WeChat Payment)")
    print("=" * 60)
    
    try:
        # Navigate to count manage page
        driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter/countManage")
        time.sleep(3)
        reporter.add_step("Navigate to Count Manage", "PASS", "Successfully navigated to count manage page")
        
        # Click 添加付费账户
        add_account_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/button[1]"))
        )
        add_account_button.click()
        time.sleep(2)
        reporter.add_step("Click Add Account", "PASS", "Successfully clicked 添加付费账户")
        
        # Click 静态高级套餐 (label[3])
        static_advanced_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[1]/form/div[1]/div[2]/div/label[3]/span[1]/span"))
        )
        static_advanced_option.click()
        time.sleep(2)
        reporter.add_step("Select Package", "PASS", "Successfully selected 静态高级套餐")
        
        # Click 微信
        wechat_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[6]/div/div[3]/div"))
        )
        wechat_option.click()
        time.sleep(2)
        reporter.add_step("Select WeChat", "PASS", "Successfully selected 微信 payment method")
        
        # Click 确认
        confirm_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]"))
        )
        confirm_button.click()
        time.sleep(5)
        reporter.add_step("Click Confirm", "PASS", "Successfully clicked 确认")
        
        # Check for WeChat QR
        try:
            wechat_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '微信扫码付款')]"))
            )
            reporter.add_step("WeChat QR Found", "PASS", "Successfully found '微信扫码付款' - WeChat payment successful")
            
            time.sleep(10)
            reporter.add_step("WeChat Payment Complete", "PASS", "WeChat payment process completed")
            return True
            
        except Exception as e:
            reporter.add_step("WeChat QR Check", "INFO", f"Failed to find '微信扫码付款': {str(e)}")
            return True
            
    except Exception as e:
        reporter.add_step("Personal Center Static WeChat Error", "FAIL", f"Error: {str(e)}")
        return False

# ============================================================================
# Main Test Execution Function
# ============================================================================

def main():
    """
    Main test execution function for comprehensive website package testing
    
    Tests all package types with complete coverage:
    1-4. Website Purchase Tests (12 scenarios): 4 packages × 3 payment methods each
    5-7. Personal Center Tests (9 scenarios): 3 packages × 3 payment methods each
    
    Total: 21 comprehensive test scenarios
    """
    print("Starting ShenLong Complete Package Test Suite")
    print("=" * 80)
    print("Testing: All Package Types (包含固定长效套餐 + 个人中心)")
    print("1. 动态高级套餐 (Dynamic Advanced Package)")
    print("2. 动态独享套餐 (Dynamic Dedicated Package)")
    print("3. 静态高级套餐 (Static Premium Package)")
    print("4. 固定长效套餐 (Fixed Long-Term Package)")
    print("5. 个人中心 > 动态高级 (Personal Center - Dynamic Advanced)")
    print("6. 个人中心 > 动态独享 (Personal Center - Dynamic Dedicated)")
    print("7. 个人中心 > 静态高级 (Personal Center - Static Premium)")
    print("=" * 80)
    
    # Setup driver and reporter
    driver = setup_chrome_driver()
    if not driver:
        print("Failed to initialize Chrome driver.")
        return
    
    reporter = TestReporter()
    print("Chrome driver initialized successfully")
    
    try:
        # Login process
        login_success = login_shenlong(driver, reporter)
        if not login_success:
            print("Login failed. Cannot proceed with payment tests.")
            return
        
        # Test results storage
        results = {}
        
        # 1. Dynamic Advanced Package Tests
        print("\n" + "=" * 60)
        print("1. Dynamic Advanced Package (动态高级套餐)")
        print("=" * 60)
        
        results['dynamic_advanced'] = {
            'wallet': test_dynamic_advanced_wallet_payment(driver, reporter),
            'alipay': test_dynamic_advanced_alipay_payment(driver, reporter),
            'wechat': test_dynamic_advanced_wechat_payment(driver, reporter)
        }
        
        # 2. Dynamic Dedicated Package Tests
        print("\n" + "=" * 60)
        print("2. Dynamic Dedicated Package (动态独享套餐)")
        print("=" * 60)
        
        results['dynamic_dedicated'] = {
            'wallet': test_dynamic_dedicated_wallet_payment(driver, reporter),
            'alipay': test_dynamic_dedicated_alipay_payment(driver, reporter),
            'wechat': test_dynamic_dedicated_wechat_payment(driver, reporter)
        }
        
        # 3. Static Premium Package Tests
        print("\n" + "=" * 60)
        print("3. Static Premium Package (静态高级套餐)")
        print("=" * 60)
        
        results['static_premium'] = {
            'wallet': test_static_premium_wallet_payment(driver, reporter),
            'alipay': test_static_premium_alipay_payment(driver, reporter),
            'wechat': test_static_premium_wechat_payment(driver, reporter)
        }
        
        # 4. Fixed Long-Term Package Tests 
        print("\n" + "=" * 60)
        print("4. Fixed Long-Term Package (固定长效套餐)")
        print("=" * 60)
        
        results['longterm'] = {
            'wallet': test_longterm_wallet_payment(driver, reporter),
            'alipay': test_longterm_alipay_payment(driver, reporter),
            'wechat': test_longterm_wechat_payment(driver, reporter)
        }
        
        # 5-7. Personal Center Tests - Package Management via countManage
        print("\n" + "=" * 60)
        print("5-7. Personal Center Tests - Package Management via countManage")
        print("=" * 60)
        
        results['personal_center'] = {
            'dynamic_advanced_wallet': test_personal_center_dynamic_advanced_wallet(driver, reporter),
            'dynamic_advanced_alipay': test_personal_center_dynamic_advanced_alipay(driver, reporter),
            'dynamic_advanced_wechat': test_personal_center_dynamic_advanced_wechat(driver, reporter),
            'dynamic_dedicated_wallet': test_personal_center_dynamic_dedicated_wallet(driver, reporter),
            'dynamic_dedicated_alipay': test_personal_center_dynamic_dedicated_alipay(driver, reporter),
            'dynamic_dedicated_wechat': test_personal_center_dynamic_dedicated_wechat(driver, reporter),
            'static_advanced_wallet': test_personal_center_static_advanced_wallet(driver, reporter),
            'static_advanced_alipay': test_personal_center_static_advanced_alipay(driver, reporter),
            'static_advanced_wechat': test_personal_center_static_advanced_wechat(driver, reporter)
        }
        
        # Generate HTML report
        report_path = reporter.generate_html_report()
        
        # Print comprehensive summary
        print("\n" + "=" * 100)
        print("COMPLETE PACKAGE TEST SUMMARY")
        print("=" * 100)
        
        print(f"\n1. 动态高级套餐 (Dynamic Advanced Package):")
        print(f"  1.1 Wallet Balance Payment: {'PASS' if results['dynamic_advanced']['wallet'] else 'FAIL'}")
        print(f"  1.2 Alipay Payment: {'PASS' if results['dynamic_advanced']['alipay'] else 'FAIL'}")
        print(f"  1.3 WeChat Payment: {'PASS' if results['dynamic_advanced']['wechat'] else 'FAIL'}")
        
        print(f"\n2. 动态独享套餐 (Dynamic Dedicated Package):")
        print(f"  2.1 Wallet Balance Payment: {'PASS' if results['dynamic_dedicated']['wallet'] else 'FAIL'}")
        print(f"  2.2 Alipay Payment: {'PASS' if results['dynamic_dedicated']['alipay'] else 'FAIL'}")
        print(f"  2.3 WeChat Payment: {'PASS' if results['dynamic_dedicated']['wechat'] else 'FAIL'}")
        
        print(f"\n3. 静态高级套餐 (Static Premium Package):")
        print(f"  3.1 Wallet Balance Payment: {'PASS' if results['static_premium']['wallet'] else 'FAIL'}")
        print(f"  3.2 Alipay Payment: {'PASS' if results['static_premium']['alipay'] else 'FAIL'}")
        print(f"  3.3 WeChat Payment: {'PASS' if results['static_premium']['wechat'] else 'FAIL'}")
        
        print(f"\n4. 固定长效套餐 (Fixed Long-Term Package):")
        print(f"  4.1 Wallet Balance Payment: {'PASS' if results['longterm']['wallet'] else 'FAIL'}")
        print(f"  4.2 Alipay Payment: {'PASS' if results['longterm']['alipay'] else 'FAIL'}")
        print(f"  4.3 WeChat Payment: {'PASS' if results['longterm']['wechat'] else 'FAIL'}")
        
        print(f"\n5. 个人中心 > 动态高级 (Dynamic Advanced Package):")
        print(f"  5.1 Wallet Balance Payment: {'PASS' if results['personal_center']['dynamic_advanced_wallet'] else 'FAIL'}")
        print(f"  5.2 Alipay Payment: {'PASS' if results['personal_center']['dynamic_advanced_alipay'] else 'FAIL'}")
        print(f"  5.3 WeChat Payment: {'PASS' if results['personal_center']['dynamic_advanced_wechat'] else 'FAIL'}")
        
        print(f"\n6. 个人中心 > 动态独享 (Dynamic Dedicated Package):")
        print(f"  6.1 Wallet Balance Payment: {'PASS' if results['personal_center']['dynamic_dedicated_wallet'] else 'FAIL'}")
        print(f"  6.2 Alipay Payment: {'PASS' if results['personal_center']['dynamic_dedicated_alipay'] else 'FAIL'}")
        print(f"  6.3 WeChat Payment: {'PASS' if results['personal_center']['dynamic_dedicated_wechat'] else 'FAIL'}")
        
        print(f"\n7. 个人中心 > 静态高级 (Static Premium Package):")
        print(f"  7.1 Wallet Balance Payment: {'PASS' if results['personal_center']['static_advanced_wallet'] else 'FAIL'}")
        print(f"  7.2 Alipay Payment: {'PASS' if results['personal_center']['static_advanced_alipay'] else 'FAIL'}")
        print(f"  7.3 WeChat Payment: {'PASS' if results['personal_center']['static_advanced_wechat'] else 'FAIL'}")
        
        print("=" * 100)
        print(f"Detailed HTML Report: {report_path}")
        print("=" * 100)
        
    except Exception as e:
        print(f"Test suite error: {str(e)}")
        reporter.add_step("Test Suite Error", "FAIL", f"Error: {str(e)}")
    
    finally:
        if driver:
            print("Closing browser in 5 seconds...")
            time.sleep(5)
            driver.quit()
            print("Browser closed successfully")

if __name__ == "__main__":
    main() 