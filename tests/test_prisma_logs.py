# tests/test_prisma_logs.py
from literature_search.prisma_logs import output_prisma_results, create_prisma_drawio_diagram
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
    """Test the create_prisma_drawio_diagram function."""
    output_dir = tmp_path / "output"
    os.makedirs(output_dir, exist_ok=True)

    criteria_counts = {
        "inclusion": 50,
        "exclusion": 30,
        "by_criteria": {"criterion_1": 20, "criterion_2": 10}
    }
    total_records = 100
    total_duplicates = 20

    # Create a valid template with placeholders
    template_path = os.path.join(output_dir, "prisma_flow_diagram.drawio")
    with open(template_path, "w") as f:
        f.write(
            "<mxfile>"
            "{ADD_KEYWORDS}"
            "{TOTAL_RECORDS_WITH_DUPLICATES}"
            "{TOTAL_DUPLICATES}"
            "{TOTAL_RECORDS}"
            "{AFTER_INCLUSION_EXCLUSION}"
            "</mxfile>"
        )

    # Call the function
    create_prisma_drawio_diagram(criteria_counts, total_records, total_duplicates, output_dir=str(output_dir))

    # Verify the filled diagram file is created
    filled_diagram_path = os.path.join(output_dir, "prisma_flow_diagram_filled.drawio")
    assert os.path.exists(filled_diagram_path), "Filled diagram file was not created."

    # Verify the content of the filled diagram
    with open(filled_diagram_path, "r") as f:
        content = f.read()
        assert str(total_records + total_duplicates) in content
        assert str(total_duplicates) in content
        assert str(total_records) in content
        assert str(criteria_counts["inclusion"]) in content
