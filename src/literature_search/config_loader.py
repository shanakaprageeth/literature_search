# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of literature_search and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.
from typing import Any, Dict
import json
import os
import sys


def load_config(config_file: str) -> Dict[str, Any]:
    """Load, parse, and validate the config JSON file.
    
    Provides user-friendly error messages and exits gracefully on validation failures.
    
    Args:
        config_file: Path to the JSON configuration file
        
    Returns:
        Dict containing validated configuration data
        
    Raises:
        SystemExit: On any validation failure with descriptive error message
    """
    # Check if file exists
    if not os.path.exists(config_file):
        print(f"ERROR: Configuration file '{config_file}' not found.", file=sys.stderr)
        print("Please ensure the file path is correct and the file exists.", file=sys.stderr)
        sys.exit(1)
    
    # Try to parse JSON
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in configuration file '{config_file}':", file=sys.stderr)
        print(f"  {e}", file=sys.stderr)
        print("Please check the JSON syntax and ensure it's properly formatted.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Could not read configuration file '{config_file}': {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate required top-level fields
    if not isinstance(input_data, dict):
        print("ERROR: Configuration file must contain a JSON object (not array or primitive).", file=sys.stderr)
        sys.exit(1)
    
    if 'initial_prisma_values' not in input_data:
        print("ERROR: Missing required field 'initial_prisma_values' in configuration file.", file=sys.stderr)
        print("The configuration must include PRISMA methodology parameters.", file=sys.stderr)
        print("Please refer to the sample_input.json for the correct format.", file=sys.stderr)
        sys.exit(1)
    
    criteria = input_data['initial_prisma_values']
    if not isinstance(criteria, dict):
        print("ERROR: 'initial_prisma_values' must be a JSON object.", file=sys.stderr)
        sys.exit(1)
    
    # Validate required criteria fields with helpful messages
    required_fields = [
        ('date_range', "Date range for literature search (e.g., '2015-2025')"),
        ('inclusion_criteria', "List of inclusion criteria for literature selection"),
        ('exclusion_criteria', "List of exclusion criteria for literature selection")
    ]
    
    for field, description in required_fields:
        if field not in criteria:
            print(f"ERROR: Missing required field '{field}' in initial_prisma_values.", file=sys.stderr)
            print(f"This field should contain: {description}", file=sys.stderr)
            sys.exit(1)
    
    # Validate field types
    if not isinstance(criteria['inclusion_criteria'], list):
        print("ERROR: 'inclusion_criteria' must be a list of strings in initial_prisma_values.", file=sys.stderr)
        print("Example: [\"review\", \"thesis\", \"journal\", \"book\"]", file=sys.stderr)
        sys.exit(1)
    
    if not isinstance(criteria['exclusion_criteria'], list):
        print("ERROR: 'exclusion_criteria' must be a list of strings in initial_prisma_values.", file=sys.stderr)
        print("Example: [\"non-english\", \"conference\"]", file=sys.stderr)
        sys.exit(1)
    
    if 'databases' in criteria and not isinstance(criteria['databases'], list):
        print("ERROR: 'databases' must be a list of database names in initial_prisma_values.", file=sys.stderr)
        print("Example: [\"PubMed\", \"CrossRef\", \"arXiv\", \"CORE\", \"SemanticScholar\"]", file=sys.stderr)
        sys.exit(1)
    
    # Validate research_topic or keywords
    has_topic = bool(input_data.get('research_topic', '').strip())
    has_keywords = bool(input_data.get('keywords'))
    
    if not has_topic and not has_keywords:
        print("ERROR: Either 'research_topic' or 'keywords' must be provided in configuration file.", file=sys.stderr)
        print("  - research_topic: A descriptive topic for auto-generating keywords", file=sys.stderr)
        print("  - keywords: A list or comma-separated string of specific search terms", file=sys.stderr)
        sys.exit(1)
    
    # Process keywords field - handle both list and comma-separated string
    if 'keywords' in input_data:
        keywords = input_data['keywords']
        if isinstance(keywords, str):
            # Convert comma-separated string to list and strip whitespace
            keywords_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
            if not keywords_list:
                print("WARNING: Empty keywords string provided, will auto-generate from research topic.", file=sys.stderr)
                if not has_topic:
                    print("ERROR: No valid keywords found and no research topic provided.", file=sys.stderr)
                    sys.exit(1)
            input_data['keywords'] = keywords_list
        elif isinstance(keywords, list):
            # Ensure all keywords are strings and strip whitespace
            keywords_list = [str(kw).strip() for kw in keywords if str(kw).strip()]
            if not keywords_list:
                print("WARNING: Empty keywords list provided, will auto-generate from research topic.", file=sys.stderr)
                if not has_topic:
                    print("ERROR: No valid keywords found and no research topic provided.", file=sys.stderr)
                    sys.exit(1)
            input_data['keywords'] = keywords_list
        else:
            print("ERROR: 'keywords' must be a list or comma-separated string.", file=sys.stderr)
            print("Examples:", file=sys.stderr)
            print("  List format: [\"machine learning\", \"deep learning\"]", file=sys.stderr)
            print("  String format: \"machine learning, deep learning\"", file=sys.stderr)
            sys.exit(1)
    
    # Validate api_keys if present
    if 'api_keys' in input_data and not isinstance(input_data['api_keys'], dict):
        print("ERROR: 'api_keys' must be a dictionary if provided.", file=sys.stderr)
        print("Example: {\"CORE\": \"your_api_key\", \"SemanticScholar\": \"your_api_key\"}", file=sys.stderr)
        sys.exit(1)
    
    # Validate date_range format
    date_range = criteria['date_range']
    if not isinstance(date_range, str):
        print("ERROR: 'date_range' must be a string.", file=sys.stderr)
        print("Examples: \"2015-2025\", \"2020\"", file=sys.stderr)
        sys.exit(1)
    
    # Try to parse date range
    try:
        if '-' in date_range:
            start_str, end_str = date_range.split('-', 1)
            start_year = int(start_str.strip())
            end_year = int(end_str.strip())
            if start_year > end_year:
                print(f"ERROR: Invalid date range '{date_range}' - start year cannot be greater than end year.", file=sys.stderr)
                sys.exit(1)
        else:
            year = int(date_range.strip())
            if year < 1000 or year > 9999:
                print(f"ERROR: Invalid year '{date_range}' - must be a 4-digit year.", file=sys.stderr)
                sys.exit(1)
    except ValueError:
        print(f"ERROR: Invalid date range format '{date_range}'.", file=sys.stderr)
        print("Valid formats: \"2015-2025\" or \"2020\"", file=sys.stderr)
        sys.exit(1)
    
    # Return validated config
    return input_data
