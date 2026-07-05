#!/usr/bin/env python3
import time
from pathlib import Path
from datetime import datetime

SHARED_DIR = Path.home() / "초보프로젝트" / "hermes-ag-shared"
MESSAGES_DIR = SHARED_DIR / "messages"

file_mtimes = {}

def check_changes():
    if not MESSAGES_DIR.exists():
        print(f"[{datetime.now()}] Messages directory not found: {MESSAGES_DIR}")
        return

    current_files = {}
    for file in MESSAGES_DIR.glob("*.md"):
        stat = file.stat()
        current_files[file.name] = stat.st_mtime

    for filename, mtime in current_files.items():
        if filename not in file_mtimes:
            print(f"[{datetime.now()}] 🆕 새 메시지 발견: {filename}")
            file_mtimes[filename] = mtime
        elif mtime > file_mtimes[filename]:
            print(f"[{datetime.now()}] 📝 메시지 수정됨: {filename}")
            file_mtimes[filename] = mtime

    deleted = [f for f in file_mtimes.keys() if f not in current_files]
    for filename in deleted:
        print(f"[{datetime.now()}] 🗑️ 메시지 삭제됨: {filename}")
        del file_mtimes[filename]

def main():
    print(f"[{datetime.now()}] MadCat Watcher 시작")
    print(f"감시 폴더: {MESSAGES_DIR}")
    print(f"체크 간격: 60초")
    print("-" * 50)

    while True:
        try:
            check_changes()
            time.sleep(60)
        except KeyboardInterrupt:
            print(f"\n[{datetime.now()}] Watcher 종료")
            break
        except Exception as e:
            print(f"[{datetime.now()}] 에러: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()