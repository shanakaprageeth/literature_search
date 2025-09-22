# Copyright (c) 2024 Shanaka Abeysiriwardhana
# This file is part of literature_search and is licensed under the GNU GPL v3.
# Please carry the copyright notice in derived works.
# See LICENSE file for details.
import re
from typing import List, Set

STOPWORDS: Set[str] = set([
    'the', 'and', 'for', 'with', 'that', 'from', 'this', 'have', 'are', 'was', 'were', 'has', 'had', 'but', 'not', 'all', 'can', 'will', 'into', 'out', 'over', 'under', 'more', 'than', 'such', 'their', 'they', 'them', 'been', 'also', 'which', 'when', 'where', 'who', 'what', 'how', 'why', 'your', 'about', 'after', 'before', 'between', 'each', 'other', 'some', 'any', 'our', 'his', 'her', 'its', 'on', 'in', 'of', 'to', 'by', 'as', 'at', 'an', 'or', 'is', 'a', 'be', 'it'
])

def get_keywords(research_topic: str) -> List[str]:
    """Extracts keywords from a research topic string."""
    words = re.findall(r'\b\w+\b', research_topic.lower())
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 3]
    return list(set(keywords))
