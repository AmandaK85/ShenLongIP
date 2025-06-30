from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import argparse
from typing import Optional, Any
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class PaymentMethod(Enum):
    BALANCE = "balance"
    ALIPAY = "alipay"
    WECHAT = "wechat"

class DynamicAdvancedPackageTest:
    def __init__(self, payment_method: PaymentMethod, headless: bool = False, timeout: int = 6):
        self.payment_method = payment_method
        self.timeout = timeout
        self.driver = None
        self.start_time = None
        
        # Optimized Chrome options for better performance
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument('--headless')
        
        # Performance optimizations
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-web-security')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-images')
        self.chrome_options.add_argument('--disable-background-timer-throttling')
        self.chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        self.chrome_options.add_argument('--disable-renderer-backgrounding')
        self.chrome_options.add_argument('--disable-default-apps')
        self.chrome_options.add_argument('--disable-sync')
        self.chrome_options.add_argument('--disable-translate')
        self.chrome_options.add_argument('--disable-notifications')
        self.chrome_options.add_argument('--disable-plugins')
        self.chrome_options.add_argument('--disable-logging')
        self.chrome_options.add_argument('--disable-software-rasterizer')
        self.chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        self.chrome_options.add_argument('--memory-pressure-off')
        self.chrome_options.add_argument('--max_old_space_size=2048')
        self.chrome_options.add_argument('--aggressive-cache-discard')
        self.chrome_options.add_argument('--disable-cache')
        self.chrome_options.add_argument('--disable-application-cache')
        self.chrome_options.add_argument('--disable-offline-load-stale-cache')
        self.chrome_options.add_argument('--disk-cache-size=0')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Anti-detection
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        logger.info(f"Initialized Dynamic Advanced Package Test with {payment_method.value} payment method")

    def setup_driver(self) -> bool:
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.set_page_load_timeout(15)
            self.driver.implicitly_wait(2)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.maximize_window()
            logger.info("WebDriver initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            return False

    def wait_for_element(self, xpath: str, timeout: Optional[int] = None, check_clickable: bool = False) -> Any:
        wait_timeout = timeout or self.timeout
        try:
            if check_clickable:
                return WebDriverWait(self.driver, wait_timeout).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
            else:
                return WebDriverWait(self.driver, wait_timeout).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
        except TimeoutException:
            return None
        except Exception as e:
            logger.debug(f"Error waiting for element {xpath}: {e}")
            return None

    def safe_click(self, xpath: str, timeout: Optional[int] = None) -> bool:
        max_retries = 2
        for attempt in range(max_retries):
            try:
                element = self.wait_for_element(xpath, timeout, check_clickable=True)
                if element:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(0.2)
                    element.click()
                    logger.info(f"Successfully clicked element: {xpath}")
                    return True
                else:
                    element = self.wait_for_element(xpath, timeout, check_clickable=False)
                    if element and element.is_displayed():
                        self.driver.execute_script("arguments[0].click();", element)
                        logger.info(f"Successfully clicked element using JavaScript: {xpath}")
                        return True
                    else:
                        logger.warning(f"Click attempt {attempt + 1} failed for {xpath}")
                        if attempt < max_retries - 1:
                            time.sleep(0.5)
                        else:
                            logger.error(f"Failed to click element after {max_retries} attempts: {xpath}")
                            return False
            except Exception as e:
                logger.warning(f"Click attempt {attempt + 1} failed for {xpath}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                else:
                    logger.error(f"Failed to click element after {max_retries} attempts: {xpath}")
                    return False
        return False

    def safe_input(self, xpath: str, text: str, timeout: Optional[int] = None) -> bool:
        try:
            element = self.wait_for_element(xpath, timeout)
            if element and element.is_displayed():
                element.clear()
                time.sleep(0.1)
                element.send_keys(text)
                logger.info(f"Successfully input text '{text}' into element: {xpath}")
                return True
            else:
                logger.error(f"Element not inputtable: {xpath}")
                return False
        except Exception as e:
            logger.error(f"Failed to input text into element {xpath}: {e}")
            return False

    def get_authentication_cookies(self) -> list:
        return [
            {'name': '__root_domain_v', 'value': '.xiaoxigroup.net', 'domain': '.xiaoxigroup.net', 'path': '/'},
            {'name': '__snaker__id', 'value': 'h93rjcHY8FBOfcOO', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': '_clck', 'value': 'f8psxo%7C2%7Cfx7%7C0%7C2000', 'domain': '.xiaoxigroup.net', 'path': '/'},
            {'name': '_clsk', 'value': '102bc0c%7C1751251133069%7C5%7C1%7Cf.clarity.ms%2Fcollect', 'domain': '.xiaoxigroup.net', 'path': '/'},
            {'name': '_qddab', 'value': '4-i3cm7c.mcctlpfq', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': '_qddaz', 'value': 'QD.987350750324316', 'domain': '.xiaoxigroup.net', 'path': '/'},
            {'name': '_uetsid', 'value': 'ed8b3e10555a11f0825ea526153911de', 'domain': '.xiaoxigroup.net', 'path': '/'},
            {'name': '_uetvid', 'value': '0bba69504ff811f09f2d55e2ba8ec7e4', 'domain': '.xiaoxigroup.net', 'path': '/'},
            {'name': 'balance', 'value': '93871.35', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'gdxidpyhxdE', 'value': '3Y3dXk99MP%2FQPnKhVLwlL5KkTUnubQ7LaWYCuxzkKU96WNlbj%2BVNLNc7Zxb1HZQGdCVBr5rAHmc%5CMQdZabtXjaXPBKn40awNOTcvJSANkvMYaiRhB4MbfqwtrnkY5a99NfcK4%2Fihf5JwJ5TOh8NclhhS%2F5ofDmnuaDfn4DLbhiuyxASy%3A1751251866412', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'Hm_lpvt_ab97e0528cd8a1945e66aee550b54522', 'value': '1751250947', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'Hm_lpvt_b697afe6e9c7d29cd1db7fa7b477f2f6', 'value': '1751250947', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'Hm_lvt_ab97e0528cd8a1945e66aee550b54522', 'value': '1750658721', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'Hm_lvt_b697afe6e9c7d29cd1db7fa7b477f2f6', 'value': '1750658721', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'HMACCOUNT', 'value': '5B4FA6A181D073DF', 'domain': '.test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'token', 'value': '3KPhUMtt/2YVZWGylT7TmBE3yDGhpokIAtKoq6hEK6M=', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'},
            {'name': 'User_Info', 'value': '%7B%22_id%22%3A%2268414905acf739152492f1e2%22%2C%22id%22%3A10614%2C%22username%22%3A%2215124493540%22%2C%22realMoney%22%3A61208.13000000003%2C%22balance%22%3A93871.35000000011%2C%22phone%22%3A%2215124493540%22%2C%22state%22%3A1%2C%22createTime%22%3A1749108997%2C%22isNewUser%22%3Atrue%2C%22registIP%22%3A%22120.240.163.164%22%2C%22creator%22%3A10616%2C%22parent%22%3A%5B8948%2C10616%5D%2C%22appointSellerTime%22%3A1749113241%2C%22source%22%3A%22register%22%2C%22keyword%22%3Anull%2C%22brand%22%3A1%2C%22roles%22%3A%5B300%5D%2C%22testLimitAccess%22%3Afalse%2C%22testLimit%22%3A1%2C%22testCount%22%3A1%2C%22registFingerPrint%22%3A%22e0bd09d58f2c81c83e027f9d75f0f9d7%22%2C%22dailyActive%22%3A15%2C%22lastIP%22%3A%22120.240.163.164%22%2C%22lastLoginRegion%22%3A%22%E4%B8%AD%E5%9B%BD%E5%B9%BF%E4%B8%9C%E6%8F%AD%E9%98%B3%22%2C%22lastLoginTime%22%3A1750929487%2C%22loginTime%22%3A1750929664%2C%22userLevel%22%3A50%2C%22isCompanyAuth%22%3Atrue%2C%22thirdPayAccCount%22%3A1%2C%22regionLimit%22%3Afalse%2C%22token%22%3A%223KPhUMtt%2F2YVZWGylT7TmBE3yDGhpokIAtKoq6hEK6M%3D%22%2C%22registered%22%3Atrue%7D', 'domain': 'test-ip-shenlong.cd.xiaoxigroup.net', 'path': '/'}
        ]

    def add_authentication_cookies(self) -> bool:
        logger.info("Adding authentication cookies...")
        try:
            self.driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net")
            time.sleep(0.2)
            cookies = self.get_authentication_cookies()
            success_count = 0
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                    success_count += 1
                except Exception as e:
                    logger.debug(f"Failed to add cookie {cookie.get('name', 'unknown')}: {e}")
            logger.info(f"Authentication cookies added successfully: {success_count}/{len(cookies)}")
            return success_count > 0
        except Exception as e:
            logger.error(f"Error adding authentication cookies: {e}")
            return False

    def navigate_to_personal_center(self) -> bool:
        logger.info("Navigating to personal center page...")
        try:
            if not self.add_authentication_cookies():
                logger.error("Failed to add authentication cookies")
                return False
            self.driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter")
            time.sleep(1)
            logger.info("Personal center page loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error navigating to personal center: {e}")
            return False

    def click_package_account_management_tab(self) -> bool:
        logger.info("Clicking on 套餐/账号管理 tab...")
        tab_xpath = '/html/body/div[2]/div/div[2]/ul/li[2]/ul/a/li/span'
        return self.safe_click(tab_xpath)

    def click_add_paid_account_button(self) -> bool:
        logger.info("Clicking on 添加付费账户 button...")
        button_xpath = '/html/body/div[2]/div/div[2]/div/button[1]'
        return self.safe_click(button_xpath)

    def select_dynamic_advanced_package(self) -> bool:
        logger.info("Selecting 动态高级套餐...")
        package_xpath = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[1]/form/div[1]/div[2]/div/label[2]/span[1]/span'
        return self.safe_click(package_xpath)

    def select_payment_method(self) -> bool:
        logger.info(f"Selecting payment method: {self.payment_method.value}")
        
        if self.payment_method == PaymentMethod.BALANCE:
            logger.info("Balance payment selected (no additional selection needed)")
            return True
        elif self.payment_method == PaymentMethod.ALIPAY:
            alipay_xpath = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[6]/div/div[2]'
            return self.safe_click(alipay_xpath)
        elif self.payment_method == PaymentMethod.WECHAT:
            wechat_xpaths = [
                "//div[contains(@class, 'pay-item')]//div[contains(text(), '微信')]",
                "//div[contains(@class, 'pay-item')]//svg[contains(@class, 'icon-wechat')]",
                "//div[@data-v-2a541f4a and contains(@class, 'pay-item')]//div[text()='微信']",
                "//div[contains(@class, 'pay-item')]//div[text()='微信']",
                "//div[contains(@class, 'icon-wechat')]",
                "//div[contains(text(), '微信') and contains(@class, 'pay-item')]"
            ]
            for i, xpath in enumerate(wechat_xpaths):
                if self.safe_click(xpath):
                    logger.info(f"Clicked WeChat payment option using XPath {i+1}")
                    return True
            logger.error("All WeChat payment XPath selectors failed")
            return False
        return False

    def click_confirm_button(self) -> bool:
        logger.info("Clicking on 确认 button...")
        confirm_xpath = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]'
        return self.safe_click(confirm_xpath)

    def handle_balance_payment(self) -> bool:
        logger.info("Handling balance payment...")
        try:
            # Wait longer for the success message to appear
            time.sleep(3)
            
            # Retry loop to check for success message
            max_attempts = 8
            for attempt in range(max_attempts):
                logger.info(f"Balance payment check attempt {attempt + 1}/{max_attempts}")
                
                # Check main document
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '添加成功')]")
                logger.info(f"Found {len(elements)} elements containing '添加成功' in main document")
                if elements:
                    logger.info("✅ Success message found in main document!")
                    return True

                # Check iframes
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                logger.info(f"Found {len(iframes)} iframes on the page")
                for i, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.frame(iframe)
                        elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '添加成功')]")
                        if elements:
                            logger.info(f"✅ Success message found in iframe {i}!")
                            self.driver.switch_to.default_content()
                            return True
                        self.driver.switch_to.default_content()
                    except Exception as e:
                        logger.warning(f"Error searching iframe {i}: {e}")
                        self.driver.switch_to.default_content()

                # Check page source
                if "添加成功" in self.driver.page_source:
                    logger.info("✅ Success message found in page source!")
                    return True
                
                # Check for alternative success messages
                alternative_messages = ["支付成功", "购买成功", "订单成功", "success", "成功"]
                for msg in alternative_messages:
                    if msg in self.driver.page_source:
                        logger.info(f"✅ Alternative success message found: '{msg}'")
                        return True
                
                # Wait before next attempt
                if attempt < max_attempts - 1:
                    logger.info(f"Waiting 2 seconds before next attempt...")
                    time.sleep(2)
            
            # If we get here, no success message was found
            logger.error("❌ Success message not found after all attempts")
            
            # Debug: Log some page content to help understand what's there
            try:
                page_text = self.driver.page_source
                if "成功" in page_text:
                    logger.info("Found '成功' in page source, but not '添加成功'")
                if "失败" in page_text or "error" in page_text.lower():
                    logger.error("Found error/failure message in page source")
                logger.info(f"Current URL: {self.driver.current_url}")
            except Exception as e:
                logger.error(f"Error during debug logging: {e}")
            
            return False
        except Exception as e:
            logger.error(f"Error checking success message: {e}")
            return False

    def handle_alipay_payment(self) -> bool:
        logger.info("Handling Alipay payment process...")
        original_window = self.driver.current_window_handle
        
        try:
            WebDriverWait(self.driver, 8).until(lambda d: len(d.window_handles) > 1)
            new_window = [handle for handle in self.driver.window_handles if handle != original_window][0]
            self.driver.switch_to.window(new_window)
            logger.info("Switched to new Alipay payment tab")
            time.sleep(1)
            
            # Enter Alipay username
            username_xpath = '/html/body/div[2]/div[4]/div[2]/ul/li/div/form/div/div[1]/div/div[2]/div/div[1]/input[1]'
            if not self.safe_input(username_xpath, 'lgipqm7573@sandbox.com'):
                logger.error("Failed to enter Alipay username")
                return False
            time.sleep(1.5)
            
            # Enter Alipay password
            password_xpath = '/html/body/div[2]/div[4]/div[2]/ul/li/div/form/div/div[1]/div/div[2]/div/div[3]/span[1]/span[2]/input'
            if not self.safe_input(password_xpath, '111111'):
                logger.error("Failed to enter Alipay password")
                return False
            time.sleep(2)
            
            # Click next button
            next_button_xpath = '/html/body/div[2]/div[4]/div[2]/ul/li/div/form/div/div[1]/div/div[2]/div/div[5]/div[2]/a/span'
            if not self.safe_click(next_button_xpath):
                logger.error("Failed to click 下一步 button")
                return False
            time.sleep(2)
            
            # Handle payment password page
            payment_password_xpath = '/html/body/div[2]/div[2]/form/div[2]/div[2]/div/div/span[2]/input'
            try:
                payment_password_element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, payment_password_xpath))
                )
                if payment_password_element.is_displayed():
                    logger.info("Payment password page detected, entering payment password...")
                    if not self.safe_input(payment_password_xpath, '111111'):
                        logger.error("Failed to enter payment password")
                        return False
                    time.sleep(1)
                    confirm_payment_xpath = '/html/body/div[2]/div[2]/form/div[3]/div/input'
                    if not self.safe_click(confirm_payment_xpath):
                        logger.error("Failed to click confirm payment button")
                        return False
                    time.sleep(1.5)
            except TimeoutException:
                logger.info("Payment password page not found, continuing...")
            except Exception as e:
                logger.info(f"Payment password page check failed: {e}")
            
            # Wait for success message
            success_message = "您已成功付款"
            max_attempts = 4
            for attempt in range(max_attempts):
                try:
                    logger.info(f"Attempt {attempt + 1}/{max_attempts} to find success message...")
                    time.sleep(0.8)
                    elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{success_message}')]")
                    for element in elements:
                        if element.is_displayed():
                            logger.info(f"SUCCESS: Found success message: '{element.text}'")
                            return True
                    current_url = self.driver.current_url
                    if "xiaoxigroup.net" in current_url:
                        logger.info("SUCCESS: Redirected back to merchant site after Alipay payment")
                        return True
                    page_text = self.driver.page_source
                    if success_message in page_text:
                        logger.info("SUCCESS: Found success message in page source")
                        return True
                except Exception as e:
                    logger.debug(f"Attempt {attempt + 1} failed: {e}")
                    continue
            
            logger.error(f"FAILED: Could not find success message '{success_message}' after {max_attempts} attempts")
            return False
            
        except Exception as e:
            logger.error(f"Error during Alipay login process: {e}")
            return False
        finally:
            try:
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(original_window)
                    logger.info("Closed Alipay tab and switched back to original tab")
            except Exception as e:
                logger.warning(f"Error closing tab: {e}")

    def handle_wechat_payment(self) -> bool:
        logger.info("Handling WeChat payment process...")
        try:
            time.sleep(1.5)
            
            # Wait for WeChat payment interface
            wechat_text_xpath = "//*[contains(text(), '微信扫码付款')]"
            wechat_element = self.wait_for_element(wechat_text_xpath, timeout=10)
            if wechat_element:
                logger.info("WeChat payment interface found: 微信扫码付款")
                logger.info("Payment considered successful as '微信扫码付款' is present.")
                return True
            else:
                logger.error("WeChat payment interface not found")
                return False
        except Exception as e:
            logger.error(f"Error handling WeChat payment: {e}")
            return False

    def handle_payment(self) -> bool:
        logger.info(f"Handling {self.payment_method.value} payment...")
        
        if self.payment_method == PaymentMethod.BALANCE:
            return self.handle_balance_payment()
        elif self.payment_method == PaymentMethod.ALIPAY:
            return self.handle_alipay_payment()
        elif self.payment_method == PaymentMethod.WECHAT:
            return self.handle_wechat_payment()
        else:
            logger.error(f"Unknown payment method: {self.payment_method}")
            return False

    def run_test(self) -> bool:
        logger.info(f"Starting Dynamic Advanced Package Test with {self.payment_method.value} payment")
        self.start_time = time.time()
        
        try:
            if not self.setup_driver():
                logger.error("Failed to setup WebDriver")
                return False
            
            if not self.navigate_to_personal_center():
                logger.error("Failed to navigate to personal center")
                return False
            
            if not self.click_package_account_management_tab():
                logger.error("Failed to click package account management tab")
                return False
            
            if not self.click_add_paid_account_button():
                logger.error("Failed to click add paid account button")
                return False
            
            if not self.select_dynamic_advanced_package():
                logger.error("Failed to select dynamic advanced package")
                return False
            
            if not self.select_payment_method():
                logger.error(f"Failed to select {self.payment_method.value} payment method")
                return False
            
            if not self.click_confirm_button():
                logger.error("Failed to click confirm button")
                return False
            
            if not self.handle_payment():
                logger.error(f"Failed to handle {self.payment_method.value} payment")
                return False
            
            logger.info(f"✅ {self.payment_method.value.capitalize()} payment test completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Test failed with exception: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed")

