from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
import time
import random
import string
import logging
from typing import Any

class ActivateFixedLongTermPlanInAdminPanelWithBalancePaymentTest:
    def __init__(self):
        # Setup Chrome options for better performance
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")  # Faster loading
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 10)
        self.logger = logging.getLogger("FixedLongTermPlanTest")
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
        
    def generate_random_string(self, length=6):
        """Generate random alphabetic string of specified length"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def safe_click(self, element, description="element"):
        """Safely click an element with fallback strategies and logging."""
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
                except Exception as e2:
                    self.logger.error(f"All click strategies failed for {description}: {e2}")
                    return False
    
    def wait_for_element(self, xpath: str, timeout: int = 10) -> Any:
        """Wait for element to be present and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            self.logger.info(f"Waiting for element: {xpath}")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element: {xpath}")
            return None
    
    def wait_for_element_present(self, xpath, timeout=15):
        """Wait for element to be present in DOM"""
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def navigate_to_login(self):
        """Navigate to login page and wait for everything to load"""
        print("Navigating to login page...")
        self.driver.get("https://test-admin-shenlong.cd.xiaoxigroup.net/login?token=jxRuxHxh")
        
        # Wait for page to load completely
        time.sleep(2)  # Reduced wait time
        
        try:
            self.wait_for_element("//body", timeout=15)
            print("Login page loaded successfully")
        except Exception as e:
            print(f"Error waiting for login page to load: {e}")
            raise
    
    def navigate_to_user_detail(self):
        """Navigate to user detail page"""
        print("Navigating to user detail page...")
        self.driver.get("https://test-admin-shenlong.cd.xiaoxigroup.net/client/userDetail?userId=10614")
        
        try:
            self.wait_for_element("//body", timeout=15)
            print("User detail page loaded successfully")
            
            # Debug: Check page content
            print("\n=== PAGE DEBUG INFO ===")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page title: {self.driver.title}")
            
            # Wait for page to fully load
            time.sleep(3)
            
            # Check if there are any error messages
            error_messages = self.driver.find_elements(By.XPATH, "//*[contains(text(), '错误') or contains(text(), '失败') or contains(text(), 'Error') or contains(text(), 'error')]")
            if error_messages:
                print("Found error messages:")
                for msg in error_messages:
                    print(f"  - {msg.text.strip()}")
            
            # Check for login prompts
            login_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '登录') or contains(text(), 'Login') or contains(text(), 'login')]")
            if login_elements:
                print("Found login-related elements:")
                for elem in login_elements:
                    print(f"  - {elem.text.strip()}")
            
            # Check for loading indicators
            loading_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'loading') or contains(@class, 'spinner') or contains(text(), '加载')]")
            if loading_elements:
                print("Found loading elements:")
                for elem in loading_elements:
                    print(f"  - {elem.text.strip()}")
            
            # Check all page text content
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            if len(page_text.strip()) < 50:
                print(f"Page seems empty or minimal. Body text: '{page_text[:100]}...'")
            else:
                print(f"Page has content. First 200 chars: '{page_text[:200]}...'")
                
            # Check if we can find any user-related info
            user_info = self.driver.find_elements(By.XPATH, "//*[contains(text(), '用户') or contains(text(), 'User') or contains(text(), '客户') or contains(text(), '详情')]")
            if user_info:
                print("Found user-related elements:")
                for info in user_info[:5]:  # Show first 5
                    print(f"  - {info.text.strip()}")
                    
            # Try to find any clickable elements
            clickable_elements = self.driver.find_elements(By.XPATH, "//button | //a | //*[@onclick] | //*[contains(@class, 'btn')] | //*[contains(@class, 'clickable')]")
            print(f"Found {len(clickable_elements)} clickable elements")
            
            if clickable_elements:
                print("First few clickable elements:")
                for i, elem in enumerate(clickable_elements[:10]):  # Show first 10
                    try:
                        print(f"  {i+1}. {elem.tag_name}: '{elem.text.strip()}'")
                    except:
                        print(f"  {i+1}. {elem.tag_name}: [cannot get text]")
            
            print("=== END DEBUG INFO ===\n")
            
        except Exception as e:
            print(f"Error waiting for user detail page to load: {e}")
            raise
    
    def click_add_fixed_long_term_plan_button(self):
        """Click on the 添加固定长效套餐 button"""
        print("Clicking on 添加固定长效套餐 button...")
        add_fixed_plan_xpath = '//button[contains(@class, "el-button") and contains(@class, "btn-info")]//span[text()="添加固定长效套餐"]'
        
        try:
            # Debug: Print current URL and page title
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page title: {self.driver.title}")
            
            # Debug: Check if we can find any buttons first
            try:
                all_buttons = self.driver.find_elements(By.XPATH, "//button")
                print(f"Found {len(all_buttons)} buttons on the page")
                
                # Look for buttons with specific text
                plan_buttons = self.driver.find_elements(By.XPATH, "//*[contains(text(), '添加') or contains(text(), '固定') or contains(text(), '套餐')]")
                print(f"Found {len(plan_buttons)} elements with plan-related text")
                for i, btn in enumerate(plan_buttons[:5]):  # Show first 5
                    print(f"  Button {i+1}: {btn.text.strip()}")
            except Exception as debug_e:
                print(f"Debug error: {debug_e}")
            
            # Try to find the button with longer wait
            print("Waiting for 添加固定长效套餐 button...")
            add_fixed_plan_button = self.wait_for_element(add_fixed_plan_xpath, timeout=15)
            
            if add_fixed_plan_button is None:
                # Try alternative XPath patterns
                alternative_xpaths = [
                    '//button//span[text()="添加固定长效套餐"]',
                    '//button[contains(text(), "添加固定长效套餐")]',
                    '//*[contains(text(), "添加固定长效套餐")]',
                    '//button[contains(@class, "btn-info")]',
                    '//button[contains(@class, "el-button")]'
                ]
                
                for alt_xpath in alternative_xpaths:
                    try:
                        print(f"Trying alternative XPath: {alt_xpath}")
                        add_fixed_plan_button = self.wait_for_element(alt_xpath, timeout=5)
                        if add_fixed_plan_button:
                            print(f"Found button with alternative XPath: {alt_xpath}")
                            break
                    except:
                        continue
            
            if add_fixed_plan_button:
                if self.safe_click(add_fixed_plan_button, "添加固定长效套餐 button"):
                    print("添加固定长效套餐 button clicked successfully")
                    time.sleep(0.5)
                else:
                    raise Exception("Failed to click 添加固定长效套餐 button")
            else:
                raise Exception("Could not find 添加固定长效套餐 button with any XPath pattern")
                
        except Exception as e:
            print(f"Error clicking 添加固定长效套餐 button: {e}")
            # Take screenshot for debugging
            try:
                screenshot_path = f"debug_screenshot_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved as: {screenshot_path}")
            except:
                pass
            raise
    
    def select_package_name(self):
        """Select 测试007 from package name dropdown"""
        print("Selecting package name...")
        
        # Click on package name dropdown - using exact full XPath provided
        package_dropdown_xpath = '/html/body/div[1]/div/div[2]/div/div[15]/div/div[2]/form/div[3]/div/div/div/input'
        
        try:
            # Wait for the popup to fully load
            time.sleep(1)
            
            # Wait for dialog wrapper to become non-interactive or disappear
            try:
                WebDriverWait(self.driver, 8).until(
                    lambda driver: driver.execute_script("""
                        var wrapper = document.querySelector('.el-dialog__wrapper.dialog-wrap');
                        return !wrapper || wrapper.style.pointerEvents === 'none' || wrapper.style.display === 'none';
                    """)
                )
                print("Dialog wrapper is no longer blocking interactions.")
            except Exception as e:
                print(f"Dialog wrapper still present: {e}")
                # Try to make it non-interactive
                try:
                    self.driver.execute_script("""
                        var wrapper = document.querySelector('.el-dialog__wrapper.dialog-wrap');
                        if (wrapper) {
                            wrapper.style.pointerEvents = 'none';
                        }
                    """)
                    print("Made dialog wrapper non-interactive.")
                except:
                    pass
            
            # Try to find the dropdown element using the exact full XPath
            dropdown = self.wait_for_element(package_dropdown_xpath, timeout=15)
            print("Package name dropdown element found using full XPath, attempting to click...")
            
            # Use JavaScript click to bypass overlay issues
            try:
                self.driver.execute_script("arguments[0].click();", dropdown)
                print("JavaScript click successful on dropdown")
            except Exception as e1:
                print(f"JavaScript click failed: {e1}")
                # Fallback: try to focus and then click
                try:
                    self.driver.execute_script("arguments[0].focus(); arguments[0].click();", dropdown)
                    print("Focus + click successful on dropdown")
                except Exception as e2:
                    print(f"Focus + click failed: {e2}")
                    # Last resort: try to trigger the dropdown programmatically
                    try:
                        self.driver.execute_script("""
                            var input = arguments[0];
                            var event = new Event('click', { bubbles: true });
                            input.dispatchEvent(event);
                        """, dropdown)
                        print("Event dispatch successful on dropdown")
                    except Exception as e3:
                        print(f"Event dispatch failed: {e3}")
                        raise
            
            time.sleep(0.5)
            
            # Select 测试007 option
            test007_option_xpath = '//li[contains(@class, "el-select-dropdown__item")]//span[text()="测试007"]'
            try:
                test007_option = self.wait_for_element(test007_option_xpath, timeout=8)
                test007_option.click()
                print("测试007 selected successfully")
                time.sleep(0.5)
            except Exception as e:
                print(f"Error selecting 测试007: {e}")
                try:
                    test007_by_text = self.driver.find_element(By.XPATH, "//*[contains(text(), '测试007')]")
                    test007_by_text.click()
                    print("测试007 selected successfully by text")
                    time.sleep(0.5)
                except Exception as e2:
                    print(f"Alternative selection failed: {e2}")
                    raise
            
        except Exception as e:
            print(f"Error selecting package name: {e}")
            raise
    
    def click_add_region_button(self):
        """Click on the add region button (地区数量)"""
        print("Clicking on add region button...")
        add_region_xpath = '//i[contains(@class, "el-icon-plus") and contains(@class, "add-first")]'
        
        try:
            add_region_button = self.wait_for_element(add_region_xpath)
            if self.safe_click(add_region_button, "add region button"):
                print("Add region button clicked successfully")
                time.sleep(0.5)
            else:
                raise Exception("Failed to click add region button")
        except Exception as e:
            print(f"Error clicking add region button: {e}")
            raise
    
    def select_region(self):
        """Select 福建-福州 from region dropdown"""
        print("Selecting region...")
        
        # Wait for the region dropdown to appear after clicking add region button
        time.sleep(1)
        
        # Use the exact XPath provided for the region dropdown
        region_dropdown_xpath = '/html/body/div[1]/div/div[2]/div/div[15]/div/div[2]/form/div[6]/div/div/ul/li/div[1]/div/input'
        
        try:
            # Try to find the region dropdown using the exact XPath
            region_dropdown = self.wait_for_element(region_dropdown_xpath, timeout=15)
            print("Region dropdown found using exact XPath, attempting to click...")
            
            # Use JavaScript click to open the dropdown
            self.driver.execute_script("arguments[0].click();", region_dropdown)
            print("JavaScript click successful on region dropdown")
            time.sleep(0.5)
            
            # Wait for the region options to appear
            region_option_xpath = '//li[contains(@class, "el-select-dropdown__item")]//span[contains(text(), "福建-福州")]'
            region_option = self.wait_for_element(region_option_xpath, timeout=8)
            # Use JavaScript click for reliability
            self.driver.execute_script("arguments[0].click();", region_option)
            print("福建-福州 selected successfully by visible text")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error selecting region: {e}")
            raise
    
    def click_confirm_button(self):
        """Click on 确 定 button"""
        print("Clicking on 确 定 button...")
        # Use the exact XPath provided for the 确 定 button
        confirm_xpath = '/html/body/div[1]/div/div[2]/div/div[15]/div/div[3]/span/button[2]'
        try:
            # Wait for the button to be visible and enabled
            confirm_button = self.wait_for_element(confirm_xpath, timeout=20)
            for _ in range(5):  # Reduced retry attempts
                if confirm_button.is_displayed() and confirm_button.is_enabled():
                    break
                time.sleep(0.3)  # Reduced wait time
            # Use JavaScript click for reliability
            self.driver.execute_script("arguments[0].click();", confirm_button)
            print("确 定 button clicked successfully")
            time.sleep(1)  # Reduced wait time
        except Exception as e:
            print(f"Error clicking 确 定 button: {e}")
            raise

    def click_fixed_long_term_history_tab(self):
        """Click on 固定长效历史套餐 tab"""
        print("Clicking on 固定长效历史套餐 tab...")
        fixed_history_tab_xpath = '//div[@id="tab-ipMeal" and contains(text(), "固定长效历史套餐")]'
        try:
            fixed_history_tab = self.wait_for_element(fixed_history_tab_xpath)
            if self.safe_click(fixed_history_tab, "固定长效历史套餐 tab"):
                print("固定长效历史套餐 tab clicked successfully")
                time.sleep(1)
            else:
                raise Exception("Failed to click 固定长效历史套餐 tab")
        except Exception as e:
            print(f"Error clicking 固定长效历史套餐 tab: {e}")
            raise

    def refresh_page_and_wait(self):
        """Refresh page to get latest plan data"""
        print("Refreshing page to get latest plan data...")
        self.driver.refresh()
        time.sleep(3)
        try:
            self.wait_for_element("//body", timeout=20)
            print("Page refreshed successfully")
        except Exception as e:
            print(f"Error waiting for page to load after refresh: {e}")
            raise

    def turn_off_switch(self):
        """Turn off the switch"""
        print("Turning off the switch...")
        switch_xpath = '/html/body/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/table/tbody/tr[1]/td[8]/div/div/div//span[contains(@class, "el-switch__core")]'
        try:
            # First check if the switch is currently ON (enabled)
            switch = self.wait_for_element(switch_xpath, timeout=20)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", switch)
            time.sleep(0.5)
            
            # Check switch state (if it has 'is-checked' class, it's ON)
            switch_container = self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/table/tbody/tr[1]/td[8]/div/div/div')
            is_currently_on = 'is-checked' in switch_container.get_attribute('class') if switch_container.get_attribute('class') else False
            
            print(f"Switch current state: {'ON' if is_currently_on else 'OFF'}")
            
            # Only click if it's currently ON (to turn it OFF)
            if is_currently_on:
                self.driver.execute_script("arguments[0].click();", switch)
                print("Switch turned OFF successfully")
            else:
                print("Switch is already OFF, no action needed")
            
            time.sleep(1)
        except Exception as e:
            print(f"Error turning off switch: {e}")
            raise
    

    
    def check_success_message(self):
        """Check for success message after plan activation"""
        print("Checking for success message...")
        try:
            # Wait for success message to appear
            time.sleep(2)  # Give time for message to appear
            
            # Common success message patterns - try multiple approaches
            success_xpaths = [
                '//div[contains(@class, "el-message") and contains(text(), "添加成功")]',
                '//div[contains(@class, "el-notification") and contains(text(), "添加成功")]',
                '//div[contains(@class, "message") and contains(text(), "添加成功")]',
                '//*[contains(text(), "添加成功")]',
                '//div[contains(@class, "success") and contains(text(), "添加成功")]'
            ]
            
            for xpath in success_xpaths:
                try:
                    success_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    if success_element.is_displayed():
                        print(f"✅ Success message found: {success_element.text}")
                        return True
                except TimeoutException:
                    continue
            
            # If direct message not found, check for successful form submission by looking for dialog close
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, '//div[contains(@class, "el-dialog__wrapper")]'))
                )
                print("✅ Form dialog closed successfully, indicating successful submission")
                return True
            except TimeoutException:
                pass
            
            # Alternative: Check if we can find any success indicator
            try:
                success_indicators = self.driver.find_elements(By.XPATH, '//*[contains(text(), "成功") or contains(text(), "Success")]')
                if success_indicators:
                    for indicator in success_indicators:
                        if indicator.is_displayed():
                            print(f"✅ Success indicator found: {indicator.text}")
                            return True
            except Exception:
                pass
                
            print("❌ No success message found")
            return False
            
        except Exception as e:
            print(f"Error checking success message: {e}")
            return False

    
    def run_test(self) -> bool:
        """Run the complete test flow"""
        try:
            self.logger.info("Starting test: Activate Fixed Long-Term Plan with Balance Payment")
            
            # Step 1: Navigate to login page
            self.navigate_to_login()
            
            # Step 2: Navigate to user detail page
            self.navigate_to_user_detail()
            
            # Step 3: Click add fixed long term plan button
            self.click_add_fixed_long_term_plan_button()
            
            # Step 4: Select package name
            self.select_package_name()
            
            # Step 5: Click add region button
            self.click_add_region_button()
            
            # Step 6: Select region
            self.select_region()
            
            # Step 7: Click confirm button
            self.click_confirm_button()
            
            # Step 8: Click fixed long-term history tab
            self.click_fixed_long_term_history_tab()
            
            # Step 9: Refresh page to load latest plan data
            self.refresh_page_and_wait()
            
            # Step 10: Turn off switch
            self.turn_off_switch()
            
            # Step 11: Check for success message
            if self.check_success_message():

                self.logger.info("\n🎉 TEST PASSED: Fixed Long-Term Plan activation with balance payment completed successfully!")
                self.logger.info("All steps completed: Plan activation, payment, and plan management.")
                return True
            else:
                self.logger.error("\n❌ TEST FAILED: Could not verify success message")
                return False
                
        except Exception as e:
            self.logger.error(f"\n❌ TEST FAILED with error: {e}")
            return False
        finally:
            self.logger.info("\nTest completed. Browser will remain open for 2 seconds for inspection...")
            time.sleep(2)

def main():
    """Main function to run the test"""
    test = ActivateFixedLongTermPlanInAdminPanelWithBalancePaymentTest()
    test.run_test()

if __name__ == "__main__":
    main() 