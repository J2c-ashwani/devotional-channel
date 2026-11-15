from fastapi import APIRouter, Query, BackgroundTasks
from typing import Dict, Any, Optional
from backend.app.pipeline.orchestrator import ProductionPipelineOrchestrator
from backend.app.modules.character.registry import CharacterRegistry
from backend.app.modules.research.trends_analyzer import TrendsAnalyzer
from backend.app.modules.research.topic_scorer import TopicScorer
from backend.app.modules.analytics.metrics_collector import AnalyticsCollector
from backend.app.modules.analytics.feedback_learner import FeedbackLearner

router = APIRouter(prefix="/api/pipeline", tags=["Pipeline Execution"])

@router.post("/trigger")
async def trigger_pipeline_run(
    format_type: str = Query("SHORT", enum=["SHORT", "LONG_FORM", "MONTHLY_SPECIAL"]),
    simulate_upload: bool = True
) -> Dict[str, Any]:
    orchestrator = ProductionPipelineOrchestrator()
    result = await orchestrator.execute_production_run(
        format_type=format_type,
        simulate_upload=simulate_upload
    )
    return result

@router.get("/characters")
async def list_characters() -> Dict[str, Any]:
    registry = CharacterRegistry()
    return {"count": len(registry.characters), "characters": list(registry.characters.values())}

@router.get("/topics/discover")
async def discover_topics() -> Dict[str, Any]:
    analyzer = TrendsAnalyzer()
    scorer = TopicScorer()
    candidates = analyzer.get_candidate_topics()
    scored = []
    for c in candidates:
        scores = scorer.calculate_score(c)
        scored.append({
            "title_hindi": c["title_hindi"],
            "epic_source": c["epic_source"],
            "format": c["format_type"],
            "scores": scores
        })
    return {"count": len(scored), "topics": scored}

@router.get("/analytics/feedback")
async def get_analytics_feedback() -> Dict[str, Any]:
    short_metrics = AnalyticsCollector.harvest_video_analytics("yt_sample_01", "SHORT")
    long_metrics = AnalyticsCollector.harvest_video_analytics("yt_sample_02", "LONG_FORM")
    learner = FeedbackLearner.evaluate_retention_and_adapt([short_metrics, long_metrics])
    return {
        "recent_metrics": [short_metrics, long_metrics],
        "feedback_loop": learner
    }
