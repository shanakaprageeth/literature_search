# tests/test_prisma_logs.py
from research_search_shanaka.prisma_logs import output_prisma_results, create_prisma_drawio_diagram
import os
from collections import Counter

def test_output_prisma_results(tmp_path):
    results = [
        {"Title": "Paper 1", "Authors": "Author A", "Year": 2020, "Journal": "Journal A", "Included": "Yes", "Reasons": "Meets all criteria"},
        {"Title": "Paper 2", "Authors": "Author B", "Year": 2019, "Journal": "Journal B", "Included": "No", "Reasons": "Missing inclusion: review"}
    ]
    criteria_counts = {"inclusion": 1, "exclusion": 1, "by_criteria": Counter()}
    total_records = 2
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    output_prisma_results(results, criteria_counts, total_records, output_dir=str(output_dir))

    # Check that all required files exist
    assert (output_dir / "output_results.csv").exists()  # backward compatibility
    assert (output_dir / "all_publications_found.csv").exists()  # new: all publications
    assert (output_dir / "selected_publications.csv").exists()  # new: selected only
    assert (output_dir / "results.json").exists()
    
    # Verify content of selected publications CSV (should only have included papers)
    with open(output_dir / "selected_publications.csv", 'r') as f:
        content = f.read()
        assert "Paper 1" in content  # included paper
        assert "Paper 2" not in content  # excluded paper

def test_create_prisma_drawio_diagram(tmp_path):
    criteria_counts = {"inclusion": 1, "exclusion": 1, "by_criteria": {"reason 1": 1}}
    total_records = 2
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    create_prisma_drawio_diagram(criteria_counts, total_records, output_dir=str(output_dir))

    assert (output_dir / "prisma_flow_diagram.drawio").exists()
