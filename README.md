# Proyecto: El machine learning y su aporte en el sector salud para mayor efectividad en formulación de medicamentos

## Resumen
El objetivo de este proyecto es ver la capacidad de las ec2 utilizando modelos de ML, el modelo se baso en un sistema de salud, donde el usuario digite sus sintomas, condiciones o enfermedades, contraindicaciones o alergias a ciertos medicamentos y su edad, el resultado debe ser capaz de leer dicha informacion y con data suministrada para la creacion del modelo (data clinica) dara un medicamento optimo segun los datos del paciente

## Arquitectura
![ProyectoAYGO](https://github.com/user-attachments/assets/a064e89a-a13f-4870-8f58-62cea3784af8)

Se carga la información a una base de datos de Dynamo para poder extraer la información en un CSV con la estructura json que propone la BD, dicho csv es usado por un script de py el cual genera el modelo de ML, este retorna 2 archivos el modelo en sí y el encoder es decir las clasificaciones de los medicamentos recomendados en formato numérico. 
Tenemos un usuario que escribe sus datos de entrada y los deja en un csv y por medio de otro script validamos el modelo y lo datos, ejecutamos el resultado y obtenemos un valor numérico, luego con el encoder revisamos a que medicamento hace referencia dicho numero y retornamos la respuesta recomendada al usuario según los síntomas, contraindicaciones y condiciones registradas
Todo este mecanismo esta dentro de una EC2, se creo con una t2micro, por la volumetria y el tipo de modelo, si es neceario un modelo mas robusto y muchos mas datos, se puede considerar elevar el tamaño de la VM

## Implementacion

Descargar `git` y `python` en la VM luego instalar las librerias `scikit-learn` y `pandas`, ejecutamos los archivos en orden `python3 crear_datos.py` asi nos genera el primer csv o los datos que irian en la BD, luego `python3 crearModelo.py` nos generara los 2 archivos pkl que usaremos mas adelante.
Luego `python3 crearDatos.py` en este tenemos una variable n donde podemos colocar la cantidad de pruebas que queremos testear con el modelo, por ultimo ejecutamos el modelo para ver los resultados de los medicamentos propuestos `python3 ejecutarModelo.py`

## Evidencias

Se hace una carga masiva de datos, donde se generan 2000 datos de pacientes y podemos ver que la VM no sube mas del 10% de su capacidad, como se menciono anteriormente para ser una t2micro es un dato bastante bueno, por el hecho que tiene una CPU y un nucleo.

![image](https://github.com/user-attachments/assets/baadeebb-e14b-4b46-8fa9-120cd751cce0)
![image](https://github.com/user-attachments/assets/e1f2d9f9-8d39-4dfd-8a5f-4795e5cbca52)

Se muestra un video con la implementacion y los resultados propuestos
https://youtu.be/H4l3003nINc
