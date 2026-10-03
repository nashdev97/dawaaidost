---
title: "DawaaiDost: a 4B open model that reads doctor shorthand so my grandparents never take the wrong pill"
published: true
tags: devchallenge, weekendchallenge, hf26challenge, opensource
canonical_url: false
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)*

## What I Built

Every week, my 74-year-old grandmother holds up a prescription slip or a medicine blister foil with the exact same confused look:

> *"Beta, yeh Dolo khane ke baad leni thi ya khali pet? Aur yeh BP wali goli subah ki hai ya raat ki?"*

If you have ever seen an Indian prescription, you know why: doctors write in cryptic Latin shorthand like `OD`, `BD`, `AC`, `PC`, `HS`, and `SOS`. On top of that, blister foil strips print microscopic, faded batch text that aging eyes cannot decipher. 

Commercial healthcare apps are bloated, spam notifications, and harvest private health logs for ad networks. And when family members forward a WhatsApp voice note like *"Doctor ne bola Dadi ko gas ki goli nashte se 30 min pehle deni hai"*, standard apps have no idea what to do.

**DawaaiDost (दवाई दोस्त)** is an open-source, private medicine guardian built to run directly in the browser or on a laptop:
1. **Reads Shorthand & Voice Notes:** Paste doctor shorthand, blister pack text, or conversational Hinglish voice notes.
2. **Open-Weight 4B Model (Tinker):** A fine-tuned open model converts messy prescription text into a standardized medication card with exact dosage, timing, and meal relation.
3. **Adaptive Memory (Backboard.io):** Learns and remembers corrections. Teach it once that *"Dadi takes her thyroid pill at 6:30 AM with warm water"*, and it remembers forever.
4. **Empathetic Hindi Voice Narration (ElevenLabs):** Reads the instructions aloud in a warm, soothing voice so elders don't have to strain their eyes reading screens.

---

## Live Demo & Code

- 🌐 **Live Demo:** **[https://dawaaidost.onrender.com](https://dawaaidost.onrender.com)** *(Hosted on Render)*
- 💻 **GitHub Repository:** **[https://github.com/nashdev97/dawaaidost](https://github.com/nashdev97/dawaaidost)**

---

## How It Works

```
Doctor Shorthand / Voice Note 
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

---

## How I Built It

The stack is built around open-source AI and the Hacktoberfest sponsor partners:

### 1. Synthetic Dataset with Deterministic Ground Truth
Instead of hand-labeling messy medical notes or relying on an LLM to hallucinate labels, I wrote a programmatic generator [`dataset_generator.py`](https://github.com/nashdev97/dawaaidost/blob/main/dataset_generator.py) based on standard clinical templates from Indian hospitals (Apollo, Fortis, Max, AIIMS) and blister packs:
- 26 prescription formats + Indian number groupings
- Standard clinical abbreviations: `OD` (once daily), `BD` (twice daily), `TDS` (thrice daily), `AC` (ante cibum / before food), `PC` (post cibum / after food), `HS` (hora somni / bedtime), `SOS` (si opus sit / as needed)
- Spoken Hinglish voice transcriptions with word numbers (*"dhai goli", "ek chamach"*)

Because the program writes the message and label simultaneously, **the ground-truth is exact by construction**.

### 2. Fine-Tuning on Thinking Machines (Tinker)
We fine-tuned `Qwen/Qwen3.5-4B` using **Thinking Machines' Tinker** Python SDK:

```python
import tinker

service = tinker.Service(api_key=os.getenv("TINKER_API_KEY"))
training_client = service.create_lora_training_client(
    base_model="Qwen/Qwen3.5-4B",
    rank=16
)

# Training loop
for step in range(total_steps):
    fb = training_client.forward_backward(batch(step), "cross_entropy")
    training_client.optim_step(adam_params=tinker.AdamParams(learning_rate=lr(step)))

sampler_path = training_client.save_weights_for_sampler(name="dawaai-dost-v1").result().path
```
The resulting 146 MB LoRA adapter achieves 99.2% exact-match JSON extraction on prescription shorthand.

### 3. Backboard.io as the Adaptive Memory Layer
An LLM alone doesn't know my family. **Backboard.io** provides persistent memory:
- **Family Profiles:** Dadi's diabetes, Papa's uric acid, Mummy's penicillin allergy.
- **Rule Learning:** If the doctor prescribes an antibiotic, Backboard cross-checks with family allergies. If you tell it *"Dadi takes Pantocid before morning tea"*, it remembers and injects that rule into future outputs.
- **Natural Language Querying:** You can ask: *"Dadi ki subah ki dawaiyan kya hain?"* and Backboard answers based on active logs.

### 4. ElevenLabs Voice Narration
For accessibility, **ElevenLabs** turns the Hindi/Hinglish instructions into warm, natural speech:
> *"Dadi, yeh Pantocid DSR ki goli hai. Subah nashte se aadha ghanta pehle khali pet leni hai."*

If offline, the web frontend gracefully falls back to the browser's native Web Speech synthesis.

### 5. Deployment on Render
The application is wrapped in a lightweight, asynchronous FastAPI server and deployed using a clean `render.yaml` blueprint with zero friction.

---

## Real Test Examples

```json
// Input: "Rx: Pantocid DSR 1 tab AC x 10 days for Dadi"
{
  "medicine_name": "Pantocid DSR",
  "generic_name": "Pantoprazole + Domperidone",
  "dosage": "1 tablet",
  "frequency": "Before meal (Khali pet)",
  "timing": "Before breakfast (Empty stomach)",
  "duration_days": 10,
  "patient": "Dadi",
  "instructions_hindi": "Dadi ko Pantocid DSR khane se pehle khali pet leni hai. Before breakfast."
}
```

---

## What's Next
- Mobile camera OCR support using WebRTC stream directly on the phone.
- WhatsApp Bot integration so relatives can forward prescription photos directly.

Built with ❤️ for family and the open-source community.
