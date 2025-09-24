# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of literature_search and is licensed under the GNU GPL v3.
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


def get_publications_ieee(keyword_list: List[str], api_key: str, page_size: int = 100, logic: str = 'OR', start_year: int = None, end_year: int = None) -> List[Dict[str, Any]]:
    """Get publications from IEEE Xplore API.
    
    Args:
        keyword_list: List of keywords to search for
        api_key: IEEE API key
        page_size: Maximum number of results to return
        logic: Search logic ('AND' or 'OR')
        start_year: Start year for date filtering
        end_year: End year for date filtering
        
    Returns:
        List of publication dictionaries
    """
    if logic == 'AND':
        query = ' AND '.join([f'"{k}"' for k in keyword_list])
    else:
        query = ' OR '.join([f'"{k}"' for k in keyword_list])
    
    url = 'https://ieeexploreapi.ieee.org/api/v1/search/articles'
    params = {
        'querytext': query,
        'max_records': min(page_size, 200),  # IEEE API has max 200 per request
        'start_record': 1,
        'sort_field': 'article_number',
        'sort_order': 'asc'
    }
    
    if start_year and end_year:
        params['start_year'] = start_year
        params['end_year'] = end_year
    
    if not api_key:
        print("Warning: IEEE API key not provided. Access may be limited.")
        return []
    
    headers = {'Accept': 'application/json'}
    params['apikey'] = api_key
    
    response = robust_get(url, params=params, headers=headers)
    if not response:
        print("IEEE API error: failed after retries.")
        return []
    
    data = response.json()
    results = []
    
    for item in data.get('articles', []):
        # Extract authors
        authors = ''
        if 'authors' in item and 'authors' in item['authors']:
            authors = ', '.join([
                author.get('full_name', '') 
                for author in item['authors']['authors'] 
                if author.get('full_name')
            ])
        
        # Extract year from publication_date
        year = ''
        if 'publication_date' in item:
            try:
                year = int(item['publication_date'][:4])
            except (ValueError, TypeError):
                pass
        
        results.append({
            'Title': item.get('title', ''),
            'Source': 'IEEE',
            'Authors': authors,
            'Year': year,
            'Journal': item.get('publication_title', ''),
            'Language': 'English',
            'Type': item.get('content_type', 'article'),
            'Focus': query,
            'DOI': item.get('doi', ''),
            'Abstract': item.get('abstract', ''),
            'URL': item.get('html_url', '')
        })
    
    return results


def get_publications_springer(keyword_list: List[str], api_key: str, page_size: int = 100, logic: str = 'OR', start_year: int = None, end_year: int = None) -> List[Dict[str, Any]]:
    """Get publications from Springer API.
    
    Args:
        keyword_list: List of keywords to search for
        api_key: Springer API key
        page_size: Maximum number of results to return
        logic: Search logic ('AND' or 'OR')
        start_year: Start year for date filtering
        end_year: End year for date filtering
        
    Returns:
        List of publication dictionaries
    """
    if logic == 'AND':
        query = ' AND '.join([f'"{k}"' for k in keyword_list])
    else:
        query = ' OR '.join([f'"{k}"' for k in keyword_list])
    
    url = 'http://api.springernature.com/meta/v2/json'
    params = {
        'q': query,
        's': min(page_size, 100),  # Springer API has max 100 per request
        'p': 1
    }
    
    if start_year and end_year:
        params['q'] += f' year:{start_year}-{end_year}'
    
    if not api_key:
        print("Warning: Springer API key not provided. Access may be limited.")
        return []
    
    headers = {'Accept': 'application/json'}
    params['api_key'] = api_key
    
    response = robust_get(url, params=params, headers=headers)
    if not response:
        print("Springer API error: failed after retries.")
        return []
    
    data = response.json()
    results = []
    
    for item in data.get('records', []):
        # Extract authors
        authors = ''
        if 'creators' in item:
            authors = ', '.join([
                creator.get('creator', '') 
                for creator in item['creators'] 
                if creator.get('creator')
            ])
        
        # Extract year from publication date
        year = ''
        if 'publicationDate' in item:
            try:
                year = int(item['publicationDate'][:4])
            except (ValueError, TypeError):
                pass
        
        results.append({
            'Title': item.get('title', ''),
            'Source': 'Springer',
            'Authors': authors,
            'Year': year,
            'Journal': item.get('publicationName', ''),
            'Language': item.get('language', 'English'),
            'Type': item.get('contentType', 'article'),
            'Focus': query,
            'DOI': item.get('doi', ''),
            'Abstract': item.get('abstract', ''),
            'URL': item.get('url', [{}])[0].get('value', '') if item.get('url') else ''
        })
    
    return results


