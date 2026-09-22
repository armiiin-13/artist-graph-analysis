import unicodedata
import re
import pandas as pd

from src.graph.genre_utils import genre_similarities_value


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
    df['start_date'] = df['start_date'].astype(int)

    return df

# Establish edges
    ## Edges are established if the similarity between two artists is higher than a threshold
    ## The edge label shows the shared genres between both artists

BRIDGE_THRESHOLD = 3
CONNECTION_THRESHOLD = 2

class Node:
    def __init__(self, name, listeners, genres, language, start_date, color):
        self.name = name
        self.listeners = listeners
        self.genres = genres
        self.language = language
        self.start_date = start_date
        self.color = color

class Edge:
    def __init__(self, node_1, node_2, genres, value):
        self.node_1 = node_1
        self.node_2 = node_2
        self.genres = genres
        self.lambda_factor = 1

        if value < BRIDGE_THRESHOLD:
            self.color = "gray"
        else:
            self.color = "red"

def connection(node_1, node_2):
    # Genre Similarity
    genre_intersection = node_1['genres'].intersection(node_2['genres'])
    genre_score = genre_similarities_value(node_1['genres'], node_2['genres'])
    value = genre_score

    with open("../data/output/genre_similarity", "a", encoding="utf-8") as file:
        file.write(str(node_1['artist_name']) + ", " + str(node_2['artist_name']) + " -> " + str(value) + "\n")

    if value != 0:
        # Language Similarity
        equal_language = node_1['language'] == node_2['language']
        value += 0.5 if equal_language else 0

        # Time Similarity
        time_gap = node_1['start_date'] - node_2['start_date']
        if abs(time_gap) <= 5:
            value += 0.5

    if value < CONNECTION_THRESHOLD:
        return None
    else:
        return Edge(node_1['artist_name'], node_2['artist_name'], ','.join(genre_intersection), value)

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

    for i in range(0,len(df)):
        node_1 = df.iloc[i]
        nodes.append(Node(node_1['artist_name'], node_1['listeners'], node_1['genres'], node_1['language'], node_1['start_date'], get_node_color(node_1)))
        for j in range(i+1,len(df)): # graph not directed
            node_2 = df.iloc[j]
            edge = connection(node_1, node_2)
            if edge:
                edges.append(edge)

    return nodes, edges