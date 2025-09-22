# tests/test_keywords.py
from literature_search_shanaka.keywords import get_keywords

def test_get_keywords():
    research_topic = "Machine learning for healthcare applications"
    expected_keywords = {"machine", "learning", "healthcare", "applications"}
    extracted_keywords = set(get_keywords(research_topic))
    assert extracted_keywords == expected_keywords

def test_get_keywords_with_stopwords():
    research_topic = "The use of AI in the healthcare industry"
    expected_keywords = {"healthcare", "industry"}
    extracted_keywords = set(get_keywords(research_topic))
    assert extracted_keywords == expected_keywords
