# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of research_search_shanaka and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.
from typing import Any, Dict, List
import json
import re
import sys
import warnings


# Valid databases that are supported by the system
SUPPORTED_DATABASES = ['PubMed', 'CrossRef', 'arXiv', 'CORE', 'SemanticScholar']

# Databases that require API keys
API_KEY_REQUIRED_DATABASES = ['CORE']

# Databases that have optional API keys but work better with them
API_KEY_OPTIONAL_DATABASES = ['SemanticScholar']


def _validate_date_range(date_range: str) -> None:
    """Validate date range format and values."""
    if not isinstance(date_range, str):
        raise ValueError(
            f"ERROR: 'date_range' must be a string, got {type(date_range).__name__}. "
            f"Expected format: 'YYYY' or 'YYYY-YYYY' (e.g., '2020' or '2015-2025')"
        )
    
    # Check format with regex
    if not re.match(r'^\d{4}(-\d{4})?$', date_range):
        raise ValueError(
            f"ERROR: Invalid date_range format '{date_range}'. "
            f"Expected format: 'YYYY' or 'YYYY-YYYY' (e.g., '2020' or '2015-2025')"
        )
    
    # Parse and validate years
    if '-' in date_range:
        start_year_str, end_year_str = date_range.split('-')
        start_year, end_year = int(start_year_str), int(end_year_str)
        
        if start_year > end_year:
            raise ValueError(
                f"ERROR: Start year ({start_year}) cannot be greater than end year ({end_year}) "
                f"in date_range '{date_range}'"
            )
        
        current_year = 2025  # Set reasonable upper limit
        if start_year < 1800:
            warnings.warn(
                f"WARNING: Start year {start_year} is very early. "
                f"Consider if publications from before 1800 are relevant for your review.",
                UserWarning
            )
        
        if end_year > current_year:
            warnings.warn(
                f"WARNING: End year {end_year} is in the future. "
                f"Publications may not be available beyond {current_year}.",
                UserWarning
            )
    else:
        year = int(date_range)
        if year < 1800:
            warnings.warn(
                f"WARNING: Year {year} is very early. "
                f"Consider if publications from before 1800 are relevant for your review.",
                UserWarning
            )


def _validate_databases(databases: List[str], api_keys: Dict[str, str]) -> None:
    """Validate database list and check API key requirements."""
    if not databases:
        raise ValueError(
            f"ERROR: 'databases' list cannot be empty. "
            f"Must include at least one of: {', '.join(SUPPORTED_DATABASES)}"
        )
    
    invalid_databases = [db for db in databases if db not in SUPPORTED_DATABASES]
    if invalid_databases:
        raise ValueError(
            f"ERROR: Invalid database(s): {', '.join(invalid_databases)}. "
            f"Supported databases are: {', '.join(SUPPORTED_DATABASES)}"
        )
    
    # Check for required API keys
    missing_required_keys = []
    for db in databases:
        if db in API_KEY_REQUIRED_DATABASES and db not in api_keys:
            missing_required_keys.append(db)
    
    if missing_required_keys:
        raise ValueError(
            f"ERROR: Missing required API keys for database(s): {', '.join(missing_required_keys)}. "
            f"Please provide API keys in the 'api_keys' section of your config file."
        )
    
    # Warn about optional API keys
    missing_optional_keys = []
    for db in databases:
        if db in API_KEY_OPTIONAL_DATABASES and db not in api_keys:
            missing_optional_keys.append(db)
    
    if missing_optional_keys:
        warnings.warn(
            f"WARNING: No API keys provided for {', '.join(missing_optional_keys)}. "
            f"These databases work without API keys but may have rate limits or reduced functionality.",
            UserWarning
        )


def _validate_criteria_list(criteria_list: List[str], field_name: str) -> None:
    """Validate inclusion/exclusion criteria lists."""
    if not criteria_list:
        warnings.warn(
            f"WARNING: '{field_name}' list is empty. "
            f"This may result in very broad or very narrow filtering. "
            f"Consider adding appropriate criteria for your systematic review.",
            UserWarning
        )
    
    # Check for common issues
    for criterion in criteria_list:
        if not isinstance(criterion, str):
            raise ValueError(
                f"ERROR: All items in '{field_name}' must be strings, "
                f"got {type(criterion).__name__}: {criterion}"
            )
        
        if not criterion.strip():
            warnings.warn(
                f"WARNING: Empty or whitespace-only criterion found in '{field_name}'. "
                f"This may cause unexpected filtering behavior.",
                UserWarning
            )


