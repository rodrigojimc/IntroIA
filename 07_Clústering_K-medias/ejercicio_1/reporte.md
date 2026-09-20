### Reporte

En la corrida original se usan los centos y desviaciones siguientes:

| Centro | X | Y | Std |
|---:|---:|---:|---:|
| 1 | 0.2 | 2.3 | 0.4 |
| 2 | -1.5 | 2.3 | 0.3 |
| 3 | -2.8 | 1.8 | 0.1 |
| 4 | -2.8 | 2.8 | 0.1 |
| 5 | -2.8 | 1.3 | 0.1 |

Los cambié por:

| Centro | X | Y | Std |
|---:|---:|---:|---:|
| 1 | 0.5 | 2 | 0.2 |
| 2 | -1 | 3 | 0.3 |
| 3 | -2 | 0 | 0.5 |
| 4 | -3 | 4 | 0.3 |
| 5 | -4 | 1 | 0.4 |

Ahora se notan separados a simple vista a pesar de tener desviaciones más altas.
Como es de esperse esto impacta a las inercias:

| Versión   | k | Inertia              |
|-----------|---|-----------------------|
| Original  | 3 | 653.2167190021554     |
| Original  | 5 | 224.0743312251571     |
| Original  | 8 | 127.13141880461835    |


| Versión   | k | Inertia              |
|-----------|---|-----------------------|
| Modificado| 3 | 2105.568909464769     |
| Modificado| 5 | 495.71303482864073    |
| Modificado| 8 | 357.2322039075418     |


Aún así, tanto el codo como la silueta ya no apuntan a 4, si no 5.