# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of research_search_shanaka and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.
import os
import csv
import json
from collections import Counter
from typing import List, Dict, Any
import drawpyo

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

def create_prisma_drawio_diagram(criteria_counts: Dict[str, Any], total_records: int, output_dir: str = 'output') -> None:
    """Create and save PRISMA flow diagram as a draw.io file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    draw_io_file = drawpyo.File(file_name="prisma_flow_diagram.drawio", file_path=output_dir)
    page = drawpyo.Page(file=draw_io_file)
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
    draw_io_file.write()
    print(f"\nPRISMA flow diagram saved as '{os.path.join(output_dir, 'prisma_flow_diagram.drawio')}' (draw.io compatible).")
