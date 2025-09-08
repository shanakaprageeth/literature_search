import json
import csv

# Load input data
with open('sample_input.json', 'r') as f:
    input_data = json.load(f)

# Simulated publication database (normally this would be fetched from APIs)
publications = [
    {
        'Title': 'Deep Learning for MRI Analysis',
        'Authors': 'Smith et al',
        'Year': 2020,
        'Journal': 'Medical Imaging Journal',
        'Language': 'English',
        'Type': 'Peer-reviewed article',
        'Focus': 'machine learning in medical imaging'
    },
    {
        'Title': 'AI in Radiology: A Review',
        'Authors': 'Jones and Lee',
        'Year': 2021,
        'Journal': 'Journal of Radiology',
        'Language': 'English',
        'Type': 'Peer-reviewed article',
        'Focus': 'machine learning in medical imaging'
    },
    {
        'Title': 'Machine Learning in CT Scans',
        'Authors': 'Wang et al',
        'Year': 2019,
        'Journal': 'Imaging Science',
        'Language': 'English',
        'Type': 'Conference abstract',
        'Focus': 'machine learning in medical imaging'
    }
]

criteria = input_data['initial_prisma_values']

# Apply inclusion/exclusion criteria and track reasons
results = []
criteria_counts = { 'inclusion': 0, 'exclusion': 0, 'by_criteria': {} }
for pub in publications:
    included = True
    reasons = []
    # Inclusion criteria
    if pub['Type'] != 'Peer-reviewed article':
        included = False
        reasons.append('Not peer-reviewed')
    if pub['Year'] < 2018:
        included = False
        reasons.append('Published before 2018')
    if 'machine learning' not in pub['Focus']:
        included = False
        reasons.append('Focus not on machine learning in medical imaging')
    # Exclusion criteria
    if pub['Language'] != 'English':
        included = False
        reasons.append('Non-English')
    if pub['Type'] == 'Conference abstract':
        included = False
        reasons.append('Conference abstract only')
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
            criteria_counts['by_criteria'][r] = criteria_counts['by_criteria'].get(r, 0) + 1

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

# Output methodology text
with open('sample_prisma_method.txt', 'r') as f:
    method_text = f.read()
print('\nMethodology for Literature Review Section:\n')
print(method_text)
