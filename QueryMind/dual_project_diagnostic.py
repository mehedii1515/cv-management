import os
import sys
import requests
import json
from pathlib import Path

def check_querymind_libraries():
    """Check QueryMind's document processing libraries"""
    print("🔍 Checking QueryMind Libraries...")
    
    try:
        # Ensure we're in the QueryMind directory
        current_dir = os.getcwd()
        if not current_dir.endswith('QueryMind'):
            print(f"⚠️ Current directory: {current_dir}")
            print("💡 Please run this script from the QueryMind directory")
        
        # Try to import QueryMind modules
        try:
            from Include import Filestream as fs
            print("✅ QueryMind Include.Filestream imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import QueryMind modules: {e}")
            return False, f"Import error: {e}"
        
        # Find a .doc file for testing
        test_file = find_doc_file()
        if not test_file:
            print("❌ No .doc files found for testing")
            return False, "No test files available"
        
        print(f"📄 Testing QueryMind with: {os.path.basename(test_file)}")
        
        try:
            text = fs.Extract_Text_From_File(test_file)
            if text and len(text.strip()) > 10:
                print(f"✅ QueryMind extracted {len(text)} characters from .doc")
                print(f"📝 Sample text: {text[:100]}...")
                return True, f"Extracted {len(text)} characters"
            else:
                print(f"❌ QueryMind extracted little/no text from .doc")
                print(f"📝 Extracted: '{text[:50] if text else 'None'}'")
                return False, f"Poor extraction: '{text[:50] if text else 'None'}'"
        except Exception as e:
            print(f"❌ QueryMind .doc extraction error: {e}")
            return False, f"Extraction error: {e}"
            
    except Exception as e:
        print(f"❌ QueryMind library check error: {e}")
        return False, f"Library check error: {e}"

def find_doc_file():
    """Find a .doc file for testing"""
    search_paths = [
        "./DROPPED PROJECTS/",
        "../DROPPED PROJECTS/",
        "./test_files/",
        "./"
    ]
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.lower().endswith('.doc') and not file.startswith('~'):
                        return os.path.join(root, file)
    return None

def check_resume_parser_libraries():
    """Check Resume Parser backend libraries"""
    print("\n🔍 Checking Resume Parser Backend...")
    
    try:
        # Find the backend directory
        possible_backend_paths = [
            "../backend/",
            "../../backend/",
            "../Resume Parser/backend/",
            "./backend/"
        ]
        
        backend_path = None
        for path in possible_backend_paths:
            if os.path.exists(path):
                backend_path = os.path.abspath(path)
                break
        
        if not backend_path:
            print("❌ Backend directory not found")
            print(f"💡 Searched paths: {possible_backend_paths}")
            return False, "Backend directory not found"
        
        print(f"✅ Found backend directory: {backend_path}")
        
        # Check backend requirements.txt
        backend_req_file = os.path.join(backend_path, "requirements.txt")
        if os.path.exists(backend_req_file):
            with open(backend_req_file, 'r', encoding='utf-8') as f:
                requirements = f.read()
            
            print("📋 Resume Parser backend requirements.txt contains:")
            doc_related = []
            all_packages = []
            
            for line in requirements.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    all_packages.append(line)
                    if any(keyword in line.lower() for keyword in ['doc', 'pdf', 'text', 'extract', 'spire', 'pypdf', 'docx']):
                        doc_related.append(line)
                        print(f"   📦 {line}")
            
            print(f"📊 Total packages: {len(all_packages)}")
            print(f"📊 Document-related packages: {len(doc_related)}")
            
            if not doc_related:
                print("⚠️ No obvious document processing libraries found")
                
            return True, {
                'total_packages': len(all_packages),
                'doc_packages': doc_related,
                'all_packages': all_packages
            }
        else:
            print(f"❌ No requirements.txt found at: {backend_req_file}")
            
            # Check if there are other requirement files
            req_files = []
            for file in os.listdir(backend_path):
                if 'requirements' in file.lower() or 'req' in file.lower():
                    req_files.append(file)
            
            if req_files:
                print(f"💡 Found other requirement files: {req_files}")
            
            return False, "No requirements.txt found"
            
    except Exception as e:
        print(f"❌ Error checking Resume Parser: {e}")
        return False, f"Check error: {e}"

def test_resume_parser_connection():
    """Test if Resume Parser backend is running"""
    print("\n🔍 Testing Resume Parser Connection...")
    
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        print(f"✅ Resume Parser backend is running (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Resume Parser backend not running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Connection test error: {e}")
        return False

def test_doc_upload_to_backend():
    """Test uploading a .doc file to Resume Parser backend"""
    print("\n🔍 Testing .doc File Upload to Resume Parser...")
    
    # Check if backend is running first
    if not test_resume_parser_connection():
        return False
    
    test_file = find_doc_file()
    if not test_file:
        print("❌ No .doc files found for testing")
        return False
    
    print(f"📄 Testing upload: {os.path.basename(test_file)}")
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': (os.path.basename(test_file), f, 'application/msword')}
            data = {
                'source': 'DiagnosticTest',
                'parse_immediately': True
            }
            
            response = requests.post(
                "http://localhost:8000/api/resumes/upload/",
                files=files,
                data=data,
                timeout=60
            )
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print("✅ Upload successful!")
                    
                    # Check what was returned
                    result_str = str(result).lower()
                    if any(key in result_str for key in ['name', 'email', 'phone', 'text']):
                        print("✅ Resume parsing appears successful")
                        print(f"📄 Response keys: {list(result.keys()) if isinstance(result, dict) else 'Non-dict response'}")
                        return True
                    else:
                        print("⚠️ Upload successful but parsing may have failed")
                        print(f"📄 Response: {str(result)[:200]}...")
                        return False
                        
                except json.JSONDecodeError:
                    print("⚠️ Upload successful but got non-JSON response")
                    print(f"📄 Response: {response.text[:200]}...")
                    return False
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"📄 Error: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Upload test error: {e}")
        return False

