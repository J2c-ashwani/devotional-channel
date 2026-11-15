# पौराणिक गाथा (Pauranik Gatha) - Autonomous AI-Powered YouTube Channel Studio

An enterprise-grade, fully autonomous content creation, video rendering, quality validation, and YouTube publishing platform built specifically for **Cinematic Hindi Indian Mythology and Epic Storytelling**.

---

## 🚩 Channel Identity & Niche
- **Core Subject Matter:** Valmiki Ramayana, Vyasa Mahabharata, Shiva Purana, Bhagavata Purana, Vishnu Purana, and lesser-known historical and moral dilemmas within traditional Indian lore.
- **Audience:** Hindi-speaking audiences across India and global diaspora (16–45 years).
- **Language & Script:** Natural, conversational Hindi in Devanagari script (`hi-IN-MadhurNeural`). Correct Sanskrit phonetic pronunciation.
- **Anti-Pattern Guard:** Strictly prohibits generic motivational quotes, devotional bhajans, clickbait fabrications, and sensationalist religious controversies.

---

## 🏛️ System Architecture & Modules

```
                    ┌────────────────────────────┐
                    │  1. Autonomous Scheduler   │
                    │  (GitHub Actions / Cron)   │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Module A: Content Research & 100-Point Topic Scorer   │
      └───────────────────────────┬────────────────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Module B: Mythology Fact-Checker & Source Grounding   │
      │  (Valmiki Ramayana, Mahabharata, Puranas - 2 Passes)   │
      └───────────────────────────┬────────────────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Module C: Hindi Screenplay Engine & Originality Guard │
      └───────────────────────────┬────────────────────────────┘
                                  │
               ┌──────────────────┴──────────────────┐
               ▼                                     ▼
┌─────────────────────────────┐       ┌─────────────────────────────┐
│ Module D: Shorts Generator  │       │ Module E: Long-Form Engine  │
│ (9:16 Vertical, 30–60s)     │       │ (16:9 Widescreen, 8–15m)    │
└──────────────┬──────────────┘       └──────────────┬──────────────┘
               └──────────────────┬──────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Module G: Character Consistency Engine (Visual DNA)   │
      └───────────────────────────┬────────────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Module H: Visual│      │ Module I: Hindi │      │ Module J: Music │
│ & Animation Gen │      │ Voiceover (TTS) │      │ & Sound Design  │
└────────┬────────┘      └────────┬────────┘      └────────┬────────┘
         └────────────────────────┼────────────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Module K: Automatic FFmpeg Video Editor & Subtitles   │
      └───────────────────────────┬────────────────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Module L: Mobile-First Thumbnails & SEO Metadata      │
      └───────────────────────────┬────────────────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Module M: YouTube Policy & Monetization Compliance    │
      └───────────────────────────┬────────────────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Module N: 12-Factor Quality Control (Fail-Closed)     │
      │  Score >= 90 required. Hard Blockers Reject to Queue.  │
      └───────────────────────────┬────────────────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Module O: YouTube Resumable Upload & Private publishAt│
      └───────────────────────────┬────────────────────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│ Module P: Analytics & Feedback  │       │ Module Q: Micro-Cost Tracker    │
│ (Retention & CTR Closed Loop)   │       │ & Hard Spend Ceiling ($150/mo)  │
└─────────────────────────────────┘       └─────────────────────────────────┘
```

---

## 📅 Publishing Calendar (IST - Asia/Kolkata)

| Slot | Frequency | Format | Target Time (IST) | Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **Shorts** | Monday through Saturday (6x/week) | Single-event high-impact narrative | **12:30 PM** or **7:00 PM** | 1080 × 1920 (9:16) |
| **Long-Form Story** | Every Sunday (1x/week) | Deep multi-act dramatic arc | **7:00 PM** | 1920 × 1080 (16:9) |
| **Monthly Special** | Final Sunday of the Month | Multi-chapter premium cinematic | **7:00 PM** | 1920 × 1080 (16:9) |

*Videos are uploaded 12–24 hours in advance as `private` with the `publishAt` timestamp set to ensure 1080p/4K processing is finished before release.*

---

## 🔒 YouTube Monetization & Policy Compliance

1. **Reused Content Defense:** Zero copyrighted television, movie, or third-party audio clips. 100% original screenplay, modular visual generation, and procedural/royalty-free Indian classical soundtrack.
2. **Synthetic Media Disclosure:** Automated tagging with `hasAlteredOrSyntheticContent = true` per YouTube guidelines.
3. **Fail-Closed Quality Gate:** 12 automated checks must achieve a minimum composite score of **90/100**. Any unresolved factual discrepancy, copyright concern, or audio flaw halts publication immediately.
4. **Permanent Character Database:** Strict visual DNA preservation for Lord Shiva, Lord Rama, Lord Hanuman, Lord Krishna, Arjuna, Karna, and Ravana.

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.13+
- FFmpeg 8.x with `libass` and `libx264`

### 2. Environment Setup
```bash
git clone https://github.com/your-username/pauranik-gatha-studio.git
cd devotional

# Create virtual environment
python3 -m venv backend/.venv
source backend/.venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
pip install edge-tts greenlet
```

### 3. Initialize Database
```bash
python backend/app/init_db.py
```

### 4. Run Admin Dashboard
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open [http://localhost:8000](http://localhost:8000) to view the Admin Dashboard.

### 5. Run Production via CLI
```bash
# Produce and schedule a daily Short (9:16)
python scripts/run_pipeline.py --format SHORT

# Produce and schedule a Sunday Long-form Story (16:9)
python scripts/run_pipeline.py --format LONG_FORM

# Emergency Kill Switch (Immediately stops all autonomous publishing)
python scripts/run_pipeline.py --kill-switch
```

### 6. Run Test Suite
```bash
pytest backend/tests/ -v
```

---

## 🐳 Docker Deployment
```bash
docker build -t pauranik-gatha-studio .
docker run -p 8000:8000 --env-file .env pauranik-gatha-studio
```
