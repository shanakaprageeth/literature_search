# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of literature_search and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.

"""
Tests for new database API clients (IEEE, Springer, DBLP, Scopus).
"""
import pytest
from unittest.mock import patch, MagicMock
from literature_search.api_clients import (
    get_publications_ieee,
    get_publications_springer,
    get_publications_dblp,
    get_publications_scopus
)


class TestIEEEAPI:
    """Test IEEE Xplore API client."""
    
    @patch('literature_search.api_clients.robust_get')
    def test_get_publications_ieee_success(self, mock_get):
        """Test successful IEEE API response."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Deep Learning for Computer Vision',
                    'authors': {
                        'authors': [
                            {'full_name': 'John Doe'},
                            {'full_name': 'Jane Smith'}
                        ]
                    },
                    'publication_date': '2022-03-15',
                    'publication_title': 'IEEE Transactions on Neural Networks',
                    'content_type': 'Journals',
                    'doi': '10.1109/example',
                    'abstract': 'This paper presents...',
                    'html_url': 'https://ieeexplore.ieee.org/document/123'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test API call
        results = get_publications_ieee(['machine learning'], 'test_api_key', 10, 'OR')
        
        # Assertions
        assert len(results) == 1
        assert results[0]['Title'] == 'Deep Learning for Computer Vision'
        assert results[0]['Source'] == 'IEEE'
        assert results[0]['Authors'] == 'John Doe, Jane Smith'
        assert results[0]['Year'] == 2022
        assert results[0]['Journal'] == 'IEEE Transactions on Neural Networks'
        assert results[0]['DOI'] == '10.1109/example'
        
        # Verify API call
        mock_get.assert_called_once()
    
    @patch('literature_search.api_clients.robust_get')
    def test_get_publications_ieee_no_api_key(self, mock_get):
        """Test IEEE API without API key."""
        results = get_publications_ieee(['test'], None, 10, 'OR')
        assert results == []
        mock_get.assert_not_called()


class TestSpringerAPI:
    """Test Springer API client."""
    
    @patch('literature_search.api_clients.robust_get')
    def test_get_publications_springer_success(self, mock_get):
        """Test successful Springer API response."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'records': [
                {
                    'title': 'Machine Learning Applications',
                    'creators': [
                        {'creator': 'Alice Johnson'},
                        {'creator': 'Bob Wilson'}
                    ],
                    'publicationDate': '2021-06-01',
                    'publicationName': 'Machine Learning Journal',
                    'contentType': 'Article',
                    'language': 'en',
                    'doi': '10.1007/example',
                    'abstract': 'Abstract text...',
                    'url': [{'value': 'https://link.springer.com/article/123'}]
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test API call
        results = get_publications_springer(['machine learning'], 'test_api_key', 10, 'OR')
        
        # Assertions
        assert len(results) == 1
        assert results[0]['Title'] == 'Machine Learning Applications'
        assert results[0]['Source'] == 'Springer'
        assert results[0]['Authors'] == 'Alice Johnson, Bob Wilson'
        assert results[0]['Year'] == 2021
        assert results[0]['Journal'] == 'Machine Learning Journal'


class TestDBLPAPI:
    """Test DBLP API client."""
    
    @patch('literature_search.api_clients.robust_get')
    def test_get_publications_dblp_success(self, mock_get):
        """Test successful DBLP API response."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': {
                'hits': {
                    'hit': [
                        {
                            'info': {
                                'title': 'Neural Network Architectures',
                                'authors': {
                                    'author': [
                                        {'text': 'Charlie Brown'},
                                        {'text': 'Diana Prince'}
                                    ]
                                },
                                'year': '2020',
                                'venue': 'ICML',
                                'type': 'Conference Paper',
                                'doi': 'dblp_doi_example',
                                'url': 'https://dblp.org/rec/123'
                            }
                        }
                    ]
                }
            }
        }
        mock_get.return_value = mock_response
        
        # Test API call
        results = get_publications_dblp(['neural networks'], 10, 'OR')
        
        # Assertions
        assert len(results) == 1
        assert results[0]['Title'] == 'Neural Network Architectures'
        assert results[0]['Source'] == 'DBLP'
        assert results[0]['Authors'] == 'Charlie Brown, Diana Prince'
        assert results[0]['Year'] == 2020
        assert results[0]['Journal'] == 'ICML'


class TestScopusAPI:
    """Test Scopus API client."""
    
    @patch('literature_search.api_clients.robust_get')
    def test_get_publications_scopus_success(self, mock_get):
        """Test successful Scopus API response."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'search-results': {
                'entry': [
                    {
                        'dc:title': 'Deep Learning Survey',
                        'author': [
                            {'authname': 'Smith, J.'},
                            {'authname': 'Doe, A.'}
                        ],
                        'prism:coverDate': '2023-01-15',
                        'prism:publicationName': 'Nature Machine Intelligence',
                        'prism:aggregationType': 'Journal',
                        'prism:doi': '10.1038/example',
                        'link': [
                            {'@href': 'https://www.scopus.com/record/123'}
                        ]
                    }
                ]
            }
        }
        mock_get.return_value = mock_response
        
        # Test API call
        results = get_publications_scopus(['deep learning'], 'test_api_key', 10, 'OR')
        
        # Assertions
        assert len(results) == 1
        assert results[0]['Title'] == 'Deep Learning Survey'
        assert results[0]['Source'] == 'Scopus'
        assert results[0]['Authors'] == 'Smith, J., Doe, A.'
        assert results[0]['Year'] == 2023
        assert results[0]['Journal'] == 'Nature Machine Intelligence'
        assert results[0]['DOI'] == '10.1038/example'