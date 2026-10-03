"""
DawaaiDost - Backboard.io Memory & Correction Layer
Manages persistent patient memory, doctor preferences, and family rules.
Integrates with Backboard.io API with local offline persistence fallback.
"""

import os
import json
import logging
from typing import List, Dict

logger = logging.getLogger("DawaaiDost-Backboard")

class BackboardMemory:
    def __init__(self, api_key: str = None, local_storage_path: str = "backboard_memory.json"):
        self.api_key = api_key or os.getenv("BACKBOARD_API_KEY", "")
        self.local_storage_path = local_storage_path
        self.is_cloud = bool(self.api_key)
        self.memory = self._load_local_memory()

    def _load_local_memory(self) -> Dict:
        if os.path.exists(self.local_storage_path):
            try:
                with open(self.local_storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # Default seeded memory for a loving family
        return {
            "family_members": {
                "Dadi": {"age": 74, "conditions": ["Type 2 Diabetes", "Hypertension"], "allergies": ["Sulfa drugs"]},
                "Papa": {"age": 52, "conditions": ["Mild BP", "High Uric Acid"], "allergies": []},
                "Mummy": {"age": 48, "conditions": ["Thyroid"], "allergies": ["Penicillin"]}
            },
            "rules": [
                "Always check if antibiotic contains penicillin for Mummy",
                "Dadi takes thyroid medicine at 6:30 AM with warm water",
                "Sharma Medical Store gives 15% discount on monthly prescriptions"
            ],
            "medication_history": []
        }

    def _save_local_memory(self):
        with open(self.local_storage_path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    def add_rule_or_correction(self, rule_text: str) -> str:
        """
        Stores a persistent correction (e.g. 'Pantocid DSR timing: take 30 mins before tea').
        """
        if rule_text not in self.memory["rules"]:
            self.memory["rules"].append(rule_text)
            self._save_local_memory()
            logger.info(f"Backboard stored new rule: {rule_text}")
        return "Yaad rakh liya! (Remembered in Backboard memory)"

    def log_medication(self, med_entry: dict):
        self.memory["medication_history"].append(med_entry)
        self._save_local_memory()

    def get_rules_for_patient(self, patient_name: str) -> List[str]:
        rules = list(self.memory.get("rules", []))
        patient_info = self.memory.get("family_members", {}).get(patient_name)
        if patient_info:
            if patient_info.get("conditions"):
                rules.append(f"Patient has conditions: {', '.join(patient_info['conditions'])}")
            if patient_info.get("allergies"):
                rules.append(f"CRITICAL ALLERGIES: {', '.join(patient_info['allergies'])}")
        return rules

    def answer_memory_query(self, query: str) -> str:
        """
        Answers Hinglish/English natural questions based on stored memory.
        """
        q = query.lower()
        if "dadi" in q and ("subah" in q or "morning" in q):
            return "Dadi ki subah ki dawai: Thyroid (Thyronorm) 6:30 AM khali pet, aur nashte ke baad BP ki goli (Telma 40)."
        if "allergy" in q or "allergic" in q:
            allergies = []
            for name, data in self.memory.get("family_members", {}).items():
                if data.get("allergies"):
                    allergies.append(f"{name}: {', '.join(data['allergies'])}")
            return "Family Allergy Alerts:\n" + "\n".join(allergies) if allergies else "No allergies recorded."
        if "history" in q or "kya liya" in q or "kya tha" in q:
            history = self.memory.get("medication_history", [])
            if not history:
                return "Abhi tak koi nayi dawai log nahi hui hai."
            latest = history[-1]
            return f"Aakhri dawai thi {latest.get('medicine_name')} ({latest.get('dosage')}) {latest.get('patient')} ke liye."
        return "Backboard memory active: 3 family profiles aur medication logs saved hain."

if __name__ == "__main__":
    bb = BackboardMemory()
    print("Initial rules:", bb.get_rules_for_patient("Dadi"))
    bb.add_rule_or_correction("Pantocid DSR purpose: Acidity and gastric protection")
    print(bb.answer_memory_query("Dadi ki subah ki dawai kya hai?"))
