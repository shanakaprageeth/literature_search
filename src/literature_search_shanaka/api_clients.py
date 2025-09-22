# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of literature_search_shanaka and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.
from typing import List, Dict, Optional, Any
import xml.etree.ElementTree as ET
from .utils import robust_get


def get_publications_europe_pmc(keyword_list: List[str], page_size: int = 100, logic: str = 'OR') -> List[Dict[str, Any]]:
    if logic == 'AND':
        query = ' AND '.join(keyword_list)
    else:
        query = ' OR '.join(keyword_list)
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        'query': query,
        'format': 'json',
        'pageSize': page_size
    }
    response = robust_get(url, params=params)
    if not response:
        return []
    data = response.json()
    results = []
    for record in data.get('resultList', {}).get('result', []):
        results.append({
            'Title': record.get('title', ''),
            'Source': record.get('source', 'MED'),
            'Authors': record.get('authorString', ''),
            'Year': int(record.get('pubYear', 0)) if record.get('pubYear') else '',
            'Journal': record.get('journalTitle', ''),
            'Language': record.get('language', 'English'),
            'Type': record.get('pubType', ''),
            'Focus': query
        })
    return results

def get_publications_crossref(keyword_list: List[str], page_size: int = 100, logic: str = 'OR') -> List[Dict[str, Any]]:
    query = ' '.join(keyword_list)
    url = f'https://api.crossref.org/works'
    params = {'query': query, 'rows': page_size}
    response = robust_get(url, params=params)
    if not response:
        return []
    data = response.json()
    results = []
    for item in data.get('message', {}).get('items', []):
        year = ''
        issued = item.get('issued', {})
        date_parts = issued.get('date-parts') if issued else None
        if date_parts and isinstance(date_parts, list) and len(date_parts) > 0 and isinstance(date_parts[0], list) and len(date_parts[0]) > 0 and date_parts[0][0]:
            year = int(date_parts[0][0])
        results.append({
            'Title': item.get('title', [''])[0],
            'Source': 'CrossRef',
            'Authors': ', '.join([a.get('family', '') for a in item.get('author', [])]) if 'author' in item else '',
            'Year': year,
            'Journal': item.get('container-title', [''])[0] if item.get('container-title') else '',
            'Language': item.get('language', 'English'),
            'Type': item.get('type', ''),
            'Focus': query
        })
    return results

def get_publications_arxiv(keyword_list: List[str], page_size: int = 100, logic: str = 'OR') -> List[Dict[str, Any]]:
    query = '+AND+'.join(keyword_list) if logic == 'AND' else '+OR+'.join(keyword_list)
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={page_size}'
    response = robust_get(url)
    if not response:
        return []
    root = ET.fromstring(response.content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    results = []
    for entry in root.findall('atom:entry', ns):
        authors = ', '.join([a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)])
        year = entry.find('atom:published', ns).text[:4]
        results.append({
            'Title': entry.find('atom:title', ns).text.strip(),
            'Source': 'arXiv',
            'Authors': authors,
            'Year': int(year),
            'Journal': 'arXiv',
            'Language': 'English',
            'Type': 'preprint',
            'Focus': query
        })
    return results

def get_publications_core(keyword_list: List[str], api_key: str, page_size: int = 100, logic: str = 'OR', start_year: int = None, end_year: int = None) -> List[Dict[str, Any]]:
    if logic == 'AND':
        title_query = ' AND '.join([f'title:"{k}"' for k in keyword_list])
    else:
        title_query = ' OR '.join([f'title:"{k}"' for k in keyword_list])
    year_query = ''
    if start_year and end_year:
        year_query = f' AND yearPublished>="{start_year}" AND yearPublished<="{end_year}"'
    fulltext_query = ' AND _exists_:fullText'
    query = f'({title_query}){year_query}{fulltext_query}'
    url = 'https://api.core.ac.uk/v3/search/works'
    params = {'q': query, 'limit': page_size}
    if api_key:
        headers = {'Accept': 'application/json', 'Authorization': api_key}
    else:
        headers = {'Accept': 'application/json'}
        print("Warning: CORE API key not provided. Access may be limited.")
    response = robust_get(url, params=params, headers=headers)
    if not response:
        print(f"CORE API error: failed after retries.")
        return []
    data = response.json()
    results = []
    for item in data.get('results', []):
        authors = ''
        if isinstance(item.get('authors', []), list):
            authors = ', '.join([a.get('name', '') for a in item.get('authors', []) if isinstance(a, dict) and 'name' in a])
        results.append({
            'Title': item.get('title', ''),
            'Source': 'CORE',
            'Authors': authors,
            'Year': item.get('yearPublished', ''),
            'Journal': item.get('publisher', ''),
            'Language': item.get('language', 'English'),
            'Type': item.get('documentType', ''),
            'Focus': query
        })
    return results

def get_publications_semanticscholar(keyword_list: List[str], page_size: int = 100, logic: str = 'OR', start_year: int = None, end_year: int = None, open_access: bool = False, fields_of_study: Optional[list] = None, extra_fields: Optional[list] = None) -> List[Dict[str, Any]]:
    query = ' '.join(keyword_list)
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    params = {'query': query, 'limit': page_size}
    if start_year and end_year:
        params['year'] = f'{start_year}-{end_year}'
    if open_access:
        params['openAccessPdf'] = 'true'
    if fields_of_study:
        params['fieldsOfStudy'] = ','.join(fields_of_study)
    base_fields = ['title', 'year', 'authors', 'venue']
    if extra_fields:
        base_fields += extra_fields
    params['fields'] = ','.join(base_fields)
    response = robust_get(url, params=params)
    if not response:
        return []
    data = response.json()
    results = []
    for item in data.get('data', []):
        authors = ', '.join([a.get('name', '') for a in item.get('authors', [])])
        results.append({
            'Title': item.get('title', ''),
            'Source': 'SemanticScholar',
            'Authors': authors,
            'Year': item.get('year', ''),
            'Journal': item.get('venue', ''),
            'Language': 'English',
            'Type': 'journal article',
            'Focus': query,
            'Url': item.get('url', ''),
            'Abstract': item.get('abstract', '')
        })
    return results
