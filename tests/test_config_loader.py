# tests/test_config_loader.py
import pytest
from research_search_shanaka.config_loader import load_config
import json
from tempfile import NamedTemporaryFile
import warnings


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
        with pytest.raises(ValueError, match="Missing required field 'initial_prisma_values'"):
            load_config(temp_file.name)


def test_load_config_invalid_date_range():
    invalid_config = {
        "initial_prisma_values": {
            "date_range": "2025-2015",  # Start year > end year
            "inclusion_criteria": ["journal"],
            "exclusion_criteria": ["review"]
        },
        "research_topic": "machine learning"
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(invalid_config, temp_file)
        temp_file.close()
        with pytest.raises(ValueError, match="Start year .* cannot be greater than end year"):
            load_config(temp_file.name)


def test_load_config_invalid_date_format():
    invalid_config = {
        "initial_prisma_values": {
            "date_range": "invalid-date",
            "inclusion_criteria": ["journal"],
            "exclusion_criteria": ["review"]
        },
        "research_topic": "machine learning"
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(invalid_config, temp_file)
        temp_file.close()
        with pytest.raises(ValueError, match="Invalid date_range format"):
            load_config(temp_file.name)


def test_load_config_invalid_database():
    invalid_config = {
        "initial_prisma_values": {
            "date_range": "2015-2025",
            "inclusion_criteria": ["journal"],
            "exclusion_criteria": ["review"],
            "databases": ["InvalidDB", "PubMed"]
        },
        "research_topic": "machine learning"
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(invalid_config, temp_file)
        temp_file.close()
        with pytest.raises(ValueError, match="Invalid database.*InvalidDB"):
            load_config(temp_file.name)


def test_load_config_missing_api_key_for_core():
    invalid_config = {
        "initial_prisma_values": {
            "date_range": "2015-2025",
            "inclusion_criteria": ["journal"],
            "exclusion_criteria": ["review"],
            "databases": ["CORE", "PubMed"]
        },
        "research_topic": "machine learning",
        "api_keys": {}
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(invalid_config, temp_file)
        temp_file.close()
        with pytest.raises(ValueError, match="Missing required API keys for database.*CORE"):
            load_config(temp_file.name)


def test_load_config_missing_research_topic_and_keywords():
    invalid_config = {
        "initial_prisma_values": {
            "date_range": "2015-2025",
            "inclusion_criteria": ["journal"],
            "exclusion_criteria": ["review"]
        }
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(invalid_config, temp_file)
        temp_file.close()
        with pytest.raises(ValueError, match="Either 'research_topic'.*or 'keywords'.*must be provided"):
            load_config(temp_file.name)


def test_load_config_invalid_criteria_type():
    invalid_config = {
        "initial_prisma_values": {
            "date_range": "2015-2025",
            "inclusion_criteria": "not a list",  # Should be list
            "exclusion_criteria": ["review"]
        },
        "research_topic": "machine learning"
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(invalid_config, temp_file)
        temp_file.close()
        with pytest.raises(ValueError, match="'inclusion_criteria' must be a list"):
            load_config(temp_file.name)


def test_load_config_warnings_for_optional_api_key():
    valid_config = {
        "initial_prisma_values": {
            "date_range": "2015-2025",
            "inclusion_criteria": ["journal"],
            "exclusion_criteria": ["review"],
            "databases": ["SemanticScholar", "PubMed"]
        },
        "research_topic": "machine learning",
        "api_keys": {}
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(valid_config, temp_file)
        temp_file.close()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            load_config(temp_file.name)
            # Check that warning was issued for missing SemanticScholar API key
            warning_messages = [str(warning.message) for warning in w]
            assert any("SemanticScholar" in msg for msg in warning_messages)


def test_load_config_warning_empty_criteria():
    valid_config = {
        "initial_prisma_values": {
            "date_range": "2015-2025",
            "inclusion_criteria": [],  # Empty list should trigger warning
            "exclusion_criteria": ["review"]
        },
        "research_topic": "machine learning"
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(valid_config, temp_file)
        temp_file.close()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            load_config(temp_file.name)
            # Check that warning was issued for empty inclusion criteria
            warning_messages = [str(warning.message) for warning in w]
            assert any("inclusion_criteria" in msg and "empty" in msg for msg in warning_messages)


def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError, match="Configuration file.*not found"):
        load_config("/non/existent/file.json")


def test_load_config_invalid_json():
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        temp_file.write('{"invalid": json,}')  # Invalid JSON
        temp_file.close()
        with pytest.raises(json.JSONDecodeError, match="Invalid JSON"):
            load_config(temp_file.name)


def test_load_config_with_keywords_only():
    valid_config = {
        "initial_prisma_values": {
            "date_range": "2015-2025",
            "inclusion_criteria": ["journal"],
            "exclusion_criteria": ["review"]
        },
        "keywords": ["machine learning", "AI"]
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(valid_config, temp_file)
        temp_file.close()
        config = load_config(temp_file.name)
        assert config == valid_config


def test_load_config_both_topic_and_keywords():
    valid_config = {
        "initial_prisma_values": {
            "date_range": "2015-2025",
            "inclusion_criteria": ["journal"],
            "exclusion_criteria": ["review"]
        },
        "research_topic": "AI research",
        "keywords": ["machine learning", "AI"]
    }
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        json.dump(valid_config, temp_file)
        temp_file.close()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            config = load_config(temp_file.name)
            # Check that info message was issued about using keywords over topic
            warning_messages = [str(warning.message) for warning in w]
            assert any("Both 'research_topic' and 'keywords' provided" in msg for msg in warning_messages)
        assert config == valid_config
