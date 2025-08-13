"""
QueryMind File Watcher - Automatic Resume Detection
"""
import os
import time
import threading
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import your existing QueryMind functions
from main import process_file, send_cv_to_resume_parser, load_processed_files, save_processed_files

class ResumeFileHandler(FileSystemEventHandler):
    """Handler for file system events to detect new resume files"""
    
    def __init__(self):
        super().__init__()
        self.processed_files = load_processed_files()
        self.pending_files = []
        self.lock = threading.Lock()
        self.stats = {
            'files_detected': 0,
            'cvs_found': 0,
            'cvs_sent_to_parser': 0,
            'errors': 0
        }
        self.last_stats_print = {}
        self.last_activity = time.time()
        
        # Start background processor
        self.processor_thread = threading.Thread(target=self._process_pending_files, daemon=True)
        self.processor_thread.start()
        
        print("🎯 Resume File Handler initialized")
    
    def on_created(self, event):
        """Called when a new file is created"""
        if not event.is_directory:
            self._queue_file_for_processing(event.src_path, "created")
    
    def on_moved(self, event):
        """Called when a file is moved/renamed"""
        if not event.is_directory:
            self._queue_file_for_processing(event.dest_path, "moved")
    
    def on_modified(self, event):
        """Called when a file is modified (with debouncing to avoid duplicates)"""
        if not event.is_directory:
            # Add debouncing to avoid processing the same file multiple times
            current_time = time.time()
            if current_time - self.last_activity > 2:  # Wait 2 seconds between processing
                try:
                    if os.path.exists(event.src_path) and os.path.getsize(event.src_path) > 1024:
                        self._queue_file_for_processing(event.src_path, "modified")
                        self.last_activity = current_time
                except OSError:
                    pass  # File might be in use
    
    def _is_valid_file(self, file_path):
        """Check if file should be processed"""
        if not os.path.exists(file_path):
            return False
        
        if file_path in self.processed_files:
            return False
        
        file_lower = os.path.basename(file_path).lower()
        
        # Check allowed extensions
        allowed_extensions = ['.pdf', '.doc', '.docx', '.rtf', '.txt']
        if not any(file_lower.endswith(ext) for ext in allowed_extensions):
            return False
        
        # Skip temporary files
        skip_prefixes = ['~$', '~', '._']
        if any(file_lower.startswith(prefix) for prefix in skip_prefixes):
            return False
        
        # Check file size (must be larger than 1KB)
        try:
            if os.path.getsize(file_path) < 1024:
                return False
        except OSError:
            return False
        
        return True
    
    def _queue_file_for_processing(self, file_path, event_type):
        """Add file to processing queue with duplicate prevention"""
        if self._is_valid_file(file_path):
            with self.lock:
                if file_path not in self.pending_files:
                    self.pending_files.append(file_path)
                    self.stats['files_detected'] += 1
                    print(f"📄 New file detected ({event_type}): {os.path.basename(file_path)}")
    
    def _process_pending_files(self):
        """Background thread to process queued files"""
        while True:
            time.sleep(8)  # Process every 8 seconds to allow batching
            
            with self.lock:
                if not self.pending_files:
                    continue
                files_to_process = self.pending_files.copy()
                self.pending_files.clear()
            
            if files_to_process:
                print(f"🔄 Processing {len(files_to_process)} new files...")
                self._process_files_batch(files_to_process)
    
    def _process_files_batch(self, file_paths):
        """Process a batch of files"""
        for file_path in file_paths:
            try:
                # Wait a moment to ensure file is completely written
                time.sleep(2)
                
                if not os.path.exists(file_path):
                    continue
                
                print(f"🔍 Analyzing: {os.path.basename(file_path)}")
                
                # Use your existing process_file function
                file_name, result, ocr_flag = process_file(file_path)
                
                # Mark as processed
                self.processed_files.add(file_path)
                
                # If it's a CV, send to resume parser
                if result.startswith("YES"):
                    self.stats['cvs_found'] += 1
                    print(f"✅ CV detected: {file_name} {ocr_flag}")
                    
                    if send_cv_to_resume_parser(file_path, file_name):
                        self.stats['cvs_sent_to_parser'] += 1
                        print(f"🎯 CV sent to resume parser successfully")
                    else:
                        print(f"⚠️ Failed to send CV to resume parser")
                else:
                    print(f"📄 Not a CV: {file_name} ({result})")
                
            except Exception as e:
                self.stats['errors'] += 1
                print(f"❌ Error processing {os.path.basename(file_path)}: {e}")
        
        # Save progress and show stats
        save_processed_files(self.processed_files)
        self._print_stats()
    
    def _print_stats(self):
        """Print current statistics (fixed to avoid duplicates)"""
        # Only print if stats have changed significantly
        if (self.stats != self.last_stats_print and 
            (self.stats['files_detected'] > 0 or self.stats['cvs_found'] > 0)):
            
            print(f"\n📊 Session Statistics:")
            print(f"   📄 Files detected: {self.stats['files_detected']}")
            print(f"   📄 CVs found: {self.stats['cvs_found']}")
            print(f"   🎯 CVs sent to parser: {self.stats['cvs_sent_to_parser']}")
            print(f"   ❌ Errors: {self.stats['errors']}")
            
            if self.stats['cvs_found'] > 0:
                success_rate = (self.stats['cvs_sent_to_parser'] / self.stats['cvs_found']) * 100
                print(f"   📈 Parser success rate: {success_rate:.1f}%")
            
            print(f"   🕒 Last update: {time.strftime('%H:%M:%S')}")
            print()
            
            # Update last printed stats
            self.last_stats_print = self.stats.copy()

