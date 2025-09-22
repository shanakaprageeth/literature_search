# tests/test_config_loader.py
import pytest
from literature_search_shanaka.config_loader import load_config
import json
import sys
from tempfile import NamedTemporaryFile
from unittest.mock import patch
import io


def test_load_config_valid():
    """Test loading a valid configuration file."""
    valid_config = {
        "initial_prisma_values": {
            "date_range": "2000-2020",
            "inclusion_criteria": ["journal article"],
            "exclusion_criteria": ["review"],
            "databases": ["PubMed"]
        },
        "research_topic": "machine learning",
        "api_keys": {}
    }
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(valid_config, temp_file)
        temp_file.close()
        config = load_config(temp_file.name)
        assert config == valid_config


def test_load_config_missing_file():
    """Test loading a non-existent configuration file."""
    with pytest.raises(SystemExit) as exc_info:
        load_config('nonexistent_file.json')
    assert exc_info.value.code == 1


def test_load_config_missing_field():
    """Test configuration missing required initial_prisma_values field."""
    invalid_config = {
        "research_topic": "machine learning"
    }
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(invalid_config, temp_file)
        temp_file.close()
        with pytest.raises(SystemExit) as exc_info:
            load_config(temp_file.name)
        assert exc_info.value.code == 1


def test_load_config_invalid_json():
    """Test configuration file with invalid JSON syntax."""
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        temp_file.write('{ invalid json }')
        temp_file.close()
        with pytest.raises(SystemExit) as exc_info:
            load_config(temp_file.name)
        assert exc_info.value.code == 1

def test_load_config_keywords_comma_separated():
    """Test that comma-separated keywords string is converted to list."""
    config = {
        "initial_prisma_values": {
            "date_range": "2000-2020",
            "inclusion_criteria": ["journal article"],
            "exclusion_criteria": ["review"],
            "databases": ["PubMed"]
        },
        "keywords": "machine learning, deep learning, neural networks",
        "api_keys": {}
    }
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(config, temp_file)
        temp_file.close()
        loaded_config = load_config(temp_file.name)
        expected_keywords = ["machine learning", "deep learning", "neural networks"]
        assert loaded_config["keywords"] == expected_keywords


def test_load_config_keywords_list():
    """Test that keyword list is preserved and cleaned."""
    config = {
        "initial_prisma_values": {
            "date_range": "2000-2020",
            "inclusion_criteria": ["journal article"],
            "exclusion_criteria": ["review"],
            "databases": ["PubMed"]
        },
        "keywords": ["machine learning", " deep learning ", "neural networks"],
        "api_keys": {}
    }
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(config, temp_file)
        temp_file.close()
        loaded_config = load_config(temp_file.name)
        expected_keywords = ["machine learning", "deep learning", "neural networks"]
        assert loaded_config["keywords"] == expected_keywords


def test_load_config_keywords_invalid_type():
    """Test that invalid keyword type raises error."""
    config = {
        "initial_prisma_values": {
            "date_range": "2000-2020",
            "inclusion_criteria": ["journal article"],
            "exclusion_criteria": ["review"],
            "databases": ["PubMed"]
        },
        "keywords": 123,  # Invalid type
        "api_keys": {}
    }
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(config, temp_file)
        temp_file.close()
        with pytest.raises(SystemExit) as exc_info:
            load_config(temp_file.name)
        assert exc_info.value.code == 1


def test_load_config_missing_both_topic_and_keywords():
    """Test configuration missing both research_topic and keywords."""
    config = {
        "initial_prisma_values": {
            "date_range": "2000-2020",
            "inclusion_criteria": ["journal article"],
            "exclusion_criteria": ["review"],
        }
    }
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(config, temp_file)
        temp_file.close()
        with pytest.raises(SystemExit) as exc_info:
            load_config(temp_file.name)
        assert exc_info.value.code == 1


def test_load_config_invalid_date_range():
    """Test configuration with invalid date range format."""
    config = {
        "initial_prisma_values": {
            "date_range": "invalid-date",
            "inclusion_criteria": ["journal article"],
            "exclusion_criteria": ["review"],
        },
        "research_topic": "test topic"
    }
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(config, temp_file)
        temp_file.close()
        with pytest.raises(SystemExit) as exc_info:
            load_config(temp_file.name)
        assert exc_info.value.code == 1


def test_load_config_date_range_backwards():
    """Test configuration with backwards date range."""
    config = {
        "initial_prisma_values": {
            "date_range": "2025-2015",  # Start > End
            "inclusion_criteria": ["journal article"],
            "exclusion_criteria": ["review"],
        },
        "research_topic": "test topic"
    }
    with NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(config, temp_file)
        temp_file.close()
        with pytest.raises(SystemExit) as exc_info:
            load_config(temp_file.name)
        assert exc_info.value.code == 1
