import json
import random
import uuid  # Para generar patient_id único
from faker import Faker

fake = Faker()

# Lista ampliada de síntomas, condiciones y contraindicaciones
symptoms = ["fever", "headache", "cold", "cough", "sore throat", "fatigue", "nausea", "dizziness", "body aches", "shortness of breath"]
conditions = ["diabetes", "hypertension", "asthma", "heart disease", "arthritis", "obesity", "kidney disease", "cancer"]
contraindications = ["ibuprofen", "paracetamol", "antihistamine", "aspirin", "codeine", "naproxen", "acetaminophen"]

# Medicaciones y sus respectivas contraindicaciones para asegurar que no se crucen
medications = {
    "fever": "Paracetamol",
    "headache": "Ibuprofen",
    "cold": "Antihistamine",
    "cough": "Cough Syrup",
    "sore throat": "Throat Lozenges",
    "fatigue": "Rest",
    "nausea": "Anti-nausea Medication",
    "dizziness": "Dizzy Relief",
    "body aches": "Pain Reliever",
    "shortness of breath": "Bronchodilator"
}

# Generación de datos en formato compatible con DynamoDB
data = []
for _ in range(1000):
    age = random.randint(1, 90)
    symptom_list = random.sample(symptoms, k=random.randint(1, 3))
    condition_list = random.sample(conditions, k=random.randint(0, 2))
    contraindication_list = random.sample(contraindications, k=random.randint(0, 2))
    
    # Recomendar medicamentos, asegurando que no se crucen con las contraindicaciones
    recommended = [
        med for sym in symptom_list if (med := medications.get(sym)) not in contraindication_list
    ]

    # Crear un diccionario con el formato de DynamoDB
    data.append({
        'patient_id': {'S': str(uuid.uuid4())},  # Generar un ID único
        'age': {'N': str(age)},
        'symptoms': {'L': [{'S': sym} for sym in symptom_list]},
        'conditions': {'L': [{'S': cond} for cond in condition_list]},
        'contraindications': {'L': [{'S': con} for con in contraindication_list]},
        'recommended_medication': {'L': [{'S': med} for med in recommended]}
    })

# Guardar los datos en un archivo JSON compatible con DynamoDB
with open("patient_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Datos generados y guardados en 'patient_data_dynamo.json' con formato compatible con DynamoDB.")
