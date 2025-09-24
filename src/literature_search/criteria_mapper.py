# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of literature_search and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.

from typing import List, Dict, Any


# Database-specific field mappings for inclusion/exclusion criteria
DATABASE_FIELD_MAPPINGS = {
    'PubMed': {
        # Map user criteria to database-specific fields
        'type': 'Type',
        'publication_type': 'Type',
        'pubtype': 'Type',
        'language': 'Language',
        'source': 'Source',
        'journal': 'Journal',
        'authors': 'Authors'
    },
    'CrossRef': {
        'type': 'Type',
        'publication_type': 'Type',
        'language': 'Language',
        'source': 'Source',
        'journal': 'Journal',
        'authors': 'Authors'
    },
    'arXiv': {
        'type': 'Type',
        'publication_type': 'Type',
        'language': 'Language',
        'source': 'Source',
        'journal': 'Journal',
        'authors': 'Authors'
    },
    'CORE': {
        'type': 'Type',
        'publication_type': 'Type',
        'document_type': 'Type',
        'language': 'Language',
        'source': 'Source',
        'journal': 'Journal',
        'authors': 'Authors'
    },
    'SemanticScholar': {
        'type': 'Type',
        'publication_type': 'Type',
        'language': 'Language',
        'source': 'Source',
        'journal': 'Journal',
        'venue': 'Journal',
        'authors': 'Authors'
    },
    'IEEE': {
        'type': 'Type',
        'publication_type': 'Type',
        'content_type': 'Type',
        'language': 'Language',
        'source': 'Source',
        'journal': 'Journal',
        'publication_title': 'Journal',
        'authors': 'Authors'
    },
    'Springer': {
        'type': 'Type',
        'publication_type': 'Type',
        'content_type': 'Type',
        'language': 'Language',
        'source': 'Source',
        'journal': 'Journal',
        'publication_name': 'Journal',
        'authors': 'Authors'
    },
    'DBLP': {
        'type': 'Type',
        'publication_type': 'Type',
        'language': 'Language',
        'source': 'Source',
        'journal': 'Journal',
        'venue': 'Journal',
        'authors': 'Authors'
    },
    'Scopus': {
        'type': 'Type',
        'publication_type': 'Type',
        'aggregation_type': 'Type',
        'language': 'Language',
        'source': 'Source',
        'journal': 'Journal',
        'publication_name': 'Journal',
        'authors': 'Authors'
    }
}


def get_database_name_from_source(source: str) -> str:
    """
    Map publication source to standardized database name.
    
    Args:
        source: Source field from publication
        
    Returns:
        Standardized database name for mapping
    """
    source_lower = source.lower()
    
    # Europe PMC can have different source values
    if source_lower in ['med', 'pmc', 'pmcid']:
        return 'PubMed'
    elif source_lower == 'crossref':
        return 'CrossRef'
    elif source_lower == 'arxiv':
        return 'arXiv'
    elif source_lower == 'core':
        return 'CORE'
    elif source_lower == 'semanticscholar':
        return 'SemanticScholar'
    elif source_lower == 'ieee':
        return 'IEEE'
    elif source_lower == 'springer':
        return 'Springer'
    elif source_lower == 'dblp':
        return 'DBLP'
    elif source_lower == 'scopus':
        return 'Scopus'
    else:
        # Default to PubMed for backward compatibility
        return 'PubMed'


def get_mapped_field_for_criteria(db_name: str, criteria_field: str) -> str:
    """
    Get the mapped publication field name for a given database and criteria field.
    
    Args:
        db_name: Name of the database (PubMed, CrossRef, etc.)
        criteria_field: The field name used in criteria (type, language, etc.)
    
    Returns:
        The publication field name to check against, defaults to 'Type' for backward compatibility
    """
    mapping = DATABASE_FIELD_MAPPINGS.get(db_name, {})
    return mapping.get(criteria_field.lower(), 'Type')


def parse_criteria_with_fields(criteria_list: List[str]) -> List[Dict[str, str]]:
    """
    Parse criteria to extract field specifications and values.
    
    Supports formats like:
    - "journal article" (defaults to type field)
    - "type:journal article" 
    - "language:english"
    - "source:pubmed"
    
    Args:
        criteria_list: List of criteria strings
    
    Returns:
        List of dictionaries with 'field' and 'value' keys
    """
    parsed_criteria = []
    
    for criteria in criteria_list:
        criteria = criteria.strip()
        if ':' in criteria:
            field, value = criteria.split(':', 1)
            parsed_criteria.append({
                'field': field.strip().lower(),
                'value': value.strip().lower()
            })
        else:
            # Default to 'type' field for backward compatibility
            parsed_criteria.append({
                'field': 'type',
                'value': criteria.lower()
            })
    
    return parsed_criteria


def check_criteria_match(publication: Dict[str, Any], criteria_list: List[str], db_name: str = None) -> bool:
    """
    Check if a publication matches the given criteria.
    
    Args:
        publication: Publication metadata dictionary
        criteria_list: List of criteria strings (inclusion or exclusion)
        db_name: Database name for field mapping (optional, will be derived from Source if not provided)
    
    Returns:
        True if any criteria matches, False otherwise
    """
    if not criteria_list:
        return True  # No criteria means all match
    
    # Get database name from publication source if not provided
    if db_name is None:
        db_name = get_database_name_from_source(publication.get('Source', ''))
    
    parsed_criteria = parse_criteria_with_fields(criteria_list)
    
    for criteria in parsed_criteria:
        field_name = get_mapped_field_for_criteria(db_name, criteria['field'])
        pub_value = str(publication.get(field_name, '')).lower()
        
        if criteria['value'] in pub_value:
            return True
    
    return False


def get_criteria_mismatch_reasons(publication: Dict[str, Any], criteria_list: List[str], criteria_type: str, db_name: str = None) -> List[str]:
    """
    Get reasons why criteria don't match for a publication.
    
    Args:
        publication: Publication metadata dictionary
        criteria_list: List of criteria strings
        criteria_type: 'inclusion' or 'exclusion' for better error messages
        db_name: Database name for field mapping (optional, will be derived from Source if not provided)
    
    Returns:
        List of reason strings explaining why criteria don't match
    """
    if not criteria_list:
        return []
    
    # Get database name from publication source if not provided
    if db_name is None:
        db_name = get_database_name_from_source(publication.get('Source', ''))
    
    reasons = []
    parsed_criteria = parse_criteria_with_fields(criteria_list)
    
    for criteria in parsed_criteria:
        field_name = get_mapped_field_for_criteria(db_name, criteria['field'])
        pub_value = str(publication.get(field_name, '')).lower()
        
        if criteria['value'] not in pub_value:
            if criteria['field'] == 'type':
                # Backward compatibility message
                reasons.append(f"Missing {criteria_type}: {criteria['value']}")
            else:
                reasons.append(f"Missing {criteria_type} {criteria['field']}: {criteria['value']}")
    
    return reasons