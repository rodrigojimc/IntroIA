### Compararación de BFS, UCS, DFS, DLS e IDS en el mapa de Rumania


**Origen:** Zerind
**Destino:** Hirsova

| Algorithm | Path | Depth | Cost | Expanded | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| BFS | Zerind → Arad → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova | 6 roads | 708 km | 14 nodes | success |
| UCS | Zerind → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova | 7 roads  | 676 km | 15 nodes | success |
| DFS | Zerind → Arad → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova | 6 roads | 708 km | 12 nodes | success |
| DLS: 4 | X | X | X | 13 nodes| cutoff |
| DLS: 5 | X | X | X | 21 nodes| cutoff |
| DLS: 6 | Zerind → Arad → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova | 6 roads | 708 km | 8 nodes | success |
| DLS: 8 | Zerind → Arad → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova | 6 roads | 708 km | 13 nodes | success |
| IDS| Zerind → Arad → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova | 6 roads | 708 km | 52 nodes | success |

**Análisis**

Únicamente DLS, con límites menores a 6, no encontró camino. USC encontró el de menor costo con 676 km usando 7 carreteras. Todos los demás encontraron el mismo de 708 km usando 6 carreteras.

Debido a que camino más con menor número de carrteras es 6 (garantizado con BFS), DLS no puede encontrar solución con límites inferiores.

A diferencia los demás, UCS toma en consideración el costo para determinar las rutas a explorar. Es por ello que, si existe una ruta más larga pero de menor costo la explorará primero. En este caso:

Sibiu → Rimnicu Vilcea → Pitesti → Bucharest (80+97+101 = 278)

en lugar de:

Sibiu → Fagaras → Bucharest (97+211 = 308)

DFS expandió 12 nodos, menos que cuelquier versión de DFS. Pero, si Timisoara hubiera aparecido primero como posible destino desde Arad, DFS hubiera seguido por esa ruta y le habría tomado **al menos** 7 carreteras llegar hasta Bucharest. En cambio, DFS, al barrer un nivel a la vez es "inmune" a eso; al costo de almacenar en general más nodos en memoria.

