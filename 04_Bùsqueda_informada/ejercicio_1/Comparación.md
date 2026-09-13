### Compararación de Greedy y A* en el mapa de Rumania


**Origen:** Timisoara
**Destino:** Vaslui

**Heurística**
| h(n) | city |
| :--- | :---: |
| 0 | **Vaslui** | 
| 72 | Iasi |
| 97 | Hirsova |
| 108 | Urziceni |
| 139 | Neamt |
| 160 | Bucharest |
| 160 | Eforie |
| 204 | Pitesti |
| 204 | Fagaras |
| 220 | Giurgiu |
| 278 | Rimnicu Vilcea |
| 300 | Craiova |
| 302 | Sibiu |
| 350 | Lugoj |
| 357 | Mehadia |
| 373 | Drobeta |
| 399 | Oradea |
| 410 | Zerind |
| 416 | **Timisoara** |
| 421 | Arad |


**Tablas Comparativa**
| Algorithm | Path | Depth | Cost | Expanded | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Greedy  | Timisoara → Lugoj → Mehadia → Drobeta → Craiova → Pitesti → Bucharest → Urziceni → Vaslui | 8 roads | 842 km | 8 nodes | success |
| A* | Timisoara → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Vaslui | 7 roads  | 763 km | 14 nodes | success |

Greedy
| city       | g   | h   | f   |
|------------|----:|----:|----:|
| Timisoara  | 0   | 416 | 416 |
| Lugoj      | 111 | 350 | 461 |
| Mehadia     | 181 | 357 | 538 |
| Drobeta     | 256 | 373 | 629 |
| Craiova     | 376 | 300 | 676 |
| Pitesti     | 514 | 204 | 718 |
| Bucharest  | 615 | 160 | 775 |
| Urziceni   | 700 | 108 | 808 |
| Vaslui     | 842 | 0   | 842 |

A*
| city      | g   | h   | f   |
|-----------|----:|----:|----:|
| Timisoara | 0   | 416 | 416 |
| Arad      | 118 | 421 | 539 |
| Sibiu     | 258 | 302 | 560 |
| Rimnicu Vilcea | 338 | 278 | 616 |
| Pitesti   | 435 | 204 | 639 |
| Bucharest | 536 | 160 | 696 |
| Urziceni  | 621 | 108 | 729 |
| Vaslui    | 763 | 0   | 763 |

**Análisis**

Desde el principio toman caminos distintos hasta coicidir en Pitesti. Greedy decide en un prinicipio por Lugoj ya que tiene un costo estimado menor que Arad y contínua usando ese criterio basandose únicamente en h. En cambio cuando A* llega a Mehadia después de Lugoj se da cuenta de que el costo acumulado ya es de 111+70=181 y decide explorar Arad ya que el costo es menor: 118; luego explora primero Zerid, pero eventualmente descartará esa rama ya que termina siendo más costoso que ir directo a Sibiu. Eventualmente hará lo mismo con la rama original que sale de Lugoj y la que nace de Sibiu a Fagaras, optando por las alternativas menos costosas. Explora más, y por consiguiente tarda más y consume más memoria, pero garantiza el menor costo en km.



