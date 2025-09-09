import json
import csv
import requests
import argparse
import matplotlib.pyplot as plt
import drawpyo
from collections import Counter
import re

STOPWORDS = set([
    'the', 'and', 'for', 'with', 'that', 'from', 'this', 'have', 'are', 'was', 'were', 'has', 'had', 'but', 'not', 'all', 'can', 'will', 'into', 'out', 'over', 'under', 'more', 'than', 'such', 'their', 'they', 'them', 'been', 'also', 'which', 'when', 'where', 'who', 'what', 'how', 'why', 'your', 'about', 'after', 'before', 'between', 'each', 'other', 'some', 'any', 'our', 'his', 'her', 'its', 'on', 'in', 'of', 'to', 'by', 'as', 'at', 'an', 'or', 'is', 'a', 'be', 'it'
])

def get_keywords(research_topic):
    # Improved keyword extraction: remove stopwords, punctuation, lowercase, unique
    words = re.findall(r'\b\w+\b', research_topic.lower())
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 3]
    return list(set(keywords))

def get_publications_europe_pmc(keyword_list, page_size=100, logic='OR'):
    """
    Fetches publication data from Europe PMC API for a given query.
    logic: 'OR' (default) or 'AND' to combine keywords
    Returns a list of dicts with publication info.
    """
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
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    with open('europe_pmc_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    results = []
    for record in data.get('resultList', {}).get('result', []):
        results.append({
            'Title': record.get('title', ''),
            'Source' : record.get('source', 'MED'),
            'Authors': record.get('authorString', ''),
            'Year': int(record.get('pubYear', 0)) if record.get('pubYear') else '',
            'Journal': record.get('journalTitle', ''),
            'Language': record.get('language', 'English'),
            'Type': record.get('pubType', ''),
            'Focus': query
        })
    return results

def search_database(keyword_list, page_size=100, db_name='PubMed', logic='OR'):
    if db_name == 'PubMed':
        return get_publications_europe_pmc(keyword_list, page_size, logic)
    else:
        print(f'No database {db_name} Found')
        return []

def parse_date_range(date_range):
    # Expects format 'YYYY-YYYY' or 'YYYY'
    if '-' in date_range:
        start, end = date_range.split('-')
        return int(start), int(end)
    else:
        year = int(date_range)
        return year, year

def create_prisma_drawio_diagram(criteria_counts, total_records):
    import drawpyo
    file = drawpyo.File(file_name="prisma_flow_diagram.drawio")
    page = drawpyo.Page(file=file)
    # Main boxes
    box_identified = drawpyo.diagram.Object(page=page, x=400, y=80, width=200, height=60, text=f"Records identified:\n{total_records}")
    box_screened = drawpyo.diagram.Object(page=page, x=400, y=200, width=200, height=60, text=f"Records screened:\n{total_records}")
    box_excluded = drawpyo.diagram.Object(page=page, x=120, y=320, width=200, height=60, text=f"Records excluded:\n{criteria_counts['exclusion']}")
    box_included = drawpyo.diagram.Object(page=page, x=400, y=440, width=200, height=60, text=f"Records included:\n{criteria_counts['inclusion']}")
    # Arrows between main boxes
    drawpyo.diagram.Object(page=page, source=box_identified, target=box_screened)
    drawpyo.diagram.Object(page=page, source=box_screened, target=box_excluded)
    drawpyo.diagram.Object(page=page, source=box_screened, target=box_included)
    # Exclusion criteria boxes on right
    y_start = 320
    for i, (crit, count) in enumerate(criteria_counts['by_criteria'].items()):
        y = y_start + i*80
        excl_box = drawpyo.diagram.Object(page=page, x=700, y=y, width=260, height=50, text=f"{crit}: {count}")
        drawpyo.diagram.Object(page=page, source=box_excluded, target=excl_box)
    # Save as draw.io file
    file.write()
    print("\nPRISMA flow diagram saved as 'prisma_flow_diagram.drawio' (draw.io compatible).")

def output_prisma_results(results, criteria_counts, total_records):
    # Write output CSV
    with open('sample_output.csv', 'w', newline='') as csvfile:
        fieldnames = ['Title', 'Authors', 'Year', 'Journal', 'Included']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({k: row[k] for k in fieldnames})
    # Print summary of criteria effects
    print('PRISMA Criteria Application Summary:')
    print(f"Included: {criteria_counts['inclusion']}")
    print(f"Excluded: {criteria_counts['exclusion']}")
    for crit, count in criteria_counts['by_criteria'].items():
        print(f"Excluded by '{crit}': {count}")
    # Output PRISMA flowchart (ASCII art)
    print('\nPRISMA Selection Flowchart:')
    exclusion_details = '\n'.join([f"    └─ {crit}: {count}" for crit, count in criteria_counts['by_criteria'].items()])
    print(f"""
    Records identified: {total_records}
        |
        ├─ Records screened: {total_records}
        |     |
        |     ├─ Records excluded: {criteria_counts['exclusion']}
    {exclusion_details}
        |     |
        |     └─ Records included: {criteria_counts['inclusion']}
    """)
    # Output PRISMA flow diagram (Mermaid syntax, for research figure):
    print('\nPRISMA Flow Diagram (Mermaid syntax, for research figure):')
    print(f'''\ngraph TD\n    A[Records identified: {total_records}] --> B[Records screened: {total_records}]\n    B --> C[Records excluded: {criteria_counts['exclusion']}]''')
    for crit, count in criteria_counts['by_criteria'].items():
        print(f"    C --> C_{crit.replace(' ', '_')}[{crit}: {count}]")
    print(f"    B --> D[Records included: {criteria_counts['inclusion']}]")
    print("'")
    # Output methodology text
    with open('sample_prisma_method.txt', 'r') as f:
        method_text = f.read()
    print('\nMethodology for Literature Review Section:\n')
    print(method_text)

def search_prisma(config_file='sample_input.json', logic='OR', page_size=100):
    with open(config_file, 'r') as f:
        input_data = json.load(f)
    criteria = input_data['initial_prisma_values']
    research_topic = input_data.get('research_topic', '')
    keyword_list = input_data.get('keywords') or get_keywords(research_topic)
    date_range = criteria.get('date_range', '1900-2100')
    start_year, end_year = parse_date_range(date_range)
    inclusion_criteria = [c.lower() for c in criteria.get('inclusion_criteria', [])]
    exclusion_criteria = [c.lower() for c in criteria.get('exclusion_criteria', [])]
    databases = input_data.get('databases', ['PubMed'])
    results = []
    criteria_counts = { 'inclusion': 0, 'exclusion': 0, 'by_criteria': Counter() }
    publications = []
    for db_name in databases:
        publications += search_database(keyword_list, page_size, db_name, logic)
    for pub in publications:
        included = True
        reasons = []
        if pub['Year'] and (pub['Year'] < start_year or pub['Year'] > end_year):
            included = False
            reasons.append(f'Published outside {date_range}')
        for inc in inclusion_criteria:
            if inc not in pub['Type'].lower():
                included = False
                reasons.append(f"Missing inclusion: {inc}")
        # Exclusion criteria
        for exc in exclusion_criteria:
            if exc in pub['Type'].lower():
                included = False
                reasons.append(f"Has exclusion: {exc}")
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
    output_prisma_results(results, criteria_counts, total_records)
    create_prisma_drawio_diagram(criteria_counts, total_records)
def main():
    parser = argparse.ArgumentParser(description='PRISMA Literature Review Tool')
    parser.add_argument('--config', type=str, default='sample_input.json', help='Path to config JSON file')
    parser.add_argument('--logic', type=str, choices=['AND', 'OR'], default='OR', help='Keyword combination logic')
    parser.add_argument('--page_size', type=int, default=100, help='Number of results per database')
    args = parser.parse_args()
    search_prisma(config_file=args.config, logic=args.logic, page_size=args.page_size)

if __name__ == "__main__":
    main()
