"""
DawaaiDost - Main Application Backend (FastAPI)
Binds together Thinking Machines (Tinker), Backboard.io, ElevenLabs, and Render.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
import os
import json

from train_tinker import TinkerMedicineModel
from memory_backboard import BackboardMemory
from voice_elevenlabs import ElevenLabsVoiceNarrator

app = FastAPI(title="DawaaiDost · Ghar Ka Prescription Guardian")

# Initialize partner clients
tinker_model = TinkerMedicineModel()
backboard = BackboardMemory()
elevenlabs = ElevenLabsVoiceNarrator()

class ParseRequest(BaseModel):
    text: str
    patient: str = "Dadi"

class CorrectionRequest(BaseModel):
    rule: str

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    # Embedded high-performance, responsive UI
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DawaaiDost · Medicine & Prescription Guardian</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .glass-card {
      background: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(226, 232, 240, 0.8);
    }
  </style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen">
  <!-- Top Navigation -->
  <header class="border-b border-slate-200 bg-white/80 sticky top-0 z-50 backdrop-blur-md">
    <div class="max-w-6xl mx-auto px-4 py-3.5 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white font-bold text-xl shadow-md shadow-emerald-500/20">
          💊
        </div>
        <div>
          <h1 class="text-xl font-extrabold tracking-tight">DawaaiDost</h1>
          <p class="text-xs text-slate-500 font-medium">Built for my Grandparents · Hacktoberfest 2026</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          Tinker + Backboard + ElevenLabs
        </span>
      </div>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-4 py-8">
    <!-- Intro Hero Card -->
    <div class="mb-8 p-6 rounded-2xl bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 text-white shadow-xl relative overflow-hidden">
      <div class="max-w-2xl relative z-10">
        <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Build for a Friend & Family</span>
        <h2 class="text-2xl sm:text-3xl font-bold mt-2 mb-2">No more confusing doctor handwriting or tiny blister fonts.</h2>
        <p class="text-slate-300 text-sm leading-relaxed">
          Paste doctor shorthand, prescription photos, or speak Hinglish notes. Fine-tuned with <strong>Tinker</strong>, remembered by <strong>Backboard.io</strong>, spoken aloud with <strong>ElevenLabs</strong>.
        </p>
      </div>
    </div>

    <!-- Quick Presets -->
    <div class="mb-6 flex flex-wrap gap-2 items-center">
      <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Try Examples:</span>
      <button onclick="setSample(1)" class="text-xs font-medium bg-white hover:bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-lg transition shadow-sm">
        👵 Dadi's Rx: Pantocid DSR 1 tab AC
      </button>
      <button onclick="setSample(2)" class="text-xs font-medium bg-white hover:bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-lg transition shadow-sm">
        👴 Dadu's Glycomet GP 1 OD x 30 days
      </button>
      <button onclick="setSample(3)" class="text-xs font-medium bg-white hover:bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-lg transition shadow-sm">
        🗣️ Hinglish: "Mummy ko Augmentin 625 din me 2 baar dena hai"
      </button>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <!-- Input Column -->
      <div class="lg:col-span-6 space-y-6">
        <div class="glass-card p-6 rounded-2xl shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <label class="font-bold text-sm text-slate-800">Prescription / SMS / Voice Note</label>
            <select id="patientSelect" class="text-xs font-semibold bg-slate-100 border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700">
              <option value="Dadi">Patient: Dadi (74y)</option>
              <option value="Dadu">Patient: Dadu (78y)</option>
              <option value="Mummy">Patient: Mummy (48y)</option>
              <option value="Papa">Patient: Papa (52y)</option>
            </select>
          </div>
          <textarea id="inputText" rows="4" placeholder="Paste prescription text, blister pack OCR, or spoken Hindi notes here..." class="w-full p-3.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"></textarea>
          
          <div class="mt-4 flex items-center justify-between">
            <button onclick="parsePrescription()" class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm shadow-md shadow-emerald-600/20 transition flex items-center gap-2">
              <span>Decode & Read Aloud</span> 🎙️
            </button>
            <span id="loadingSpinner" class="hidden text-xs text-slate-500 font-medium">Processing through Tinker...</span>
          </div>
        </div>

        <!-- Backboard Memory Query & Rule Addition -->
        <div class="glass-card p-6 rounded-2xl shadow-sm">
          <h3 class="font-bold text-sm text-slate-800 flex items-center gap-2 mb-3">
            <span>🧠 Backboard.io Memory Assistant</span>
            <span class="text-xs font-normal text-slate-400">(Learns & remembers corrections)</span>
          </h3>
          
          <div class="space-y-3">
            <div class="flex gap-2">
              <input id="queryText" type="text" placeholder="Ask memory (e.g. Dadi ki subah ki dawaiyan kya hain?)" class="flex-1 p-2.5 text-sm rounded-lg border border-slate-200">
              <button onclick="askMemory()" class="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white font-medium text-xs rounded-lg transition">Ask</button>
            </div>
            <div id="memoryAnswer" class="hidden p-3 rounded-lg bg-emerald-50 text-emerald-800 text-xs border border-emerald-200 font-medium"></div>

            <div class="pt-2 border-t border-slate-100 flex gap-2">
              <input id="ruleText" type="text" placeholder="Teach memory (e.g. Pantocid DSR timing: 30 mins before morning chai)" class="flex-1 p-2 text-xs rounded-lg border border-slate-200">
              <button onclick="teachMemory()" class="px-3 py-1.5 bg-teal-600 hover:bg-teal-700 text-white font-medium text-xs rounded-lg transition">Teach</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Output Column -->
      <div class="lg:col-span-6 space-y-6">
        <div id="resultCard" class="glass-card p-6 rounded-2xl shadow-sm border border-slate-200">
          <div class="flex items-center justify-between pb-4 border-b border-slate-100">
            <div>
              <span class="text-xs font-bold text-emerald-600 uppercase tracking-wider">Normalized Medicine Card</span>
              <h3 id="resMedicine" class="text-xl font-extrabold text-slate-900">Waiting for input...</h3>
              <p id="resGeneric" class="text-xs text-slate-500 font-medium"></p>
            </div>
            <button id="audioPlayBtn" onclick="speakText()" class="hidden px-3 py-2 rounded-xl bg-emerald-100 text-emerald-800 font-semibold text-xs hover:bg-emerald-200 transition flex items-center gap-1.5">
              <span>🔊 Listen</span>
            </button>
          </div>

          <div class="grid grid-cols-2 gap-4 my-4">
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
              <span class="text-xs text-slate-400 font-semibold">Dosage & Frequency</span>
              <p id="resDosage" class="text-sm font-bold text-slate-800 mt-0.5">-</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
              <span class="text-xs text-slate-400 font-semibold">Exact Timing</span>
              <p id="resTiming" class="text-sm font-bold text-slate-800 mt-0.5">-</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
              <span class="text-xs text-slate-400 font-semibold">Purpose</span>
              <p id="resPurpose" class="text-sm font-bold text-slate-800 mt-0.5">-</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-100">
              <span class="text-xs text-slate-400 font-semibold">Patient Assigned</span>
              <p id="resPatient" class="text-sm font-bold text-slate-800 mt-0.5">-</p>
            </div>
          </div>

          <div class="p-4 rounded-xl bg-emerald-50/60 border border-emerald-100 mb-3">
            <span class="text-xs font-bold text-emerald-800 uppercase tracking-wider">Hindi Audio Note (ElevenLabs)</span>
            <p id="resHindi" class="text-sm font-semibold text-emerald-950 mt-1">Instructions will appear here in natural spoken Hindi.</p>
          </div>

          <div class="p-4 rounded-xl bg-slate-50 border border-slate-100">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">English Summary</span>
            <p id="resEnglish" class="text-sm text-slate-700 mt-1">-</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <script>
    let currentHindiText = "";

    function setSample(idx) {
      const samples = {
        1: { text: "Rx: Pantocid DSR 1 tab AC x 10 days before morning tea", patient: "Dadi" },
        2: { text: "Glycomet GP 1 tab OD PC for Dadu after morning breakfast", patient: "Dadu" },
        3: { text: "Doctor ne bola Mummy ke liye Augmentin 625 din me do baar khane ke baad dena hai 5 din", patient: "Mummy" }
      };
      document.getElementById('inputText').value = samples[idx].text;
      document.getElementById('patientSelect').value = samples[idx].patient;
    }

    async function parsePrescription() {
      const text = document.getElementById('inputText').value.trim();
      const patient = document.getElementById('patientSelect').value;
      if (!text) return alert("Please enter prescription text or spoken note");

      document.getElementById('loadingSpinner').classList.remove('hidden');

      try {
        const res = await fetch('/api/parse', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text, patient })
        });
        const data = await res.json();
        
        document.getElementById('resMedicine').innerText = data.medicine_name;
        document.getElementById('resGeneric').innerText = "Generic: " + data.generic_name;
        document.getElementById('resDosage').innerText = data.dosage + " · " + data.frequency;
        document.getElementById('resTiming').innerText = data.timing;
        document.getElementById('resPurpose').innerText = data.purpose;
        document.getElementById('resPatient').innerText = data.patient;
        document.getElementById('resHindi').innerText = data.instructions_hindi;
        document.getElementById('resEnglish').innerText = data.instructions_english;
        
        currentHindiText = data.instructions_hindi;
        document.getElementById('audioPlayBtn').classList.remove('hidden');
        speakText();
      } catch (err) {
        alert("Error parsing: " + err);
      } finally {
        document.getElementById('loadingSpinner').classList.add('hidden');
      }
    }

    function speakText() {
      if (!currentHindiText) return;
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(currentHindiText);
        utterance.lang = 'hi-IN';
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
      }
    }

    async function askMemory() {
      const query = document.getElementById('queryText').value.trim();
      if (!query) return;
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await res.json();
      const box = document.getElementById('memoryAnswer');
      box.innerText = data.answer;
      box.classList.remove('hidden');
    }

    async function teachMemory() {
      const rule = document.getElementById('ruleText').value.trim();
      if (!rule) return;
      const res = await fetch('/api/memory/correct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule })
      });
      const data = await res.json();
      alert(data.message);
      document.getElementById('ruleText').value = '';
    }
  </script>
</body>
</html>
"""
    return html_content

@app.post("/api/parse")
async def parse_text(req: ParseRequest):
    # 1. Fetch rules from Backboard memory for this patient
    rules = backboard.get_rules_for_patient(req.patient)
    
    # 2. Parse using Tinker model with memory context
    parsed_json = tinker_model.parse_prescription(req.text, user_rules=rules)
    parsed_json["patient"] = req.patient
    
    # 3. Log to Backboard history
    backboard.log_medication(parsed_json)
    
    # 4. Generate voice synthesis with ElevenLabs
    voice_res = elevenlabs.generate_audio(parsed_json["instructions_hindi"])
    parsed_json["voice_status"] = voice_res
    
    return parsed_json

@app.post("/api/memory/correct")
async def add_correction(req: CorrectionRequest):
    msg = backboard.add_rule_or_correction(req.rule)
    return {"status": "success", "message": msg}

@app.post("/api/ask")
async def ask_assistant(req: QueryRequest):
    ans = backboard.answer_memory_query(req.query)
    return {"query": req.query, "answer": ans}

@app.get("/api/history")
async def get_history():
    return backboard.memory

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
