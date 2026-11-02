import unicodedata
import re
import pandas as pd

from src.graph.contribution_functions import qualitative_contribution, interval_contribution, jaccard_index, \
    set_contribution
from src.graph.genre_utils import get_macrogenres_for_set


# Establish data types to attributes
def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Remove accents
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Clean extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

def genres_to_set(value):
    if pd.isna(value) or value == "":
        return set()

    genre_list = value.split(',')
    genres = set()

    for genre in genre_list:
        clean_text = genre.strip().lower()
        if clean_text != "":
            genres.add(clean_text)

    return genres

# Import data
def etl_data():
    df = pd.read_csv("../data/output/artists.csv")

    df["artist_name"] = df["artist_name"].apply(normalize_text)
    df['genres'] = df['genres'].apply(genres_to_set)
    df['min_date'] = df['min_date'].astype(int)
    df['max_date'] = df['max_date'].astype(int)
    df['min_golden_date'] = df['min_golden_date'].fillna(0).astype(int)
    df['max_golden_date'] = df['max_golden_date'].fillna(0).astype(int)

    return df

# Establish edges
    ## Edges are established if the similarity between two artists is higher than a threshold
    ## The edge label shows the shared genres between both artists

BRIDGE_THRESHOLD = 3.5
CONNECTION_THRESHOLD = 3.0
MIN_CONNECTION_THRESHOLD = 2.3
MIN_DEGREE = 5

class Node:
    def __init__(self, name, listeners, genres, language, min_date, color):
        self.name = name
        self.listeners = listeners
        self.genres = genres
        self.language = language
        self.min_date = min_date
        self.color = color

class Edge:
    def __init__(self, node_1, node_2, genres, value):
        self.node_1 = node_1
        self.node_2 = node_2
        self.genres = genres
        self.lambda_factor = 1
        self.weight = value

        if value < BRIDGE_THRESHOLD:
            self.color = "gray"
        else:
            self.color = "red"

def connection(node_1, node_2, threshold=BRIDGE_THRESHOLD):
    # Genre Similarity
    jaccard = jaccard_index(get_macrogenres_for_set(node_1['genres']), get_macrogenres_for_set(node_2['genres']))
    genre_similarity = set_contribution(node_1['genres'], node_2['genres'])

    with open("../data/output/genre_similarity", "a", encoding="utf-8") as file:
        file.write(str(node_1['artist_name']) + ", " + str(node_2['artist_name']) + " -> " + str(jaccard + genre_similarity) + "\n")

    # Language Similarity
    equal_language = qualitative_contribution(node_1['language'], node_2['language'])

    # Time Similarity
    time_gap = interval_contribution(node_1['min_date'], node_1['max_date'],
                                     node_2['min_date'], node_2['max_date']) * 0.2

    # Golden Time Similarity
    golden_time_gap = interval_contribution(node_1['min_golden_date'], node_1['max_golden_date'],
                                            node_2['min_golden_date'], node_2['max_golden_date']) * 0.8

    genre_score = jaccard + genre_similarity
    delta = 1 if genre_score > 0 else 0
    index_name = genre_score + delta * (equal_language + time_gap + golden_time_gap)

    with open("../data/output/index_similarity", "a", encoding="utf-8") as file:
        file.write(str(node_1['artist_name']) + ", " + str(node_2['artist_name']) + " -> " + str(round(index_name,1)) + "\n")

    if index_name < threshold:
        return None
    else:
        return Edge(node_1['artist_name'], node_2['artist_name'],
                    ','.join(node_1['genres'].intersection(node_2['genres'])), round(index_name,1))

# Assign node colors
GENRE_COLORS = {
    "pop": "#ff7eb6",
    "rock": "#ff6b6b",
    "hip-hop": "#f4a261",
    "r&b": "#9b5de5",
    "latin": "#ffb703",
    "classical": "#90be6d",
    "jazz": "#577590",
    "folk": "#43aa8b",
    "country": "#bc6c25",
    "reggae": "#2a9d8f",
    "k-pop": "#c77dff",
    "french": "#4895ef",
    "italian": "#06d6a0",
    "ambient": "#adb5bd",
    "metal": "#343a40",
    "punk": "#d00000"
}

def get_node_color(node):
    intersection = node["genres"].intersection(set(GENRE_COLORS.keys()))

    if len(intersection) == 1:
        return GENRE_COLORS[next(iter(intersection))]
    else:
        return 'gray'

def generate_graph():
    df = etl_data()
    nodes = []
    edges = []
    candidates = []
    degree = {}

    for i in range(len(df)):
        artist = df.iloc[i]
        name = artist["artist_name"]

        nodes.append(Node(
            name, artist["listeners"], artist["genres"],
            artist["language"], artist["min_date"],
            get_node_color(artist)
        ))
        degree[name] = 0

    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            edge = connection(df.iloc[i], df.iloc[j], threshold=MIN_CONNECTION_THRESHOLD)

            if edge is None:
                continue

            if edge.weight >= CONNECTION_THRESHOLD:
                edges.append(edge)
                degree[edge.node_1] += 1
                degree[edge.node_2] += 1
            else:
                candidates.append(edge)

    candidates.sort(key=lambda e: e.weight, reverse=True)

    for edge in candidates:
        if (degree[edge.node_1] < MIN_DEGREE or
                degree[edge.node_2] < MIN_DEGREE):

            edges.append(edge)
            degree[edge.node_1] += 1
            degree[edge.node_2] += 1

    return nodes, edges