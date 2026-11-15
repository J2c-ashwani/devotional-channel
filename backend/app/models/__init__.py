from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class ChannelSetting(Base):
    __tablename__ = "channel_settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(100), unique=True, nullable=False)
    channel_name = Column(String(200), nullable=False)
    niche = Column(String(200), nullable=False)
    emergency_kill_switch = Column(Boolean, default=False)
    monthly_budget_usd = Column(Float, default=150.0)
    timezone = Column(String(50), default="Asia/Kolkata")
    settings_json = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ContentTopic(Base):
    __tablename__ = "content_topics"
    
    id = Column(String(50), primary_key=True)
    title_hindi = Column(String(300), nullable=False)
    title_english = Column(String(300), nullable=False)
    epic_source = Column(String(100), nullable=False) # Ramayana, Mahabharata, Shiva Purana, etc.
    format_type = Column(String(20), nullable=False)  # SHORT, LONG_FORM, MONTHLY_SPECIAL
    
    # 100-point scoring breakdown
    audience_demand_score = Column(Float, default=0.0)      # Max 25
    viral_potential_score = Column(Float, default=0.0)      # Max 20
    storytelling_potential_score = Column(Float, default=0.0) # Max 15
    competition_opportunity_score = Column(Float, default=0.0) # Max 15
    long_form_potential_score = Column(Float, default=0.0)  # Max 15
    cultural_relevance_score = Column(Float, default=0.0)   # Max 10
    total_score = Column(Float, default=0.0)                # Sum / 100
    
    search_evidence = Column(JSON, default=dict)
    competing_videos = Column(JSON, default=list)
    cultural_festival_link = Column(String(100), nullable=True)
    priority_order = Column(Integer, default=1)
    status = Column(String(50), default="PROPOSED") # PROPOSED, APPROVED, IN_PRODUCTION, PUBLISHED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)

