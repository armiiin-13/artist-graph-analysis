# 🎵 Artist Graph

This project collects, processes and analyses music artist data in order to build a graph representing relationships between artists.

## 🌐 Data sources

The data pipeline currently uses:

- **🍎 Apple Music API**
  - Artist ID
  - Album release dates
  - Featured album release dates

- **🎧 iTunes Search API**
  - Main album genres

- **📻 Last.fm API**
  - MusicBrainz ID
  - Listener count
  - Top tags

## ⚙️ Data processing

For each artist:

1. 🔎 The artist is identified through Apple Music.
2. 📅 Album release dates are collected.
3. ✨ Featured albums are used to estimate the artist's canonical or "golden" period.
4. 🎼 iTunes album genres are collected and normalized.
5. 🏷️ Last.fm top tags are filtered using:
   - an allowed-tags list;
   - the macrogenres obtained from iTunes;
   - a tag-to-macrogenre mapping.
6. 🧩 All information is combined into a single artist record.

## 📄 Artist dataset

The processed artist data is exported to:

```text
data/output/artists.csv
```

with fields such as:

```text
id_apple
id_lastfm
artist_name
listeners
genres
min_date
max_date
min_golden_date
max_golden_date
language
```

Artists for which one of the external APIs fails are recorded separately in:

```text
data/output/errors.csv
```

## 🕸️ Graph construction

Once the artist dataset has been generated, the **Build Graph** stage constructs the base artist graph.

This graph contains the nodes, edges and attributes required by the rest of the project and acts as the common representation used by the graph libraries.

## 🎨 Graph visualization

**PyVis** is used to generate an interactive visualization of the artist graph.

It provides a visual representation of the relationships between artists and allows the network structure to be explored interactively.

## 📊 Graph analysis

**NetworkX** is used to perform graph algorithms and network analysis on the generated graph.

The resulting metrics and analysis results are exported to **CSV files** for further study.

The general workflow is therefore:

```text
APIs
  ↓
Artist data
  ↓
Filtering & processing
  ↓
artists.csv
  ↓
Build Graph
  ↓
Graph
  ├── 🎨 PyVis      → visualization
  └── 📊 NetworkX   → graph algorithms → CSV results
```

## 🔐 Environment variables

Create a `.env` file containing the required credentials:

```env
APPLE_TOKEN=...
LASTFM_API_KEY=...
```

⚠️ Do not commit `.env` or Apple private keys (`.p8`) to the repository.

## ▶️ Running

From the project environment:

```bash
python src/main.py
```

This processes the artists defined in the input file and regenerates the project data.