# --- Backend grafico: DEVE stare prima di importare pyplot/seaborn ---
import matplotlib
matplotlib.use('TkAgg')

import sys
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_base_path() -> Path:
    """Restituisce il percorso base sia in sviluppo che nel pacchetto .exe"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Siamo in un eseguibile PyInstaller
        return Path(sys._MEIPASS)
    else:
        # Siamo in sviluppo normale
        return Path(__file__).resolve().parent.parent


# Uso
BASE_DIR = get_base_path()
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'output' / 'grafici'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def carica_dati() -> pd.DataFrame:
    meta = pd.read_csv(DATA_DIR / 'track_metadata.csv')
    audio = pd.read_csv(DATA_DIR / 'audio_features.csv')
    panel = pd.read_csv(DATA_DIR / 'chart_longevity_panel.csv')

    df = meta.merge(audio, on='track_id', how='left') \
             .merge(panel, on='track_id', how='left')

    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year
    return df


def plot_generi_per_anno(df: pd.DataFrame) -> None:
    """Barplot: numero di canzoni per genere, separato per anno."""
    conteggio = (
        df.groupby(['year', 'genre'])
          .size()
          .reset_index(name='numero_canzoni')
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(data=conteggio, x='year', y='numero_canzoni', hue='genre')
    plt.title('Numero di canzoni per genere e anno')
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / 'generi_per_anno.png', dpi=150, bbox_inches='tight')
    print(f"Grafico salvato in: {OUTPUT_DIR / 'generi_per_anno.png'}")

    plt.show()
    plt.close()


def plot_energia_longevita(df: pd.DataFrame) -> None:
    """Scatter: energia vs settimane in classifica, colorato per genere."""
    df_clean = df.dropna(subset=['energy', 'weeks_on_top_100'])

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df_clean,
        x='energy',
        y='weeks_on_top_100',
        hue='genre',
        alpha=0.6
    )
    plt.title('Energia vs settimane in classifica')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'energia_longevita.png', dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()


if __name__ == '__main__':
    df = carica_dati()
    print("Shape:", df.shape)
    print("Colonne:", df.columns.tolist())

    plot_generi_per_anno(df)
    plot_energia_longevita(df)