def load_config(config_file: str) -> Dict[str, Any]:
    """
    Load, parse, and validate the configuration JSON file.
    
    Performs comprehensive validation of all required and optional fields,
    provides clear error messages for missing or invalid fields, and
    warns about potential configuration issues.
    
    Args:
        config_file: Path to the JSON configuration file
        
    Returns:
        Validated configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file contains invalid JSON
        ValueError: If required fields are missing or have invalid values
    """
    # Load and parse JSON file
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file '{config_file}' not found. "
            f"Please ensure the file exists and the path is correct."
        )
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in configuration file '{config_file}': {e}. "
            f"Please check your JSON syntax (commas, quotes, brackets).",
            e.doc, e.pos
        )
    
    errors = []
    
    # Validate top-level structure
    if not isinstance(input_data, dict):
        errors.append("Configuration file must contain a JSON object at the root level")
    
    if 'initial_prisma_values' not in input_data:
        errors.append("Missing required field 'initial_prisma_values'")
    elif not isinstance(input_data['initial_prisma_values'], dict):
        errors.append("'initial_prisma_values' must be an object/dictionary")
    
    if errors:
        error_message = "Critical configuration errors found:\n" + "\n".join(f"  - {error}" for error in errors)
        raise ValueError(error_message)
    
    criteria = input_data['initial_prisma_values']
    
    # Validate required fields in initial_prisma_values
    required_criteria_fields = ['date_range', 'inclusion_criteria', 'exclusion_criteria']
    for field in required_criteria_fields:
        if field not in criteria:
            errors.append(f"Missing required field '{field}' in initial_prisma_values")
    
    # Validate date_range
    if 'date_range' in criteria:
        try:
            _validate_date_range(criteria['date_range'])
        except ValueError as e:
            errors.append(str(e))
    
    # Validate inclusion_criteria
    if 'inclusion_criteria' in criteria:
        if not isinstance(criteria['inclusion_criteria'], list):
            errors.append(
                f"'inclusion_criteria' must be a list of strings, "
                f"got {type(criteria['inclusion_criteria']).__name__}"
            )
        else:
            try:
                _validate_criteria_list(criteria['inclusion_criteria'], 'inclusion_criteria')
            except ValueError as e:
                errors.append(str(e))
    
    # Validate exclusion_criteria
    if 'exclusion_criteria' in criteria:
        if not isinstance(criteria['exclusion_criteria'], list):
            errors.append(
                f"'exclusion_criteria' must be a list of strings, "
                f"got {type(criteria['exclusion_criteria']).__name__}"
            )
        else:
            try:
                _validate_criteria_list(criteria['exclusion_criteria'], 'exclusion_criteria')
            except ValueError as e:
                errors.append(str(e))
    
    # Validate databases (optional field, defaults to ['PubMed'])
    databases = criteria.get('databases', ['PubMed'])
    if not isinstance(databases, list):
        errors.append(
            f"'databases' must be a list of strings, "
            f"got {type(databases).__name__}"
        )
    
    # Validate research_topic or keywords requirement
    has_topic = bool(input_data.get('research_topic', '').strip())
    has_keywords = bool(input_data.get('keywords'))
    
    if not has_topic and not has_keywords:
        errors.append(
            "Either 'research_topic' (non-empty string) or 'keywords' (non-empty list) "
            "must be provided"
        )
    
    # Validate keywords if provided
    if 'keywords' in input_data:
        keywords = input_data['keywords']
        if not isinstance(keywords, list):
            errors.append(
                f"'keywords' must be a list of strings, "
                f"got {type(keywords).__name__}"
            )
        elif not keywords:
            warnings.warn(
                "WARNING: 'keywords' list is empty. "
                "Ensure 'research_topic' is provided or add keywords.",
                UserWarning
            )
        else:
            for i, keyword in enumerate(keywords):
                if not isinstance(keyword, str):
                    errors.append(
                        f"All keywords must be strings, "
                        f"got {type(keyword).__name__} at index {i}: {keyword}"
                    )
                elif not keyword.strip():
                    warnings.warn(
                        f"WARNING: Empty or whitespace-only keyword at index {i}",
                        UserWarning
                    )
    
    # Validate api_keys if provided
    api_keys = input_data.get('api_keys', {})
    if not isinstance(api_keys, dict):
        errors.append(
            f"'api_keys' must be a dictionary, "
            f"got {type(api_keys).__name__}"
        )
    
    # Report critical errors
    if errors:
        error_message = "Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
        raise ValueError(error_message)
    
    # Validate databases and API keys (after ensuring no critical errors)
    try:
        _validate_databases(databases, api_keys)
    except ValueError as e:
        raise ValueError(str(e))
    
    # Success - provide helpful information
    print(f"✓ Configuration loaded successfully from '{config_file}'")
    
    if has_topic and has_keywords:
        warnings.warn(
            "INFO: Both 'research_topic' and 'keywords' provided. "
            "'keywords' will be used directly, and 'research_topic' will be ignored.",
            UserWarning
        )
    
    print(f"✓ Search will use {len(databases)} database(s): {', '.join(databases)}")
    
    if 'keywords' in input_data and input_data['keywords']:
        print(f"✓ Using {len(input_data['keywords'])} predefined keywords")
    elif has_topic:
        print(f"✓ Will generate keywords from research topic: '{input_data['research_topic']}'")
    
    return input_data
