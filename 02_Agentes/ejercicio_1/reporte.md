# Reporte

El primer mapa fue pensado para comparar cómo los agentes enfrentaban el reto de dar una vuelta rodeada de peligros.

```
4 |P . . . 
3 |. . W .
2 |. P G .
1 |> . P .
   _ _ _ _
   1 2 3 4
   ```

Los primeros 3 agentes eventualmente se quedan girando en la posición [2,1]; el 4to, por el contrario, explora esa posición y sale sólo para luego ir directo a la posición [1,4] y caerse por un pozo.

**Agente:** Simple Reflex
**Resultado:**  stopped without gold  steps=200  score=-200.0

**Agente:** Model Based
**Resultado:** stopped without gold  steps=200  score=-200.0


**Agente:** Goal Based
**Resultado:** stopped without gold  steps=200  score=-200.0

**Agente:** Utility Based
**Resultado:** died without gold  steps=8  score=-1008.0

A causa de la insatsfacción causada por el resultado del experimento con el primer mapa, a pesar que existe un camino seguro de ida y vuelta, se eliminó el pozo en la posición [3,1] y se movió el oro a la posición [2,4].

```
4 |P G . . 
3 |. . W .
2 |. P . .
1 |> . . .
   _ _ _ _
   1 2 3 4
   ```

Se obtuvo el mismo resultado.

# Conclusiones

Despúes de analizar los resultados, notamos que pesar de que los mapas son distintos, las percepciones de los agentes son las mismas; en este caso, brisa en las posiciones [2,1], [1,2] y [1,3].

Podemos inferir que los modelos tienen comportamientos deterministicos.

Desafortunadamente no fuimos testigos de algún agente logrando obtener el oro y salir de la cueva, tampoco la muerte de algún Wumpus. Aún así, creo que el aprendizaje es valioso.



