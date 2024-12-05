import random
import pandas as pd

# Listas de ejemplo para generar datos aleatorios
symptoms_list = ["fever", "headache", "body aches", "cough", "sore throat", "fatigue", "cold", "shortness of breath"]
conditions_list = ["hypertension", "diabetes", "asthma", "heart disease", "obesity"]
contraindications_list = ["ibuprofen", "aspirin", "paracetamol", "codeine", "antihistamine", "naproxen"]

# Función para generar datos aleatorios
def generate_random_data(num_rows):
    data = []
    for _ in range(num_rows):
        # Generar entre 1 y 3 síntomas
        symptoms = random.sample(symptoms_list, random.randint(1, 3))
        # Generar entre 0 y 2 condiciones
        conditions = random.sample(conditions_list, random.randint(0, 2))
        # Generar entre 0 y 2 contraindicaciones
        contraindications = random.sample(contraindications_list, random.randint(0, 2))
        # Generar una edad entre 18 y 90
        age = random.randint(18, 90)

        data.append({
            "symptoms": ",".join(symptoms),
            "conditions": ",".join(conditions),
            "contraindications": ",".join(contraindications),
            "age": age
        })

    return data

# Número de filas de datos a generar
num_rows = 2

# Generar los datos
random_data = generate_random_data(num_rows)

# Crear un DataFrame con los datos
df = pd.DataFrame(random_data)

# Guardar los datos en un archivo CSV
output_file = "input_data.csv"
df.to_csv(output_file, index=False)

print(f"Datos de prueba generados y guardados en {output_file}")
