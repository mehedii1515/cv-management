"""
Test script to demonstrate QueryMind File Watcher
"""
import os
import time
import shutil

def test_file_watcher():
    """Test the file watcher by copying a test file"""
    
    print("🧪 Testing QueryMind File Watcher")
    print("=" * 40)
    
    # Check if DROPPED PROJECTS folder exists
    test_folder = "./DROPPED PROJECTS/"
    if not os.path.exists(test_folder):
        print("❌ Test folder not found:", test_folder)
        return
    
    # Find an existing CV file to copy
    test_files = []
    for root, dirs, files in os.walk(test_folder):
        for file in files:
            if file.lower().endswith(('.pdf', '.doc', '.docx')):
                test_files.append(os.path.join(root, file))
                if len(test_files) >= 3:  # Only need a few for testing
                    break
        if len(test_files) >= 3:
            break
    
    if not test_files:
        print("❌ No test files found in", test_folder)
        return
    
    print(f"✅ Found {len(test_files)} test files")
    
    # Create a test subfolder
    test_target_folder = os.path.join(test_folder, "TEST_WATCHER")
    os.makedirs(test_target_folder, exist_ok=True)
    
    print("\n🎯 Instructions for testing:")
    print("1. Make sure the file watcher is running:")
    print("   python file_watcher.py --test")
    print("\n2. Run this test script in another terminal:")
    print("   python test_watcher.py")
    print("\n3. Watch the file watcher detect and process the files!")
    
    input("\nPress Enter when the file watcher is running...")
    
    # Copy files one by one with delays
    for i, source_file in enumerate(test_files, 1):
        filename = os.path.basename(source_file)
        target_file = os.path.join(test_target_folder, f"test_{i}_{filename}")
        
        print(f"\n📄 Copying test file {i}: {filename}")
        shutil.copy2(source_file, target_file)
        print(f"   → Copied to: {target_file}")
        print("   → Watch the file watcher console for detection...")
        
        # Wait before copying next file
        if i < len(test_files):
            print(f"   ⏳ Waiting 10 seconds before next file...")
            time.sleep(10)
    
    print("\n✅ Test complete!")
    print("📊 Check the file watcher console for processing results")
    print(f"📁 Test files are in: {test_target_folder}")
    
    # Cleanup option
    cleanup = input("\n🗑️ Delete test files? (y/n): ").lower().strip()
    if cleanup == 'y':
        try:
            shutil.rmtree(test_target_folder)
            print("✅ Test files cleaned up")
        except Exception as e:
            print(f"⚠️ Error cleaning up: {e}")

if __name__ == "__main__":
    test_file_watcher()
