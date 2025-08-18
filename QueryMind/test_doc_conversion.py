"""
Test script to verify DOC to DOCX conversion functionality
"""
import os
import sys
sys.path.append('Include')

import Include.Filestream as fs

def test_doc_conversion():
    """Test DOC to DOCX conversion"""
    print("🧪 Testing DOC to DOCX conversion...")
    
    # Look for a test DOC file in DROPPED PROJECTS
    test_folder = "DROPPED PROJECTS"
    if not os.path.exists(test_folder):
        print(f"❌ Test folder '{test_folder}' not found")
        return False
    
    # Find a .doc file
    doc_file = None
    for root, dirs, files in os.walk(test_folder):
        for file in files:
            if file.lower().endswith('.doc') and not file.startswith('~$'):
                doc_file = os.path.join(root, file)
                break
        if doc_file:
            break
    
    if not doc_file:
        print("❌ No .doc test file found in DROPPED PROJECTS")
        return False
    
    print(f"📄 Testing with file: {os.path.basename(doc_file)}")
    
    # Test conversion
    try:
        docx_content = fs.Convert_DOC_to_DOCX(doc_file)
        
        if docx_content:
            print(f"✅ Conversion successful! Generated {len(docx_content)} bytes of DOCX data")
            
            # Test if we can also extract text from original for comparison
            original_text = fs.Extract_Text_From_DOC(doc_file)
            print(f"📝 Original text length: {len(original_text)} characters")
            
            return True
        else:
            print("❌ Conversion failed - no DOCX content generated")
            return False
            
    except Exception as e:
        print(f"❌ Conversion error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 QueryMind DOC to DOCX Conversion Test")
    print("=" * 50)
    
    success = test_doc_conversion()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("🎯 QueryMind is now ready to convert DOC files to DOCX for better AI parsing")
    else:
        print("\n❌ Test failed!")
        print("⚠️ Check Spire.doc installation and test file availability")
