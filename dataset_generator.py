"""
DawaaiDost - Synthetic Dataset Generator
Generates realistic Indian prescription shorthand, OTC blister pack text,
and Hinglish spoken notes with deterministic ground-truth JSON labels.
"""

import json
import random
import os

MEDICINES = [
    {"name": "Pantocid DSR", "generic": "Pantoprazole + Domperidone", "purpose": "Acidity / Gas", "std_timing": "Before breakfast (Empty stomach)"},
    {"name": "Glycomet GP 1", "generic": "Metformin + Glimepiride", "purpose": "Type 2 Diabetes", "std_timing": "Morning post breakfast"},
    {"name": "Telma 40", "generic": "Telmisartan", "purpose": "Blood Pressure", "std_timing": "Morning after breakfast"},
    {"name": "Dolo 650", "generic": "Paracetamol", "purpose": "Fever & Body pain", "std_timing": "SOS (When needed, after food)"},
    {"name": "Shelcal 500", "generic": "Calcium + Vitamin D3", "purpose": "Bone & Joint health", "std_timing": "After dinner"},
    {"name": "Thyronorm 50mcg", "generic": "Thyroxine Sodium", "purpose": "Thyroid", "std_timing": "Early morning empty stomach"},
    {"name": "Becosules Z", "generic": "B-Complex + Zinc", "purpose": "Multivitamin & Immunity", "std_timing": "After lunch"},
    {"name": "Augmentin 625 Duo", "generic": "Amoxicillin + Clavulanic Acid", "purpose": "Bacterial Infection", "std_timing": "Twice daily after meals"},
    {"name": "Montair LC", "generic": "Montelukast + Levocetirizine", "purpose": "Allergy & Cold", "std_timing": "Night before sleep"},
    {"name": "Atorva 10", "generic": "Atorvastatin", "purpose": "Cholesterol", "std_timing": "Night after dinner"},
]

SHORTHANDS = [
    {"code": "OD", "meaning": "Once a day", "hi": "Din me 1 baar"},
    {"code": "BD", "meaning": "Twice a day", "hi": "Din me 2 baar"},
    {"code": "TDS", "meaning": "Thrice a day", "hi": "Din me 3 baar"},
    {"code": "SOS", "meaning": "As needed", "hi": "Jab dard/zarurat ho"},
    {"code": "HS", "meaning": "At bedtime", "hi": "Raat ko sone se pehle"},
    {"code": "AC", "meaning": "Before meal", "hi": "Khane se pehle (khali pet)"},
    {"code": "PC", "meaning": "After meal", "hi": "Khane ke baad"},
]

PATIENTS = ["Dadi", "Dadu", "Mummy", "Papa", "Rohan", "Me"]

TEMPLATES = [
    # Doctor slip format
    "Rx: {med} 1 tab {code} x {days} days. {timing_note}",
    # Blister pack OCR format
    "{med} B.No. K{batch} Mfg 03/26 Exp 02/28 Dosage: As directed by physician. Take {code}",
    # Hinglish voice note format
    "Doctor ne bola {patient} ke liye {med} {timing_hi} dena hai {days} din tak",
    # Everyday WhatsApp forward format
    "Yeh {med} kab khani hai? Slip pe likha hai {code} {days} din",
    # Informal spoken Hindi
    "{patient} ki {purpose} wali goli {med} {timing_hi} 1 leni hai na?",
]

def generate_sample():
    med = random.choice(MEDICINES)
    sh = random.choice(SHORTHANDS)
    patient = random.choice(PATIENTS)
    days = random.choice([3, 5, 7, 10, 15, 30])
    batch = random.randint(1000, 9999)
    template = random.choice(TEMPLATES)
    
    text = template.format(
        med=med["name"],
        code=sh["code"],
        days=days,
        timing_note=med["std_timing"],
        timing_hi=sh["hi"],
        patient=patient,
        purpose=med["purpose"],
        batch=batch
    )
    
    label = {
        "medicine_name": med["name"],
        "generic_name": med["generic"],
        "purpose": med["purpose"],
        "dosage": "1 tablet",
        "frequency": sh["meaning"],
        "timing": med["std_timing"],
        "duration_days": days,
        "patient": patient,
        "instructions_hindi": f"{patient} ko {med['name']} {sh['hi']} leni hai. {med['std_timing']}.",
        "instructions_english": f"Take 1 tablet of {med['name']} {sh['meaning']}, {med['std_timing']} for {days} days."
    }
    
    return {
        "input_text": text,
        "ground_truth": label
    }

def generate_dataset(n_train=200, n_val=30, n_test=30, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    
    splits = {
        "train.jsonl": [generate_sample() for _ in range(n_train)],
        "val.jsonl": [generate_sample() for _ in range(n_val)],
        "test.jsonl": [generate_sample() for _ in range(n_test)],
    }
    
    for filename, rows in splits.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"Generated {len(rows)} samples in {filepath}")

if __name__ == "__main__":
    generate_dataset()
