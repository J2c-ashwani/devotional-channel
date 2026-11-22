"""
Episodic Ledger for Itihasa Saga.
Tracks the chronological narrative progression of:
1. The Ramayana Arc (Morning 7:00 AM IST)
2. The Mahabharata Arc (Evening 6:30 PM IST)
Ensures 100% automated, uninterrupted episodic continuity.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parents[4]
STORAGE_DIR = BASE_DIR / "storage"
PROGRESS_FILE = STORAGE_DIR / "episodic_progress.json"

RAMAYANA_SERIES: List[Dict[str, Any]] = [
    {
        "id": "ramayana_ep01",
        "episode_num": 1,
        "track": "RAMAYANA",
        "title_hindi": "श्री राम का धनुर्भंग: जब मिथिला में शिव का पिनाक धनुष टूटा",
        "title_english": "Dhanurbhanga: Lord Rama Lifts the Pinaka Bow of Shiva in Mithila",
        "epic_source": "Valmiki Ramayana (Bala Kanda Sarga 66-67)",
        "completed": True  # Episode 1 is already published!
    },
    {
        "id": "ramayana_ep02",
        "episode_num": 2,
        "track": "RAMAYANA",
        "title_hindi": "भगवान परशुराम का मिथिला में आगमन: पिनाक टूटने पर भीषण क्रोध और लक्ष्मण संवाद",
        "title_english": "The Wrath of Bhagwan Parashurama: The Earth-Shaking Confrontation at Mithila",
        "epic_source": "Valmiki Ramayana (Bala Kanda Sarga 74-76)",
        "completed": False
    },
    {
        "id": "ramayana_ep03",
        "episode_num": 3,
        "track": "RAMAYANA",
        "title_hindi": "श्री राम और माता सीता का दिव्य विवाह: जनकपुरी में आनंदोत्सव और अयोध्या आगमन",
        "title_english": "The Celestial Wedding of Shri Rama and Mata Sita in Mithila",
        "epic_source": "Valmiki Ramayana (Bala Kanda Sarga 77)",
        "completed": False
    },
    {
        "id": "ramayana_ep04",
        "episode_num": 4,
        "track": "RAMAYANA",
        "title_hindi": "मंथरा का कुचक्र और कैकेयी का कोपभवन: अयोध्या के राज्याभिषेक में विनाशकारी षड्यंत्र",
        "title_english": "Manthara's Poison and Kaikeyi's Two Fatal Boons",
        "epic_source": "Valmiki Ramayana (Ayodhya Kanda Sarga 7-12)",
        "completed": False
    },
    {
        "id": "ramayana_ep05",
        "episode_num": 5,
        "track": "RAMAYANA",
        "title_hindi": "श्री राम का वन गमन: सरयू तट पर अयोध्यावासियों का विलाप और निषादराज मिलन",
        "title_english": "Lord Rama Departs for the Forest: The Sorrow of Ayodhya and Meeting Guha",
        "epic_source": "Valmiki Ramayana (Ayodhya Kanda Sarga 45-52)",
        "completed": False
    },
    {
        "id": "ramayana_ep06",
        "episode_num": 6,
        "track": "RAMAYANA",
        "title_hindi": "केवट की अनूठी भक्ति: जब भक्त ने भगवान के चरण धोकर गंगा पार कराया",
        "title_english": "The Devotion of Kevat: Washing the Lotus Feet of the Lord",
        "epic_source": "Ramcharitmanas (Ayodhya Kanda) & Valmiki Ramayana",
        "completed": False
    },
    {
        "id": "ramayana_ep07",
        "episode_num": 7,
        "track": "RAMAYANA",
        "title_hindi": "पंचवटी में शूर्पणखा का मानमर्दन: जब लक्ष्मण ने काटी रावण की बहन की नाक",
        "title_english": "Surpanakha in Panchavati: Lakshmana Cuts the Demoness's Nose",
        "epic_source": "Valmiki Ramayana (Aranya Kanda Sarga 17-19)",
        "completed": False
    },
    {
        "id": "ramayana_ep08",
        "episode_num": 8,
        "track": "RAMAYANA",
        "title_hindi": "मारीच का स्वर्ण मृग कपट और सीता हरण: रावण का छल और लक्ष्मण रेखा का उल्लंघन",
        "title_english": "The Golden Deer Deception and the Abduction of Mata Sita",
        "epic_source": "Valmiki Ramayana (Aranya Kanda Sarga 42-49)",
        "completed": False
    },
    {
        "id": "ramayana_ep09",
        "episode_num": 9,
        "track": "RAMAYANA",
        "title_hindi": "महापराक्रमी जटायु का अंतिम युद्ध: अधर्म के विरुद्ध आकाश में पक्षीराज का बलिदान",
        "title_english": "The Valor of Jatayu: The King of Vultures Fights Ravana in the Sky",
        "epic_source": "Valmiki Ramayana (Aranya Kanda Sarga 50-51)",
        "completed": False
    },
    {
        "id": "ramayana_ep10",
        "episode_num": 10,
        "track": "RAMAYANA",
        "title_hindi": "माता शबरी के जूठे बेर: जब मर्यादा पुरुषोत्तम ने भक्ति को कुल और जाति से ऊपर रखा",
        "title_english": "Mata Shabari's Berries: Devotion Beyond Caste and Status",
        "epic_source": "Valmiki Ramayana (Aranya Kanda Sarga 74)",
        "completed": False
    }
]

MAHABHARATA_SERIES: List[Dict[str, Any]] = [
    {
        "id": "mahabharata_ep01",
        "episode_num": 1,
        "track": "MAHABHARATA",
        "title_hindi": "माँ गंगा का त्याग और देवव्रत का जन्म: जब राजा शांतनु ने तोड़ा अपना वचन",
        "title_english": "The Sacrifice of Goddess Ganga and the Birth of Devavrata (Bhishma)",
        "epic_source": "Mahabharata (Adi Parva - Sambhava Parva Adhyaya 96-98)",
        "completed": False
    },
    {
        "id": "mahabharata_ep02",
        "episode_num": 2,
        "track": "MAHABHARATA",
        "title_hindi": "देवव्रत की 'भीष्म प्रतिज्ञा': पिता के सुख के लिए आजीवन ब्रह्मचर्य और राज्य का त्याग",
        "title_english": "The Terrible Vow of Bhishma: Renouncing the Throne for Father's Happiness",
        "epic_source": "Mahabharata (Adi Parva Adhyaya 100)",
        "completed": False
    },
    {
        "id": "mahabharata_ep03",
        "episode_num": 3,
        "track": "MAHABHARATA",
        "title_hindi": "एकलव्य की गुरु-दक्षिणा: जब निष्ठावान शिष्य ने मुस्कुराते हुए काट दिया अपना अंगूठा",
        "title_english": "The Guru-Dakshina of Eklavya: Severing the Right Thumb for Dronacharya",
        "epic_source": "Mahabharata (Adi Parva - Sambhava Parva Adhyaya 132)",
        "completed": False
    },
    {
        "id": "mahabharata_ep04",
        "episode_num": 4,
        "track": "MAHABHARATA",
        "title_hindi": "रंगभूमि में महारथी कर्ण का प्राकट्य: अर्जुन को चुनौती और दुर्योधन द्वारा अंगराज का तिलक",
        "title_english": "The Emergence of Karna: Challenging Arjuna in the Hastinapur Arena",
        "epic_source": "Mahabharata (Adi Parva Adhyaya 135-138)",
        "completed": False
    },
    {
        "id": "mahabharata_ep05",
        "episode_num": 5,
        "track": "MAHABHARATA",
        "title_hindi": "लाक्षागृह का षड्यंत्र: जब जलते महल से सुरंग बनाकर जीवित निकले पांडव",
        "title_english": "The House of Lac (Lakshagriha): The Pandavas' Secret Escape from Fire",
        "epic_source": "Mahabharata (Adi Parva - Jatugriha Parva Adhyaya 141-150)",
        "completed": False
    },
    {
        "id": "mahabharata_ep06",
        "episode_num": 6,
        "track": "MAHABHARATA",
        "title_hindi": "द्रौपदी स्वयंवर: अर्जुन का अद्वितीय मत्स्य-वेध और महारथी कर्ण की विवशता",
        "title_english": "Draupadi's Swayamvara: Arjuna Pierces the Eye of the Rotating Fish",
        "epic_source": "Mahabharata (Adi Parva - Vaivahika Parva Adhyaya 176-189)",
        "completed": False
    },
    {
        "id": "mahabharata_ep07",
        "episode_num": 7,
        "track": "MAHABHARATA",
        "title_hindi": "राजसूय यज्ञ और शिशुपाल के 100 अपराध: भगवान श्री कृष्ण का सुदर्शन चक्र प्रहार",
        "title_english": "Shishupala's 100 Sins: Lord Krishna Unleashes the Sudarshana Chakra",
        "epic_source": "Mahabharata (Sabha Parva - Shishupala-vadha Parva Adhyaya 36-45)",
        "completed": False
    },
    {
        "id": "mahabharata_ep08",
        "episode_num": 8,
        "track": "MAHABHARATA",
        "title_hindi": "शकुनि का कपटी द्यूत क्रीड़ा: जब धर्मराज युधिष्ठिर ने दांव पर लगा दिया सब कुछ",
        "title_english": "The Dice Game of Shakuni: The Ruin of the Pandavas in the Royal Court",
        "epic_source": "Mahabharata (Sabha Parva - Dyuta Parva Adhyaya 58-65)",
        "completed": False
    },
    {
        "id": "mahabharata_ep09",
        "episode_num": 9,
        "track": "MAHABHARATA",
        "title_hindi": "कुरुसभा में द्रौपदी चीरहरण: जब मौन रहे भीष्म-द्रोण और भगवान कृष्ण ने बढ़ाया चीर",
        "title_english": "The Disrobing of Draupadi: Divine Protection from Lord Krishna",
        "epic_source": "Mahabharata (Sabha Parva - Dyuta Parva Adhyaya 67-69)",
        "completed": False
    },
    {
        "id": "mahabharata_ep10",
        "episode_num": 10,
        "track": "MAHABHARATA",
        "title_hindi": "कुरुक्षेत्र में गीता ज्ञान: जब विषादग्रस्त अर्जुन को भगवान कृष्ण ने दिखाया विश्वरूप",
        "title_english": "The Cosmic Vision of the Gita: Lord Krishna Reveals the Vishwaroopa to Arjuna",
        "epic_source": "Mahabharata (Bhishma Parva - Bhagavad Gita Adhyaya 11)",
        "completed": False
    }
]

class EpisodicLedger:
    @staticmethod
    def _load_progress() -> Dict[str, Any]:
        if PROGRESS_FILE.exists():
            try:
                with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"completed_ids": ["ramayana_ep01"]}

    @staticmethod
    def _save_progress(data: Dict[str, Any]):
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def get_next_topic(cls, track: str = "RAMAYANA") -> Dict[str, Any]:
        progress = cls._load_progress()
        completed = set(progress.get("completed_ids", []))

        series = RAMAYANA_SERIES if track.upper() == "RAMAYANA" else MAHABHARATA_SERIES
        for ep in series:
            if ep["id"] not in completed:
                return {
                    "id": ep["id"],
                    "title_hindi": ep["title_hindi"],
                    "title_english": ep["title_english"],
                    "epic_source": ep["epic_source"],
                    "format_type": "SHORT",
                    "track": ep["track"],
                    "episode_num": ep["episode_num"]
                }
        # Fallback if series completes
        first = series[0]
        return {
            "id": f"{first['id']}_loop",
            "title_hindi": first["title_hindi"],
            "title_english": first["title_english"],
            "epic_source": first["epic_source"],
            "format_type": "SHORT",
            "track": first["track"],
            "episode_num": 1
        }

    @classmethod
    def mark_completed(cls, topic_id: str):
        progress = cls._load_progress()
        completed = progress.get("completed_ids", [])
        if topic_id not in completed:
            completed.append(topic_id)
            progress["completed_ids"] = completed
            cls._save_progress(progress)
            print(f"📖 Episodic Ledger: Marked {topic_id} as completed!")
