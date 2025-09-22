# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of literature_search and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.
# src/literature_search/utils.py
import time
import requests
from typing import Optional, Dict

def robust_get(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, max_retries: int = 5) -> Optional[requests.Response]:
    """HTTP GET with retries and exponential backoff."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                return response
            else:
                wait = 2 ** attempt
                print(f"Request failed {url} (status {response.status_code}), retrying in {wait}s...")
                time.sleep(wait)
        except Exception as e:
            wait = 2 ** attempt
            print(f"Request error {url}: {e}, retrying in {wait}s...")
            time.sleep(wait)
    print(f"Failed to get a valid response from {url} after {max_retries} attempts.")
    return None
