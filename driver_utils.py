from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_chrome_driver():
    """
    Set up and return a Chrome WebDriver instance with optimized settings
    and comprehensive error handling for browser console warnings
    
    Returns:
        WebDriver instance or None if setup fails
    """
    try:
        # Enhanced Chrome options for better performance and error suppression
        chrome_options = Options()
        
        # ============================================================================
        # STABILITY & PERFORMANCE OPTIONS
        # ============================================================================
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        
        # ============================================================================
        # GPU & HARDWARE ACCELERATION FIXES
        # ============================================================================
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-gpu-sandbox')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-accelerated-2d-canvas')
        chrome_options.add_argument('--disable-accelerated-jpeg-decoding')
        chrome_options.add_argument('--disable-accelerated-mjpeg-decode')
        chrome_options.add_argument('--disable-accelerated-video-decode')
        chrome_options.add_argument('--disable-accelerated-video-encode')
        
        # ============================================================================
        # NETWORK & SSL FIXES
        # ============================================================================
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-cross-origin-auth-prompt')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        # ============================================================================
        # CONSOLE WARNING SUPPRESSION
        # ============================================================================
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--disable-console-logging')
        chrome_options.add_argument('--disable-logging-redirect')
        
        # ============================================================================
        # AUTOMATION DETECTION PREVENTION
        # ============================================================================
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.media_stream": 2,
        })
        
        # ============================================================================
        # USER AGENT & WINDOW SETTINGS
        # ============================================================================
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # ============================================================================
        # DRIVER INITIALIZATION WITH MULTIPLE FALLBACK METHODS
        # ============================================================================
        driver = None
        
        # Method 1: Try with ChromeDriverManager (Recommended)
        try:
            logger.info("Attempting to initialize driver with ChromeDriverManager...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("✅ Driver initialized successfully with ChromeDriverManager")
        except Exception as e:
            logger.warning(f"❌ ChromeDriverManager approach failed: {e}")
            
        # Method 2: Try without service (system PATH)
        if driver is None:
            try:
                logger.info("Attempting to initialize driver from system PATH...")
                driver = webdriver.Chrome(options=chrome_options)
                logger.info("✅ Driver initialized successfully from system PATH")
            except Exception as e:
                logger.warning(f"❌ System PATH approach failed: {e}")
        
        # Method 3: Try with explicit chromedriver.exe path
        if driver is None:
            try:
                logger.info("Attempting to find chromedriver.exe in common locations...")
                common_paths = [
                    r"C:\chromedriver\chromedriver.exe",
                    r"C:\Program Files\Google\Chrome\Application\chromedriver.exe",
                    r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chromedriver.exe".format(os.getenv('USERNAME')),
                    "./chromedriver.exe",
                    "./chromedriver"
                ]
                
                for path in common_paths:
                    if os.path.exists(path):
                        logger.info(f"Found chromedriver at: {path}")
                        service = Service(path)
                        driver = webdriver.Chrome(service=service, options=chrome_options)
                        logger.info(f"✅ Driver initialized successfully with path: {path}")
                        break
                        
            except Exception as e:
                logger.warning(f"❌ Explicit path approach failed: {e}")
        
        if driver is None:
            logger.error("❌ All driver initialization methods failed")
            return None
            
        # ============================================================================
        # POST-INITIALIZATION CONFIGURATION
        # ============================================================================
        try:
            # Set timeouts
            driver.set_page_load_timeout(60)
            driver.implicitly_wait(10)
            
            # Execute anti-detection scripts
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            # Suppress console errors and warnings
            driver.execute_script("""
                // Override console methods to suppress warnings
                const originalConsole = {
                    log: console.log,
                    warn: console.warn,
                    error: console.error
                };
                
                console.warn = function() {};
                console.error = function() {};
                
                // Suppress specific warnings
                window.addEventListener('error', function(e) {
                    if (e.message.includes('GPU') || 
                        e.message.includes('WebGL') || 
                        e.message.includes('network') ||
                        e.message.includes('SSL') ||
                        e.message.includes('certificate')) {
                        e.preventDefault();
                        return false;
                    }
                });
                
                // Suppress unhandled promise rejections
                window.addEventListener('unhandledrejection', function(e) {
                    e.preventDefault();
                });
            """)
            
            # Maximize window
            driver.maximize_window()
            
            logger.info("✅ WebDriver setup completed successfully with all optimizations")
            return driver
            
        except Exception as e:
            logger.warning(f"⚠️ Post-initialization configuration failed: {e}")
            # Return driver even if post-config fails
            return driver
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize WebDriver: {e}")
        return None 