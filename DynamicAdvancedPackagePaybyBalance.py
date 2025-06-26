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

class DynamicAdvancedPackagePaybyBalanceTest:
    def __init__(self, headless: bool = False, timeout: int = 15):
        """
        Initialize the test with configurable options
        
        Args:
            headless: Run browser in headless mode
            timeout: Default timeout for element waits
        """
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.setup_driver(headless)
        
    def setup_driver(self, headless: bool):
        """Setup Chrome WebDriver with optimized options"""
        chrome_options = Options()
        
        # Performance optimizations
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # Faster loading
        chrome_options.add_argument("--disable-javascript")  # If not needed
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        # Anti-detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        if not headless:
            chrome_options.add_argument("--start-maximized")
        else:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, self.timeout)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def generate_random_string(self, length: int = 6) -> str:
        """Generate random alphabetic string of specified length"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def wait_for_element(self, xpath: str, timeout: Optional[int] = None) -> Any:
        """
        Wait for element to be present and clickable with improved error handling
        
        Args:
            xpath: XPath of the element
            timeout: Custom timeout (uses default if None)
            
        Returns:
            WebElement if found and clickable
        """
        timeout = timeout or self.timeout
        
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            logger.debug(f"Element found and clickable: {xpath}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {timeout}s: {xpath}")
            # Try to find if element exists but not clickable
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                logger.warning(f"Element found but not clickable: {element.text if element.text else 'No text'}")
                return element
            except NoSuchElementException:
                logger.error(f"Element not found at all: {xpath}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error waiting for element {xpath}: {e}")
            raise
    
    def safe_click(self, xpath: str, timeout: Optional[int] = None) -> bool:
        """
        Safely click an element with retry logic
        
        Args:
            xpath: XPath of the element to click
            timeout: Custom timeout
            
        Returns:
            True if click successful, False otherwise
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                element = self.wait_for_element(xpath, timeout)
                element.click()
                logger.info(f"Successfully clicked element: {xpath}")
                return True
            except Exception as e:
                logger.warning(f"Click attempt {attempt + 1} failed for {xpath}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error(f"Failed to click element after {max_retries} attempts: {xpath}")
                    return False
        return False
    
    def get_authentication_cookies(self) -> list:
        """Get authentication cookies configuration"""
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
        """Add authentication cookies with improved error handling"""
        logger.info("Adding authentication cookies...")
        
        try:
            # First navigate to the domain to set cookies
            self.driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net")
            time.sleep(1)  # Reduced wait time
            
            cookies = self.get_authentication_cookies()
            success_count = 0
            
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                    success_count += 1
                    logger.debug(f"Added cookie: {cookie['name']}")
                except Exception as e:
                    logger.warning(f"Error adding cookie {cookie['name']}: {e}")
            
            logger.info(f"Authentication cookies added successfully: {success_count}/{len(cookies)}")
            return success_count >= len(cookies) * 0.8  # Allow 20% failure rate
            
        except Exception as e:
            logger.error(f"Failed to add authentication cookies: {e}")
            return False
    
    def navigate_to_personal_center(self) -> bool:
        """Navigate to personal center page with authentication"""
        logger.info("Navigating to personal center page...")
        
        try:
            # Add authentication cookies
            if not self.add_authentication_cookies():
                logger.error("Failed to add authentication cookies")
                return False
            
            # Navigate to personal center
            self.driver.get("https://test-ip-shenlong.cd.xiaoxigroup.net/personalCenter")
            time.sleep(2)  # Reduced wait time
            
            # Verify page loaded
            self.wait_for_element("//body", timeout=30)
            logger.info("Personal center page loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to personal center: {e}")
            return False
    
    def click_package_account_management_tab(self) -> bool:
        """Click on 套餐/账号管理 tab"""
        logger.info("Clicking on 套餐/账号管理 tab...")
        xpath = '/html/body/div[2]/div/div[2]/ul/li[2]/ul/a/li/span'
        return self.safe_click(xpath)
    
    def click_add_paid_account_button(self) -> bool:
        """Click on 添加付费账户 button"""
        logger.info("Clicking on 添加付费账户 button...")
        xpath = '/html/body/div[2]/div/div[2]/div/button[1]'
        return self.safe_click(xpath)
    
    def select_dynamic_advanced_package(self) -> bool:
        """Select 动态高级套餐 choice"""
        logger.info("Selecting 动态高级套餐...")
        xpath = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div/div[1]/form/div[1]/div[2]/div/label[2]/span[1]/span'
        return self.safe_click(xpath)
    
    def click_confirm_button(self) -> bool:
        """Click on 确认 button"""
        logger.info("Clicking on 确认 button...")
        xpath = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/footer/div/button[2]'
        return self.safe_click(xpath)
    
    def check_success_message(self) -> bool:
        logger.info("Checking for success message...")
        try:
            # Wait for success message to appear
            success_xpath = "//div[contains(text(), '添加成功') or contains(text(), 'Success')]"
            success_element = self.wait_for_element(success_xpath, timeout=10)
            if success_element:
                logger.info("✅ Success message found!")
                return True
            else:
                logger.error("❌ Success message not found")
                return False
        except Exception as e:
            logger.error(f"Error checking success message: {e}")
            return False
    
    def run_test(self) -> bool:
        logger.info("Starting Dynamic Advanced Package Balance Payment Test")
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
            
            if not self.click_confirm_button():
                logger.error("Failed to click confirm button")
                return False
            
            if not self.check_success_message():
                logger.error("Failed to check success message")
                return False
            
            logger.info("✅ Balance payment test completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Test failed with exception: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed")

def main():
    """Main function to run the test with configurable options"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Dynamic Advanced Package Test')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--timeout', type=int, default=15, help='Default timeout in seconds')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    test = DynamicAdvancedPackagePaybyBalanceTest(
        headless=args.headless,
        timeout=args.timeout
    )
    
    success = test.run_test()
    exit(0 if success else 1)

if __name__ == "__main__":
    main() 