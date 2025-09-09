# tests/test_prisma_logs.py
from research_search_shanaka.prisma_logs import output_prisma_results, create_prisma_drawio_diagram
import os
from collections import Counter

def test_output_prisma_results(tmp_path):
    results = [
        {"Title": "Paper 1", "Authors": "Author A", "Year": 2020, "Journal": "Journal A", "Included": "Yes"},
        {"Title": "Paper 2", "Authors": "Author B", "Year": 2019, "Journal": "Journal B", "Included": "No"}
    ]
    criteria_counts = {"inclusion": 1, "exclusion": 1, "by_criteria": Counter()}
    total_records = 2
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    output_prisma_results(results, criteria_counts, total_records, output_dir=str(output_dir))

    assert (output_dir / "output_results.csv").exists()
    assert (output_dir / "results.json").exists()

def test_create_prisma_drawio_diagram(tmp_path):
    criteria_counts = {"inclusion": 1, "exclusion": 1, "by_criteria": {"reason 1": 1}}
    total_records = 2
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    create_prisma_drawio_diagram(criteria_counts, total_records, output_dir=str(output_dir))

    assert (output_dir / "prisma_flow_diagram.drawio").exists()
