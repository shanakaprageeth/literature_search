# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of literature_search and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.
import os
import csv
import json
import sys
from collections import Counter
from typing import List, Dict, Any
import drawpyo
import pkgutil  # Add this import for handling frozen packages

def output_prisma_results(results: List[Dict[str, Any]], criteria_counts: Dict[str, Any], total_records: int, output_dir: str = 'output') -> None:
    """Write PRISMA results to CSV, JSON, and print summary/flowcharts."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Write all publications found CSV
    all_publications_path = os.path.join(output_dir, 'all_publications_found.csv')
    with open(all_publications_path, 'w', newline='') as csvfile:
        fieldnames = ['Title', 'Authors', 'Year', 'Journal', 'Included', 'Reasons']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    
    # Write selected publications CSV (only included ones)
    selected_publications = [row for row in results if row['Included'] == 'Yes']
    selected_path = os.path.join(output_dir, 'selected_publications.csv')
    with open(selected_path, 'w', newline='') as csvfile:
        fieldnames = ['Title', 'Authors', 'Year', 'Journal']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in selected_publications:
            writer.writerow({k: row[k] for k in fieldnames})
    
    # Write original output CSV for backward compatibility
    csv_path = os.path.join(output_dir, 'output_results.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Title', 'Authors', 'Year', 'Journal', 'Included']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({k: row[k] for k in fieldnames})
    
    # Write output JSON
    json_path = os.path.join(output_dir, 'results.json')
    with open(json_path, 'w') as jf:
        json.dump({
            'results': results,
            'criteria_counts': {k: (v if not isinstance(v, Counter) else dict(v)) for k, v in criteria_counts.items()},
            'total_records': total_records
        }, jf, indent=2)
    # Print summary of criteria effects
    print('PRISMA Criteria Application Summary:')
    print(f"Included: {criteria_counts['inclusion']}")
    print(f"Excluded: {criteria_counts['exclusion']}")
    for crit, count in criteria_counts['by_criteria'].items():
        print(f"Excluded by '{crit}': {count}")
    # Output PRISMA flowchart (ASCII art)
    print('\nPRISMA Selection Flowchart:')
    print(f"Records identified: {total_records}")
    print("    |")
    print(f"    ├─ Records screened: {total_records}")
    print("    |     |\n    |     ├─ Records excluded: {0}".format(criteria_counts['exclusion']))
    for crit, count in criteria_counts['by_criteria'].items():
        print(f"    |     |    └─ {crit}: {count}")
    print("    |     |\n    |     └─ Records included: {0}".format(criteria_counts['inclusion']))
    
    # Print output file information
    print(f'\nOutput files created in "{output_dir}" directory:')
    print(f"  - all_publications_found.csv: All {total_records} publications with inclusion status and reasons")
    print(f"  - selected_publications.csv: Only the {criteria_counts['inclusion']} included publications")
    print(f"  - output_results.csv: All publications with inclusion status (backward compatibility)")
    print(f"  - results.json: Complete results in JSON format")
    
    # Output PRISMA flow diagram (Mermaid syntax, for research figure):
    print('\nPRISMA Flow Diagram (Mermaid syntax, for research figure):')
    print(f'''\ngraph TD\n    A[Records identified: {total_records}] --> B[Records screened: {total_records}]\n    B --> C[Records excluded: {criteria_counts['exclusion']}]''')
    for crit, count in criteria_counts['by_criteria'].items():
        print(f"    C --> C_{crit.replace(' ', '_')}[{crit}: {count}]")
    print(f"    B --> D[Records included: {criteria_counts['inclusion']}]")
    print("'")
    # Output methodology text
    method_path = os.path.join(output_dir, 'sample_prisma_method.txt')
    if os.path.exists(method_path):
        with open(method_path, 'r') as f:
            method_text = f.read()
        print('\nMethodology for Literature Review Section:\n')
        print(method_text)

def create_prisma_drawio_diagram(criteria_counts: Dict[str, Any], total_records: int, total_duplicates: int, output_dir: str = 'output', keywords: str = '') -> None:
    """Fill data into the provided PRISMA flow diagram template or use the default template."""
    user_template_path = os.path.join(output_dir, 'prisma_flow_diagram.drawio')
    default_template_path = os.path.join(os.path.dirname(__file__), 'prisma_flow_diagram.drawio')

    # Determine the template to use
    if os.path.exists(user_template_path):
        template_path = user_template_path
    else:
        # Handle frozen package scenario
        try:
            default_template_content = pkgutil.get_data(__package__, 'prisma_flow_diagram.drawio')
            if default_template_content is not None:
                default_template_content = default_template_content.decode('utf-8')
        except Exception:
            default_template_content = None

        if default_template_content:
            template_path = None  # Use in-memory content
        elif os.path.exists(default_template_path):
            template_path = default_template_path
        else:
            print(f"ERROR: Template file not found in '{user_template_path}' or '{default_template_path}'.", file=sys.stderr)
            return

    filled_diagram_path = os.path.join(output_dir, 'prisma_flow_diagram_filled.drawio')

    # Read template content
    if template_path:
        with open(template_path, 'r') as template_file:
            diagram_content = template_file.read()
    else:
        diagram_content = default_template_content

    # Replace placeholders with actual values
    diagram_content = diagram_content.replace("{ADD_KEYWORDS}", keywords)
    diagram_content = diagram_content.replace("{TOTAL_RECORDS_WITH_DUPLICATES}", str(total_records + total_duplicates))
    diagram_content = diagram_content.replace("{TOTAL_DUPLICATES}", str(total_duplicates))
    diagram_content = diagram_content.replace("{TOTAL_RECORDS}", str(total_records))
    diagram_content = diagram_content.replace("{AFTER_INCLUSION_EXCLUSION}", str(criteria_counts['inclusion']))
    diagram_content = diagram_content.replace("{EXCLUSION_COUNTS}", json.dumps(criteria_counts['by_criteria'], indent=2))

    # Write the filled diagram
    with open(filled_diagram_path, 'w') as filled_file:
        filled_file.write(diagram_content)

    print(f"PRISMA flow diagram filled and saved as '{filled_diagram_path}'.")