def compare_requirements():
    """Compare requirements between QueryMind and Resume Parser"""
    print("\n🔍 Comparing Project Requirements...")
    
    # QueryMind requirements
    qm_req_file = "./requirements.txt"
    qm_packages = set()
    
    if os.path.exists(qm_req_file):
        try:
            with open(qm_req_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Extract package name (before == or >= etc.)
                        pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                        qm_packages.add(pkg_name.lower())
            print(f"📦 QueryMind: {len(qm_packages)} packages")
        except Exception as e:
            print(f"❌ Error reading QueryMind requirements: {e}")
    else:
        print("❌ QueryMind requirements.txt not found")
    
    # Resume Parser requirements
    backend_req_file = None
    for path in ["../backend/requirements.txt", "../../backend/requirements.txt"]:
        if os.path.exists(path):
            backend_req_file = path
            break
    
    rp_packages = set()
    if backend_req_file:
        try:
            with open(backend_req_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                        rp_packages.add(pkg_name.lower())
            print(f"📦 Resume Parser: {len(rp_packages)} packages")
        except Exception as e:
            print(f"❌ Error reading Resume Parser requirements: {e}")
    else:
        print("❌ Resume Parser requirements.txt not found")
    
    if qm_packages and rp_packages:
        common = qm_packages & rp_packages
        qm_only = qm_packages - rp_packages
        rp_only = rp_packages - qm_packages
        
        print(f"\n📊 Package Analysis:")
        print(f"   🔗 Common: {len(common)}")
        print(f"   🔵 QueryMind only: {len(qm_only)}")
        print(f"   🟣 Resume Parser only: {len(rp_only)}")
        
        # Document processing packages
        doc_keywords = ['doc', 'pdf', 'text', 'extract', 'spire', 'pypdf', 'docx', 'antiword', 'textract']
        
        print(f"\n📄 Document Processing Packages:")
        qm_doc = [pkg for pkg in qm_packages if any(keyword in pkg for keyword in doc_keywords)]
        rp_doc = [pkg for pkg in rp_packages if any(keyword in pkg for keyword in doc_keywords)]
        
        print(f"   🔵 QueryMind: {qm_doc}")
        print(f"   🟣 Resume Parser: {rp_doc}")
        
        return {
            'qm_packages': qm_packages,
            'rp_packages': rp_packages,
            'qm_doc': qm_doc,
            'rp_doc': rp_doc
        }
    
    return None

def main():
    """Main diagnostic function"""
    print("🔧 Dual Project .doc File Diagnostic Tool")
    print("=" * 60)
    print(f"📍 Current directory: {os.getcwd()}")
    print(f"📍 Python path: {sys.executable}")
    print("=" * 60)
    
    results = {}
    
    # Test 1: QueryMind capabilities
    print("\n1️⃣ QUERYMIND ANALYSIS")
    print("-" * 30)
    qm_works, qm_details = check_querymind_libraries()
    results['querymind'] = {'works': qm_works, 'details': qm_details}
    
    # Test 2: Resume Parser setup
    print("\n2️⃣ RESUME PARSER ANALYSIS")
    print("-" * 30)
    rp_works, rp_details = check_resume_parser_libraries()
    results['resume_parser'] = {'works': rp_works, 'details': rp_details}
    
    # Test 3: Backend connection
    print("\n3️⃣ BACKEND CONNECTION")
    print("-" * 30)
    backend_running = test_resume_parser_connection()
    results['backend_running'] = backend_running
    
    # Test 4: Upload test
    print("\n4️⃣ UPLOAD TEST")
    print("-" * 30)
    upload_works = test_doc_upload_to_backend()
    results['upload_test'] = upload_works
    
    # Test 5: Requirements comparison
    print("\n5️⃣ REQUIREMENTS COMPARISON")
    print("-" * 30)
    req_comparison = compare_requirements()
    results['requirements'] = req_comparison
    
    # Final Analysis
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    print(f"🔵 QueryMind .doc processing: {'✅ WORKING' if qm_works else '❌ FAILED'}")
    print(f"🟣 Resume Parser setup: {'✅ FOUND' if rp_works else '❌ NOT FOUND'}")
    print(f"🌐 Backend connection: {'✅ RUNNING' if backend_running else '❌ NOT RUNNING'}")
    print(f"📤 Upload test: {'✅ SUCCESS' if upload_works else '❌ FAILED'}")
    
    print(f"\n💡 RECOMMENDATIONS:")
    if not qm_works:
        print("   1. Fix QueryMind's .doc processing (check Include/Filestream.py)")
    if not rp_works:
        print("   2. Check Resume Parser backend requirements.txt location")
    if not backend_running:
        print("   3. Start Resume Parser backend: python manage.py runserver")
    if qm_works and backend_running and not upload_works:
        print("   4. Resume Parser backend needs .doc processing libraries")
        print("   5. Check Django logs for specific errors")
    
    if qm_works and upload_works:
        print("   ✅ Both systems work - integration should be successful!")
    
    return results

if __name__ == "__main__":
    try:
        results = main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Diagnostic interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Diagnostic failed with error: {e}")
        import traceback
        traceback.print_exc()