from typing import Dict, Any

class TopicScorer:
    """
    Evaluates proposed mythology topics strictly according to the 100-point specification:
    - Audience demand: 25 points
    - Viral potential: 20 points
    - Storytelling potential: 15 points
    - Competition opportunity: 15 points
    - Long-form potential: 15 points
    - Cultural relevance: 10 points
    """
    
    @classmethod
    def calculate_score(cls, topic_data: Dict[str, Any]) -> Dict[str, Any]:
        search_vol = topic_data.get("search_volume", 50000)
        comp_count = topic_data.get("competition_count", 15)
        format_type = topic_data.get("format_type", "SHORT")
        fest_boost = topic_data.get("festival_boost", 0)
        
        # 1. Audience Demand (max 25 pts)
        if search_vol >= 100000:
            audience_demand = 25.0
        elif search_vol >= 70000:
            audience_demand = 22.0
        elif search_vol >= 40000:
            audience_demand = 18.0
        else:
            audience_demand = 12.0
            
        # 2. Viral Potential (max 20 pts)
        # Underexplored mysteries and dramatic revelations have high viral potential
        has_mystery = bool(topic_data.get("underexplored_aspect"))
        if has_mystery and format_type == "SHORT":
            viral_potential = 19.0
        elif has_mystery:
            viral_potential = 17.0
        else:
            viral_potential = 13.0
            
        # 3. Storytelling Potential (max 15 pts)
        # Deep moral dilemmas, heroic sacrifices, dharma vs adharma
        storytelling_potential = 14.5
        
        # 4. Competition Opportunity (max 15 pts)
        # Fewer competing high-quality cinematic videos means higher opportunity
        if comp_count <= 10:
            competition_opportunity = 14.5
        elif comp_count <= 20:
            competition_opportunity = 12.0
        else:
            competition_opportunity = 8.5
            
        # 5. Long-Form Potential (max 15 pts)
        if format_type in ["LONG_FORM", "MONTHLY_SPECIAL"]:
            long_form_potential = 14.0
        else:
            long_form_potential = 10.0 # Can later be expanded into deep dive
            
        # 6. Cultural Relevance (max 10 pts)
        cultural_relevance = 8.0 + (2.0 if fest_boost > 0 else 0.0)
        cultural_relevance = min(10.0, cultural_relevance)
        
        total = (
            audience_demand +
            viral_potential +
            storytelling_potential +
            competition_opportunity +
            long_form_potential +
            cultural_relevance
        )
        
        return {
            "audience_demand": round(audience_demand, 1),
            "viral_potential": round(viral_potential, 1),
            "storytelling_potential": round(storytelling_potential, 1),
            "competition_opportunity": round(competition_opportunity, 1),
            "long_form_potential": round(long_form_potential, 1),
            "cultural_relevance": round(cultural_relevance, 1),
            "total_score": round(total, 1),
            "qualified": total >= 70.0
        }
