# ApuestasSeguras

Este proyecto tiene como objetivo encontrar [apuestas seguras](https://es.wikipedia.org/wiki/Surebet) comparando diferentes casas de apuestas deportivas online.

## Idea del algoritmo:
- Mediante webscrapping se obtienen las odds de [distintas casas de apuestas](#casas_de_apuestas)

- Un algoritmo diseñado por mi se encarga de enparejar los partidos de cada casa de apuestas en función de su nombre.

- Se aplica una búsqueda de [la condición matemática](#condicion_matematica) con tal de encontrar apuestas seguras.

- Para cada apuesta segura, se calcula cual es la apuesta ideal para maximizar las ganancias.

## Resultados del algoritmo
Se puede ver una demostración del proyecto en: https://aure.aurelm.repl.co/apuestasseguras/

![](visualizacion.png)

# Condición matemática de las apuestas seguras <a name="condicion_matematica"></a>

## Ejemplo 1

Supongamos que en la casa1 se paga (por euros apostado) 2.20 si gana Nadal y 1.20 si pierde nadal. Supongamos que en la casa2 se paga 1.40 si gana Nadal y 2.05 si pierde nadal.

|	            | casa1 | casa2 |
|-------------|-------|-------|
|gana Nadal   | 2.20  | 1.20  |
|pierde Nadal | 1.40  | 2.05  |

En este caso, apostamos 1 euro en la casa1 a que gana Nadal y 1 euro en la casa2 a que pierde Nadal.
- Si gana Nadal  : nuestro beneficio será de 1*2.20-2=0.2
- Si pierde Nadal: nuestro beneficio será de 1*2.05-2=0.05

## Ejemplo 2
En el siguiente caso:

|	            | casa1 | casa2 |
|-------------|-------|-------|
|gana Nadal   | 3.10  |   b   |
|pierde Nadal |   a   | 1.55  |

Apostamos 1 euro en la casa1 por Nadal y 2 euros en la casa2 por "no Nadal"
- Si gana Nadal  : 1*3.10-3=0.10
- Si pierde Nadal: 2*1.55-3=0.1

## Caso general
Consideremos la siguiente situación:

|	      	    | casa1 | casa2 |
|-------------|-------|-------|
|gana jugador1   |   B   |   b   |
|pierde jugador1 |   a   |   A   |

A,a,B,b>1

Digamos que apostamos $x>0$ euros en la casa1 por el jugador1 y $y>0$ euros en la casa2 por el jugador 2. La apuesta será segura si los beneficios netos obtenidos en cada unos de las apuestas (es decir, $x(B-1)$ y $y(A-1)$ respectivamente) superan la apuesta hecha (y perdida) en la otra casa (es decir, $y$ y $x$ respectivamente).

En otras palabras, la apuesta será segura si existen $x,y>0$ tales que

$$x(B-1)>y,\quad y(A-1)>x $$

De aquí se deduce que una condición necesaria para una apuesta segura es
$$B-1>\frac{y}{x}>\frac{1}{A-1} $$
y multiplicando por $A-1>0$ obtenemos
$$(B-1)(A-1)>1. $$

Por otro lado, la misma condición $(B-1)(A-1)-1>0$ sería suficiente para asegurar que se trata de una puesta segura. En efecto, si apuesto $1$ euro en casa1 por el jugador1 y $B-1$ euros por el jugador2 en la casa2 (por lo tanto en total he apostado $B$ euros), sucede que
- Si gana jugador1: B-B=0
- Si gana jugador2: (B-1)(A-1)-1>0


# Casas de apuestas <a name="casas_de_apuestas"></a>
_Se lleva a cabo web scraping a las webs:_

- williamhill
- betfair
- betstars
- bwin
- leovegas

# Autor ✒️<a name="autor"></a>

**Aurelio Losquiño** 
- email: aurelm95@gmail.com
- [Linkedin](https://es.linkedin.com/in/aurelio-losqui%C3%B1o-mu%C3%B1oz-b7284b204)

[//]: # (Plantilla para el readme: https://gist.github.com/Villanuevand/6386899f70346d4580c723232524d35a) 

[//]: # (Para editar el readme: https://pandao.github.io/editor.md/en.html) 



