# Procesamiento de Lenguaje Natural (NLP)

El Procesamiento de Lenguaje Natural es la rama de la inteligencia artificial que se ocupa de la interacción entre computadoras y lenguaje humano. Permite a las máquinas comprender, interpretar y generar texto y lenguaje hablado de manera útil y significativa.

## Desafíos del NLP

### Ambigüedad
El lenguaje humano es profundamente ambiguo. Una misma oración puede tener múltiples significados dependiendo del contexto. Por ejemplo, la palabra "banco" puede referirse a una institución financiera o a un asiento.

### Variabilidad
Las personas expresan las mismas ideas de muchas formas diferentes. El mismo concepto puede ser comunicado de innumerables maneras, con diferentes vocabularios y estructuras gramaticales.

### Dependencia del Contexto
El significado de las palabras y frases depende altamente del contexto en el que aparecen. Entender el contexto amplio es crucial para la comprensión correcta.

## Procesamiento de Tokens

### Tokenización
La tokenización es el proceso de dividir un texto en unidades más pequeñas llamadas tokens. Típicamente, los tokens son palabras, pero también pueden ser caracteres o subpalabras. La tokenización puede ser:
- A nivel de palabra: dividir por espacios
- A nivel de subpalabra: usar algoritmos como BPE (Byte Pair Encoding)
- A nivel de carácter: cada carácter es un token

### Normalización
La normalización convierte el texto a un formato estándar:
- Convertir a minúsculas
- Remover acentos
- Eliminar puntuación
- Remover espacios extra

## Representaciones de Palabras

### Bag of Words (BoW)
En la representación Bag of Words, un documento se representa como un vector donde cada posición corresponde a una palabra del vocabulario y el valor es la frecuencia de esa palabra. Esta representación es simple pero pierde información sobre el orden de las palabras.

### TF-IDF
TF-IDF (Term Frequency - Inverse Document Frequency) es una variación de BoW que pesa los términos según su importancia. Términos que aparecen en muchos documentos (como palabras frecuentes) tienen menor peso que términos que aparecen en pocos documentos.

### Word2Vec
Word2Vec es un modelo que aprende representaciones densas (embeddings) de palabras. El modelo se entrena con un objetivo simple: predecir palabras vecinas. Las palabras con significados similares terminan con embeddings similares.

### GloVe (Global Vectors for Word Representation)
GloVe combina información global de coocurrencia de palabras con métodos de aprendizaje local. El resultado son embeddings de palabras que capturan tanto significado semántico como sintáctico.

## Modelos de Secuencia

### RNNs y LSTMs
Las Redes Neuronales Recurrentes procesan secuencias de entrada una palabra a la vez, manteniendo un estado oculto que captura información de palabras anteriores. Las LSTMs resuelven el problema de degradación del gradiente que aquejaba a RNNs simples.

### GRU (Gated Recurrent Unit)
Similar a LSTM pero con una arquitectura más simple y eficiente computacionalmente. Funciona bien para muchas tareas NLP.

### Transformers
Los Transformers utilizan el mecanismo de atención para procesar todas las palabras en paralelo, lo que los hace más rápidos de entrenar que RNNs. Modelos como BERT, GPT y T5 están basados en arquitecturas transformer.

## Tareas Comunes en NLP

### Análisis de Sentimientos
Determinar si un texto expresa sentimiento positivo, negativo o neutral. Esta tarea es útil para análisis de redes sociales, revisiones de productos y feedback de clientes.

### Etiquetado de Partes del Discurso (POS Tagging)
Etiquetar cada palabra en un texto con su parte del discurso (nombre, verbo, adjetivo, etc.). Esto es el primer paso en muchos análisis sintácticos.

### Reconocimiento de Entidades Nombradas (NER)
Identificar y clasificar entidades nombradas en el texto como personas, lugares, organizaciones y fechas.

### Traducción Automática
Convertir texto de un idioma a otro. Los modelos transformer han mejorado significativamente la calidad de la traducción automática.

### Generación de Texto
Producir texto coherente y relevante basado en un prompt o contexto. Los modelos generativos como GPT son especialmente buenos en esta tarea.

## Modelos Pre-entrenados

Los modelos pre-entrenados han revolucionado el NLP. Modelos como BERT se entrenan en grandes corpus de texto no etiquetado y luego se pueden afinar (fine-tune) para tareas específicas. Esto reduce significativamente el tiempo de entrenamiento y mejora el rendimiento en tareas con datos limitados.

## Desafíos Actuales

### Sesgo en el Lenguaje
Los modelos entrenados en datos reales heredan sesgos presentes en el lenguaje humano. Pueden reflejar o amplificar prejuicios demográficos.

### Explicabilidad
Entender por qué un modelo hace una predicción particular es difícil, especialmente con modelos grandes y complejos.

### Requisitos de Datos
Los modelos modernos requieren cantidades masivas de datos de entrenamiento para funcionar bien.

## Aplicaciones Prácticas

El NLP tiene aplicaciones en:
- Asistentes virtuales como Siri, Alexa y Google Assistant
- Chatbots y sistemas de atención al cliente
- Análisis de sentimientos en redes sociales
- Búsqueda y recuperación de información
- Detección de spam y phishing
- Resumen automático de documentos
