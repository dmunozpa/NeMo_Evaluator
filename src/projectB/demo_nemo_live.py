import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")


model_target = {
    "api_endpoint": {
        "url": "http://host.docker.internal:1234/v1",
        "model_id": "nvidia_llama-3.1-nemotron-nano-8b-v1",
    }
}

correctness_prompt = """
Your task is to determine if the summary correctly reflects the consultation.

CONSULTATION CONTENT: {{content}}
SUMMARY: {{summary}}

Reply with a score between 0 and 4, where 0 is the worst and 4 is the best. You must response with: "SCORE: <score>" only.
"""


response = client.evaluation.live(
# Create an evaluation job
    config={
        "type": "custom",
        "timeout": None,
        "tasks": {
            "correctness": {
                "type": "data",
                "metrics": {
                    "correctness-likert": {
                        "type": "llm-judge",
                        "params": {
                            "model": model_target,
                            "template": {
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": "detailed thinking off"
                                    },
                                    {
                                        "role": "user",
                                        "content": correctness_prompt
                                    }
                                ]
                            },
                            "scores": {
                                "correct": {
                                    "type": "int",
                                    "parser": {
                                        "type": "regex",
                                        "pattern": "SCORE: (\\d)"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    target={
        "type": "rows",
        "rows": [
            {"ID": "C001", "content": "Date: 2025-04-01\nChief Complaint (CC): Cough and fever\nHistory of Present Illness (HPI): three‑day history of productive cough with yellow sputum and low‑grade fevers peaking at 38.5 °C. He denies pleuritic chest pain but reports mild shortness of breath while climbing stairs.\nPast Medical History (PMH): History significant for essential hypertension well‑controlled on lisinopril. No prior pulmonary disease. Immunizations up to date.\nReview of Systems (ROS): Denies unintentional weight loss, night sweats, or hemoptysis. Endorses mild malaise.\nPhysical Examination (PE): Vital signs: T 38.1 °C, HR 96 bpm, BP 132/80 mm Hg, RR 18, SpO₂ 96 % RA. General: alert, mildly ill‑appearing. Lungs: bronchial breath sounds with crackles at right base. Cardiac: regular rhythm, no murmurs. Abdomen: soft, non‑tender. No peripheral edema.\nFamily History (FHx): Father with coronary artery disease diagnosed at 55; mother with rheumatoid arthritis.\nSocial History (SocHx): Non‑smoker, occasional alcohol, works as software engineer, walks 30 minutes daily.\nAssessment & Plan: Discussed likely community‑acquired pneumonia. Initiated amoxicillin‑clavulanate 875 mg twice daily for 10 days, advised rest, hydration, and proper cough hygiene. Educated patient on red‑flag symptoms such as worsening dyspnea or persistent fever.\nLabs / Imaging Ordered: CBC with differential, basic metabolic panel, chest radiograph PA/lat.", "summary": "Patient fine, probs viral.\nCase Summary: ¯\\_(ツ)_/¯\nDisease Specific Elements: none included because meh.\nPaste Medical History: unimportant."},
            {"ID": "C002", "content": "Date: 2025-04-02\nChief Complaint (CC): Sharp substernal chest pain\nHistory of Present Illness (HPI): sudden‑onset, stabbing chest pain that began one hour prior to arrival while shoveling snow. The pain is non‑radiating, rated 7/10, partially relieved by resting and sitting upright.\nPast Medical History (PMH): Known hyperlipidemia managed with a statin. No previous cardiac events.\nReview of Systems (ROS): Reports diaphoresis with exertion but no palpitations or presyncope.\nPhysical Examination (PE): Vitals: BP 148/88 mm Hg, HR 90 bpm, RR 20, afebrile. Cardiovascular: no JVD; S1, S2 normal; no murmurs. Chest wall non‑tender. Lungs clear. Extremities: no edema.\nFamily History (FHx): Mother with breast cancer diagnosed at 60; no early cardiac deaths in family.\nSocial History (SocHx): Smokes one pack per day for 15 years, no alcohol; works as mechanic.\nAssessment & Plan: Obtained ECG and baseline troponin. Administered 325 mg aspirin and nitroglycerin spray with symptomatic improvement. Will repeat troponin in 3 hours and admit to observation for serial cardiac enzymes and potential cardiology consult.\nLabs / Imaging Ordered: Serial troponins, stat ECG, chest X‑ray, lipid panel.", "summary": "New Clinical Problem: Sharp substernal chest pain\nCase Summary: sudden‑onset, stabbing chest pain that began one hour prior to arrival while shoveling snow. The pain is non‑radiating, rated 7/10, partially relieved by resting and sitting upright.\nDisease Specific Elements: ROS: Reports diaphoresis with exertion but no palpitations or presyncope.. PE: Vitals: BP 148/88 mm Hg, HR 90 bpm, RR 20, afebrile. Cardiovascular: no JVD; S1, S2 normal; no murmurs. Chest….\nPaste Medical History: Known hyperlipidemia managed with a statin. No previous cardiac events."},
            {"ID": "C003", "content": "Date: 2025-04-03\nChief Complaint (CC): Diffuse abdominal discomfort\nHistory of Present Illness (HPI): gradually worsening, cramp‑like abdominal pain that started around the umbilicus six hours ago and has now localized to the right lower quadrant. Associated symptoms include nausea and anorexia, with no bowel movements today.\nPast Medical History (PMH): No significant past medical or surgical history.\nReview of Systems (ROS): Positive for anorexia and nausea; negative for hematochezia, melena, or dysuria.\nPhysical Examination (PE): Vitals stable. Abdomen: soft with guarding in RLQ; rebound tenderness present; positive Rovsing sign. Bowel sounds hypoactive.\nFamily History (FHx): No known hereditary diseases in immediate family.\nSocial History (SocHx): No tobacco, drinks wine socially; accountant who exercises at gym twice weekly.\nAssessment & Plan: NPO status, started IV fluids and performed pain management with morphine. Surgical consult requested for possible appendectomy. Ceftriaxone 1 g IV administered as prophylactic antibiotic.\nLabs / Imaging Ordered: CBC, CMP, CRP, abdominal ultrasound if CT unavailable.", "summary": "New Clinical Problem: Diffuse abdominal discomfort\nCase Summary: gradually worsening, cramp‑like abdominal pain that started around the umbilicus six hours ago and has now localized to the right lower quadrant. Associated symptoms include nausea and anorexia, with no bowel movements today.\nDisease Specific Elements: ROS: Positive for anorexia and nausea; negative for hematochezia, melena, or dysuria.. PE: Vitals stable. Abdomen: soft with guarding in RLQ; rebound tenderness present; positive Rovsing sign. Bowel sounds hypoactive..\nPaste Medical History: No significant past medical or surgical history."},
            {"ID": "C004", "content": "Date: 2025-04-04\nChief Complaint (CC): Throbbing frontal headache\nHistory of Present Illness (HPI): intermittent, pulsating headaches over the last week, predominantly in the frontal region, accompanied by photophobia and phonophobia. Over‑the‑counter ibuprofen provides partial relief.\nPast Medical History (PMH): Migraine headaches since adolescence, currently on low‑dose propranolol.\nReview of Systems (ROS): Positive photophobia and phonophobia; denies vision changes or weakness.\nPhysical Examination (PE): Afebrile. Neurological exam intact. Fundoscopic exam shows no papilledema. Neck supple. No focal deficits.\nFamily History (FHx): Mother suffers from migraines; father healthy.\nSocial History (SocHx): Former smoker, quit five years ago; IT consultant; enjoys cycling.\nAssessment & Plan: Increased propranolol long‑acting to 80 mg daily. Encouraged migraine diary and trigger avoidance. Provided information about triptan therapy if headaches persist.\nLabs / Imaging Ordered: No labs today; MRI brain if headaches worsen.", "summary": "New Clinical Problem: Throbbing frontal headache\nCase Summary: intermittent, pulsating headaches over the last week, predominantly in the frontal region, accompanied by photophobia and phonophobia. Over‑the‑counter ibuprofen provides partial relief.\nDisease Specific Elements: ROS: Positive photophobia and phonophobia; denies vision changes or weakness.. PE: Afebrile. Neurological exam intact. Fundoscopic exam shows no papilledema. Neck supple. No focal deficits..\nPaste Medical History: Migraine headaches since adolescence, currently on low‑dose propranolol."},
            {"ID": "C005", "content": "Date: 2025-04-05\nChief Complaint (CC): Progressive exertional shortness of breath\nHistory of Present Illness (HPI): shortness of breath on exertion for the past two weeks, now noticeable after climbing two flights of stairs. She endorses mild orthopnea requiring two pillows at night but denies chest tightness.\nPast Medical History (PMH): Paroxysmal atrial fibrillation on apixaban; otherwise healthy.\nReview of Systems (ROS): Denies paroxysmal nocturnal dyspnea; endorses mild ankle swelling.\nPhysical Examination (PE): Blood pressure 140/90 mm Hg; pulse 88 bpm. Lungs: mild bibasilar crackles. Heart: regular rate. No peripheral edema.\nFamily History (FHx): Father with congestive heart failure; mother with hypertension.\nSocial History (SocHx): Never smoked; occasionally consumes beer; office administrator with sedentary lifestyle.\nAssessment & Plan: Ordered transthoracic echocardiogram and BNP level to evaluate for heart failure exacerbation. Increased furosemide to 40 mg daily and reinforced sodium‑restricted diet.\nLabs / Imaging Ordered: BNP, basic metabolic panel, echocardiogram.", "summary": "New Clinical Problem: Progressive exertional shortness of breath\nCase Summary: shortness of breath on exertion for the past two weeks, now noticeable after climbing two flights of stairs. She endorses mild orthopnea requiring two pillows at night but denies chest tightness.\nDisease Specific Elements: ROS: Denies paroxysmal nocturnal dyspnea; endorses mild ankle swelling.. PE: Blood pressure 140/90 mm Hg; pulse 88 bpm. Lungs: mild bibasilar crackles. Heart: regular rate. No peripheral edema..\nPaste Medical History: Paroxysmal atrial fibrillation on apixaban; otherwise healthy."},
        ]
    }
)


print(f"Status: {response.status}")
print(f"Results: {response.result.tasks['correctness'].metrics['correctness-likert'].scores}")