#!/usr/bin/env python3
"""
Debug version of main.py with enhanced tracking and progress monitoring
"""

import os
import sys
import time
from pathlib import Path

# Add the main script directory to Python path
sys.path.append(os.path.dirname(__file__))

# Import from main.py
from main import (
    SOURCE_FOLDER, LOG_FILE, BATCH_SIZE,
    load_processed_files, save_processed_files, add_processed_file,
    process_file, IsResume_With_Confidence
)

def debug_tracking_system():
    """Test the new tracking system"""
    print("🔍 Testing new tracking system...")
    
    # Load existing processed files
    processed_files = load_processed_files()
    print(f"📊 Loaded {len(processed_files)} previously processed files")
    
    if len(processed_files) > 0:
        print(f"📋 Sample processed files:")
        for i, file_path in enumerate(sorted(processed_files)[:5]):
            print(f"  {i+1}. {os.path.basename(file_path)}")
        if len(processed_files) > 5:
            print(f"  ... and {len(processed_files)-5} more files")
    
    return processed_files

def scan_folder_status():
    """Check source folder status"""
    print(f"\n📁 Checking source folder: {SOURCE_FOLDER}")
    
    if not os.path.exists(SOURCE_FOLDER):
        print(f"❌ Source folder does not exist!")
        return False
    
    print(f"✅ Source folder exists")
    
    # Count total files
    total_files = 0
    cv_extensions = {'.pdf', '.doc', '.docx', '.rtf', '.txt'}
    
    try:
        for root, dirs, files in os.walk(SOURCE_FOLDER):
            for file in files:
                if any(file.lower().endswith(ext) for ext in cv_extensions):
                    total_files += 1
            
            # Show progress every 1000 files
            if total_files % 1000 == 0 and total_files > 0:
                print(f"  📊 Found {total_files} potential CV files so far...")
                
    except Exception as e:
        print(f"❌ Error scanning folder: {e}")
        return False
    
    print(f"📊 Total potential CV files found: {total_files}")
    return total_files > 0

def test_small_batch():
    """Process a small batch of files for testing"""
    print(f"\n🧪 Testing small batch processing...")
    
    processed_files = load_processed_files()
    cv_extensions = {'.pdf', '.doc', '.docx', '.rtf', '.txt'}
    test_files = []
    
    # Find first 3 unprocessed files
    try:
        for root, dirs, files in os.walk(SOURCE_FOLDER):
            for file in files:
                if any(file.lower().endswith(ext) for ext in cv_extensions):
                    file_path = os.path.join(root, file)
                    if file_path not in processed_files:
                        test_files.append(file_path)
                        if len(test_files) >= 3:
                            break
            if len(test_files) >= 3:
                break
    except Exception as e:
        print(f"❌ Error finding test files: {e}")
        return
    
    if not test_files:
        print("🎉 No unprocessed files found - all files have been processed!")
        return
    
    print(f"📋 Found {len(test_files)} unprocessed files for testing:")
    for i, file_path in enumerate(test_files, 1):
        print(f"  {i}. {os.path.basename(file_path)}")
    
    # Process test files
    for i, file_path in enumerate(test_files, 1):
        print(f"\n🔍 Processing test file {i}/{len(test_files)}: {os.path.basename(file_path)}")
        
        try:
            # Process using the main process_file function
            file_name, result, ocr_flag = process_file(file_path)
            print(f"  📝 CV Detection Result: {result} (OCR: {ocr_flag})")
            
            # Add to processed files
            add_processed_file(file_path, processed_files)
            print(f"  ✅ Added to tracking system")
            
        except Exception as e:
            print(f"  ❌ Error processing file: {e}")
    
    print(f"\n✅ Test batch complete!")

if __name__ == "__main__":
    print("🚀 QueryMind Debug & Test Script")
    print("=" * 50)
    
    # Test tracking system
    processed_files = debug_tracking_system()
    
    # Check folder status
    folder_ok = scan_folder_status()
    
    if folder_ok:
        # Test small batch
        test_small_batch()
    
    print("\n🎯 Debug session complete!")
    print("=" * 50)
