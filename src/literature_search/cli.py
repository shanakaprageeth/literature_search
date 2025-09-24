# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of literature_search and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.

"""
Command-line interface for PRISMA Literature Review Tool.
"""

import argparse
import sys
import os
from collections import Counter, defaultdict
from .config_loader import load_config
from .keywords import get_keywords
from .api_clients import (
    get_publications_europe_pmc,
    get_publications_crossref,
    get_publications_arxiv,
    get_publications_core,
    get_publications_semanticscholar,
    get_publications_ieee,
    get_publications_springer,
    get_publications_dblp,
    get_publications_scopus
)
from .prisma_logs import output_prisma_results, create_prisma_drawio_diagram
from .utils import robust_get
from .criteria_mapper import check_criteria_match, get_criteria_mismatch_reasons, get_mapped_field_for_criteria, get_database_name_from_source


def parse_date_range(date_range):
    """Parse date range string into start and end years.
    
    Args:
        date_range: String in format 'YYYY-YYYY' or 'YYYY'
        
    Returns:
        Tuple of (start_year, end_year)
    """
    try:
        if '-' in date_range:
            start, end = date_range.split('-', 1)
            return int(start.strip()), int(end.strip())
        else:
            year = int(date_range.strip())
            return year, year
    except ValueError as e:
        print(f"ERROR: Invalid date range format '{date_range}': {e}", file=sys.stderr)
        sys.exit(1)


def search_database(keyword_list, api_key=None, page_size=100, db_name='PubMed', logic='OR', output_dir='output', start_year=None, end_year=None, open_access=False, fields_of_study=None, extra_fields=None):
    if db_name == 'PubMed':
        return get_publications_europe_pmc(keyword_list, page_size, logic)
    elif db_name == 'CrossRef':
        return get_publications_crossref(keyword_list, page_size, logic)
    elif db_name == 'arXiv':
        return get_publications_arxiv(keyword_list, page_size, logic)
    elif db_name == 'CORE':
        return get_publications_core(keyword_list, api_key, page_size, logic, start_year, end_year)
    elif db_name == 'SemanticScholar':
        return get_publications_semanticscholar(keyword_list, page_size, logic, start_year, end_year, open_access, fields_of_study, extra_fields)
    elif db_name == 'IEEE':
        return get_publications_ieee(keyword_list, api_key, page_size, logic, start_year, end_year)
    elif db_name == 'Springer':
        return get_publications_springer(keyword_list, api_key, page_size, logic, start_year, end_year)
    elif db_name == 'DBLP':
        return get_publications_dblp(keyword_list, page_size, logic)
    elif db_name == 'Scopus':
        return get_publications_scopus(keyword_list, api_key, page_size, logic, start_year, end_year)
    else:
        print(f'No database {db_name} Found')
        return []


def remove_duplicates(publications):
    """Remove duplicate publications based on title and authors.
    
    Args:
        publications: List of publication dictionaries.
        
    Returns:
        Tuple of (unique_publications, total_duplicates).
    """
    seen = set()
    unique_publications = []
    total_duplicates = 0

    for pub in publications:
        identifier = (pub['Title'].lower(), tuple(pub['Authors']))
        if identifier not in seen:
            seen.add(identifier)
            unique_publications.append(pub)
        else:
            total_duplicates += 1

    return unique_publications, total_duplicates