class ResearchSource(Base):
    __tablename__ = "research_sources"
    
    id = Column(String(50), primary_key=True)
    topic_id = Column(String(50), ForeignKey("content_topics.id"), nullable=True)
    epic_name = Column(String(100), nullable=False) # e.g. "Valmiki Ramayana - Yuddha Kanda"
    chapter_or_canto = Column(String(100), nullable=True)
    source_edition = Column(String(200), nullable=False) # Canonical public-domain reference
    original_text_excerpt = Column(Text, nullable=True)
    summary_hindi = Column(Text, nullable=False)
    factual_bullet_points = Column(JSON, default=list)
    traditional_variations = Column(JSON, default=list)
    copyright_public_domain_certified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class StoryScript(Base):
    __tablename__ = "story_scripts"
    
    id = Column(String(50), primary_key=True)
    topic_id = Column(String(50), ForeignKey("content_topics.id"), nullable=False)
    version = Column(Integer, default=1)
    target_format = Column(String(20), nullable=False) # SHORT, LONG_FORM, MONTHLY_SPECIAL
    language = Column(String(10), default="hi")
    
    opening_hook_hindi = Column(Text, nullable=False)
    narrative_body_hindi = Column(Text, nullable=False)
    climax_hindi = Column(Text, nullable=False)
    conclusion_hindi = Column(Text, nullable=False)
    full_screenplay_devanagari = Column(Text, nullable=False)
    dialogue_excerpts = Column(JSON, default=list)
    
    estimated_duration_sec = Column(Integer, nullable=False)
    originality_score = Column(Float, default=100.0) # Check against previous scripts
    fact_check_passed = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ScriptVersion(Base):
    __tablename__ = "script_versions"
    
    id = Column(String(50), primary_key=True)
    script_id = Column(String(50), ForeignKey("story_scripts.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    changes_made = Column(Text, nullable=False)
    screenplay_snapshot = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CharacterProfile(Base):
    __tablename__ = "character_profiles"
    
    id = Column(String(50), primary_key=True)
    name_hindi = Column(String(100), nullable=False)
    name_english = Column(String(100), nullable=False)
    epithets = Column(JSON, default=list)
    visual_dna = Column(JSON, nullable=False) # facial, clothing, jewellery, proportions, hairstyle, skin_tone, age, accessories
    voice_profile = Column(JSON, nullable=False) # provider voice id, pitch, rate, style
    personality = Column(Text, nullable=False)
    prompt_keywords = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CharacterReferenceAsset(Base):
    __tablename__ = "character_reference_assets"
    
    id = Column(String(50), primary_key=True)
    character_id = Column(String(50), ForeignKey("character_profiles.id"), nullable=False)
    asset_type = Column(String(50), default="PORTRAIT") # PORTRAIT, ACTION_POSE, FULL_BODY
    file_path = Column(String(500), nullable=False)
    prompt_used = Column(Text, nullable=False)
    seed = Column(Integer, default=42)
    is_approved_dna = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Storyboard(Base):
    __tablename__ = "storyboards"
    
    id = Column(String(50), primary_key=True)
    script_id = Column(String(50), ForeignKey("story_scripts.id"), nullable=False)
    scene_count = Column(Integer, nullable=False)
    aspect_ratio = Column(String(10), default="9:16") # 9:16 or 16:9
    scenes_data = Column(JSON, nullable=False) # list of scene specs: id, visual_prompt, camera, lighting, duration, audio_segment
    status = Column(String(50), default="PLANNED")
    created_at = Column(DateTime, default=datetime.utcnow)

class SceneAsset(Base):
    __tablename__ = "scene_assets"
    
    id = Column(String(50), primary_key=True)
    storyboard_id = Column(String(50), ForeignKey("storyboards.id"), nullable=False)
    scene_index = Column(Integer, nullable=False)
    asset_type = Column(String(20), nullable=False) # IMAGE, VIDEO
    file_path = Column(String(500), nullable=False)
    provider = Column(String(50), nullable=False) # gemini, modular_motion, mock
    prompt = Column(Text, nullable=False)
    camera_movement = Column(String(100), default="Cinematic slow push in")
    duration_sec = Column(Float, nullable=False)
    status = Column(String(50), default="GENERATED")
    created_at = Column(DateTime, default=datetime.utcnow)

class Voiceover(Base):
    __tablename__ = "voiceovers"
    
    id = Column(String(50), primary_key=True)
    script_id = Column(String(50), ForeignKey("story_scripts.id"), nullable=False)
    scene_index = Column(Integer, nullable=False)
    file_path = Column(String(500), nullable=False)
    duration_seconds = Column(Float, nullable=False)
    provider = Column(String(50), default="edge_tts")
    transcript_hindi = Column(Text, nullable=False)
    ssml_payload = Column(Text, nullable=True)
    loudness_lufs = Column(Float, default=-14.0)
    audio_quality_score = Column(Float, default=95.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class MusicAsset(Base):
    __tablename__ = "music_assets"
    
    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    mood = Column(String(100), nullable=False) # Epic, Devotional, Intense Battle, Meditative, Tragic
    genre = Column(String(100), default="Indian Classical Orchestral")
    bpm = Column(Integer, default=90)
    file_path = Column(String(500), nullable=False)
    license_type = Column(String(100), default="Royalty-Free / Generated Original")
    usage_rights = Column(String(200), default="Commercial Monetized YouTube Production")
    attribution_required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProductionJob(Base):
    __tablename__ = "production_jobs"
    
    id = Column(String(50), primary_key=True)
    topic_id = Column(String(50), ForeignKey("content_topics.id"), nullable=False)
    script_id = Column(String(50), ForeignKey("story_scripts.id"), nullable=True)
    storyboard_id = Column(String(50), ForeignKey("storyboards.id"), nullable=True)
    format_type = Column(String(20), nullable=False) # SHORT, LONG_FORM, MONTHLY_SPECIAL
    
    status = Column(String(50), default="QUEUED")
    # QUEUED, RESEARCHING, SCRIPTING, STORYBOARDING, RENDERING, QC_AUDIT, READY_FOR_UPLOAD, UPLOADED, PUBLISHED, FAILED, QUARANTINED
    
    progress_percentage = Column(Integer, default=0)
    output_video_path = Column(String(500), nullable=True)
    output_thumbnail_path = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)
    execution_timeline = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class QualityControlReport(Base):
    __tablename__ = "quality_control_reports"
    
    id = Column(String(50), primary_key=True)
    job_id = Column(String(50), ForeignKey("production_jobs.id"), nullable=False)
    overall_score = Column(Float, nullable=False) # 0 to 100, min 90 to pass
    is_passed = Column(Boolean, default=False)
    hard_blocker_triggered = Column(Boolean, default=False)
    hard_blocker_reason = Column(String(300), nullable=True)
    
    # 12 specific factor audit breakdown
    research_validation_score = Column(Float, default=20.0)      # max 20
    factual_consistency_score = Column(Float, default=20.0)      # max 20
    story_originality_score = Column(Float, default=20.0)        # max 20
    visual_quality_score = Column(Float, default=15.0)           # max 15
    audio_quality_score = Column(Float, default=10.0)            # max 10
    copyright_safety_score = Column(Float, default=10.0)         # max 10
    policy_compliance_score = Column(Float, default=10.0)        # max 10
    
    detailed_audit_logs = Column(JSON, default=dict)
    evaluated_at = Column(DateTime, default=datetime.utcnow)

class CopyrightRecord(Base):
    __tablename__ = "copyright_records"
    
    id = Column(String(50), primary_key=True)
    job_id = Column(String(50), ForeignKey("production_jobs.id"), nullable=False)
    script_originality_verified = Column(Boolean, default=True)
    image_license_certified = Column(Boolean, default=True)
    music_license_certified = Column(Boolean, default=True)
    sfx_license_certified = Column(Boolean, default=True)
    policy_monetization_approved = Column(Boolean, default=True)
    audit_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class VideoMetadata(Base):
    __tablename__ = "video_metadata"
    
    id = Column(String(50), primary_key=True)
    job_id = Column(String(50), ForeignKey("production_jobs.id"), nullable=False)
    title_hindi = Column(String(200), nullable=False)
    description_hindi = Column(Text, nullable=False)
    tags = Column(JSON, default=list)
    category_id = Column(String(10), default="27") # Education / Film & Animation
    made_for_kids = Column(Boolean, default=False)
    has_altered_or_synthetic_content = Column(Boolean, default=True)
    chapter_timestamps = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

class UploadRecord(Base):
    __tablename__ = "upload_records"
    
    id = Column(String(50), primary_key=True)
    job_id = Column(String(50), ForeignKey("production_jobs.id"), nullable=False)
    youtube_video_id = Column(String(100), nullable=True)
    youtube_url = Column(String(300), nullable=True)
    file_sha256 = Column(String(64), nullable=False)
    upload_status = Column(String(50), default="PENDING") # PENDING, UPLOADED, SCHEDULED, PUBLISHED, FAILED
    scheduled_publish_at_ist = Column(DateTime, nullable=True)
    privacy_status = Column(String(20), default="private")
    resumable_upload_uri = Column(String(500), nullable=True)
    error_log = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, nullable=True)

class PublishingSchedule(Base):
    __tablename__ = "publishing_schedules"
    
    id = Column(String(50), primary_key=True)
    slot_name = Column(String(50), nullable=False) # SHORTS_MON, SHORTS_TUE, LONG_SUN, etc.
    day_of_week = Column(String(20), nullable=False)
    scheduled_time_ist = Column(String(10), nullable=False) # e.g. "12:30" or "19:00"
    current_job_id = Column(String(50), ForeignKey("production_jobs.id"), nullable=True)
    status = Column(String(20), default="SCHEDULED")
    updated_at = Column(DateTime, default=datetime.utcnow)

class YouTubeAnalytic(Base):
    __tablename__ = "youtube_analytics"
    
    id = Column(String(50), primary_key=True)
    video_id = Column(String(100), nullable=False)
    format_type = Column(String(20), nullable=False)
    views = Column(Integer, default=0)
    watch_time_hours = Column(Float, default=0.0)
    subscribers_gained = Column(Integer, default=0)
    click_through_rate_pct = Column(Float, default=0.0)
    average_view_duration_seconds = Column(Float, default=0.0)
    average_percentage_viewed = Column(Float, default=0.0)
    drop_off_points_sec = Column(JSON, default=list)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class ApiUsage(Base):
    __tablename__ = "api_usage"
    
    id = Column(String(50), primary_key=True)
    job_id = Column(String(50), nullable=True)
    provider = Column(String(50), nullable=False)
    service_type = Column(String(50), nullable=False) # LLM_TOKENS, IMAGE_GEN, VIDEO_GEN, TTS_CHARS, RENDER_CPU
    units = Column(Float, default=0.0)
    estimated_cost_usd = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String(20), default="INFO") # INFO, WARNING, ERROR, CRITICAL
    module = Column(String(50), nullable=False)
    event = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    context_data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
