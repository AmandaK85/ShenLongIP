# ShenLong IP Admin Panel Test Suite

This repository contains comprehensive Selenium test automation scripts for the ShenLong IP Admin Panel.

## Test Files Overview

The test suite includes the following automated tests:

1. **ActivateFixedLongTermPlaninAdminPanelwithBalancePayment.py** - Tests fixed long-term plan activation with balance payment
2. **AdminPanel_PurchaseFixedLongTermPlanActivateFixedLongTermPlaninAdminPanelwithPendingPaymentOrder.py** - Tests fixed long-term plan with pending payment order
3. **ActivateDynamicPremiumPlaninAdminPanelwithBalancePayment.py** - Tests dynamic premium plan activation with balance payment
4. **OpenStaticPremiumPackageinManagementBackendandManagePaymentinManagementBackendBalancePayment.py** - Tests static premium package with balance payment
5. **ActivateDynamicDedicatedPlaninAdminPanelwithBalancePayment.py** - Tests dynamic dedicated plan with balance payment
6. **OpenStaticPremiumPackageinManagementBackendandManagePaymentinManagementBackendGenerateOrderstoBePaid.py** - Tests static premium package with order generation
7. **AdminPanel_ActivateDynamicPremiumPlanandGeneratePendingPaymentOrder.py** - Tests dynamic premium plan with pending order generation
8. **ActivateDynamicDedicatedPlaninAdminPanelwithPaymentviaPendingOrder.py** - Tests dynamic dedicated plan with pending order payment

## Quick Start - Run All Tests Together

### Windows Users (Recommended):
```bash
# Use PowerShell script for best Unicode support:
powershell -ExecutionPolicy Bypass -File run_all_tests.ps1
```

### Python Directly:
```bash
python run_all_tests.py
```

### Option 2: Run Individual Tests

To run a specific test file:

```bash
python ActivateFixedLongTermPlaninAdminPanelwithBalancePayment.py
```

## Features of the Test Runner

The `run_all_tests.py` script provides:

- ✅ **Sequential Execution**: Runs all tests one by one to avoid conflicts
- ⏱️ **Timeout Protection**: 5-minute timeout per test to prevent hanging
- 📊 **Detailed Reporting**: Shows pass/fail status and execution time
- 📄 **Results Logging**: Saves detailed results to `test_results.txt`
- 🎯 **Error Handling**: Graceful handling of failures and timeouts
- 📈 **Success Rate**: Calculates overall test success percentage
- 🌐 **Unicode Support**: Proper handling of Chinese characters on Windows

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Selenium WebDriver** package
3. **Chrome Browser** installed
4. **ChromeDriver** (automatically managed by Selenium)

## Installation

1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install selenium
   ```

## Test Execution Output

When you run the test suite, you'll see output like this:

```
================================================================================
SHENLONG IP ADMIN PANEL - COMPREHENSIVE TEST SUITE
================================================================================
Test Run Started: 2024-01-15 14:30:25
Total Tests to Run: 8
================================================================================

Found 8 test files to run

Test 1/8
Running: ActivateFixedLongTermPlaninAdminPanelwithBalancePayment.py
------------------------------------------------------------
PASSED: ActivateFixedLongTermPlaninAdminPanelwithBalancePayment.py (Duration: 37.21s)
------------------------------------------------------------

Waiting 3 seconds before next test...

...

================================================================================
TEST EXECUTION SUMMARY
================================================================================
Total Execution Time: 368.12 seconds
Passed: 8/8
Failed: 0/8
Success Rate: 100.0%
================================================================================
```

## Configuration

### Test URLs
All tests use the following URLs:
- **Login URL**: `https://test-admin-shenlong.cd.xiaoxigroup.net/login?token=jxRuxHxh`
- **User Detail URL**: `https://test-admin-shenlong.cd.xiaoxigroup.net/client/userDetail?userId=10614`

### Browser Settings
- Chrome browser with automation detection disabled
- Maximized window
- Disabled images for faster loading
- 10-20 second timeouts for element interactions

## Troubleshooting

### Common Issues:

1. **ChromeDriver Issues**: 
   - The tests use Selenium's built-in ChromeDriver manager
   - Ensure Chrome browser is installed and up to date

2. **Timeout Errors**:
   - Network issues may cause timeouts
   - Check internet connection
   - Increase timeout values in individual test files if needed

3. **Element Not Found**:
   - Website structure may have changed
   - Check if the test URLs are still valid
   - Update XPath selectors if necessary

4. **Unicode/Encoding Issues** (Windows):
   - Use the PowerShell script: `powershell -ExecutionPolicy Bypass -File run_all_tests.ps1`
   - Or ensure proper UTF-8 encoding in your terminal

### Debug Mode:
Each test file includes a `debug_page_structure()` method that can be called to:
- Save page source to `page_source.html`
- Print page structure information
- Take screenshots for manual inspection

## File Structure

```
ShenLongIP/
├── run_all_tests.py              # Main test runner (Unicode-compatible)
├── run_all_tests.ps1             # PowerShell script for Windows
├── test_results.txt              # Generated test results
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── [Individual test files...]    # 8 Selenium test scripts
```

## Contributing

When adding new tests:
1. Follow the existing naming convention
2. Include proper error handling
3. Add the test file to the `test_files` list in `run_all_tests.py`
4. Update this README with test description

## Support

For issues or questions:
1. Check the `test_results.txt` file for detailed error information
2. Review individual test output for specific failures
3. Ensure all prerequisites are met
4. Verify test URLs are accessible 