def search_prisma(config_file='sample_input.json', logic='OR', page_size=100, output_dir='output'):
    """Execute PRISMA literature search with the given configuration.
    
    Args:
        config_file: Path to JSON configuration file
        logic: Keyword combination logic ('AND' or 'OR')
        page_size: Number of results per database
        output_dir: Directory to save output files
    """
    # Load and validate configuration
    input_data = load_config(config_file)
    
    criteria = input_data['initial_prisma_values']
    api_keys = input_data.get('api_keys', {})
    research_topic = input_data.get('research_topic', '')
    
    # Handle keywords with warning when auto-generated
    if input_data.get('keywords'):
        keyword_list = input_data['keywords']
        print(f"Using user-provided keywords: {keyword_list}")
    else:
        keyword_list = get_keywords(research_topic)
        print(f"WARNING: No keywords provided in config. Auto-generated keywords from research topic: {keyword_list}")
    
    # Create output directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
    except PermissionError:
        print(f"ERROR: Permission denied when creating output directory '{output_dir}'.", file=sys.stderr)
        print("Please ensure you have write permissions to the specified location.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Could not create output directory '{output_dir}': {e}", file=sys.stderr)
        sys.exit(1)
    
    date_range = criteria.get('date_range', '1900-2100')
    start_year, end_year = parse_date_range(date_range)
    inclusion_criteria = [c.lower() for c in criteria.get('inclusion_criteria', [])]
    exclusion_criteria = [c.lower() for c in criteria.get('exclusion_criteria', [])]
    databases = criteria.get('databases', ['PubMed'])
    results = []
    criteria_counts = {'inclusion': 0, 'exclusion': 0, 'by_criteria': Counter()}
    publications = []
    for db_name in databases:
        publications += search_database(
            keyword_list,
            api_key=api_keys.get(db_name, None),
            page_size=page_size,
            db_name=db_name,
            logic=logic,
            output_dir=output_dir,
            start_year=start_year,
            end_year=end_year
        )
    
    # Remove duplicates
    publications, total_duplicates = remove_duplicates(publications)
    print(f"Total duplicates removed: {total_duplicates}")
    
    for pub in publications:
        included = False
        reasons = []
        in_date_range = pub['Year'] and (start_year <= pub['Year'] <= end_year)
        
        # Use the new criteria mapping system
        has_inclusion = check_criteria_match(pub, inclusion_criteria)
        if in_date_range and has_inclusion:
            included = True
        
        # Check exclusion criteria
        if check_criteria_match(pub, exclusion_criteria):
            included = False
            # For exclusion, we want to say what matched (caused exclusion)
            for criteria in exclusion_criteria:
                if ':' in criteria:
                    field, value = criteria.split(':', 1)
                    field_name = get_mapped_field_for_criteria(get_database_name_from_source(pub.get('Source', '')), field.strip().lower())
                    pub_value = str(pub.get(field_name, '')).lower()
                    if value.strip().lower() in pub_value:
                        if field.strip().lower() == 'type':
                            reasons.append(f"Has exclusion type: {value.strip().lower()}")
                        else:
                            reasons.append(f"Has exclusion {field.strip().lower()}: {value.strip().lower()}")
                else:
                    # Default to type field for backward compatibility
                    if criteria.lower() in pub['Type'].lower():
                        reasons.append(f"Has exclusion: {criteria.lower()}")
        
        if not included:
            if not in_date_range:
                reasons.append(f'Published outside {date_range}')
            if not has_inclusion:
                inclusion_reasons = get_criteria_mismatch_reasons(pub, inclusion_criteria, 'inclusion')
                reasons.extend(inclusion_reasons)
        results.append({
            'Title': pub['Title'],
            'Authors': pub['Authors'],
            'Year': pub['Year'],
            'Journal': pub['Journal'],
            'Included': 'Yes' if included else 'No',
            'Reasons': '; '.join(reasons) if reasons else 'Meets all criteria'
        })
        if included:
            criteria_counts['inclusion'] += 1
        else:
            criteria_counts['exclusion'] += 1
            for r in reasons:
                criteria_counts['by_criteria'][r] += 1
    total_records = len(publications)
    output_prisma_results(results, criteria_counts, total_records, output_dir=output_dir)
    create_prisma_drawio_diagram(
        criteria_counts, 
        total_records, 
        total_duplicates, 
        output_dir=output_dir, 
        keywords=', '.join(keyword_list)
    )


def main():
    """Main entry point for the PRISMA Literature Review Tool."""
    parser = argparse.ArgumentParser(
        description='PRISMA Literature Review Tool',
        epilog='Example: prisma-search --config sample_input.json --logic OR --page_size 100'
    )
    parser.add_argument('--config', type=str, default='sample_input.json', 
                        help='Path to config JSON file (default: sample_input.json)')
    parser.add_argument('--logic', type=str, choices=['AND', 'OR'], default='OR', 
                        help='Keyword combination logic (default: OR)')
    parser.add_argument('--page_size', type=int, default=100, 
                        help='Number of results per database (default: 100)')
    parser.add_argument('--output_dir', type=str, default='output', 
                        help='Directory to save outputs (default: output)')
    
    try:
        args = parser.parse_args()
        
        # Validate page_size
        if args.page_size <= 0:
            print("ERROR: Page size must be a positive integer.", file=sys.stderr)
            sys.exit(1)
        
        # Run the search
        search_prisma(
            config_file=args.config, 
            logic=args.logic, 
            page_size=args.page_size, 
            output_dir=args.output_dir
        )
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        print("Please check your configuration and try again.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()