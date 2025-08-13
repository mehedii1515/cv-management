"""
Simple QueryMind Integration Setup and Test
"""
import os
import sys
import subprocess
import requests
import json
from datetime import datetime

def check_resume_parser_connection():
    """Check if the resume parser backend is running"""
    print("🔍 Checking resume parser connection...")
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        print("✅ Resume parser backend is running")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Resume parser backend is not running")
        print("   Please start your Django backend first:")
        print("   cd backend && python manage.py runserver")
        return False
    except Exception as e:
        print(f"⚠️ Error checking connection: {e}")
        return False

def test_integration():
    """Test the integration setup"""
    print("🧪 Testing QueryMind integration...")
    
    # Import the main module
    try:
        import main
        print("✅ QueryMind main module imported successfully")
    except ImportError as e:
        print(f"❌ Error importing main module: {e}")
        return False
    
    # Check configuration
    print(f"📁 Source folder: {main.SOURCE_FOLDER}")
    print(f"🔗 Resume parser URL: {main.RESUME_PARSER_URL}")
    print(f"🎯 Integration enabled: {main.INTEGRATION_ENABLED}")
    
    if not os.path.exists(main.SOURCE_FOLDER):
        print(f"⚠️ Source folder does not exist: {main.SOURCE_FOLDER}")
        return False
    
    return True

def enable_integration():
    """Enable integration in the main.py file"""
    print("🔧 Enabling integration...")
    
    # Read the file
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace INTEGRATION_ENABLED = False with True
    if "INTEGRATION_ENABLED = False" in content:
        content = content.replace("INTEGRATION_ENABLED = False", "INTEGRATION_ENABLED = True")
        
        # Write back to file
        with open("main.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ Integration enabled in main.py")
        return True
    elif "INTEGRATION_ENABLED = True" in content:
        print("✅ Integration is already enabled")
        return True
    else:
        print("❌ Could not find INTEGRATION_ENABLED setting")
        return False

def disable_integration():
    """Disable integration in the main.py file"""
    print("🔧 Disabling integration...")
    
    # Read the file
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace INTEGRATION_ENABLED = True with False
    if "INTEGRATION_ENABLED = True" in content:
        content = content.replace("INTEGRATION_ENABLED = True", "INTEGRATION_ENABLED = False")
        
        # Write back to file
        with open("main.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ Integration disabled in main.py")
        return True
    elif "INTEGRATION_ENABLED = False" in content:
        print("✅ Integration is already disabled")
        return True
    else:
        print("❌ Could not find INTEGRATION_ENABLED setting")
        return False

def run_test():
    """Run a test of the QueryMind system"""
    print("🚀 Running QueryMind test...")
    
    try:
        # Import and run main
        import main
        main.main()
        print("✅ QueryMind test completed successfully")
        return True
    except Exception as e:
        print(f"❌ Error running QueryMind: {e}")
        return False

def show_status():
    """Show current status"""
    print("📊 QueryMind Integration Status")
    print("=" * 40)
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py not found")
        return
    
    # Check integration status
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    if "INTEGRATION_ENABLED = True" in content:
        print("🟢 Integration: ENABLED")
    elif "INTEGRATION_ENABLED = False" in content:
        print("🔴 Integration: DISABLED")
    else:
        print("⚠️ Integration status: UNKNOWN")
    
    # Check resume parser connection
    check_resume_parser_connection()
    
    # Check source folder
    try:
        import main
        if os.path.exists(main.SOURCE_FOLDER):
            file_count = sum(len(files) for _, _, files in os.walk(main.SOURCE_FOLDER))
            print(f"📁 Source folder: {main.SOURCE_FOLDER} ({file_count} files)")
        else:
            print(f"❌ Source folder not found: {main.SOURCE_FOLDER}")
    except ImportError:
        print("❌ Cannot import main module")

def main_menu():
    """Main menu for the setup script"""
    while True:
        print("\n" + "=" * 50)
        print("🎯 QueryMind Integration Manager")
        print("=" * 50)
        print("1. Show current status")
        print("2. Enable integration")
        print("3. Disable integration")
        print("4. Test connection to resume parser")
        print("5. Run QueryMind test")
        print("6. Exit")
        print()
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == "1":
            show_status()
        elif choice == "2":
            enable_integration()
        elif choice == "3":
            disable_integration()
        elif choice == "4":
            check_resume_parser_connection()
        elif choice == "5":
            run_test()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="QueryMind Integration Manager")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--enable", action="store_true", help="Enable integration")
    parser.add_argument("--disable", action="store_true", help="Disable integration")
    parser.add_argument("--test", action="store_true", help="Run test")
    
    args = parser.parse_args()
    
    if args.status:
        show_status()
    elif args.enable:
        enable_integration()
    elif args.disable:
        disable_integration()
    elif args.test:
        run_test()
    else:
        main_menu()
