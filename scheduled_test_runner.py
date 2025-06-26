#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scheduled Test Runner for ShenLong IP Admin Panel
Runs tests daily at 9:00 AM
"""

import schedule
import time
import subprocess
import sys
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_test_suite():
    """Run the complete test suite"""
    try:
        logger.info("=" * 60)
        logger.info("STARTING SCHEDULED TEST SUITE")
        logger.info("=" * 60)
        
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_runner_path = os.path.join(script_dir, "run_all_tests.py")
        
        # Set environment variables for Unicode support
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
        
        # Run the test suite
        result = subprocess.run(
            [sys.executable, test_runner_path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=1800,  # 30 minutes timeout
            env=env,
            cwd=script_dir
        )
        
        if result.returncode == 0:
            logger.info("✅ Test suite completed successfully!")
            logger.info(f"Output: {result.stdout}")
        else:
            logger.error("❌ Test suite failed!")
            logger.error(f"Error: {result.stderr}")
            logger.info(f"Output: {result.stdout}")
            
    except subprocess.TimeoutExpired:
        logger.error("❌ Test suite timed out after 30 minutes")
    except Exception as e:
        logger.error(f"❌ Error running test suite: {e}")
    
    logger.info("=" * 60)
    logger.info("SCHEDULED TEST SUITE COMPLETED")
    logger.info("=" * 60)

def main():
    """Main function to set up and run the scheduler"""
    logger.info("🚀 ShenLong IP Test Scheduler Starting...")
    logger.info(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Schedule the test to run daily at 9:00 AM
    schedule.every().day.at("09:00").do(run_test_suite)
    
    logger.info("📅 Test suite scheduled to run daily at 9:00 AM")
    logger.info("⏰ Scheduler is running... Press Ctrl+C to stop")
    logger.info("=" * 60)
    
    # Run the test suite immediately if it's the first time
    logger.info("🔄 Running initial test suite...")
    run_test_suite()
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main() 