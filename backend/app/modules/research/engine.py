import uuid
from typing import List, Dict, Any
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import ContentTopic, SystemLog
from backend.app.modules.research.trends_analyzer import TrendsAnalyzer
from backend.app.modules.research.topic_scorer import TopicScorer

class ContentResearchEngine:
    """
    Module A: Content Research Engine.
    Discovers, scores, and prioritizes topics based on trends, audience demand, and scripture potential.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.analyzer = TrendsAnalyzer()
        self.scorer = TopicScorer()
        
    async def discover_and_rank_topics(self) -> List[Dict[str, Any]]:
        raw_candidates = self.analyzer.get_candidate_topics()
        scored_topics = []
        
        # Check existing topics to prevent duplicates
        stmt = select(ContentTopic.title_hindi)
        result = await self.db.execute(stmt)
        existing_titles = set(result.scalars().all())
        
        for candidate in raw_candidates:
            if candidate["title_hindi"] in existing_titles:
                continue
                
            scores = self.scorer.calculate_score(candidate)
            topic_id = f"topic_{uuid.uuid4().hex[:10]}"
            
            topic = ContentTopic(
                id=topic_id,
                title_hindi=candidate["title_hindi"],
                title_english=candidate["title_english"],
                epic_source=candidate["epic_source"],
                format_type=candidate["format_type"],
                audience_demand_score=scores["audience_demand"],
                viral_potential_score=scores["viral_potential"],
                storytelling_potential_score=scores["storytelling_potential"],
                competition_opportunity_score=scores["competition_opportunity"],
                long_form_potential_score=scores["long_form_potential"],
                cultural_relevance_score=scores["cultural_relevance"],
                total_score=scores["total_score"],
                search_evidence={
                    "search_volume": candidate["search_volume"],
                    "keywords": candidate["keywords"],
                    "underexplored_aspect": candidate["underexplored_aspect"]
                },
                competing_videos=[{"count": candidate["competition_count"]}],
                cultural_festival_link=candidate.get("deity"),
                priority_order=1 if scores["total_score"] >= 85 else 2,
                status="PROPOSED"
            )
            
            self.db.add(topic)
            scored_topics.append({
                "id": topic_id,
                "title_hindi": candidate["title_hindi"],
                "score": scores["total_score"],
                "format": candidate["format_type"]
            })
            
        await self.db.commit()
        
        log = SystemLog(
            level="INFO",
            module="RESEARCH_ENGINE",
            event="TOPICS_DISCOVERED",
            message=f"Discovered and scored {len(scored_topics)} new mythology topics",
            context_data={"topics": scored_topics}
        )
        self.db.add(log)
        await self.db.commit()
        
        return scored_topics

    async def get_highest_priority_topic(self, format_type: str = "SHORT") -> ContentTopic:
        stmt = select(ContentTopic).where(
            ContentTopic.format_type == format_type,
            ContentTopic.status == "PROPOSED"
        ).order_by(ContentTopic.total_score.desc())
        
        result = await self.db.execute(stmt)
        topic = result.scalars().first()
        return topic
