import pytest
from backend.app.modules.research.trends_analyzer import TrendsAnalyzer
from backend.app.modules.research.topic_scorer import TopicScorer

def test_trends_discovery_and_festivals():
    analyzer = TrendsAnalyzer()
    topics = analyzer.get_candidate_topics()
    assert len(topics) >= 4
    
    # Check that deity topics receive cultural boost
    shiva_topics = [t for t in topics if "शिव" in t["title_hindi"]]
    assert len(shiva_topics) > 0
    assert shiva_topics[0]["festival_boost"] > 0

def test_topic_scoring_algorithm():
    scorer = TopicScorer()
    sample = {
        "title_hindi": "भगवान शिव का नीलकंठ अवतार",
        "format_type": "SHORT",
        "search_volume": 85000,
        "competition_count": 12,
        "underexplored_aspect": "Deep cosmic dilemma",
        "festival_boost": 25
    }
    
    scores = scorer.calculate_score(sample)
    assert scores["audience_demand"] >= 20.0
    assert scores["viral_potential"] >= 15.0
    assert scores["storytelling_potential"] >= 14.0
    assert scores["total_score"] >= 80.0
    assert scores["qualified"] is True
