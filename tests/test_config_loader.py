# tests/test_config_loader.py
import pytest
from research_search_shanaka.config_loader import load_config
import json
from tempfile import NamedTemporaryFile

def test_load_config_valid():
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
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(valid_config, temp_file)
        temp_file.close()
        config = load_config(temp_file.name)
        assert config == valid_config

def test_load_config_missing_field():
    invalid_config = {
        "research_topic": "machine learning"
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(invalid_config, temp_file)
        temp_file.close()
        with pytest.raises(ValueError, match="Missing 'initial_prisma_values' in config file."):
            load_config(temp_file.name)

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
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
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
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
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
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(config, temp_file)
        temp_file.close()
        with pytest.raises(ValueError, match="'keywords' must be a list or comma-separated string."):
            load_config(temp_file.name)
