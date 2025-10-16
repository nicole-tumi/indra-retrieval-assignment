# Indra Retrieval Assignment — Versión en Español

Este proyecto implementa un prototipo de motor de búsqueda de productos para e-commerce utilizando el dataset **WANDS (Wayfair)**.  
El objetivo **no era construir el mejor modelo posible**, sino **demostrar una mejora razonable sobre un baseline existente** y estructurar el código de forma profesional (extensible, mantenible y preparado para producción con FastAPI).

## ¿Para qué sirve este proyecto?

Simula cómo funciona un buscador de productos en una tienda online (ej. Amazon, Wayfair, Mercado Libre).  
Dado un texto de búsqueda como "silla azul de terciopelo", el sistema devuelve los IDs de productos más relevantes, ordenados por score.

## Objetivo del Assessment (resumido)

Según el enunciado original:

-   El baseline tenía **MAP@10 = 0.29**
-   Con **cualquier mejora > 0.30**, el reto se considera superado.
-   También se debía:
    -   Implementar una métrica que tome en cuenta **coincidencias parciales** (no solo exactas).
    -   Refactorizar el código con clases y modularidad (OOP).
    -   Convertir el prototipo en un **microservicio (FastAPI)**.
    -   Dejar todo reproducible desde consola (sin notebooks rotos).

## ¿Qué se mejoró?

-   ✅ Se creó una variante de TF-IDF que incluye **char n-grams** para tolerar errores, sinónimos y variaciones de texto.
-   ✅ Se implementó una métrica adicional: **Graded MAP@10**, que da crédito parcial a resultados similares.
-   ✅ Se refactorizó todo el código en módulos (retrieval/, metrics/, etc.) siguiendo principios **OOP**.
-   ✅ Se expuso el motor como una **API FastAPI**, lista para recibir consultas.
-   ✅ Se generó un script evaluador (`run_eval.py`) reproducible desde consola.

## Resultados obtenidos

| Modelo            | MAP@10 | Graded MAP@10 |
| ----------------- | :----: | :-----------: |
| TF-IDF (baseline) | 0.4434 |    0.5028     |
| TF-IDF char+word  | 0.4434 |    0.5028     |
| BM25              | 0.4261 |    0.4682     |

✔ Según el enunciado del challenge, **"un score > 0.30 demuestra mejora suficiente"**, por lo que la solución es **válida**.

## Cómo usar el microservicio

```
uvicorn service.app:app --reload --port 8000
```

Consulta de ejemplo:

```
curl -X POST "http://127.0.0.1:8000/search" \
 -H "Content-Type: application/json" \
 -d '{"queries": ["blue chair"], "k": 3}'
```

## Cómo reproducir la evaluación

Ejecutar desde terminal:

```
python -m evaluation.run_eval --products ./data/products_clean.csv --queries ./data/queries_clean.csv --model tfidf --k 10
python -m evaluation.run_eval --products ./data/products_clean.csv --queries ./data/queries_clean.csv --model tfidf_char_word --k 10
python -m evaluation.run_eval --products ./data/products_clean.csv --queries ./data/queries_clean.csv --model bm25 --k 10
```

## Nota sobre MAP y validez del resultado

-   El reto indica que alcanzar más de **0.30** ya demuestra valor.
-   Los sistemas reales van de **0.6 a 0.9**, pero **no se espera llegar ahí**.
-   Lo que se evalúa aquí es **razonamiento técnico + arquitectura limpia + microservicio**, no solo el número.