def get_publications_dblp(keyword_list: List[str], page_size: int = 100, logic: str = 'OR') -> List[Dict[str, Any]]:
    """Get publications from DBLP API.
    
    Args:
        keyword_list: List of keywords to search for  
        page_size: Maximum number of results to return
        logic: Search logic ('AND' or 'OR') 
        
    Returns:
        List of publication dictionaries
    """
    if logic == 'AND':
        query = ' '.join(keyword_list)  # DBLP treats space as AND by default
    else:
        query = ' | '.join(keyword_list)  # Use | for OR in DBLP
    
    url = 'https://dblp.org/search/publ/api'
    params = {
        'q': query,
        'h': min(page_size, 1000),  # DBLP allows up to 1000 results
        'format': 'json'
    }
    
    response = robust_get(url, params=params)
    if not response:
        print("DBLP API error: failed after retries.")
        return []
    
    data = response.json()
    results = []
    
    hits = data.get('result', {}).get('hits', {})
    if not hits:
        return results
    
    for item in hits.get('hit', []):
        info = item.get('info', {})
        
        # Extract authors
        authors = ''
        if 'authors' in info and 'author' in info['authors']:
            author_list = info['authors']['author']
            if isinstance(author_list, list):
                authors = ', '.join([
                    author.get('text', '') if isinstance(author, dict) else str(author)
                    for author in author_list
                ])
            else:
                authors = author_list.get('text', '') if isinstance(author_list, dict) else str(author_list)
        
        # Extract year
        year = ''
        if 'year' in info:
            try:
                year = int(info['year'])
            except (ValueError, TypeError):
                pass
        
        # Extract venue/journal
        venue = ''
        if 'venue' in info:
            venue = info['venue']
        
        results.append({
            'Title': info.get('title', ''),
            'Source': 'DBLP',
            'Authors': authors,
            'Year': year,
            'Journal': venue,
            'Language': 'English',
            'Type': info.get('type', 'article'),
            'Focus': query,
            'DOI': info.get('doi', ''),
            'URL': info.get('url', '')
        })
    
    return results


def get_publications_scopus(keyword_list: List[str], api_key: str, page_size: int = 100, logic: str = 'OR', start_year: int = None, end_year: int = None) -> List[Dict[str, Any]]:
    """Get publications from Scopus API.
    
    Args:
        keyword_list: List of keywords to search for
        api_key: Scopus API key (Elsevier API key)
        page_size: Maximum number of results to return
        logic: Search logic ('AND' or 'OR')
        start_year: Start year for date filtering
        end_year: End year for date filtering
        
    Returns:
        List of publication dictionaries
    """
    if logic == 'AND':
        query = ' AND '.join([f'TITLE-ABS-KEY("{k}")' for k in keyword_list])
    else:
        query = ' OR '.join([f'TITLE-ABS-KEY("{k}")' for k in keyword_list])
    
    if start_year and end_year:
        query += f' AND PUBYEAR > {start_year-1} AND PUBYEAR < {end_year+1}'
    
    url = 'https://api.elsevier.com/content/search/scopus'
    params = {
        'query': query,
        'count': min(page_size, 200),  # Scopus API has max 200 per request
        'start': 0,
        'sort': 'pubyear'
    }
    
    if not api_key:
        print("Warning: Scopus API key not provided. Access may be limited.")
        return []
    
    headers = {
        'Accept': 'application/json',
        'X-ELS-APIKey': api_key
    }
    
    response = robust_get(url, params=params, headers=headers)
    if not response:
        print("Scopus API error: failed after retries.")
        return []
    
    data = response.json()
    results = []
    
    search_results = data.get('search-results', {})
    entries = search_results.get('entry', [])
    
    for item in entries:
        # Extract authors
        authors = ''
        if 'author' in item:
            author_list = item['author']
            if isinstance(author_list, list):
                authors = ', '.join([
                    author.get('authname', '') for author in author_list
                    if author.get('authname')
                ])
            else:
                authors = author_list.get('authname', '') if isinstance(author_list, dict) else ''
        
        # Extract year from cover date
        year = ''
        if 'prism:coverDate' in item:
            try:
                year = int(item['prism:coverDate'][:4])
            except (ValueError, TypeError):
                pass
        
        results.append({
            'Title': item.get('dc:title', ''),
            'Source': 'Scopus',
            'Authors': authors,
            'Year': year,
            'Journal': item.get('prism:publicationName', ''),
            'Language': 'English',
            'Type': item.get('prism:aggregationType', 'article'),
            'Focus': query,
            'DOI': item.get('prism:doi', ''),
            'Abstract': '',  # Abstract not included in search results
            'URL': item.get('link', [{}])[-1].get('@href', '') if item.get('link') else ''
        })
    
    return results
