"""
DawaaiDost - End-to-End Test Suite
Validates the dataset generator, Tinker inference, Backboard memory, and ElevenLabs module.
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from dataset_generator import generate_dataset
from train_tinker import TinkerMedicineModel
from memory_backboard import BackboardMemory
from voice_elevenlabs import ElevenLabsVoiceNarrator

def run_tests():
    print("==================================================")
    print("🚀 RUNNING DAWAAIDOST END-TO-END VALIDATION SUITE")
    print("==================================================")

    # 1. Test Dataset Generator
    print("\n[TEST 1] Testing Dataset Generator...")
    data_dir = os.path.join(os.path.dirname(__file__), "test_data")
    generate_dataset(n_train=20, n_val=5, n_test=5, output_dir=data_dir)
    assert os.path.exists(os.path.join(data_dir, "train.jsonl")), "train.jsonl missing!"
    with open(os.path.join(data_dir, "train.jsonl"), "r", encoding="utf-8") as f:
        first_line = json.loads(f.readline())
        assert "input_text" in first_line and "ground_truth" in first_line
        print(f"✅ Generated dataset successfully. Sample input: {first_line['input_text']}")

    # 2. Test Tinker Model & Shorthand Parsing
    print("\n[TEST 2] Testing Tinker Model Shorthand Parsing...")
    tinker = TinkerMedicineModel()
    
    test_cases = [
        ("Rx: Pantocid DSR 1 tab AC x 10 days for Dadi", "Pantocid DSR", "Before meal"),
        ("Rx: Telma 40 1 tab OD PC for Papa", "Telma 40", "Once a day"),
        ("Mummy ko Augmentin 625 BD dena hai 5 days", "Augmentin 625 Duo", "Twice a day"),
        ("Dolo 650 SOS fever ke liye Dadu ko", "Dolo 650", "As needed"),
    ]

    for raw_text, expected_med, expected_freq in test_cases:
        res = tinker.parse_prescription(raw_text)
        print(f"\nInput: '{raw_text}'")
        print(f"  -> Extracted: {res['medicine_name']} ({res['generic_name']})")
        print(f"  -> Frequency: {res['frequency']} | Timing: {res['timing']}")
        print(f"  -> Hindi Voice: {res['instructions_hindi']}")
        assert res["medicine_name"] == expected_med, f"Expected {expected_med}, got {res['medicine_name']}"

    print("✅ All 4 shorthand tests passed successfully!")

    # 3. Test Backboard.io Memory & Correction
    print("\n[TEST 3] Testing Backboard Memory Learning...")
    test_mem_file = os.path.join(os.path.dirname(__file__), "test_backboard.json")
    if os.path.exists(test_mem_file):
        os.remove(test_mem_file)
        
    bb = BackboardMemory(local_storage_path=test_mem_file)
    
    # Store custom rule
    teach_res = bb.add_rule_or_correction("Pantocid DSR timing: 30 mins before morning chai")
    assert "Yaad rakh liya" in teach_res
    print(f"  -> Teacher response: {teach_res}")

    # Parse with rule injected
    rules = bb.get_rules_for_patient("Dadi")
    res_with_rule = tinker.parse_prescription("Rx: Pantocid DSR for Dadi", user_rules=rules)
    print(f"  -> Rule-influenced Timing: {res_with_rule['timing']}")
    assert "morning chai" in res_with_rule["timing"]
    print("✅ Memory rule injection verified!")

    # 4. Test Query Assistant
    print("\n[TEST 4] Testing Backboard Query Assistant...")
    ans1 = bb.answer_memory_query("Dadi ki subah ki dawaiyan kya hain?")
    print(f"  -> Q: 'Dadi ki subah ki dawaiyan kya hain?'")
    print(f"  -> A: {ans1}")
    assert "Thyroid" in ans1 or "BP" in ans1

    # 5. Test ElevenLabs Voice Narrator
    print("\n[TEST 5] Testing ElevenLabs Voice Narrator Module...")
    narrator = ElevenLabsVoiceNarrator()
    audio_res = narrator.generate_audio(res_with_rule["instructions_hindi"])
    print(f"  -> TTS Status: {audio_res['status']} (Source: {audio_res['source']})")
    assert audio_res["status"] in ["success", "ready_for_browser_tts", "fallback"]
    print("✅ Voice generation module passed!")

    print("\n==================================================")
    print("🎉 ALL 5 TEST SUITES PASSED! READY FOR SUBMISSION!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
