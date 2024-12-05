import joblib
import os
import logging
import sys
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Configuración de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Ruta local al archivo .pkl
MODEL_FILE_PATH = '/home/ec2-user/model.pkl' 
ENCODER_FILE_PATH = '/home/ec2-user/encoder.pkl'  
INPUT_FILE_PATH = '/home/ec2-user/input_data.csv'

# Cargar el modelo y el encoder
def load_model_and_encoder():
    if not os.path.exists(MODEL_FILE_PATH) or not os.path.exists(ENCODER_FILE_PATH):
        logger.error("El archivo del modelo o el encoder no se encuentran en la ruta especificada.")
        sys.exit(1)

    logger.info("Cargando el modelo y el encoder...")
    model = joblib.load(MODEL_FILE_PATH)
    encoder = joblib.load(ENCODER_FILE_PATH)
    logger.info("Modelo y encoder cargados exitosamente")
    return model, encoder

def read_input_data(file_path):
    try:
        input_df = pd.read_csv(file_path)
        logger.info(f"Datos de entrada leídos desde {file_path}")
        return input_df
    except Exception as e:
        logger.error(f"Error al leer el archivo de entrada: {str(e)}")
        sys.exit(1)

# Función principal para probar el script
def main():
    try:
        # Cargar el modelo y el encoder
        model, encoder = load_model_and_encoder()

        # Leer los datos de entrada desde el archivo CSV
        input_data = read_input_data(INPUT_FILE_PATH)

        # Verificar que el archivo contenga las columnas necesarias
        required_columns = ['symptoms', 'conditions', 'contraindications', 'age']
        if not all(col in input_data.columns for col in required_columns):
            logger.error(f"El archivo de entrada debe contener las columnas: {required_columns}")
            sys.exit(1)


        # Procesar cada fila de datos de entrada y hacer la predicción
        for index, row in input_data.iterrows():
            symptoms = row['symptoms'].split(',') if pd.notnull(row['symptoms']) else []
            conditions = row['conditions'].split(',') if pd.notnull(row['conditions']) else []
            contraindications = row['contraindications'].split(',') if pd.notnull(row['contraindications']) else []
            age = row['age']

            if not symptoms or age is None:
                logger.error(f"Fila {index + 1}: Faltan datos de entrada: 'symptoms' y 'age' son obligatorios.")
                continue

            # Preprocesar los datos de entrada
            input_for_prediction = {
                'symptoms': ','.join(symptoms),
                'conditions': ','.join(conditions),
                'contraindications': ','.join(contraindications),
                'age': age
            }

            input_df = pd.DataFrame([input_for_prediction])

            # Hacer la predicción
            prediction = model.predict(input_df)
            predicted_class_index = prediction[0]

            # Decodificar la predicción usando el encoder
            predicted_class = encoder.inverse_transform([predicted_class_index])[0]

            # Mostrar el resultado
            logger.info(f"Predicción realizada para la fila {index + 1} con éxito")
            print(f"Fila {index + 1} - Medicación recomendada: {predicted_class}")
    except Exception as e:
        logger.error(f"Error al procesar la solicitud: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
