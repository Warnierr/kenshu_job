#!/usr/bin/env python
"""
Script de test rapide pour vérifier que tous les connecteurs fonctionnent.

Usage:
    python test_scraper.py
"""
import sys
from pathlib import Path

# Ajouter backend au path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.connectors import (
    fetch_adzuna,
    fetch_apec,
    fetch_eures,
    fetch_france_travail,
    fetch_indeed,
    fetch_scraping,
)


def test_connector(name: str, fetch_func, *args, **kwargs):
    """Test un connecteur."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print('='*60)
    try:
        jobs = fetch_func(*args, **kwargs)
        print(f"[OK] Success: {len(jobs)} jobs found")
        
        if jobs:
            job = jobs[0]
            print(f"\nSample job:")
            print(f"  Title: {job.title}")
            print(f"  Company: {job.company}")
            print(f"  Location: {job.city}, {job.country}")
            print(f"  Remote: {job.remote_type}")
            print(f"  Contract: {job.contract_type}")
            if job.salary_min:
                print(f"  Salary: {job.salary_min}-{job.salary_max} {job.currency}/{job.salary_period}")
            print(f"  URL: {job.apply_url[:80]}...")
        
        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False


def main():
    print("\n" + "TESTING ALL JOB CONNECTORS".center(60))
    
    results = {}
    
    # Test stubs (devraient marcher)
    results["France Travail (stub)"] = test_connector(
        "France Travail API (stub)", 
        fetch_france_travail, 
        "python developer"
    )
    
    results["Adzuna (stub)"] = test_connector(
        "Adzuna API (stub)", 
        fetch_adzuna, 
        "python developer", 
        country="fr"
    )
    
    results["EURES (stub)"] = test_connector(
        "EURES API (stub)", 
        fetch_eures, 
        "python developer", 
        country="fr"
    )
    
    # Test scraping (peut échouer selon structure sites)
    results["Scraping (WTTJ + Remotive)"] = test_connector(
        "Generic Scraping", 
        fetch_scraping, 
        "python", 
        country="fr"
    )
    
    results["APEC"] = test_connector(
        "APEC (Cadres France)", 
        fetch_apec, 
        "python developer", 
        limit=10
    )
    
    results["Indeed"] = test_connector(
        "Indeed France", 
        fetch_indeed, 
        "python developer", 
        location="France", 
        limit=10
    )
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY".center(60))
    print("="*60)
    
    success_count = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, success in results.items():
        status = "[OK]" if success else "[FAIL]"
        print(f"{status} {name}")
    
    print("\n" + f"Success: {success_count}/{total}".center(60))
    
    if success_count == total:
        print("\n*** All connectors working! ***\n")
    else:
        print(f"\n*** {total - success_count} connector(s) failed ***\n")
        print("Note: Scraping failures are normal if site structure changed.")
        print("Check logs above for details.\n")


if __name__ == "__main__":
    main()

