# Indra Retrieval Assignment — Versión en Español

Este proyecto es un **prototipo funcional de motor de búsqueda de productos**, inspirado en el dataset **WANDS (Wayfair)**.
Mi enfoque fue **tener un baseline que funcione end-to-end**, que se pueda entender y que alguien más pueda extenderlo sin perderse. Me encargué de:

-   Documentar las decisiones para que el código pueda crecer.
-   Explorar pequeñas mejoras que impacten directamente en **MAP@10 > 0.30**, que era el objetivo del reto.

## ¿Qué buscaba lograr?

-   ✔ Mejorar el **MAP@10** por encima de 0.30 (el baseline original estaba en ~0.29).
-   ✔ Sumar una métrica de **relevancia parcial (Graded MAP@10)**.
-   ✔ Reorganizar el código en un **formato modular/OOP**.
-   ✔ **Exponer el pipeline como un microservicio FastAPI**.
-   ✔ Dejar un flujo de evaluación reproducible por CLI.

## ¿Qué se implementó?

-   `retrieval/pipeline.py`: Pipeline principal con `.fit()` y `.search()`.
-   `vectorizers.py`: TF-IDF word y char n-grams.
-   `retriever.py`: Adaptadores para BM25 / TF-IDF.
-   `metrics/ranking.py`: MAP@10 + Graded MAP@10.
-   `service/app.py`: Microservicio FastAPI simple.
-   `evaluation/run_eval.py`: Script CLI sin notebook.

## Resultados obtenidos (WANDS Dataset)

| Modelo            | MAP@10 | Graded MAP@10 |
| ----------------- | :----: | :-----------: |
| TF-IDF (baseline) | 0.4434 |    0.5028     |
| TF-IDF char+word  | 0.4434 |    0.5028     |
| BM25              | 0.4261 |    0.4682     |

## ¿Por qué añadí Graded MAP?

El baseline original trataba todo como relevante/no relevante. Pero en e-commerce, una coincidencia parcial también puede ser útil.
Graded MAP otorga puntaje incluso si la coincidencia no es exacta, pero sí cercana (por n-grams).

## Cómo iniciar el microservicio

```
uvicorn service.app:app --reload --port 8000
```

## Cómo ejecutar la evaluación por consola

```
python -m evaluation.run_eval --products ./data/products_clean.csv --queries ./data/queries_clean.csv --model tfidf_char_word --k 10
```

## Próximos pasos sobre el reto

| Idea                                   | Motivo                               |
| -------------------------------------- | ------------------------------------ |
| ✅ Ponderar título más que descripción | Mejora rápida sin reescribir nada    |
| ✅ Usar char n-grams                   | Ayuda con consultas cortas y errores |
| 🚧 Combinar BM25 + TF-IDF              | Podría subir recall y ranking        |
| 🚧 Re-ranker con embeddings            | Rerank ligero sólo sobre top-k       |
| 🚧 Usar señales reales de usuario      | Mejor objetivo a largo plazo         |

### Notas adicionales

Preferí entregar algo **limpio y funcional** que se pueda ejecutar fácilmente, antes que un sistema complejo difícil de mantener.
