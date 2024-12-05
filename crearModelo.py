import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import os

# Ruta para guardar el modelo en la EC2
MODEL_FILE_PATH = '/home/ec2-user/model.pkl'  # Cambia la ruta si necesitas guardarlo en otro lugar
ENCODER_FILE_PATH = '/home/ec2-user/encoder.pkl'

# Leer los datos desde el archivo CSV
CSV_FILE_PATH = 'results.csv'  # Cambiar a la ruta de tu archivo CSV
df = pd.read_csv(CSV_FILE_PATH)

# Preprocesamiento de los datos
df['symptoms'] = df['symptoms'].apply(lambda x: ','.join(str(x).split(',')))  # Asegurarse de que los síntomas sean una cadena
df['conditions'] = df['conditions'].apply(lambda x: ','.join(str(x).split(',')))  # Asegurar que las condiciones sean una cadena
df['contraindications'] = df['contraindications'].apply(lambda x: ','.join(str(x).split(',')))  # Asegurar que las contraindicaciones sean una cadena
df['recommended_medication'] = df['recommended_medication'].apply(lambda x: ','.join(str(x).split(',')))

# Codificar las etiquetas de los medicamentos
le = LabelEncoder()
df['recommended_medication'] = le.fit_transform(df['recommended_medication'])

# Preparar las características (X) y etiquetas (y)
X = df[['age', 'symptoms', 'conditions', 'contraindications']]
y = df['recommended_medication']

# Configurar el preprocesamiento de características
# Convertir columnas de texto en características numéricas con TfidfVectorizer
preprocessor = ColumnTransformer(
    transformers=[
        ('text', TfidfVectorizer(), 'symptoms'),
        ('conditions', TfidfVectorizer(), 'conditions'),
        ('contraindications', TfidfVectorizer(), 'contraindications'),
        ('age', StandardScaler(), ['age'])  # Escalar la edad para que se integre bien con las otras características
    ]
)

# Configurar el pipeline de procesamiento de texto y el modelo
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())  # Modelo de clasificación
])

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model.fit(X_train, y_train)

# Guardar el modelo en un archivo .pkl
joblib.dump(model, MODEL_FILE_PATH)
joblib.dump(le, ENCODER_FILE_PATH)

print(f'Modelo guardado localmente en {MODEL_FILE_PATH}')
