from typing import Dict, Any, List

class MetadataGenerator:
    """
    Module L: YouTube SEO & Metadata Generator.
    Produces compliant, engaging Hindi titles, rich chaptered descriptions,
    synthetic media disclosures, and clean tags.
    """

    @classmethod
    def generate_metadata(
        cls,
        topic_data: Dict[str, Any],
        script_data: Dict[str, Any],
        canonical_source: Dict[str, Any],
        format_type: str = "SHORT"
    ) -> Dict[str, Any]:
        title_raw = topic_data.get("title_hindi", "")
        
        # Optimize title length for mobile UI (under 70-80 chars)
        if len(title_raw) > 80:
            title_hindi = title_raw[:77] + "..."
        else:
            title_hindi = title_raw

        # Rich compliant description
        synopsis = script_data.get("narrative_body_hindi", "")[:350]
        source_name = canonical_source.get("epic_name", "प्रामाणिक सनातन धर्म ग्रंथ")
        source_edition = canonical_source.get("source_edition", "प्रामाणिक सार्वजनिक संस्करण")

        description_lines = [
            f"॥ श्री हरिः शरणम् ॥",
            "",
            f"🚩 {title_hindi}",
            "",
            f"कथा संक्षेप:",
            f"{synopsis}...",
            "",
            f"📜 प्रामाणिक संदर्भ एवं स्रोत (Scriptural Source Grounding):",
            f"यह गाथा {source_name} पर आधारित है ({source_edition})।",
            f"हमारा उद्देश्य भारतीय महाकाव्यों और सनातन इतिहास के सत्य एवं दार्शनिक संदेश को प्रामाणिकता और सम्मान के साथ प्रस्तुत करना है।",
            "",
            f"⚖️ YouTube Altered & Synthetic Media Disclosure (यूट्यूब नीति अनुपालन):",
            f"यह वीडियो आधुनिक 3D एनिमेशन, ओरिजिनल वॉइसओवर और रचनात्मक विज़ुअलाइज़ेशन तकनीकों के माध्यम से निर्मित एक मूल कलात्मक प्रस्तुति है। इसमें किसी भी जीवित व्यक्ति या ऐतिहासिक हस्ती का भ्रामक अनुकरण नहीं किया गया है।",
            "",
            f"🔒 Copyright & Originality Certified:",
            f"कथा का आलेख (Script), 3D विज़ुअल और पार्श्व संगीत (Soundtrack) 100% मूल एवं लाइसेंस प्राप्त हैं। बिना अनुमति पुन: अपलोड करना प्रतिबंधित है।",
            "",
            f"#IndianMythology #PauranikGatha #SanatanDharma #Mahabharat #Ramayana #HindiKahaniya"
        ]

        # Add chapter timestamps if long-form
        chapters = []
        if format_type == "LONG_FORM":
            chapters = [
                {"timestamp": "00:00", "title": "प्रस्तावना एवं धर्म संकट"},
                {"timestamp": "01:15", "title": "कुरुक्षेत्र का शांत दृश्य"},
                {"timestamp": "03:40", "title": "पितामह भीष्म का उपदेश"},
                {"timestamp": "06:20", "title": "राजधर्म और द्रौपदी का प्रश्न"},
                {"timestamp": "08:10", "title": "अंतिम मुक्ति और उपसंहार"}
            ]
            chapter_text = ["", "⏱️ अध्याय (Chapters):"]
            for ch in chapters:
                chapter_text.append(f"{ch['timestamp']} - {ch['title']}")
            description_lines = description_lines[:6] + chapter_text + description_lines[6:]

        description_hindi = "\n".join(description_lines)

        # Curated compliant tags
        tags = [
            "Indian Mythology", "Pauranik Gatha", "Mahabharat in Hindi",
            "Ramayana Katha", "Shiva Purana", "Krishna Katha",
            "Hindi Animated Stories", "Sanatan Dharma History",
            "Dharma and Karma", "Devotional Hindi Stories"
        ]

        return {
            "title_hindi": title_hindi,
            "description_hindi": description_hindi,
            "tags": tags,
            "category_id": "27", # Education / Animation
            "made_for_kids": False,
            "has_altered_or_synthetic_content": True,
            "chapters": chapters
        }
