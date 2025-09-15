# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of research_search_shanaka and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.
from typing import Any, Dict
import json

def load_config(config_file: str) -> Dict[str, Any]:
    """Load, parse, and validate the config JSON file. Raises ValueError if invalid."""
    with open(config_file, 'r') as f:
        input_data = json.load(f)
    # Validate required top-level fields
    if 'initial_prisma_values' not in input_data:
        raise ValueError("Missing 'initial_prisma_values' in config file.")
    criteria = input_data['initial_prisma_values']
    # Validate required criteria fields
    if 'date_range' not in criteria:
        raise ValueError("Missing 'date_range' in initial_prisma_values.")
    if 'inclusion_criteria' not in criteria or not isinstance(criteria['inclusion_criteria'], list):
        raise ValueError("'inclusion_criteria' must be a list in initial_prisma_values.")
    if 'exclusion_criteria' not in criteria or not isinstance(criteria['exclusion_criteria'], list):
        raise ValueError("'exclusion_criteria' must be a list in initial_prisma_values.")
    if 'databases' in criteria and not isinstance(criteria['databases'], list):
        raise ValueError("'databases' must be a list in initial_prisma_values if provided.")
    # Validate research_topic or keywords
    if not input_data.get('research_topic') and not input_data.get('keywords'):
        raise ValueError("Either 'research_topic' or 'keywords' must be provided in config file.")
    
    # Process keywords field - handle both list and comma-separated string
    if 'keywords' in input_data:
        keywords = input_data['keywords']
        if isinstance(keywords, str):
            # Convert comma-separated string to list and strip whitespace
            input_data['keywords'] = [kw.strip() for kw in keywords.split(',') if kw.strip()]
        elif isinstance(keywords, list):
            # Ensure all keywords are strings and strip whitespace
            input_data['keywords'] = [str(kw).strip() for kw in keywords if str(kw).strip()]
        else:
            raise ValueError("'keywords' must be a list or comma-separated string.")
    
    # Optionally validate api_keys
    if 'api_keys' in input_data and not isinstance(input_data['api_keys'], dict):
        raise ValueError("'api_keys' must be a dictionary if provided.")
    # Return validated config
    return input_data
