### Predicción en YOLO

**Primera corrida**

YOLOv8n identifica correctamente a 2 personas y una corbata. EL módelo no es capaz de reconocer objetos para los cuales no cuenta con etiqueta; por ejemplo Zidane.

YOLOv8n + COCO128 x 3 identifica correctamente a 4 perspnas, un camión y una señal de alto a pesar de que esta última y 2 de las personas aparecen parcialmente.

**Segunda corrida**ç

Se eligió una foto en la que aparecen un tostador, una vasija, un cuchillo y pan rebanado y los resultados difieren:

YOLOv8n:

Tostador -> maleta
vasija -> vasija
pan rebanado -> pastel y sandwich

YOLOv8n:

Tostador -> maleta
vasija -> botella
pan rebanado -> bowl y sandwich
cuchillo -> cuchara

Es entendible que no reconozca superficies la mesa o la tabla; o que identifique pan rebanado como un sandwich. Pero al cambiar la orientación lo etiqueta como pastel o bowl.

Probablemente el segundo modelo clasifico la vasija como botella debido a las características del cuello; que técnicamente podría considerarse correcto.

Esperaba que clasificara correctamente el tostador pero probablemente la forma curva y el color son mucho más comunes en maletas. 

El segundo modelo logró identificar un objeto más, que aunque no es una cuchara, un cuchillo es un cubierto; no es un ángulo claro.