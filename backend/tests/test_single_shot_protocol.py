import pytest
from backend.app.modules.qc.qc_engine import QualityControlEngine
from backend.app.modules.qc.hard_rules import HardRuleEnforcer
from backend.app.modules.mythology.episodic_ledger import EpisodicLedger

def test_single_shot_duration_hard_blocker():
    """Ensure clips under 60 seconds are blocked from publishing."""
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 500000, "duration_sec": 34.0},  # 34s is rushed!
        is_duplicate=False,
        format_type="SHORT"
    )
    assert qc["is_passed"] is False
    assert qc["hard_blocker_triggered"] is True
    assert "below mandatory 60.0s minimum" in qc["hard_blocker_reason"]

def test_single_shot_iconography_hard_blocker():
    """Ensure peacock feather on Prabhu Shri Rama triggers hard blocker."""
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 500000, "duration_sec": 65.0},
        is_duplicate=False,
        format_type="SHORT",
        script_data={"full_screenplay_devanagari": "श्री राम के मुकुट पर मयूर पंख चमक रहा था"},
        topic_title="श्री राम का धनुर्भंग"
    )
    assert qc["is_passed"] is False
    assert qc["hard_blocker_triggered"] is True
    assert "peacock feather is strictly prohibited" in qc["hard_blocker_reason"]

def test_single_shot_duplicate_suppression():
    """Ensure previously published episodes are blocked from duplicate re-uploading."""
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 500000, "duration_sec": 65.0},
        is_duplicate=True,  # Duplicate!
        format_type="SHORT"
    )
    assert qc["is_passed"] is False
    assert qc["hard_blocker_triggered"] is True
    assert "Duplicate Content Failure" in qc["hard_blocker_reason"]

def test_single_shot_perfect_pass():
    """Ensure complete 65s authentic video passes single-shot QC cleanly."""
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 50000000, "duration_sec": 65.0},
        is_duplicate=False,
        format_type="SHORT",
        director_review={"director_signoff": True, "director_score": 98.0},
        script_data={"full_screenplay_devanagari": "प्रभु श्री राम ने शिवजी के पिनाक धनुष को उठाया"},
        topic_title="श्री राम का धनुर्भंग"
    )
    assert qc["is_passed"] is True
    assert qc["hard_blocker_triggered"] is False
    assert qc["overall_score"] >= 90.0


def test_single_shot_talking_head_rule_blocker():
    """Lock talking-head rule for Ramayana & Mahabharata: character dialogue cannot be flattened into pure narrator."""
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 50000000, "duration_sec": 72.0},
        is_duplicate=False,
        format_type="SHORT",
        director_review={"director_signoff": True, "director_score": 98.0},
        script_data={
            "full_screenplay_devanagari": "देवव्रत ने भीष्म प्रतिज्ञा ली।",
            "scenes": [{
                "scene_index": 2,
                "scene_name": "Bhishma Pratigya",
                "duration_sec": 12.0,
                "dialogue_speaker": "राजकुमार देवव्रत",
                "dialogue_hindi": "मैं कभी विवाह नहीं करूँगा!",
                "is_pure_narrator": True
            }]
        },
        topic_title="देवव्रत की भीष्म प्रतिज्ञा"
    )
    assert qc["is_passed"] is False
    assert qc["hard_blocker_triggered"] is True
    assert "Talking-Head Rule Failure" in qc["hard_blocker_reason"]


def test_single_shot_audio_pacing_blocker():
    """Ensure overly dense Hindi blocks (>2.6 words/sec) in Vertex T2V are rejected before audio clipping occurs."""
    dense_text = " ".join(["शब्द"] * 40)  # 40 words in 12s = 3.33 w/s
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 50000000, "duration_sec": 75.0},
        is_duplicate=False,
        format_type="SHORT",
        director_review={"director_signoff": True, "director_score": 98.0},
        script_data={
            "full_screenplay_devanagari": dense_text,
            "scenes": [{
                "scene_index": 1,
                "scene_name": "Overstuffed Narration",
                "duration_sec": 12.0,
                "render_mode": "vertex_omni_t2v",
                "narrator_text_hindi": dense_text,
                "dialogue_speaker": None,
                "dialogue_hindi": ""
            }]
        },
        topic_title="महाभारत भाग 2"
    )
    assert qc["is_passed"] is False
    assert qc["hard_blocker_triggered"] is True
    assert "Audio Pacing Failure" in qc["hard_blocker_reason"]


def test_mahabharata_bhishma_pratigya_grounding_and_director_rules():
    """Verify Mahabharata Ep 2 canonical scripture grounding and Director character prompt lock."""
    from backend.app.modules.mythology.source_library import SourceLibrary
    from backend.app.agents.director_agent import ProductionDirectorAgent

    topic = "देवव्रत की 'भीष्म प्रतिज्ञा': पिता के सुख के लिए आजीवन ब्रह्मचर्य और राज्य का त्याग"
    src = SourceLibrary.get_canonical_source(topic)
    assert src is not None
    assert "Adi Parva" in src["kanda_or_parva"]
    assert "100" in src["sarga_or_adhyaya"]

    prompt = ProductionDirectorAgent.audit_scene_prompt("देवव्रत भीष्म", "Speaking bravely on the Yamuna riverbank")
    assert "ivory-white and gold" in prompt and "Kuru" in prompt


def test_autonomous_pipeline_tracks_and_youtube_smart_schedule():
    """Verify Morning/Evening scriptural track grounding, pixel-wrap Hindi subtitles, and YouTube past-slot fallback."""
    from datetime import datetime, timedelta
    import pytz
    from backend.app.modules.mythology.source_library import SourceLibrary
    from backend.app.agents.director_agent import ProductionDirectorAgent
    from backend.app.modules.youtube.uploader import YouTubeUploader

    # Eklavya (Mahabharata Ep 3) must NOT fall back to Ramayana citations
    eklavya_src = SourceLibrary.get_canonical_source("एकलव्य की गुरु-दक्षिणा: जब निष्ठावान शिष्य ने मुस्कुराते हुए काट दिया अपना अंगूठा")
    assert eklavya_src is not None and "Mahabharata" in eklavya_src["epic_name"]

    # Pixel-width Devanagari wrap helper produces clean non-empty lines and wraps when width is constrained
    lines = ProductionDirectorAgent.wrap_hindi_lines(
        "सुनिए निषादराज! आज ही मैं हस्तिनापुर के राजसिंहासन का त्याग करता हूँ—सत्यवती का पुत्र ही सम्राट होगा!",
        max_width=250,
    )
    assert len(lines) >= 2 and all(l.strip() for l in lines)

    # Simulate YouTube uploader future vs immediate slot threshold
    yt = YouTubeUploader()
    ist = pytz.timezone("Asia/Kolkata")
    past_dt = datetime.now(ist) - timedelta(hours=1)
    assert yt.convert_ist_to_utc_rfc3339("07:00", past_dt).endswith("Z")

    # Cross-platform Devanagari font loader must never crash on Linux CI or macOS
    font = ProductionDirectorAgent.get_hindi_font(36)
    assert font is not None


