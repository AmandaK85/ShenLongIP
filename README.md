# Admin Panel Purchase Dynamic Advanced Package Test

This Selenium test automates the purchase flow for a dynamic advanced VPN package in the admin panel.

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Chrome browser** installed
3. **ChromeDriver** - The script will attempt to use the system's ChromeDriver, but you may need to install it manually

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install ChromeDriver (if not already installed):**
   - Download from: https://chromedriver.chromium.org/
   - Add to your system PATH or place in the same directory as the script

## Test Flow

The test performs the following steps:

1. **Navigate to login page** - Opens the admin panel with the provided token
2. **Navigate to user detail page** - Goes to the specific user (ID: 10614)
3. **Click 添加VPN button** - Opens the VPN purchase popup
4. **Select package type** - Chooses "动态高级套餐" from dropdown
5. **Enter VPN account name** - Generates and enters a random 6-character name
6. **Click 确定 button** - Confirms the VPN purchase
7. **Click 历史订单 tab** - Navigates to order history
8. **Click 支付 button** - Initiates payment for the order
9. **Click 确定 button in payment popup** - Confirms payment
10. **Verify success message** - Checks for successful completion

## Running the Test

```bash
python AdminPanel_PurchaseDynamicAdvancedPackage.py
```

## Features

- **Robust error handling** - Each step includes try-catch blocks with detailed error messages
- **Explicit waits** - Uses WebDriverWait to ensure elements are present before interaction
- **Random data generation** - Generates random VPN account names for each test run
- **Detailed logging** - Provides step-by-step progress updates
- **Browser inspection** - Keeps browser open for 30 seconds after test completion for manual inspection

## Troubleshooting

### Common Issues:

1. **ChromeDriver not found:**
   - Download ChromeDriver from https://chromedriver.chromium.org/
   - Ensure it's in your PATH or in the same directory as the script

2. **Element not found errors:**
   - The page structure may have changed
   - Check if XPath selectors need updating
   - Verify the page has loaded completely

3. **Timing issues:**
   - Increase wait times in the script if pages load slowly
   - Check your internet connection

### Debug Mode:

To run with additional debugging, you can modify the Chrome options in the script:

```python
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--v=1")
```

## Notes

- The test uses the provided token for authentication
- VPN account names are randomly generated (6 characters)
- The browser will remain open for 30 seconds after test completion
- All XPath selectors are based on the current page structure and may need updates if the UI changes 