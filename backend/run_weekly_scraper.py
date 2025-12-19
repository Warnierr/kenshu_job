#!/usr/bin/env python
"""
Script standalone pour lancer le scraper hebdomadaire.

Usage:
    python run_weekly_scraper.py

Ou avec Windows Task Scheduler:
    C:\path\to\venv\Scripts\python.exe C:\path\to\backend\run_weekly_scraper.py
"""
import sys
from pathlib import Path

# Ajouter le dossier backend au path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.scheduler.weekly_scraper import run_weekly_scraper

if __name__ == "__main__":
    print("=" * 60)
    print("WEEKLY JOB SCRAPER")
    print("=" * 60)
    
    result = run_weekly_scraper()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Scraped: {result['scraped']} jobs")
    print(f"✅ Stored: {result['stored']} unique jobs")
    
    if result['errors']:
        print(f"⚠️  Errors: {len(result['errors'])}")
        for err in result['errors'][:10]:
            print(f"   - {err}")
    else:
        print("✅ No errors!")
    
    print("=" * 60)
    
    # Exit code pour monitoring externe
    sys.exit(0 if not result['errors'] else 1)

