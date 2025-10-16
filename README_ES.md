# Indra Retrieval Assignment — Versión en Español (Junior-Friendly Tone)

Este proyecto es un prototipo de motor de búsqueda para e-commerce basado en el dataset **WANDS (Wayfair)**.
El enfoque no fue buscar el modelo más avanzado posible, sino **mejorar el baseline de forma clara y justificable**, y estructurar el código pensando en que pueda crecer en el futuro (microservicio, modularidad, posibilidad de agregar nuevos modelos).

## ¿Para qué sirve este proyecto?

Imita el comportamiento de un buscador de productos como los que existen en sitios tipo **Amazon o Wayfair**.
El usuario escribe algo como "silla azul de terciopelo" y el sistema devuelve una lista ordenada de IDs de productos que considera más relevantes.

## Objetivo del Assessment (resumido en palabras simples)

El enunciado pedía:

-   El baseline original tenía **MAP@10 = 0.29**
-   Se considera suficiente **superar 0.30**
-   Además, se solicitaba:
    -   Tener en cuenta **coincidencias parciales**, no solo exactas.
    -   Organizar el código en **clases (OOP)** para hacerlo extensible.
    -   Mostrar el motor como un **microservicio FastAPI**.
    -   Asegurar que todo pueda **reproducirse por consola**, sin depender del notebook.

## ¿Qué se implementó/mejoró?

-   ✅ Se añadió una variante de TF-IDF con **char n-grams**, que ayuda cuando el texto no coincide exactamente o hay pequeñas variaciones.
-   ✅ Se agregó una métrica extra (**Graded MAP@10**) para que los resultados similares reciban algo de crédito y no se consideren totalmente irrelevantes.
-   ✅ Se reorganizó el código en módulos separados, siguiendo principios de **código mantenible y legible**.
-   ✅ Se expuso el buscador como un **endpoint de FastAPI** para simular una API real.
-   ✅ Se creó un script CLI (`run_eval.py`) para evaluar de forma rápida sin depender del notebook.

## Resultados obtenidos

| Modelo            | MAP@10 | Graded MAP@10 |
| ----------------- | :----: | :-----------: |
| TF-IDF (baseline) | 0.4434 |    0.5028     |
| TF-IDF char+word  | 0.4434 |    0.5028     |
| BM25              | 0.4261 |    0.4682     |

✔ Como el reto pedía superar **0.30**, los resultados alcanzados **cumplen el criterio de mejora**.

## Cómo iniciar el microservicio

```
uvicorn service.app:app --reload --port 8000
```

Consulta de ejemplo:

```
curl -X POST "http://127.0.0.1:8000/search" \
 -H "Content-Type: application/json" \
 -d '{"queries": ["blue chair"], "k": 3}'
```

## Cómo ejecutar la evaluación por consola

```
python -m evaluation.run_eval --products ./data/products_clean.csv --queries ./data/queries_clean.csv --model tfidf --k 10
python -m evaluation.run_eval --products ./data/products_clean.csv --queries ./data/queries_clean.csv --model tfidf_char_word --k 10
python -m evaluation.run_eval --products ./data/products_clean.csv --queries ./data/queries_clean.csv --model bm25 --k 10
```

## Notas sobre MAP y expectativas

-   El documento oficial del reto indica que **"más de 0.30 ya demuestra una mejora válida"**.
-   Los sistemas en producción suelen estar en **0.6 - 0.9**, pero **no se esperaba llegar ahí en este ejercicio**.
-   La evaluación se enfoca más en la **forma de pensar, la limpieza del código y la capacidad de preparar algo ampliable**, no solo en la métrica final.
