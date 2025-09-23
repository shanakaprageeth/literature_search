"""
Tests for criteria_mapper module.
"""
import pytest
from literature_search.criteria_mapper import (
    get_database_name_from_source,
    get_mapped_field_for_criteria,
    parse_criteria_with_fields,
    check_criteria_match,
    get_criteria_mismatch_reasons
)


def test_get_database_name_from_source():
    """Test database name mapping from source field."""
    assert get_database_name_from_source('MED') == 'PubMed'
    assert get_database_name_from_source('PMC') == 'PubMed'
    assert get_database_name_from_source('CrossRef') == 'CrossRef'
    assert get_database_name_from_source('arXiv') == 'arXiv'
    assert get_database_name_from_source('CORE') == 'CORE'
    assert get_database_name_from_source('SemanticScholar') == 'SemanticScholar'
    assert get_database_name_from_source('IEEE') == 'IEEE'
    assert get_database_name_from_source('Springer') == 'Springer'
    assert get_database_name_from_source('DBLP') == 'DBLP'
    assert get_database_name_from_source('Scopus') == 'Scopus'
    assert get_database_name_from_source('unknown') == 'PubMed'  # Default


def test_get_mapped_field_for_criteria():
    """Test field mapping for different databases."""
    # Test PubMed mappings
    assert get_mapped_field_for_criteria('PubMed', 'type') == 'Type'
    assert get_mapped_field_for_criteria('PubMed', 'language') == 'Language'
    assert get_mapped_field_for_criteria('PubMed', 'unknown_field') == 'Type'  # Default
    
    # Test CORE mappings
    assert get_mapped_field_for_criteria('CORE', 'document_type') == 'Type'
    assert get_mapped_field_for_criteria('CORE', 'type') == 'Type'
    
    # Test SemanticScholar mappings
    assert get_mapped_field_for_criteria('SemanticScholar', 'venue') == 'Journal'
    
    # Test unknown database
    assert get_mapped_field_for_criteria('UnknownDB', 'type') == 'Type'


def test_parse_criteria_with_fields():
    """Test parsing of criteria with field specifications."""
    # Test simple criteria (default to type)
    criteria = ['journal article', 'review']
    parsed = parse_criteria_with_fields(criteria)
    expected = [
        {'field': 'type', 'value': 'journal article'},
        {'field': 'type', 'value': 'review'}
    ]
    assert parsed == expected
    
    # Test criteria with field specifications
    criteria = ['type:journal article', 'language:english', 'source:pubmed']
    parsed = parse_criteria_with_fields(criteria)
    expected = [
        {'field': 'type', 'value': 'journal article'},
        {'field': 'language', 'value': 'english'},
        {'field': 'source', 'value': 'pubmed'}
    ]
    assert parsed == expected
    
    # Test mixed criteria
    criteria = ['review', 'language:english']
    parsed = parse_criteria_with_fields(criteria)
    expected = [
        {'field': 'type', 'value': 'review'},
        {'field': 'language', 'value': 'english'}
    ]
    assert parsed == expected


def test_check_criteria_match():
    """Test criteria matching logic."""
    pub = {
        'Title': 'Test Paper',
        'Source': 'CrossRef',
        'Type': 'journal-article',
        'Language': 'English',
        'Journal': 'Nature'
    }
    
    # Test simple type matching (backward compatibility)
    assert check_criteria_match(pub, ['journal'])
    assert not check_criteria_match(pub, ['conference'])
    
    # Test field-specific matching
    assert check_criteria_match(pub, ['type:journal'])
    assert check_criteria_match(pub, ['language:english'])
    assert check_criteria_match(pub, ['journal:nature'])
    assert not check_criteria_match(pub, ['language:spanish'])
    
    # Test empty criteria (should match)
    assert check_criteria_match(pub, [])
    
    # Test OR logic (any match returns True)
    assert check_criteria_match(pub, ['conference', 'journal'])
    assert check_criteria_match(pub, ['language:spanish', 'language:english'])


def test_get_criteria_mismatch_reasons():
    """Test generation of mismatch reasons."""
    pub = {
        'Title': 'Test Paper',
        'Source': 'CrossRef',
        'Type': 'journal-article',
        'Language': 'English',
        'Journal': 'Nature'
    }
    
    # Test simple type mismatch (backward compatibility)
    reasons = get_criteria_mismatch_reasons(pub, ['conference'], 'inclusion')
    assert 'Missing inclusion: conference' in reasons
    
    # Test field-specific mismatch
    reasons = get_criteria_mismatch_reasons(pub, ['language:spanish'], 'inclusion')
    assert 'Missing inclusion language: spanish' in reasons
    
    # Test multiple mismatches
    reasons = get_criteria_mismatch_reasons(pub, ['conference', 'language:spanish'], 'inclusion')
    assert len(reasons) == 2
    assert 'Missing inclusion: conference' in reasons
    assert 'Missing inclusion language: spanish' in reasons
    
    # Test no mismatch
    reasons = get_criteria_mismatch_reasons(pub, ['journal'], 'inclusion')
    assert len(reasons) == 0
    
    # Test empty criteria
    reasons = get_criteria_mismatch_reasons(pub, [], 'inclusion')
    assert len(reasons) == 0


def test_database_specific_matching():
    """Test that database-specific field mappings work correctly."""
    # Test SemanticScholar with venue mapping
    pub_semantic = {
        'Title': 'Test Paper',
        'Source': 'SemanticScholar',
        'Type': 'journal article',
        'Language': 'English',
        'Journal': 'ICML'  # venue is mapped to Journal
    }
    
    # Should match venue criteria through Journal field
    assert check_criteria_match(pub_semantic, ['venue:icml'])
    assert check_criteria_match(pub_semantic, ['journal:icml'])
    
    # Test CORE with document_type mapping
    pub_core = {
        'Title': 'Test Paper',
        'Source': 'CORE',
        'Type': 'research article',
        'Language': 'English',
        'Journal': 'Some Journal'
    }
    
    # Should match document_type criteria through Type field
    assert check_criteria_match(pub_core, ['document_type:research'])
    assert check_criteria_match(pub_core, ['type:research'])


def test_case_insensitive_matching():
    """Test that matching is case insensitive."""
    pub = {
        'Title': 'Test Paper',
        'Source': 'CrossRef',
        'Type': 'Journal-Article',
        'Language': 'ENGLISH',
        'Journal': 'Nature'
    }
    
    # Test case insensitive matching
    assert check_criteria_match(pub, ['JOURNAL'])
    assert check_criteria_match(pub, ['Type:JOURNAL'])
    assert check_criteria_match(pub, ['language:english'])
    assert check_criteria_match(pub, ['LANGUAGE:ENGLISH'])