#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified test runner that handles Unicode encoding issues
"""

import subprocess
import sys
import time
import os
from datetime import datetime

def run_test_with_encoding_fix(test_file):
    """Run a test file with proper encoding handling"""
    try:
        # Set environment variables for Unicode support
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
        
        # For Windows, we need to handle console encoding
        if os.name == 'nt':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleCP(65001)
                kernel32.SetConsoleOutputCP(65001)
            except:
                pass
        
        # Run the test with proper encoding
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace problematic characters
            timeout=300,  # 5 minutes timeout
            env=env
        )
        
        return result
        
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return None

def main():
    """Main function to run all tests"""
    
    # List of test files
    test_files = [
        "ActivateFixedLongTermPlaninAdminPanelwithBalancePayment.py",
        "AdminPanel_PurchaseFixedLongTermPlanActivateFixedLongTermPlaninAdminPanelwithPendingPaymentOrder.py",
        "ActivateDynamicPremiumPlaninAdminPanelwithBalancePayment.py",
        "OpenStaticPremiumPackageinManagementBackendandManagePaymentinManagementBackendBalancePayment.py",
        "ActivateDynamicDedicatedPlaninAdminPanelwithBalancePayment.py",
        "OpenStaticPremiumPackageinManagementBackendandManagePaymentinManagementBackendGenerateOrderstoBePaid.py",
        "AdminPanel_ActivateDynamicPremiumPlanandGeneratePendingPaymentOrder.py",
        "ActivateDynamicDedicatedPlaninAdminPanelwithPaymentviaPendingOrder.py"
    ]
    
    print("=" * 80)
    print("SHENLONG IP ADMIN PANEL - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Test Run Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Tests to Run: {len(test_files)}")
    print("=" * 80)
    print()
    
    # Check which files exist
    existing_files = [f for f in test_files if os.path.exists(f)]
    
    if not existing_files:
        print("No test files found! Please ensure the test files are in the current directory.")
        return
    
    print(f"Found {len(existing_files)} test files to run")
    print()
    
    results = {}
    start_time = time.time()
    
    # Run each test
    for i, test_file in enumerate(existing_files, 1):
        print(f"Test {i}/{len(existing_files)}")
        print(f"Running: {test_file}")
        print("-" * 60)
        
        test_start_time = time.time()
        result = run_test_with_encoding_fix(test_file)
        test_end_time = time.time()
        duration = test_end_time - test_start_time
        
        if result is None:
            print(f"ERROR: {test_file} - Failed to execute")
            results[test_file] = {
                'status': 'FAILED',
                'duration': duration,
                'error': 'Failed to execute test'
            }
        elif result.returncode == 0:
            print(f"PASSED: {test_file} (Duration: {duration:.2f}s)")
            results[test_file] = {
                'status': 'PASSED',
                'duration': duration,
                'output': result.stdout,
                'error': None
            }
        else:
            print(f"FAILED: {test_file} (Duration: {duration:.2f}s)")
            print(f"Error: {result.stderr}")
            results[test_file] = {
                'status': 'FAILED',
                'duration': duration,
                'output': result.stdout,
                'error': result.stderr
            }
        
        print("-" * 60)
        print()
        
        # Add delay between tests
        if i < len(existing_files):
            print("Waiting 3 seconds before next test...")
            time.sleep(3)
            print()
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Print summary
    print("=" * 80)
    print("TEST EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total Execution Time: {total_duration:.2f} seconds")
    
    passed = sum(1 for result in results.values() if result['status'] == 'PASSED')
    failed = sum(1 for result in results.values() if result['status'] == 'FAILED')
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {failed}/{total}")
    print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "Success Rate: 0%")
    
    if failed > 0:
        print("\nFAILED TESTS:")
        for test_name, result in results.items():
            if result['status'] == 'FAILED':
                print(f"   • {test_name}: {result.get('error', 'Unknown error')}")
    
    print("=" * 80)
    
    # Save results to file
    with open("test_results.txt", "w", encoding="utf-8") as f:
        f.write("SHENLONG IP ADMIN PANEL - TEST RESULTS\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for test_name, result in results.items():
            f.write(f"Test: {test_name}\n")
            f.write(f"Status: {result['status']}\n")
            f.write(f"Duration: {result['duration']:.2f}s\n")
            
            if result['error']:
                f.write(f"Error: {result['error']}\n")
            
            if result.get('output'):
                f.write(f"Output:\n{result['output']}\n")
            
            f.write("-" * 30 + "\n")
    
    print(f"Detailed results saved to: test_results.txt")
    
    # Return appropriate exit code
    if failed > 0:
        print(f"\n{failed} test(s) failed. Check the results above.")
        sys.exit(1)
    else:
        print("\nAll tests passed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main() 