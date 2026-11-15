import pytest
from backend.app.modules.character.registry import CharacterRegistry, CharacterPromptBuilder

def test_character_bible_loaded():
    reg = CharacterRegistry()
    assert len(reg.characters) >= 6
    assert "char_shiva" in reg.characters
    assert "char_rama" in reg.characters
    assert "char_hanuman" in reg.characters
    assert "char_krishna" in reg.characters

def test_character_matching_for_topic():
    reg = CharacterRegistry()
    matched = reg.find_characters_for_topic("भगवान शिव का नीलकंठ अवतार")
    assert len(matched) > 0
    assert matched[0]["id"] == "char_shiva"

def test_character_prompt_builder():
    reg = CharacterRegistry()
    shiva = reg.get_character_by_id("char_shiva")
    prompt = CharacterPromptBuilder.build_consistent_prompt(
        shiva,
        scene_action="meditating upon Kailash",
        camera_angle="Low-angle wide shot"
    )
    assert "Lord Shiva" in prompt or "भगवान शिव" in prompt
    assert "Visual DNA:" in prompt
    assert "Face:" in prompt
    assert "Skin:" in prompt
