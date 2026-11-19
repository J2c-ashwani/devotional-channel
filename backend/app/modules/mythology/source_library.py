from typing import Dict, Any, Optional, List

CANONICAL_SCRIPTURAL_SOURCES: Dict[str, Dict[str, Any]] = {
    "ramayana_dhanurbhanga_pilot": {
        "epic_name": "Valmiki Ramayana",
        "kanda_or_parva": "Bala Kanda",
        "sarga_or_adhyaya": "Sarga 66 and Sarga 67 (Dhanurbhanga - The Breaking of the Pinaka Bow)",
        "shloka_range": "Bala Kanda 1.66.1 - 1.67.20",
        "source_edition": "Valmiki Ramayana Critical Edition (Oriental Institute Baroda) & Geeta Press Gorakhpur",
        "original_sanskrit_shloka": "निमेषान्तरमात्रेण तोलयामास वीर्यवान्। आरोपयित्वा धर्मात्मा पूरयामास तद् धनुः॥ तद् बभञ्ज धनुर्मध्ये नरश्रेष्ठो महाद्युतिः। तस्य शब्दो महानासीन्निर्घातसमनिःस्वनः॥ (बालकाण्ड १.६७.१६-१७)",
        "canonical_summary_hindi": "मिथिला नरेश राजा जनक की सभा में महर्षि विश्वामित्र की आज्ञा से श्री राम ने भगवान शिव के उस विशाल पिनाक धनुष को क्षण मात्र में सहजता से उठा लिया, जिसे पांच हजार बलिष्ठ पुरुष आठ पहियों वाले लोहे के संदूक में खींचकर लाए थे। जैसे ही धर्मात्मा श्री राम ने उस पर प्रत्यंचा चढ़ाई, वह धनुष बीच से प्रचंड वज्रपात जैसी गर्जना के साथ टूट गया।",
        "factual_assertions": [
            {
                "assertion_id": "VALMIKI_BK_01",
                "fact": "धनुष भगवान शिव का 'पिनाक' धनुष था, जो दक्ष यज्ञ के बाद राजा जनक के पूर्वज देवरात को सौंपा गया था।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Bala Kanda 1.66.8-9"
            },
            {
                "assertion_id": "VALMIKI_BK_02",
                "fact": "धनुष आठ पहियों वाली लोहे की मंजूषा (लोहा संदूक) में रखा था और पांच हजार वीर उसे खींचकर लाए थे।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Bala Kanda 1.67.4-5"
            },
            {
                "assertion_id": "VALMIKI_BK_03",
                "fact": "श्री राम ने महर्षि विश्वामित्र की प्रत्यक्ष आज्ञा और राजा जनक की उपस्थिति में धनुष उठाया।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Bala Kanda 1.67.12-13"
            },
            {
                "assertion_id": "VALMIKI_BK_04",
                "fact": "श्री राम ने केवल प्रत्यंचा चढ़ाने का प्रयास किया था, और भार व खिंचाव से धनुष मध्य से टूट गया।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Bala Kanda 1.67.16-17"
            },
            {
                "assertion_id": "VALMIKI_BK_05",
                "fact": "धनुष टूटने की ध्वनि से मिथिला की भूमि हिल गई और विश्वामित्र, जनक और राम-लक्ष्मण को छोड़कर सभा के सभी लोग मूर्छित हो गए।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Bala Kanda 1.67.18"
            }
        ],
        "traditional_variations_notes": [
            {
                "variation": "रामचरितमानस (तुलसीदास) में जनक विलाप ('वीर विहीन मही मैं जानी') और लक्ष्मण का क्रोध वर्णित है, जबकि वाल्मीकि रामायण में जनक पहले ही अपनी प्रतिज्ञा विश्वामित्र को बताते हैं और राम सहजता से आज्ञा पाकर आगे बढ़ते हैं।",
                "policy": "वाल्मीकि रामायण के मूल पाठ को ऐतिहासिक आधार मानें, और तुलसीदास के भावात्मक संवाद को रचनात्मक नाटकीय संवर्धन के रूप में स्पष्ट रेखांकित करें।"
            }
        ],
        "public_domain_certified": True
    },
    "shiva_neelkanth": {
        "epic_name": "Shiva Purana (Kailash Samhita) & Bhagavata Purana (Canto 8, Chapter 7)",
        "kanda_or_parva": "Kailash Samhita / Bhagavata Skandha 8",
        "sarga_or_adhyaya": "Adhyaya 7 (Halahala Bhakshana)",
        "shloka_range": "Bhagavata 8.7.20 - 8.7.45",
        "source_edition": "Geeta Press Gorakhpur (Public Domain Canonical Sanskrit/Hindi Recension)",
        "original_sanskrit_shloka": "देवासुरैर्मथ्यमानात् क्षीरोदात् समुदस्थितः। कालकूटो विषस्तीव्रो ददाह स्थाणुजङ्गमम्॥ तं दृष्ट्वा सर्वभूतानि भयभीतानि सर्वतः। शरणं शरणं जग्मुर्महादेवं जगद्गुरुम्॥",
        "canonical_summary_hindi": "समुद्र मंथन के समय जब महाविनाशक कालकूट हलाहल विष प्रकट हुआ, तो उसके दाह से तीनों लोक जलने लगे। समस्त देवता और असुर भयभीत होकर भगवान आशुतोष महादेव की शरण में गए। जगत के कल्याण हेतु भगवान शिव ने उस विष का पान किया और उसे अपने कंठ में धारण किया, जिससे उनका कंठ नीला पड़ गया और वे 'नीलकंठ' कहलाए।",
        "factual_assertions": [
            {
                "assertion_id": "SHIVA_PUR_01",
                "fact": "विष समुद्र मंथन के दौरान प्रकट हुआ था, किसी युद्ध में नहीं।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Bhagavata 8.7.21"
            },
            {
                "assertion_id": "SHIVA_PUR_02",
                "fact": "भगवान शिव ने विष को गले में ही रोक लिया, उदर में नहीं जाने दिया।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Shiva Purana Kailash Samhita 12.14"
            },
            {
                "assertion_id": "SHIVA_PUR_03",
                "fact": "माता पार्वती ने शिवजी के कंठ को स्पर्श किया ताकि विष नीचे न उतरे।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Shiva Purana 12.16"
            }
        ],
        "traditional_variations_notes": [],
        "public_domain_certified": True
    },
    "ghatotkacha_sacrifice": {
        "epic_name": "Mahabharata",
        "kanda_or_parva": "Drona Parva (Ghatotkacha-badha Parva)",
        "sarga_or_adhyaya": "Adhyaya 179-180",
        "shloka_range": "MBh 7.179.1 - 7.180.40",
        "source_edition": "Bhandarkar Oriental Research Institute (BORI) Critical Edition",
        "original_sanskrit_shloka": "एवं स निहतो राजन् राक्षसेन्द्रो महाबलः। कर्णस्य बाणवेगेन पाण्डवानां भयङ्करः॥",
        "canonical_summary_hindi": "कुरुक्षेत्र के 14वें दिन की भीषण रात्रि में घटोत्कच ने अपनी मायावी शक्तियों से कौरव सेना में प्रलय मचा दिया। दुर्योधन की व्याकुलता देखकर कर्ण को अर्जुन के वध के लिए सहेज कर रखी गई अमोघ 'वासव शक्ति' का प्रयोग घटोत्कच पर करना पड़ा। घटोत्कच ने वीरगति प्राप्त की, परंतु अर्जुन का प्राण रक्षित हो गया।",
        "factual_assertions": [
            {
                "assertion_id": "MBH_DP_01",
                "fact": "कर्ण के पास वासव शक्ति बाण केवल एक बार उपयोग के लिए था।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Drona Parva 180.12"
            },
            {
                "assertion_id": "MBH_DP_02",
                "fact": "घटोत्कच की मृत्यु 14वीं रात्रि के युद्ध में हुई थी।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Drona Parva 179.45"
            }
        ],
        "traditional_variations_notes": [],
        "public_domain_certified": True
    },
    "bhishma_shanti_parva": {
        "epic_name": "Mahabharata",
        "kanda_or_parva": "Shanti Parva (Rajadharmanushasana & Mokshadharma Parva)",
        "sarga_or_adhyaya": "Adhyaya 56-167 (Bhishma's Discourse on the Bed of Arrows)",
        "shloka_range": "MBh 12.56.1 - 12.167.50",
        "source_edition": "Bhandarkar Oriental Research Institute (BORI) Critical Edition & Geeta Press Gorakhpur",
        "original_sanskrit_shloka": "यथा हि गर्भिणी हित्वा स्वं प्रियं मनसोऽनुगम्। गर्भस्य हितमाधत्ते तथा राज्ञाप्यसंशयम्॥ (शान्तिपर्व ५६.४५)",
        "canonical_summary_hindi": "कुरुक्षेत्र के अठारह दिवसीय महासंग्राम के उपरांत भगवान श्री कृष्ण धर्मराज युधिष्ठिर को शरशैया पर लेटे पितामह भीष्म के समीप ले गए। पितामह भीष्म ने युधिष्ठिर को राजधर्म, दंडनीति, आपद्धर्म और मोक्षधर्म का गूढ़ उपदेश दिया तथा सूर्य के उत्तरायण होने पर योगबल से प्राण त्यागे।",
        "factual_assertions": [
            {
                "assertion_id": "MBH_SP_01",
                "fact": "भगवान श्री कृष्ण युधिष्ठिर को शरशैया पर लेटे पितामह भीष्म के पास राजधर्म के उपदेश के लिए ले गए।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Shanti Parva 12.46-54"
            },
            {
                "assertion_id": "MBH_SP_02",
                "fact": "पितामह भीष्म ने राजा को गर्भवती माता की भांति अपने सुख से ऊपर प्रजा के कल्याण को रखने का राजधर्म सिखाया।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Shanti Parva 12.56.44-45"
            },
            {
                "assertion_id": "MBH_SP_03",
                "fact": "भीष्म ने कुरुसभा में द्रौपदी के अपमान के समय अपने मौन को स्वीकार किया और उत्तरायण में स्वेच्छा से प्राण त्यागे।",
                "classification": "SCRIPTURAL_CANON",
                "citation": "Anushasana Parva 13.153-154"
            }
        ],
        "traditional_variations_notes": [],
        "public_domain_certified": True
    }
}

class SourceLibrary:
    @staticmethod
    def get_canonical_source(topic_slug: str) -> Optional[Dict[str, Any]]:
        slug = topic_slug.lower()
        if "भीष्म" in slug or "शांति" in slug or "युधिष्ठिर" in slug or "bhishma" in slug:
            return CANONICAL_SCRIPTURAL_SOURCES.get("bhishma_shanti_parva")
        elif "राम" in slug or "जनक" in slug or "धनुष" in slug or "ramayana" in slug or "mithila" in slug:
            return CANONICAL_SCRIPTURAL_SOURCES.get("ramayana_dhanurbhanga_pilot")
        elif "शिव" in slug or "नीलकंठ" in slug:
            return CANONICAL_SCRIPTURAL_SOURCES.get("shiva_neelkanth")
        elif "घटोत्कच" in slug or "कर्ण" in slug:
            return CANONICAL_SCRIPTURAL_SOURCES.get("ghatotkacha_sacrifice")
        
        # Default to Ramayana Pilot
        return CANONICAL_SCRIPTURAL_SOURCES.get("ramayana_dhanurbhanga_pilot")
