# TintorIA

Indice completo di **Tintoria**, il podcast di Daniele Tinti e Stefano Rapone.

TintorIA raccoglie, struttura e indicizza tutte le puntate del podcast a partire dai dati pubblici del canale YouTube [@TintoriaPodcast](https://www.youtube.com/@TintoriaPodcast). L'obiettivo è rendere cercabile l'intero archivio per ospite, numero di puntata, tema e (in futuro) contenuto trascritto.

## Stato attuale

Il database contiene 234 puntate numerate (dalla #19 alla #292), 95 video extra, 231 ospiti unici e un totale di circa 94,5 milioni di visualizzazioni. Le puntate dalla #1 alla #18 e dalla #43 alla #77 non sono presenti sul canale YouTube (probabilmente rimosse o pubblicate altrove).

## Struttura del repository

```
data/
  episodes.json        — Dati strutturati: episodi, ospiti, metadati, statistiche
  episodes_raw.json    — Dump completo (tutti i campi YouTube rilevanti)
  tintoria.db          — Database SQLite con tabelle episodes, guests, transcriptions

scripts/
  scrape.py            — Scraping dei metadati dal canale YouTube (usa yt-dlp)
  build_data.py        — Elaborazione: parsing titoli, estrazione ospiti, creazione DB

app/
  index.html           — App web React autocontenuta: ricerca, ordinamento, card
```

## Come aggiornare i dati

```bash
pip install yt-dlp
python scripts/scrape.py
python scripts/build_data.py
```

## Prossimi passi

**Indicizzazione tematica** — Estrarre temi e argomenti da ogni puntata analizzando descrizioni e titoli, prima con parsing diretto, poi con l'aiuto di un LLM per generare tag semantici.

**Date di pubblicazione** — Il flat-playlist di yt-dlp non restituisce le date di upload. Servono chiamate individuali per video o l'API YouTube Data v3.

**Trascrizioni** — Trascrivere le puntate con Whisper, partendo dalle più viste, per abilitare la ricerca nel contenuto parlato.

**Ricerca semantica** — Embeddings vettoriali sulle trascrizioni per cercare concetti, non solo parole chiave.

## Top 10 puntate per views

| # | Ospite | Views |
|---|--------|-------|
| 146 | Pietro Sermonti | 2.892.320 |
| 156 | Rocco Tanica | 2.134.800 |
| 148 | Frank Matano | 1.828.706 |
| 166 | Maurizio Battista | 1.700.592 |
| 151 | Lillo | 1.469.590 |
| 139 | Valerio Lundini | 1.426.080 |
| 203 | Giancarlo Magalli | 1.404.322 |
| 226 | Giorgio Montanini | 1.399.843 |
| 136 | Massimo Ceccherini | 1.386.715 |
| 168 | Alberto Grandi | 1.386.391 |

---

Progetto di [Andrea Colamedici](https://andreacolamedici.com) / [Tlon](https://tlon.it)