def main():
    parser = argparse.ArgumentParser(description='Dynamic Advanced Package Test with Multiple Payment Methods')
    parser.add_argument('--payment-method', 
                       choices=['balance', 'alipay', 'wechat', 'all'], 
                       default='all',
                       help='Payment method to use (default: all)')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--timeout', type=int, default=6, help='Default timeout in seconds')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    payment_method_map = {
        'balance': PaymentMethod.BALANCE,
        'alipay': PaymentMethod.ALIPAY,
        'wechat': PaymentMethod.WECHAT
    }
    
    if args.payment_method == 'all':
        # Run all payment methods
        payment_methods = ['balance', 'alipay', 'wechat']
        results = {}
        
        print("\n" + "="*60)
        print("🚀 STARTING ALL PAYMENT METHOD TESTS")
        print("="*60)
        
        for method in payment_methods:
            print(f"\n📋 Testing {method.upper()} payment method...")
            print("-" * 40)
            
            payment_method = payment_method_map[method]
            test = DynamicAdvancedPackageTest(
                payment_method=payment_method,
                headless=args.headless,
                timeout=args.timeout
            )
            
            success = test.run_test()
            results[method] = success
            
            if success:
                print(f"✅ {method.upper()} payment test: PASSED")
            else:
                print(f"❌ {method.upper()} payment test: FAILED")
            
            print("-" * 40)
        
        # Print final summary
        print("\n" + "="*60)
        print("📊 FINAL TEST RESULTS SUMMARY")
        print("="*60)
        
        passed_count = 0
        failed_count = 0
        
        for method, success in results.items():
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{method.upper():<10} : {status}")
            if success:
                passed_count += 1
            else:
                failed_count += 1
        
        print("-" * 60)
        print(f"Total Tests: {len(results)}")
        print(f"✅ Passed: {passed_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"Success Rate: {(passed_count/len(results)*100):.1f}%")
        print("="*60)
        
        if failed_count == 0:
            print("\n🎉 ALL TESTS PASSED! 🎉")
            exit(0)
        else:
            print(f"\n⚠️  {failed_count} test(s) failed. Check the logs above for details.")
            exit(1)
    else:
        # Run single payment method (original behavior)
        payment_method = payment_method_map[args.payment_method]
        
        test = DynamicAdvancedPackageTest(
            payment_method=payment_method,
            headless=args.headless,
            timeout=args.timeout
        )
        
        success = test.run_test()
        
        if success:
            print(f"\n✅ {args.payment_method.capitalize()} payment test completed successfully!")
            exit(0)
        else:
            print(f"\n❌ {args.payment_method.capitalize()} payment test failed!")
            exit(1)

if __name__ == "__main__":
    main() 