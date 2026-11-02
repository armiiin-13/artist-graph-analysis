genre_map = {
    # POP
    "pop": ["pop"],
    "dance": ["pop", "electronic"],
    "dance pop": ["pop", "electronic"],
    "dance-pop": ["pop", "electronic"],
    "electropop": ["pop", "electronic"],
    "electro-pop": ["pop", "electronic"],
    "synthpop": ["pop", "electronic"],
    "teen pop": ["pop"],
    "pop rock": ["pop", "rock"],
    "pop punk": ["pop", "rock", "punk"],
    "power pop": ["pop", "rock"],
    "alt-pop": ["pop", "alternative"],
    "art pop": ["pop", "alternative"],
    "dream pop": ["pop", "alternative"],
    "sadcore": ["alternative"],
    "gay pop": ["pop"],

    # ROCK
    "rock": ["rock"],
    "classic rock": ["rock"],
    "alternative": ["alternative"],
    "alternative rock": ["rock", "alternative"],
    "indie": ["indie", "alternative"],
    "indie rock": ["rock", "indie", "alternative"],
    "indie pop": ["pop", "indie", "alternative"],
    "hard rock": ["rock"],
    "soft rock": ["rock"],
    "glam rock": ["rock"],
    "glam metal": ["rock", "metal"],
    "hair metal": ["rock", "metal"],
    "blues rock": ["rock", "blues"],
    "folk rock": ["rock", "folk"],
    "country rock": ["rock", "country"],
    "southern rock": ["rock", "country"],
    "heartland rock": ["rock"],
    "post-grunge": ["rock", "alternative"],
    "punk": ["punk", "rock"],
    "psychedelic": ["psychedelic"],
    "psychedelic rock": ["rock", "psychedelic"],
    "britpop": ["pop", "rock", "alternative"],
    "rock and roll": ["rock"],
    "rock n roll": ["rock"],
    "rockabilly": ["rock", "country"],

    # METAL / EXPERIMENTAL
    "metal": ["metal"],
    "heavy metal": ["metal"],
    "post-metal": ["metal", "experimental"],
    "post-rock": ["rock", "experimental"],
    "post rock": ["rock", "experimental"],
    "experimental rock": ["rock", "experimental"],
    "avant-garde": ["experimental"],

    # R&B / SOUL / FUNK
    "rnb": ["r&b"],
    "r&b": ["r&b"],
    "soul": ["soul", "r&b"],
    "funk": ["funk", "r&b"],
    "funk rock": ["funk", "rock"],
    "disco": ["disco", "dance"],
    "nu-disco": ["disco", "dance", "electronic"],
    "slow jams": ["r&b"],

    # HIP-HOP / RAP
    "hip-hop": ["hip-hop"],
    "hip hop": ["hip-hop"],
    "hiphop": ["hip-hop"],
    "rap": ["hip-hop"],
    "trap": ["hip-hop"],
    "pop rap": ["hip-hop", "pop"],
    "latin rap": ["hip-hop", "latin"],
    "alternative rap": ["hip-hop", "alternative"],
    "alternative hip-hop": ["hip-hop", "alternative"],
    "crunk": ["hip-hop"],
    "grime": ["hip-hop", "electronic"],

    # LATIN
    "latin": ["latin"],
    "latin pop": ["latin", "pop"],
    "latin rock": ["latin", "rock"],
    "reggaeton": ["latin", "urban"],
    "trap latino": ["latin", "urban", "hip-hop"],
    "reggaeton colombiano": ["latin", "urban"],
    "rock en espanol": ["latin", "rock"],
    "rock en español": ["latin", "rock"],
    "flamenco": ["latin", "folk"],
    "dancehall": ["reggae", "dance"],

    # KOREAN
    "k-pop": ["pop", "korean"],
    "kpop": ["pop", "korean"],
    "k-hiphop": ["hip-hop", "korean"],
    "korean hip-hop": ["hip-hop", "korean"],
    "k-indie": ["indie", "alternative", "korean"],
    "k-rock": ["rock", "korean"],
    "k-ballad": ["ballad", "pop", "korean"],

    # FRENCH
    "french pop": ["pop", "french"],
    "french indie pop": ["pop", "indie", "alternative", "french"],
    "french jazz": ["jazz", "french"],
    "french house": ["electronic", "house", "french"],
    "french rap": ["hip-hop", "french"],
    "rap francais": ["hip-hop", "french"],
    "chanson": ["chanson", "folk"],
    "chanson francaise": ["chanson", "folk", "french"],

    # ITALIAN
    "italian pop": ["pop", "italian"],
    "italian rap": ["hip-hop", "italian"],

    # ELECTRONIC
    "electronic": ["electronic"],
    "electronica": ["electronic"],
    "electro": ["electronic"],
    "house": ["electronic", "house"],
    "techno": ["electronic", "techno"],
    "deep house": ["electronic", "house"],
    "tech house": ["electronic", "house", "techno"],
    "idm": ["electronic", "experimental"],
    "ambient": ["ambient", "electronic"],
    "ambient electronic": ["ambient", "electronic"],
    "ambient techno": ["ambient", "electronic", "techno"],
    "acid techno": ["electronic", "techno"],
    "acid": ["electronic"],
    "dubstep": ["electronic"],
    "downtempo": ["electronic", "ambient"],
    "trip-hop": ["electronic", "hip-hop"],
    "chillout": ["electronic", "ambient"],
    "chillwave": ["electronic", "ambient", "pop"],
    "lounge": ["electronic", "ambient"],
    "future bass": ["electronic"],
    "baltimore club": ["electronic", "dance"],

    # INSTRUMENTAL / CLASSICAL
    "instrumental": ["classical"],
    "classical": ["classical"],
    "contemporary classical": ["classical"],
    "modern classical": ["classical"],
    "neoclassical": ["classical"],
    "neo-classical": ["classical"],
    "post-classical": ["classical", "experimental"],
    "minimalism": ["classical", "experimental"],

    # JAZZ
    "jazz": ["jazz"],
    "vocal jazz": ["jazz"],
    "jazz hop": ["jazz", "hip-hop"],
    "instrumental hip-hop": ["instrumental", "hip-hop"],

    # AMBIENT / EXPERIMENTAL
    "atmospheric": ["ambient"],
    "drone": ["ambient", "experimental"],

    # FOLK / COUNTRY
    "folk": ["folk"],
    "country": ["country"],
    "country pop": ["country", "pop"],
    "americana": ["country", "folk"],
    "ballad": ["ballad"],

    # OTHER
    "reggae": ["reggae"],
    "oriental pop": ["pop", "traditional"],
    "traditional": ["traditional", "folk"],
    "ethnic": ["traditional", "folk"],
}

def get_macrogenres(genre):
    return genre_map[genre]

def get_macrogenres_for_set(genres):
    supergenres = set()
    for genre in genres:
        supergenres.update(set(genre_map[genre]))
    return supergenres