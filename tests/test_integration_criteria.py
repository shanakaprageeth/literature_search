"""
Integration tests for criteria mapping with CLI functionality.
"""
import pytest
import tempfile
import json
import os
from unittest.mock import patch, MagicMock
from literature_search.cli import search_prisma


def test_criteria_mapping_integration():
    """Test that the new criteria mapping system works with the CLI."""
    
    # Mock publications from different databases
    mock_publications = [
        {
            'Title': 'Neural Networks in Medicine',
            'Source': 'MED',  # PubMed source
            'Authors': 'Smith et al.',
            'Year': 2022,
            'Journal': 'Nature Medicine',
            'Language': 'English',
            'Type': 'journal-article',
            'Focus': 'neural networks'
        },
        {
            'Title': 'Deep Learning Conference Paper',
            'Source': 'CrossRef',
            'Authors': 'Jones et al.',
            'Year': 2021,
            'Journal': 'ICML Proceedings',
            'Language': 'English',
            'Type': 'proceedings-article',
            'Focus': 'neural networks'
        },
        {
            'Title': 'ML Preprint',
            'Source': 'arXiv',
            'Authors': 'Brown et al.',
            'Year': 2023,
            'Journal': 'arXiv',
            'Language': 'English',
            'Type': 'preprint',
            'Focus': 'neural networks'
        }
    ]
    
    # Create a test config with field-specific criteria
    config = {
        "research_topic": "neural networks",
        "keywords": ["neural networks"],
        "initial_prisma_values": {
            "inclusion_criteria": ["type:journal", "language:english"],
            "exclusion_criteria": ["type:proceedings", "source:arxiv"],
            "databases": ["PubMed", "CrossRef", "arXiv"],
            "date_range": "2020-2025"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_file = f.name
    
    with tempfile.TemporaryDirectory() as output_dir:
        # Mock the search_database function to return our test publications
        with patch('literature_search.cli.search_database') as mock_search:
            mock_search.return_value = mock_publications
            
            # Mock the remove_duplicates function
            with patch('literature_search.cli.remove_duplicates') as mock_remove_dups:
                mock_remove_dups.return_value = (mock_publications, 0)
                
                # Mock the output functions to avoid file I/O during test
                with patch('literature_search.cli.output_prisma_results') as mock_output:
                    with patch('literature_search.cli.create_prisma_drawio_diagram'):
                        # Run the search
                        search_prisma(config_file, output_dir=output_dir)
                        
                        # Verify the output function was called with the right data
                        assert mock_output.called
                        results = mock_output.call_args[0][0]  # First argument to output_prisma_results
                        criteria_counts = mock_output.call_args[0][1]  # Second argument
                        
                        # Check that publications were filtered correctly
                        included_pubs = [r for r in results if r['Included'] == 'Yes']
                        excluded_pubs = [r for r in results if r['Included'] == 'No']
                        
                        # Should include: Neural Networks in Medicine (type:journal-article matches type:journal)
                        # Should exclude: Deep Learning Conference Paper (type:proceedings-article matches exclusion type:proceedings)
                        # Should exclude: ML Preprint (source:arXiv matches exclusion source:arxiv)
                        
                        assert len(included_pubs) == 1
                        assert included_pubs[0]['Title'] == 'Neural Networks in Medicine'
                        
                        assert len(excluded_pubs) == 2
                        excluded_titles = {p['Title'] for p in excluded_pubs}
                        assert 'Deep Learning Conference Paper' in excluded_titles
                        assert 'ML Preprint' in excluded_titles
                        
                        # Check reasons for exclusion
                        conference_paper = next(r for r in results if r['Title'] == 'Deep Learning Conference Paper')
                        arxiv_paper = next(r for r in results if r['Title'] == 'ML Preprint')
                        
                        assert 'Has exclusion type: proceedings' in conference_paper['Reasons']
                        assert 'Has exclusion source: arxiv' in arxiv_paper['Reasons']
    
    # Clean up
    os.unlink(config_file)


def test_backward_compatibility():
    """Test that old-style criteria (without field specification) still work."""
    
    mock_publications = [
        {
            'Title': 'Journal Article',
            'Source': 'MED',
            'Authors': 'Author A',
            'Year': 2022,
            'Journal': 'Some Journal',
            'Language': 'English',
            'Type': 'journal-article',
            'Focus': 'test'
        },
        {
            'Title': 'Review Paper',
            'Source': 'MED',
            'Authors': 'Author B',
            'Year': 2022,
            'Journal': 'Review Journal',
            'Language': 'English',
            'Type': 'review',
            'Focus': 'test'
        }
    ]
    
    # Config with old-style criteria (no field specifications)
    config = {
        "research_topic": "test topic",
        "keywords": ["test"],
        "initial_prisma_values": {
            "inclusion_criteria": ["journal", "review"],
            "exclusion_criteria": ["conference"],
            "databases": ["PubMed"],
            "date_range": "2020-2025"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_file = f.name
    
    with tempfile.TemporaryDirectory() as output_dir:
        with patch('literature_search.cli.search_database') as mock_search:
            mock_search.return_value = mock_publications
            
            with patch('literature_search.cli.remove_duplicates') as mock_remove_dups:
                mock_remove_dups.return_value = (mock_publications, 0)
                
                with patch('literature_search.cli.output_prisma_results') as mock_output:
                    with patch('literature_search.cli.create_prisma_drawio_diagram'):
                        search_prisma(config_file, output_dir=output_dir)
                        
                        results = mock_output.call_args[0][0]
                        
                        # Both publications should be included (old-style criteria default to Type field)
                        included_pubs = [r for r in results if r['Included'] == 'Yes']
                        assert len(included_pubs) == 2
    
    os.unlink(config_file)