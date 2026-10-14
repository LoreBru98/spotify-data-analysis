import matplotlib
matplotlib.use('TkAgg')

import sys
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from analisi import carica_dati, get_base_path


BASE_DIR = get_base_path()
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'output' / 'grafici'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class AppSpotify:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        root.title("Spotify - Analisi Traccie")
        root.geometry("400x250")

        # --- Menu Anno ---
        tk.Label(root, text="Anno:").pack(pady=(15, 2))
        anni = ['Tutti'] + sorted(df['year'].dropna().unique().astype(int).tolist())
        self.var_anno = tk.StringVar(value='Tutti')
        ttk.Combobox(root, textvariable=self.var_anno, values=anni,
                     state='readonly').pack()

        # --- Menu Genere ---
        tk.Label(root, text="Genere:").pack(pady=(15, 2))
        generi = ['Tutti'] + sorted(df['genre'].dropna().unique().tolist())
        self.var_genere = tk.StringVar(value='Tutti')
        ttk.Combobox(root, textvariable=self.var_genere, values=generi,
                     state='readonly').pack()

        # --- Bottone ---
        tk.Button(root, text="Genera grafico", command=self.genera_grafico,
                  bg='#1DB954', fg='white', padx=20, pady=8).pack(pady=25)

    def genera_grafico(self):
        anno = self.var_anno.get()
        genere = self.var_genere.get()

        df_filtrato = self.df.copy()
        titolo = "Tutte le traccie"
        if anno != 'Tutti':
            df_filtrato = df_filtrato[df_filtrato['year'] == int(anno)]
            titolo = f"Anno: {anno}"
        if genere != 'Tutti':
            df_filtrato = df_filtrato[df_filtrato['genre'] == genere]
            titolo += f" - Genere: {genere}"

        if df_filtrato.empty:
            print("Nessun dato per i filtri selezionati.")
            return

        if anno == 'Tutti':
            dati = (df_filtrato.groupby('year')['genre'].value_counts()
                    .rename('n').reset_index())
            x, hue = 'year', 'genre'
        else:
            dati = (df_filtrato.groupby('genre')['track_id'].count()
                    .rename('n').reset_index())
            x, hue = 'genre', None

        plt.figure(figsize=(10, 6))
        if hue:
            sns.barplot(data=dati, x=x, y='n', hue=hue)
        else:
            sns.barplot(data=dati, x=x, y='n')
        plt.title(f"Numero di traccie - {titolo}")
        plt.xticks(rotation=45)
        plt.tight_layout()

        nome_file = f"grafico_{anno}_{genere}.png".replace(' ', '_')
        percorso = OUTPUT_DIR / nome_file
        plt.savefig(percorso, dpi=150, bbox_inches='tight')
        print(f"Salvato: {percorso}")

        plt.show()
        plt.close()


if __name__ == '__main__':
    df = carica_dati()
    root = tk.Tk()
    AppSpotify(root, df)
    root.mainloop()