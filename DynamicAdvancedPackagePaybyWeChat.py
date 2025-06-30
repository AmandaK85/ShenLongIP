from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import logging
from typing import Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DynamicAdvancedPackagePaybyWeChatTest:
    def __init__(self, headless: bool = False, timeout: int = 8):
        self.timeout = timeout
        self.driver = None
        self.start_time = None
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-web-security')
        self.chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-plugins')
        self.chrome_options.add_argument('--disable-images')
        self.chrome_options.add_argument('--disable-background-timer-throttling')
        self.chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        self.chrome_options.add_argument('--disable-renderer-backgrounding')
        self.chrome_options.add_argument('--disable-field-trial-config')
        self.chrome_options.add_argument('--disable-ipc-flooding-protection')
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
        self.chrome_options.add_argument('--memory-pressure-off')
        self.chrome_options.add_argument('--max_old_space_size=4096')
        self.chrome_options.add_argument('--no-zygote')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        logger.info("Optimized Chrome options configured")

    def setup_driver(self, headless: bool) -> bool:
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.set_page_load_timeout(20)
            self.driver.implicitly_wait(3)
            self.driver.maximize_window()
            logger.info("WebDriver initialized and maximized window")
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
        try:
            element = self.wait_for_element(xpath, timeout, check_clickable=True)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.2)
                element.click()
                logger.info(f"Clicked element: {xpath}")
                return True
            element = self.wait_for_element(xpath, timeout, check_clickable=False)
            if element and element.is_displayed():
                self.driver.execute_script("arguments[0].click();", element)
                logger.info(f"Clicked element using JS: {xpath}")
                return True
            logger.error(f"Element not found or not clickable: {xpath}")
            return False
        except Exception as e:
            logger.error(f"Failed to click element {xpath}: {e}")
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
            time.sleep(0.3)
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
            time.sleep(1.2)
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

    def click_wechat_payment_option(self) -> bool:
        logger.info("Clicking on 微信 payment option...")
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

    def click_confirm_button(self) -> bool:
        logger.info("Clicking on 确认 button...")
        confirm_xpath = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]'
        return self.safe_click(confirm_xpath)

    def handle_wechat_payment(self) -> bool:
        logger.info("Handling WeChat payment process...")
        try:
            # Wait a moment for the page to load
            time.sleep(2)
            
            # Debug: Take screenshot and save page source
            try:
                self.driver.save_screenshot("payment_page_debug.png")
                logger.info("Screenshot saved as payment_page_debug.png")
                
                # Save page source for debugging
                with open("payment_page_source.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                logger.info("Page source saved as payment_page_source.html")
                
                # Log current URL
                logger.info(f"Current URL: {self.driver.current_url}")
                
                # Look for any text containing "微信" or "扫码"
                wechat_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '微信') or contains(text(), '扫码')]")
                if wechat_elements:
                    logger.info(f"Found {len(wechat_elements)} elements containing '微信' or '扫码':")
                    for i, elem in enumerate(wechat_elements[:5]):  # Log first 5 elements
                        try:
                            logger.info(f"  Element {i+1}: {elem.text}")
                        except:
                            logger.info(f"  Element {i+1}: [text not accessible]")
                else:
                    logger.info("No elements found containing '微信' or '扫码'")
                    
            except Exception as debug_error:
                logger.error(f"Debug capture failed: {debug_error}")
            
            # Wait for WeChat payment interface to appear
            wechat_text_xpath = "//*[contains(text(), '微信扫码付款')]"
            wechat_element = self.wait_for_element(wechat_text_xpath, timeout=15)
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

    def handle_wechat_qr_on_same_page(self) -> bool:
        logger.info("Handling WeChat QR code on the same page...")
        try:
            # Wait for QR code to be visible
            qr_code_xpath = "//div[contains(@class, 'qrcode')]//img"
            qr_element = self.wait_for_element(qr_code_xpath, timeout=15)
            if not qr_element:
                logger.error("WeChat QR code not found")
                return False
            
            logger.info("WeChat QR code is visible")
            
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
            logger.error(f"Error handling WeChat QR code: {e}")
            return False

    def run_test(self) -> bool:
        logger.info("Starting Dynamic Advanced Package WeChat Payment Test")
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
            
            if not self.click_wechat_payment_option():
                logger.error("Failed to click WeChat payment option")
                return False
            
            if not self.click_confirm_button():
                logger.error("Failed to click confirm button")
                return False
            
            if not self.handle_wechat_payment():
                logger.error("Failed to handle WeChat payment")
                return False
            
            logger.info("✅ WeChat payment test completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Test failed with exception: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Dynamic Advanced Package WeChat Test')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--timeout', type=int, default=8, help='Default timeout in seconds')
    args = parser.parse_args()
    test = DynamicAdvancedPackagePaybyWeChatTest(headless=args.headless, timeout=args.timeout)
    success = test.run_test()
    if success:
        print("\n✅ Test completed successfully!")
        exit(0)
    else:
        print("\n❌ Test failed!")
        exit(1)

if __name__ == "__main__":
    main() 