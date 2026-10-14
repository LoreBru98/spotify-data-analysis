# Spotify Data Analysis (2018–2026)

Analisi dell'evoluzione dei generi musicali e delle caratteristiche audio dei successi globali su Spotify.

## Cosa fa il progetto
- Unisce 3 dataset (`track_metadata`, `audio_features`, `chart_longevity_panel`) tramite `track_id`
- Analizza l'andamento dei generi per anno
- Esplora la relazione tra feature audio (energia, danceability, valence) e longevità in classifica
- Fornisce un'interfaccia grafica (Tkinter) per filtrare i dati per anno e genere

## Tecnologie
- **Python 3.13**
- **Pandas** per la manipolazione dei dati
- **Matplotlib / Seaborn** per la visualizzazione
- **Tkinter** per la GUI
- **PyInstaller** per l'esportazione in `.exe`

## Struttura del progetto
spotify-data-analysis/
├── data/ # Dataset CSV
├── src/
│ ├── main.py # Entry point
│ ├── analisi.py # Logica di analisi e grafici
│ └── gui.py # Interfaccia Tkinter
├── requirements.txt # Dipendenze
└── README.md
