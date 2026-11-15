import pytest
from datetime import datetime
from backend.app.modules.seo.metadata_gen import MetadataGenerator
from backend.app.modules.youtube.uploader import YouTubeUploader

def test_metadata_and_synthetic_media_disclosure():
    topic = {"title_hindi": "भगवान शिव का नीलकंठ अवतार"}
    script = {"narrative_body_hindi": "समुद्र मंथन की दिव्य कथा"}
    source = {"epic_name": "Shiva Purana", "source_edition": "Geeta Press"}
    
    meta = MetadataGenerator.generate_metadata(topic, script, source, format_type="SHORT")
    assert meta["has_altered_or_synthetic_content"] is True
    assert meta["made_for_kids"] is False
    assert "YouTube Altered & Synthetic Media Disclosure" in meta["description_hindi"]
    assert "Shiva Purana" in meta["description_hindi"]

def test_timezone_conversion_ist_to_utc():
    uploader = YouTubeUploader()
    # 19:00 IST is 13:30 UTC
    dt = datetime(2026, 11, 20)
    utc_str = uploader.convert_ist_to_utc_rfc3339("19:00", dt)
    assert utc_str.endswith("Z")
    assert "13:30:00Z" in utc_str
