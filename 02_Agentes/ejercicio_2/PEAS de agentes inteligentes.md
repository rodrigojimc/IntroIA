### 1. Asistente virtual de voz

- **Performance:** Entiende lo que se le dice y responde de forma coherente, correcta y segua.
- **Environment:** Habitaciones, autos, dispositivos móviles, dispositivos electrónicos. Voz.
- **Actuators:** Vocinas, Wifi, APIs.
- **Sensors:** Internet, perfiles de usuario, micrófono, texto, Wifi, Bluetooth.

### 2. Robot aspirador doméstico

- **Performance:** Limpia y cubre de manera eficiente las superficies y no se queda atascado.
- **Environment:** Inmuebles: Casas, departamentos, locales, hoteles, oficinas. Piso, paredes, muebles, personas, animales.
- **Actuators:** Motores para movimiento y bombas para succión y expulsión.
- **Sensors:** De proximidad y contacto, cámara, giroscopio, acelerometro, Wifi, Bluetooth.

### 3. Sistema de recomendación de streaming

- **Performance:** Sus recomendaciones resultan atractivas al usuario y filtra el contenido no deseado.
- **Environment:** Aplicaciones para pantallas, contenido clasificado.
- **Actuators:** APIs para perfiles de usuarios y bases de datos.
- **Sensors:** Calificaciones, historiales de reproducción, estádisticas.

### 4. Vehículo autónomo en ciudad

- **Performance:** Lleva del origen al destino cumpliendo todas la normas de vialidad en tiempos razonables. Es menos propenso a causar accidentes que un conductor humano.
- **Environment:** Vialidades: calles, carreteras, puentes, glorietas, semáforos, túneles, estacionamientos, etc.
- **Actuators: Controles del vehículo: acelerador, embrague, freno, guía, luces, limpia parabrisas, etc.
- **Sensors:** Proximidad, iluminación, clima, humedad, temperatura, cámaras, acelerometro, giroscopio, GPS, indicadores del vehículo: nivel de combustible/carga, aceite, llantas, anticongelante, etc.

### 5. Agente de trading algorítmico en bolsa

- **Performance:** Automatiza la compra y venta de valores únicamente dentro de los paramétros (rendimiendo, riesgo, frecuencia, etc...) configurados por el usuario. Identifica y predice tendencias con presición competente.
- **Environment:** El mercado financiero, brokers tanto humanos como agentes.
- **Actuators:** APIs para compra y venta, notificaciones: pop up en apps, correo, etc.
- **Sensors:** APIs, noticias, redes sociales.

### 6. Sistema de diagnóstico médico asistido por IA

- **Performance:** Diagnostica con alta presición y recomienda pruebas médicas y tratamientos con alta efectividad. En cualquier caso proporciona datos estádisticos y fuentes comprobables.
- **Environment:** Hospitales, clínicas y consultorios. Personal médico, pacientes.
- **Actuators:** Pantalla.
- **Sensors:** Texto, UI, resultados de estudios, bases de datos, internet.

### 7. Dron de inspección de infraestructura

- **Performance:** Identifica y reporta correctamente problemas estructurales. Es capaz de navegar y cubrir las áreas a insnspeccionar.
- **Environment:** Edificios, casas, fábricas, puéntes, túneles, etc.
- **Actuators:** Motores, APIs, Bluetooth, Wifi.
- **Sensors:** Cámara, acelerómetro, de proximidad, de contacto, girscopio, GPS, Wifi, micrófono, temperatura, humedad, campos magnéticos, etc.

### 8. Agente jugador de ajedrez

- **Performance:** Cumple con las reglas del ajedréz. Tiene un ELO competitivo. Puede regularse su nivel de juego.
- **Environment:** Tablero y piezas de ajedrez.
- **Actuators:** API
- **Sensors:** API

### Propiedades del ambiente
| Agente | Observable | Determinisico | Episódico | Estático | Discreto |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Asistente virtual de voz | Parcial | No | Sí | No | No|
| Robot aspirador doméstico | Parcial | No | Sí | No | No |
| Sistema de recomendación de streaming | Completo | No | Sí | Sí | Sí |
| Vehículo autónomo en ciudad | Parcial | No | No | No | No | No |
| Agente de trading algorítmico en bolsa | Parcial | No | No | No | No |
| Sistema de diagnóstico médico asistido por IA | Parcial | No | Sí | Sí | No |
| Dron de inspección de infraestructura | Parcial  | No | Sí | Sí | No |
| Agente jugador de ajedrez | Completo | Sí | Sí | Sí | Sí |
