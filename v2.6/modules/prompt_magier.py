# Aether Studio Pro - Prompt-Magier & Übersetzer (Deutsch -> Englisch & Quality Enhancer)
import re

# Comprehensive German to English AI Terminology Dictionary
DE_EN_DICT = {
    # Subjects & Characters
    "frau": "woman", "frauen": "women", "mann": "man", "männer": "men", "mädchen": "girl",
    "junge": "boy", "ritter": "knight", "krieger": "warrior", "kriegerin": "female warrior",
    "magier": "mage", "zauberer": "wizard", "hexe": "witch", "könig": "king", "königin": "queen",
    "prinz": "prince", "prinzessin": "princess", "drache": "dragon", "roboter": "robot",
    "katze": "cat", "hund": "dog", "wolf": "wolf", "löwe": "lion", "tiger": "tiger", "adler": "eagle",
    "pferd": "horse", "fuchs": "fox", "dämon": "demon", "engel": "angel", "elf": "elf", "elfe": "female elf",
    "zwerg": "dwarf", "vampir": "vampire", "cyborg": "cyborg", "samurai": "samurai", "ninja": "ninja",
    "soldat": "soldier", "astronaut": "astronaut", "pirat": "pirate", "göttin": "goddess", "gott": "god",

    # Features & Anatomy
    "haare": "hair", "augen": "eyes", "gesicht": "face", "hände": "hands", "haut": "skin",
    "blaue augen": "blue eyes", "grüne augen": "green eyes", "braune augen": "brown eyes",
    "rote haare": "red hair", "blonde haare": "blonde hair", "schwarze haare": "black hair",
    "lange haare": "long hair", "kurze haare": "short hair", "locken": "curly hair",
    "lächelnd": "smiling", "ernst": "serious", "mutig": "brave", "wunderschön": "beautiful",
    "hübsch": "pretty", "attraktiv": "attractive", "muskulös": "muscular", "schlank": "slender",

    # Clothing & Armor
    "kleid": "dress", "rüstung": "armor", "plattenrüstung": "plate armor", "lederjacke": "leather jacket",
    "mantel": "coat", "umhang": "cape", "kapuze": "hood", "anzug": "suit", "hemd": "shirt",
    "hose": "pants", "stiefel": "boots", "krone": "crown", "helm": "helmet", "schmuck": "jewelry",
    "schwert": "sword", "schild": "shield", "bogen": "bow", "feuerwaffe": "gun", "stab": "staff",

    # Environments & Scenery
    "regen": "rain", "neonregen": "neon rain", "schnee": "snow", "sturm": "storm", "gewitter": "thunderstorm",
    "nebel": "fog", "sonnenuntergang": "sunset", "sonnenaufgang": "sunrise", "nacht": "night",
    "tag": "day", "mondlicht": "moonlight", "sonnenlicht": "sunlight", "stadt": "city",
    "cyberpunk stadt": "cyberpunk city", "mittelalterliche stadt": "medieval city", "burg": "castle",
    "schloss": "castle", "palast": "palace", "ruine": "ancient ruins", "tempel": "temple",
    "wald": "forest", "dunkler wald": "dark mystical forest", "dschungel": "jungle", "berge": "mountains",
    "ozean": "ocean", "meer": "sea", "strand": "beach", "insel": "island", "wüste": "desert",
    "weltall": "outer space", "universum": "universe", "galaxie": "galaxy", "sterne": "stars",
    "straße": "street", "himmel": "sky", "wolken": "clouds", "unterwasser": "underwater",

    # Styles & Mediums
    "fotorealistisch": "photorealistic", "foto": "photograph", "porträt": "portrait",
    "ölgemälde": "oil painting", "aquarell": "watercolor painting", "konzeptkunst": "concept art",
    "digitales gemälde": "digital painting", "3d render": "3D render, Octane Render", "anime": "anime style, makoto shinkai aesthetic",
    "manga": "manga style", "düster": "dark, moody, atmospheric", "episch": "epic, breathtaking",
    "filmisch": "cinematic", "film": "movie still", "surreal": "surrealism", "vintage": "vintage aesthetic",
    "dampfpunk": "steampunk", "cyberpunk": "cyberpunk aesthetic", "fantasie": "high fantasy",
    "sci-fi": "science fiction", "nahaufnahme": "close-up shot", "weitwinkel": "wide angle shot",

    # Quality & Lighting
    "scharf": "sharp focus", "detailliert": "intricate details", "extrem detailliert": "hyperdetailed",
    "volumetrisches licht": "volumetric lighting", "dramatisches licht": "dramatic lighting",
    "weiches licht": "soft studio lighting", "kinoreif": "cinematic lighting, film grain",
    "meisterwerk": "masterpiece, best quality", "realistisch": "hyperrealistic", "glänzend": "glossy, shimmering"
}

QUALITY_MODIFIERS = [
    "masterpiece", "best quality", "hyperrealistic", "8k resolution",
    "cinematic lighting", "intricate details", "sharp focus"
]

def translate_and_enhance_prompt(prompt: str, mode: str = "auto") -> str:
    """
    Translates German terms to English and enriches the prompt with pro SDXL modifiers.
    Modes:
    - 'auto': Translate German words & add quality enhancement tags.
    - 'enhance': Keep original text and add quality enhancement tags.
    - 'translate_only': Translate German words without extra tags.
    """
    if not prompt or not prompt.strip():
        return prompt

    cleaned = prompt.strip()

    # Step 1: Translate German terms if in 'auto' or 'translate_only'
    if mode in ("auto", "translate_only"):
        # Replace longer phrases first, then single words
        sorted_dict = sorted(DE_EN_DICT.items(), key=lambda x: len(x[0]), reverse=True)
        for de_term, en_term in sorted_dict:
            pattern = re.compile(rf'\b{re.escape(de_term)}\b', re.IGNORECASE)
            cleaned = pattern.sub(en_term, cleaned)

    # Step 2: Quality Enhancement
    if mode in ("auto", "enhance"):
        # Check existing quality keywords to prevent duplicate pollution
        lower_prompt = cleaned.lower()
        additions = []
        for mod in QUALITY_MODIFIERS:
            if mod.lower() not in lower_prompt:
                additions.append(mod)

        # Append top 4 quality modifiers
        if additions:
            selected_additions = additions[:4]
            cleaned = f"{cleaned}, {', '.join(selected_additions)}"

    return cleaned
