# 💊 DawaaiDost (दवाई दोस्त)
> *A 4B Open-Weight Guardian that turns confusing doctor shorthand and Hindi voice notes into crystal-clear medicine schedules so your elders never take the wrong pill.*

Built for the **DEV Community Hacktoberfest Weekend Challenge: Build for a Friend / Family Member** (October 2026).

---

## 🌟 The Inspiration / Problem Statement
Every week, my 74-year-old grandmother holds up a prescription slip or a medicine blister pack and asks me:
> *"Beta, yeh Dolo khane ke baad leni thi ya khali pet? Aur yeh BP wali subah ki hai ya raat ki?"*

Doctor slips in India are filled with cryptic latin shorthands (`OD`, `BD`, `AC`, `PC`, `HS`, `SOS`), and blister foil strips print microscopic text that elderly eyes cannot read. 

Generic commercial healthcare apps sell user health data to ad networks, demand invasive permissions, and fail completely on conversational Hinglish notes like:
> *"Sharma ji ke clinic se bola tha Dadi ko gas ki goli nashte se pehle chai se 30 min pehle deni hai"*

**DawaaiDost** is a private, family-centric medication companion designed to run entirely locally or via lightweight open-weight adapters.

---

## 🏗️ Architecture & Partner Integration

```
Prescription / Voice Note / Blister OCR
                   │
                   ▼
┌──────────────────────────────────────────────┐
│        Qwen3.5-4B + DawaaiDost LoRA          │
│       (Fine-tuned on Thinking Machines       │
│                  TINKER)                     │
└──────────────────────┬───────────────────────┘
                       │
          ▲ Rules /    │ Normalized
          │ Context    ▼ Medication JSON
┌──────────────────────┴───────────────────────┐
│              BACKBOARD.IO                    │
│   (Persistent Family Memory & Corrections)   │
│   - "Dadi allergic to Sulfa"                 │
│   - "Pantocid is taken before morning tea"   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 ELEVENLABS                   │
│   (Empathetic Multilingual Voice Output)     │
│   "Dadi, yeh Pantocid DSR hai. Subah nashte  │
│   se pehle khali pet leni hai..."            │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│             RENDER DEPLOYMENT                │
│    (FastAPI + Responsive Glassmorphism UI)   │
└──────────────────────────────────────────────┘
```

### 1. Thinking Machines (Tinker)
- Fine-tuned `Qwen/Qwen3.5-4B` using Tinker's Python SDK (`create_lora_training_client`, `forward_backward`, `optim_step`).
- Trained on 200+ programmatically synthesized Indian prescription formats with deterministic labels.
- Exports a 146 MB LoRA adapter that can be sampled via Tinker's API or run locally with Ollama.

### 2. Backboard.io (Memory Layer)
- Solves the hallucination and consistency problem by maintaining persistent patient profiles and rules.
- When the user corrects a frequency or instructs *"Dadi takes this 30 mins before morning chai"*, Backboard stores it and ensures subsequent parsings obey this rule.
- Responds to natural Hinglish queries like *"Dadi ki subah ki dawaiyan kya hain?"*.

### 3. ElevenLabs (Voice Companion)
- Synthesizes soothing, natural spoken Hindi/English instructions.
- Eliminates screen strain for elderly family members by narrating instructions upon request.
- Falls back to browser Web Speech API if offline.

### 4. Render
- Complete Infrastructure-as-Code with `render.yaml`.
- Fast, zero-friction cloud deployment.

---

## 🚀 Quickstart Guide

### 1. Clone & Install
```bash
git clone https://github.com/nashdev97/dawaaidost.git
cd dawaaidost
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(If no API keys are provided, DawaaiDost automatically runs in graceful offline mode with local heuristics and Web Speech audio!)*

### 3. Run Test Suite
```bash
python test_samples.py
```

### 4. Start the Application
```bash
python app.py
```
Open your browser at `http://localhost:8000`.

---

## 🧪 Validated Test Cases

| Input Shorthand / Note | Tinker Extracted Medicine | Frequency | Backboard Rule Influence |
|:---|:---|:---|:---|
| `Rx: Pantocid DSR 1 tab AC x 10 days for Dadi` | Pantocid DSR | Before meal | Obeyed "take 30 min before morning chai" |
| `Rx: Telma 40 1 tab OD PC for Papa` | Telma 40 | Once a day | Mapped to Morning BP routine |
| `Mummy ko Augmentin 625 BD dena hai 5 days` | Augmentin 625 Duo | Twice a day | Penicillin allergy warning triggered |
| `Dolo 650 SOS fever ke liye Dadu ko` | Dolo 650 | As needed (SOS) | Logged to patient medication history |

---

## 📜 License
MIT License - Open Source for Hacktoberfest 2026.
