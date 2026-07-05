#!/usr/bin/env python3
import shutil
from pathlib import Path
from datetime import datetime, timedelta

SHARED_DIR = Path.home() / "초보프로젝트" / "hermes-ag-shared"
MESSAGES_DIR = SHARED_DIR / "messages"
ARCHIVE_DIR = SHARED_DIR / "archive"

DAYS_TO_KEEP = 7

def cleanup_old_archives():
    if not ARCHIVE_DIR.exists():
        print("아카이브 폴더가 없습니다.")
        return

    cutoff_date = datetime.now() - timedelta(days=DAYS_TO_KEEP)
    deleted_count = 0

    for file in ARCHIVE_DIR.glob("*.md"):
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        if mtime < cutoff_date:
            file.unlink()
            print(f"삭제: {file.name} (수정일: {mtime.date()})")
            deleted_count += 1

    print(f"총 {deleted_count}개 파일 삭제 완료")

def archive_processed_messages():
    if not MESSAGES_DIR.exists():
        print("메시지 폴더가 없습니다.")
        return

    moved_count = 0
    for file in MESSAGES_DIR.glob("*.md"):
        dest = ARCHIVE_DIR / file.name
        shutil.move(str(file), str(dest))
        print(f"이동: {file.name} → archive/")
        moved_count += 1

    print(f"총 {moved_count}개 파일 아카이브 완료")

def main():
    print(f"[{datetime.now()}] MadCat Cleanup 시작")
    print("-" * 50)

    print("\n1. 처리 완료 메시지 아카이브")
    archive_processed_messages()

    print(f"\n2. {DAYS_TO_KEEP}일 이상 된 아카이브 삭제")
    cleanup_old_archives()

    print("\n" + "=" * 50)
    print("정리 완료!")

if __name__ == "__main__":
    main()