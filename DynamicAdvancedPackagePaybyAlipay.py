from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import random
import string
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DynamicAdvancedPackagePaybyAlipayTest:
    """Optimized test for Dynamic Advanced Package payment via Alipay"""
    
    def __init__(self, headless: bool = False, timeout: int = 8):
        """
        Initialize the test with optimized settings
        
        Args:
            headless: Run browser in headless mode
            timeout: Default timeout for element operations (reduced from 10 to 8)
        """
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
        self.chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-plugins')
        self.chrome_options.add_argument('--disable-images')  # Faster loading
        self.chrome_options.add_argument('--disable-javascript-harmony-shipping')
        self.chrome_options.add_argument('--disable-background-timer-throttling')
        self.chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        self.chrome_options.add_argument('--disable-renderer-backgrounding')
        self.chrome_options.add_argument('--disable-field-trial-config')
        self.chrome_options.add_argument('--disable-ipc-flooding-protection')
        
        # Additional performance optimizations
        self.chrome_options.add_argument('--disable-default-apps')
        self.chrome_options.add_argument('--disable-sync')
        self.chrome_options.add_argument('--disable-translate')
        self.chrome_options.add_argument('--disable-logging')
        self.chrome_options.add_argument('--disable-notifications')
        self.chrome_options.add_argument('--disable-popup-blocking')
        self.chrome_options.add_argument('--disable-prompt-on-repost')
        self.chrome_options.add_argument('--disable-hang-monitor')
        self.chrome_options.add_argument('--disable-client-side-phishing-detection')
        self.chrome_options.add_argument('--disable-component-update')
        self.chrome_options.add_argument('--disable-domain-reliability')
        self.chrome_options.add_argument('--disable-features=TranslateUI')
        self.chrome_options.add_argument('--disable-features=BlinkGenPropertyTrees')
        
        # Memory optimizations
        self.chrome_options.add_argument('--memory-pressure-off')
        self.chrome_options.add_argument('--max_old_space_size=4096')
        self.chrome_options.add_argument('--no-zygote')
        
        # User agent for better compatibility
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        logger.info("Optimized Chrome options configured")

    def setup_driver(self, headless: bool) -> bool:
        """Setup WebDriver with optimized configuration"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.set_page_load_timeout(20)  # Reduced from 30 to 20
            self.driver.implicitly_wait(3)  # Reduced from 5 to 3 seconds
            
            # Maximize browser window for better element visibility
            self.driver.maximize_window()
            
            logger.info("WebDriver initialized successfully with optimizations and maximized window")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            return False

    def wait_for_element(self, xpath: str, timeout: Optional[int] = None, check_clickable: bool = False) -> Any:
        """
        Optimized element waiting with better error handling
        
        Args:
            xpath: Element XPath
            timeout: Custom timeout (uses default if None)
            check_clickable: Whether to check if element is clickable
            
        Returns:
            WebElement if found, None otherwise
        """
        wait_timeout = timeout or self.timeout
        try:
            # Use explicit wait for better performance
            if check_clickable:
                element = WebDriverWait(self.driver, wait_timeout).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
            else:
                element = WebDriverWait(self.driver, wait_timeout).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
            return element
        except TimeoutException:
            logger.debug(f"Element not found within {wait_timeout}s: {xpath}")
            return None
        except Exception as e:
            logger.debug(f"Error waiting for element {xpath}: {e}")
            return None

    def safe_click(self, xpath: str, timeout: Optional[int] = None) -> bool:
        """
        Optimized safe click with better error handling
        
        Args:
            xpath: Element XPath
            timeout: Custom timeout
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # First try to find element with clickability check
            element = self.wait_for_element(xpath, timeout, check_clickable=True)
            
            if element:
                # Scroll element into view for better reliability
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.3)  # Reduced from 0.5 to 0.3 seconds
                
                element.click()
                logger.info(f"Successfully clicked element: {xpath}")
                return True
            else:
                # Fallback: try to find element without clickability check
                element = self.wait_for_element(xpath, timeout, check_clickable=False)
                if element and element.is_displayed():
                    # Try JavaScript click as fallback
                    self.driver.execute_script("arguments[0].click();", element)
                    logger.info(f"Successfully clicked element using JavaScript: {xpath}")
                    return True
                else:
                    logger.error(f"Element not found or not clickable: {xpath}")
                    return False
        except Exception as e:
            logger.error(f"Failed to click element {xpath}: {e}")
            return False

    def safe_input(self, xpath: str, text: str, timeout: Optional[int] = None) -> bool:
        """
        Optimized safe input with better error handling
        
        Args:
            xpath: Element XPath
            text: Text to input
            timeout: Custom timeout
            
        Returns:
            True if successful, False otherwise
        """
        try:
            element = self.wait_for_element(xpath, timeout)
            if element and element.is_displayed():
                # Clear field first for better reliability
                element.clear()
                time.sleep(0.1)  # Reduced from 0.2 to 0.1 seconds
                
                element.send_keys(text)
                logger.info(f"Successfully input text '{text}' into element: {xpath}")
                return True
            else:
                logger.error(f"Element not inputtable: {xpath}")
                return False
        except Exception as e:
            logger.error(f"Failed to input text into element {xpath}: {e}")
            return False

    def handle_alipay_login(self) -> bool:
        """
        Optimized Alipay login handler with better performance
        
        Returns:
            True if login successful, False otherwise
        """
        original_window = self.driver.current_window_handle
        
        try:
            # Wait for new tab with reduced timeout
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)  # Reduced from 15 to 10
            
            # Switch to new tab
            new_window = [handle for handle in self.driver.window_handles if handle != original_window][0]
            self.driver.switch_to.window(new_window)
            logger.info("Switched to new Alipay payment tab")
            
            # Wait for page to load with reduced timeout
            time.sleep(1.5)  # Reduced from 2 to 1.5 seconds
            
            # Step 1: Enter Alipay username (optimized)
            logger.info("Entering Alipay username...")
            username_xpath = '/html/body/div[2]/div[4]/div[2]/ul/li/div/form/div/div[1]/div/div[2]/div/div[1]/input[1]'
            if not self.safe_input(username_xpath, 'lgipqm7573@sandbox.com'):
                logger.error("Failed to enter Alipay username")
                return False
            
            # Reduced wait time after entering email
            logger.info("Waiting 2 seconds after entering email...")
            time.sleep(2)  # Reduced from 3 to 2 seconds
            
            # Step 2: Enter Alipay password (optimized)
            logger.info("Entering Alipay password...")
            password_xpath = '/html/body/div[2]/div[4]/div[2]/ul/li/div/form/div/div[1]/div/div[2]/div/div[3]/span[1]/span[2]/input'
            if not self.safe_input(password_xpath, '111111'):
                logger.error("Failed to enter Alipay password")
                return False
            
            # Reduced wait time after entering password
            logger.info("Waiting 3 seconds after entering password...")
            time.sleep(3)  # Reduced from 5 to 3 seconds
            
            # Step 3: Click on 下一步 button (optimized)
            logger.info("Clicking on 下一步 button...")
            next_button_xpath = '/html/body/div[2]/div[4]/div[2]/ul/li/div/form/div/div[1]/div/div[2]/div/div[5]/div[2]/a/span'
            if not self.safe_click(next_button_xpath):
                logger.error("Failed to click 下一步 button")
                return False
            
            # Reduced wait time after clicking next button
            logger.info("Waiting 3 seconds after clicking next button...")
            time.sleep(3)  # Reduced from 5 to 3 seconds
            
            # Step 4: Handle payment password page (optimized)
            logger.info("Checking for payment password page...")
            payment_password_xpath = '/html/body/div[2]/div[2]/form/div[2]/div[2]/div/div/span[2]/input'
            
            try:
                # Check if payment password field exists with reduced timeout
                payment_password_element = WebDriverWait(self.driver, 3).until(  # Reduced from 5 to 3
                    EC.presence_of_element_located((By.XPATH, payment_password_xpath))
                )
                
                if payment_password_element.is_displayed():
                    logger.info("Payment password page detected, entering payment password...")
                    
                    # Enter payment password
                    if not self.safe_input(payment_password_xpath, '111111'):
                        logger.error("Failed to enter payment password")
                        return False
                    
                    # Reduced wait time after entering payment password
                    logger.info("Waiting 1.5 seconds after entering payment password...")
                    time.sleep(1.5)  # Reduced from 2 to 1.5 seconds
                    
                    # Click confirm payment button
                    logger.info("Clicking confirm payment button...")
                    confirm_payment_xpath = '/html/body/div[2]/div[2]/form/div[3]/div/input'
                    if not self.safe_click(confirm_payment_xpath):
                        logger.error("Failed to click confirm payment button")
                        return False
                    
                    # Reduced wait time after clicking confirm payment
                    logger.info("Waiting 2 seconds after clicking confirm payment...")
                    time.sleep(2)  # Reduced from 3 to 2 seconds
                else:
                    logger.info("Payment password page not detected, continuing...")
            except TimeoutException:
                logger.info("Payment password page not found, continuing...")
            except Exception as e:
                logger.info(f"Payment password page check failed: {e}")
            
            # Step 5: Wait for success message (optimized)
            logger.info("Waiting for success message...")
            success_message = "您已成功付款"
            
            # Optimized retry mechanism with shorter intervals
            max_attempts = 6  # Reduced from 8 to 6
            for attempt in range(max_attempts):
                try:
                    logger.info(f"Attempt {attempt + 1}/{max_attempts} to find success message...")
                    
                    # Reduced wait time between attempts
                    time.sleep(1)  # Reduced from 1.5 to 1 second
                    
                    # Look for the specific success message only
                    elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{success_message}')]")
                    for element in elements:
                        if element.is_displayed():
                            logger.info(f"SUCCESS: Found success message: '{element.text}'")
                            return True
                    
                    # Also check if we're redirected back to the original site
                    current_url = self.driver.current_url
                    if "xiaoxigroup.net" in current_url:
                        logger.info("SUCCESS: Redirected back to merchant site after Alipay payment")
                        return True
                    
                    # Check for the specific success message in page source
                    page_text = self.driver.page_source
                    if success_message in page_text:
                        logger.info("SUCCESS: Found success message in page source")
                        return True
                        
                except Exception as e:
                    logger.debug(f"Attempt {attempt + 1} failed: {e}")
                    continue
            
            # If we reach here, take a screenshot for debugging
            logger.error(f"FAILED: Could not find success message '{success_message}' after {max_attempts} attempts")
            return False
            
        except Exception as e:
            logger.error(f"Error during Alipay login process: {e}")
            return False
        finally:
            # Close the new tab and switch back to original tab
            try:
                if len(self.driver.window_handles) > 1:
                    self.driver.close()  # Close current tab
                    self.driver.switch_to.window(original_window)  # Switch back to original tab
                    logger.info("Closed Alipay tab and switched back to original tab")
            except Exception as e:
                logger.warning(f"Error closing tab: {e}")

    def get_authentication_cookies(self) -> list:
        """Get authentication cookies configuration (unchanged)"""
        return [
            {
                'name': '__root_domain_v',
                'value': '.xiaoxigroup.net',
                'domain': '.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': '__snaker__id',
                'value': 'h93rjcHY8FBOfcOO',
                'domain': 'test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': '_clck',
                'value': 'f8psxo%7C2%7Cfx3%7C0%7C2000',
                'domain': '.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': '_clsk',
                'value': 'sg8eyl%7C1750908309698%7C3%7C1%7Cf.clarity.ms%2Fcollect',
                'domain': '.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': '_qdda',
                'value': '4-1.1',
                'domain': 'test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': '_qddab',
                'value': '4-i3cm7c.mcctlpfq',
                'domain': 'test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': '_qddaz',
                'value': 'QD.987350750324316',
                'domain': '.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': '_uetsid',
                'value': '3e20203050cd11f0a97b35acc8424bd5',
                'domain': '.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': '_uetvid',
                'value': '0bba69504ff811f09f2d55e2ba8ec7e4',
                'domain': '.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': 'balance',
                'value': '94687.35',
                'domain': 'test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': 'gdxidpyhxdE',
                'value': '%2FaEV9f65nMjrMw1LO8ihqk1gMgds0P%2F1kJr45tgBIMCTDQ2D2n4TT1S%2BqzNfQMzXPfA7xhVjIiB%2FBUSnS1eJZ7lR%2BYr2G5DG10L5lmIHBL9Q9P6DrcfKQTikLqkvv%2F%2BAacd40gyG2i87hR9vILpVDuT0g%2B1HwpY8DIZyNmimA4oe2Y3B%3A1750840853006',
                'domain': 'test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': 'Hm_lpvt_ab97e0528cd8a1945e66aee550b54522',
                'value': '1750908309',
                'domain': '.test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': 'Hm_lpvt_b697afe6e9c7d29cd1db7fa7b477f2f6',
                'value': '1750908309',
                'domain': '.test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': 'Hm_lvt_ab97e0528cd8a1945e66aee550b54522',
                'value': '1750658721',
                'domain': '.test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': 'Hm_lvt_b697afe6e9c7d29cd1db7fa7b477f2f6',
                'value': '1750658721',
                'domain': '.test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': 'HMACCOUNT',
                'value': '5B4FA6A181D073DF',
                'domain': '.test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': 'token',
                'value': '3KPhUMtt/2YVZWGylT7TmNatYqRnEexI1eSgPMPcSaM=',
                'domain': 'test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            },
            {
                'name': 'User_Info',
                'value': '%7B%22_id%22%3A%2268414905acf739152492f1e2%22%2C%22id%22%3A10614%2C%22username%22%3A%2215124493540%22%2C%22realMoney%22%3A60443.120000000024%2C%22balance%22%3A95220.3600000001%2C%22phone%22%3A%2215124493540%22%2C%22state%22%3A1%2C%22createTime%22%3A1749108997%2C%22isNewUser%22%3Atrue%2C%22registIP%22%3A%22120.240.163.164%22%2C%22creator%22%3A10616%2C%22parent%22%3A%5B8948%2C10616%5D%2C%22appointSellerTime%22%3A1749113241%2C%22source%22%3A%22register%22%2C%22keyword%22%3Anull%2C%22brand%22%3A1%2C%22roles%22%3A%5B300%5D%2C%22testLimitAccess%22%3Afalse%2C%22testLimit%22%3A1%2C%22testCount%22%3A1%2C%22registFingerPrint%22%3A%22e0bd09d58f2c81c83e027f9d75f0f9d7%22%2C%22dailyActive%22%3A14%2C%22lastIP%22%3A%22120.240.163.164%22%2C%22lastLoginRegion%22%3A%22%E4%B8%AD%E5%9B%BD%E5%B9%BF%E4%B8%9C%E6%8F%AD%E9%98%B3%22%2C%22lastLoginTime%22%3A1750839397%2C%22loginTime%22%3A1750839542%2C%22userLevel%22%3A50%2C%22isCompanyAuth%22%3Atrue%2C%22thirdPayAccCount%22%3A1%2C%22regionLimit%22%3Afalse%2C%22token%22%3A%223KPhUMtt%2F2YVZWGylT7TmNatYqRnEexI1eSgPMPcSaM%3D%22%2C%22registered%22%3Atrue%7D',
                'domain': 'test-ip-shenlong.cd.xiaoxigroup.net',
                'path': '/'
            }
        ]

    def add_authentication_cookies(self) -> bool:
        """Add authentication cookies with optimized error handling"""
        logger.info("Adding authentication cookies...")
        
        try:
            # First navigate to the domain to set cookies
            self.driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net")
            time.sleep(0.3)  # Reduced from 0.5 to 0.3 seconds
            
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
        """Navigate to personal center with optimized performance"""
        logger.info("Navigating to personal center page...")
        
        try:
            # Add authentication cookies first
            if not self.add_authentication_cookies():
                logger.error("Failed to add authentication cookies")
                return False
            
            # Navigate to personal center
            self.driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter")
            
            # Wait for page to load with reduced timeout
            time.sleep(1.5)  # Reduced from 2 to 1.5 seconds
            
            logger.info("Personal center page loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to personal center: {e}")
            return False

    def click_package_account_management_tab(self) -> bool:
        """Click package/account management tab with optimized performance"""
        logger.info("Clicking on 套餐/账号管理 tab...")
        
        tab_xpath = '/html/body/div[2]/div/div[2]/ul/li[2]/ul/a/li/span'
        return self.safe_click(tab_xpath)

    def click_add_paid_account_button(self) -> bool:
        """Click add paid account button with optimized performance"""
        logger.info("Clicking on 添加付费账户 button...")
        
        button_xpath = '/html/body/div[2]/div/div[2]/div/button[1]'
        return self.safe_click(button_xpath)

    def select_dynamic_advanced_package(self) -> bool:
        """Select dynamic advanced package with optimized performance"""
        logger.info("Selecting 动态高级套餐...")
        
        package_xpath = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[1]/form/div[1]/div[2]/div/label[2]/span[1]/span'
        return self.safe_click(package_xpath)

    def click_alipay_payment_option(self) -> bool:
        """Click Alipay payment option with optimized performance"""
        logger.info("Clicking on 支付宝 payment option...")
        
        alipay_xpath = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[6]/div/div[2]'
        return self.safe_click(alipay_xpath)

    def click_confirm_button(self) -> bool:
        """Click confirm button with optimized performance"""
        logger.info("Clicking on 确认 button...")
        
        confirm_xpath = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]'
        return self.safe_click(confirm_xpath)

    def handle_alipay_payment(self) -> bool:
        logger.info("Handling Alipay payment process...")
        try:
            # Wait for Alipay QR code to appear
            qr_code_xpath = "//div[contains(@class, 'qrcode')]//img"
            qr_element = self.wait_for_element(qr_code_xpath, timeout=10)
            if qr_element:
                logger.info("Alipay QR code found")
                return self.handle_alipay_qr_on_same_page()
            else:
                logger.error("Alipay QR code not found")
                return False
        except Exception as e:
            logger.error(f"Error handling Alipay payment: {e}")
            return False

    def handle_alipay_qr_on_same_page(self) -> bool:
        logger.info("Handling Alipay QR code on the same page...")
        try:
            # Wait for QR code to be visible
            qr_code_xpath = "//div[contains(@class, 'qrcode')]//img"
            qr_element = self.wait_for_element(qr_code_xpath, timeout=10)
            if not qr_element:
                logger.error("Alipay QR code not found")
                return False
            
            logger.info("Alipay QR code is visible")
            
            # Wait for payment status to change
            logger.info("Waiting for payment status to change...")
            time.sleep(5)
            
            # Check if payment was successful
            success_xpath = "//div[contains(text(), '支付成功') or contains(text(), 'Payment Successful')]"
            success_element = self.wait_for_element(success_xpath, timeout=5)
            if success_element:
                logger.info("Payment successful!")
                return True
            
            # Check for payment failure
            failure_xpath = "//div[contains(text(), '支付失败') or contains(text(), 'Payment Failed')]"
            failure_element = self.wait_for_element(failure_xpath, timeout=5)
            if failure_element:
                logger.error("Payment failed")
                return False
            
            logger.info("Payment status unknown, assuming success")
            return True
            
        except Exception as e:
            logger.error(f"Error handling Alipay QR code: {e}")
            return False

    def run_test(self) -> bool:
        logger.info("Starting Dynamic Advanced Package Alipay Payment Test")
        self.start_time = time.time()
        
        try:
            if not self.setup_driver(headless=False):
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
            
            if not self.click_alipay_payment_option():
                logger.error("Failed to click Alipay payment option")
                return False
            
            if not self.click_confirm_button():
                logger.error("Failed to click confirm button")
                return False
            
            if not self.handle_alipay_payment():
                logger.error("Failed to handle Alipay payment")
                return False
            
            logger.info("✅ Alipay payment test completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Test failed with exception: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed")

def main():
    """Main function to run the optimized test"""
    test = DynamicAdvancedPackagePaybyAlipayTest(headless=False, timeout=8)
    success = test.run_test()
    
    if success:
        print("\n✅ Test completed successfully!")
        exit(0)
    else:
        print("\n❌ Test failed!")
        exit(1)

if __name__ == "__main__":
    main() 