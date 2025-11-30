import json
import os

# Convert existing JSON file to TXT format
json_file = "processed_files.json"
txt_file = "processed_files.txt"

if os.path.exists(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            processed_files = json.load(f)
        
        # Write to new text file
        with open(txt_file, "w", encoding="utf-8") as f:
            for file_path in sorted(processed_files):
                f.write(f"{file_path}\n")
        
        print(f"✅ Successfully converted {len(processed_files)} entries from JSON to TXT format")
        print(f"📁 Old file: {json_file} ({os.path.getsize(json_file)/1024/1024:.2f} MB)")
        print(f"📁 New file: {txt_file} ({os.path.getsize(txt_file)/1024/1024:.2f} MB)")
        
        # Backup old file
        backup_file = json_file + ".backup"
        os.rename(json_file, backup_file)
        print(f"📦 Backed up old JSON file to: {backup_file}")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
else:
    print(f"❌ JSON file {json_file} not found")
