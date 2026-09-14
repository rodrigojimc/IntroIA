### Más capas en el perceptrón multicapa (Iris)

Al añadir 2 capas más el modelo implementado con Numpy mejoró. En ambos casos el entrenamiento tomó 9s, por lo que no hay una diferencia significativa. En cambio sí la hay en el error.

Numpy 4x3x3 - 9s
Error_vec[0] = 0.7762190147353139
Error_vec[500] = 0.07444980943030063

Numpy 4x3x3x3x3 - 9s
Error_vec[0] = 0.7334603855034343
Error_vec[500] = 0.05761877472562357

Por otro lado, el resultad con el modelo implementado en Keras, empeoró. Paso de entrenarse en 39s a 36s pero el error final es mayor. Además las predicciones son peores, producen vectores con valores cercanos.

Keras/TensorFlow 4x3x3 - 39s
Epoch 1/500 - loss: 0.3004  
Epoch 500/500  - loss: 0.1633
[3,3,1,1] -> [0.50686115, 0.31040448, 0.2676654]


Keras/TensorFlow 4x3x3 - 36s
Epoch 1/500 - loss: 0.2651  
Epoch 500/500  - loss: 0.2223
[3,3,1,1] -> [0.3356188, 0.3348662, 0.3341998]

Las graficas del los modelos en la primera corrida de 4x3x3 tienen una forma similar pero en la segunda de 4x3x3x3x3, el modelo implementado con Numpy se estanca por un periodo pero vuelve a descender, en cambio el modelo implementado con Keras se queda estancado.

Basádos únicamente en estos datos, inferimos una red más profunda con capas sigmoidales apiladas y una función de pérdida de error cuadrático medio (MSE) no aprenda mejor, e incluso podría aprender peor.

Posteriormente, investigando para comparar resultados con otras fuentes, econtramos posibles razones:

- Puede requerir más datos y entrenamiento.
- Puede quedar en un mínimo local.
- Es más sensible al "overfitting": memorizar datos en lugar de aprender a generalizar
- Debido a que las funciones sigmoides tienen gradientes muy pequeños, al tener más capas, al multiplicarse durante la propagación tienden a ser insignficantes.
- MSE no es la función de pérdida más adecuada para problemas de clasificación multiclase ya que asume que los errores son continuos y distribuidos normalmente, lo cual no es el caso con las probabilidades discretas de las clases.
