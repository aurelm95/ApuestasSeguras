# ApuestasSeguras

_Este proyecto tiene como objetivo encontrar [apuestas seguras](https://es.wikipedia.org/wiki/Surebet) en diferentes casas de apuestas deportivas online._

## Introducción

### Ejemplo 1

Supongamos que en la casa1 se paga (por euros apostado) 2.20 si gana Nadal y 1.20 si pierde nadal. Supongamos que en la casa2 se paga 1.40 si gana Nadal y 2.05 si pierde nadal.

|	            | casa1 | casa2 |
|-------------|-------|-------|
|gana Nadal   | 2.20  | 1.20  |
|pierde Nadal | 1.40  | 2.05  |

En este caso, apostamos 1 euro en la casa1 a que gana Nadal y 1 euro en la casa2 a que pierde Nadal.
- Si gana Nadal  : nuestro beneficio será de 1*2.20-2=0.2
- Si pierde Nadal: nuestro beneficio será de 1*2.05-2=0.05

### Ejemplo 2
En el siguiente caso:

|	            | casa1 | casa2 |
|-------------|-------|-------|
|gana Nadal   | 3.10  |   b   |
|pierde Nadal |   a   | 1.55  |

Apostamos 1 euro en la casa1 por Nadal y 2 euros en la casa2 por "no Nadal"
- Si gana Nadal  : 1*3.10-3=0.10
- Si pierde Nadal: 2*1.55-3=0.1

### Caso general
En general si la casa1 da para el jugador1 un pago de x por euro apostado

|	      	    | casa1 | casa2 |
|-------------|-------|-------|
|gana Nadal   |   B   |   b   |
|pierde Nadal |   a   |   A   |

A,a,B,b>1

Seria suficiente que A>1+1/(B-1), equivalentemente (A-1)>1/(B-1)  (B-1)>1/(A-1)  B>1+1/(A-1), ya que en este caso apostando A-1 en la casa1 y B-1 en la casa2:
Si gana Nadal: (A-1)*B+(B-1)*b-(A-1)-(B-1)>(A-1)+1+(B-1)-(A-1)-(B-1)=1
Si pierde nadal


 la casa2 deberia dar por el jugador2 y>1+1/(x-1) euros por euro apostado

De be cumplirse
Si tenemos en cuenta los Odds (ganancias-1) entonces: Si Odd1=x buscamos Odd2>1/x

### Casas de apuestas
_Se lleva a cabo web scraping a las webs:_

- williamhill
- betfair
- betstars
- bwin

## Comenzando 🚀

_Este proyecto está pensado para poder ser ejecutado directamente en [repl.it](https://repl.it/)._


### Pre-requisitos 📋

_En caso de querer ejecutarlo en tu pc debes tener instalados los modulos request y BeautifulSoup_

## Autor ✒️

* **Aurelio Losquiño**  - aurelm95@gmail.com

[//]: # (Plantilla para el readme: https://gist.github.com/Villanuevand/6386899f70346d4580c723232524d35a) 

[//]: # (Para editar el readme: https://pandao.github.io/editor.md/en.html) 