class QueryMindWatcher:
    """Main watcher service for QueryMind"""
    
    def __init__(self, watch_folders):
        self.watch_folders = watch_folders
        self.observers = []
        self.file_handler = ResumeFileHandler()
        
    def start_watching(self):
        """Start watching all configured folders"""
        print("🚀 Starting QueryMind File Watcher")
        print("=" * 50)
        
        for folder in self.watch_folders:
            if os.path.exists(folder):
                observer = Observer()
                observer.schedule(self.file_handler, folder, recursive=True)
                observer.start()
                self.observers.append(observer)
                print(f"👀 Watching folder: {folder}")
            else:
                print(f"⚠️ Folder not found: {folder}")
        
        if not self.observers:
            print("❌ No valid folders to watch!")
            return False
        
        print(f"\n✅ Monitoring {len(self.observers)} folders for new resume files...")
        print("🔍 Supported formats: PDF, DOC, DOCX, RTF, TXT")
        print("🎯 Integration with resume parser: ENABLED")
        print("\n💡 The system will automatically:")
        print("   1. Detect new files in watched folders")
        print("   2. Classify them as CV or not using AI")
        print("   3. Send detected CVs to your resume parser")
        print("   4. Track statistics in real-time")
        print("\nPress Ctrl+C to stop monitoring...")
        print()
        
        return True
    
    def stop_watching(self):
        """Stop all file watchers"""
        print("\n🛑 Stopping file watchers...")
        for observer in self.observers:
            observer.stop()
            observer.join()
        print("✅ All watchers stopped")
    
    def run(self):
        """Run the watcher service"""
        if not self.start_watching():
            return
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🔄 Received interrupt signal...")
        finally:
            self.stop_watching()

def main():
    """Main function to run the file watcher"""
    import argparse
    
    parser = argparse.ArgumentParser(description="QueryMind File Watcher")
    parser.add_argument("--folders", nargs="+", help="Folders to watch (space-separated)")
    parser.add_argument("--test", action="store_true", help="Test mode with current DROPPED PROJECTS folder")
    
    args = parser.parse_args()
    
    # Default folders to watch
    if args.folders:
        watch_folders = args.folders
    elif args.test:
        watch_folders = [".\\DROPPED PROJECTS\\"]
    else:
        # Your actual server folders
        watch_folders = [
            r"\\server\MSL-DATA\PROJECTS\INCOMING",
            r"\\server\MSL-DATA\SHARED\NEW_DOCUMENTS",
            r"\\server\MSL-DATA\HR\APPLICATIONS",
            ".\\DROPPED PROJECTS\\"  # Test folder
        ]
    
    print("🎯 QueryMind Automatic Resume Detection Service")
    print("=" * 50)
    print("Folders to monitor:")
    for folder in watch_folders:
        status = "✅" if os.path.exists(folder) else "❌"
        print(f"  {status} {folder}")
    print()
    
    # Create and run watcher
    watcher = QueryMindWatcher(watch_folders)
    watcher.run()

if __name__ == "__main__":
    main()
