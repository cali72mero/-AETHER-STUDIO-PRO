# Aether Studio Pro - Neural KI-Übersetzer & Prompt-Ersteller
# 100% LOKAL: Übersetzt deutsche Sätze flüssig ins Englische und entlädt das Modell SOFORT aus dem Speicher!
import os
import re
import gc
import torch
import modules.default_pipeline as pipeline

# Comprehensive German to English Fallback Dictionary
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
    "fischer": "fisherman",

    # Features & Anatomy
    "haare": "hair", "augen": "eyes", "gesicht": "face", "hände": "hands", "haut": "skin",
    "blaue augen": "blue eyes", "grüne augen": "green eyes", "braune augen": "brown eyes",
    "rote haare": "red hair", "blonde haare": "blonde hair", "schwarze haare": "black hair",
    "lange haare": "long hair", "kurze haare": "short hair", "locken": "curly hair",
    "lächelnd": "smiling", "ernst": "serious", "mutig": "brave", "wunderschön": "beautiful",
    "hübsch": "pretty", "attraktiv": "attractive", "muskulös": "muscular", "schlank": "slender",
    "bärtig": "bearded",

    # Clothing & Armor
    "kleid": "dress", "rüstung": "armor", "plattenrüstung": "plate armor", "lederjacke": "leather jacket",
    "mantel": "coat", "umhang": "cape", "kapuze": "hood", "anzug": "suit", "hemd": "shirt",
    "hose": "pants", "stiefel": "boots", "krone": "crown", "helm": "helmet", "schmuck": "jewelry",
    "schwert": "sword", "schild": "shield", "bogen": "bow", "feuerwaffe": "gun", "stab": "staff",
    "netz": "net",

    # Environments & Scenery
    "regen": "rain", "neonregen": "neon rain", "schnee": "snow", "sturm": "storm", "gewitter": "thunderstorm",
    "nebel": "fog", "sonnenuntergang": "sunset", "sonnenaufgang": "sunrise", "nacht": "night",
    "tag": "day", "mondlicht": "moonlight", "sonnenlicht": "sunlight", "stadt": "city",
    "cyberpunk stadt": "cyberpunk city", "mittelalterliche stadt": "medieval city", "burg": "castle",
    "schloss": "castle", "palast": "palace", "ruine": "ancient ruins", "tempel": "temple",
    "wald": "forest", "dunkler wald": "dark mystical forest", "dschungel": "jungle", "berge": "mountains",
    "ozean": "ocean", "meer": "sea", "strand": "beach", "insel": "island", "wüste": "desert",
    "weltall": "outer space", "universum": "universe", "galaxie": "galaxy", "sterne": "stars",
    "straße": "street", "himmel": "sky", "wolken": "clouds", "unterwasser": "underwater", "hafen": "port, harbor",
    "pier": "wooden pier",

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

PROMPT_EXPANSION_KEYWORDS = [
    "masterpiece", "best quality", "photorealistic", "8k resolution",
    "cinematic lighting", "intricate details", "sharp focus", "ray tracing"
]


def dictionary_fallback_translate(text: str) -> str:
    """Fast regex/dictionary based translation fallback."""
    cleaned = text
    sorted_dict = sorted(DE_EN_DICT.items(), key=lambda x: len(x[0]), reverse=True)
    for de_term, en_term in sorted_dict:
        pattern = re.compile(rf'\b{re.escape(de_term)}\b', re.IGNORECASE)
        cleaned = pattern.sub(en_term, cleaned)
    return cleaned


def neural_translate_de_to_en(text: str) -> str:
    """
    Neural Machine Translation using Helsinki-NLP/opus-mt-de-en (100% LOCAL).
    Runs on CPU to consume 0 MB GPU VRAM and immediately purges from RAM.
    """
    if not text or not text.strip():
        return text

    try:
        from transformers import MarianMTModel, MarianTokenizer

        model_id = 'Helsinki-NLP/opus-mt-de-en'
        # Run on CPU so GPU VRAM stays 100% free for SDXL models!
        tokenizer = MarianTokenizer.from_pretrained(model_id)
        model = MarianMTModel.from_pretrained(model_id).to('cpu')

        inputs = tokenizer(text.strip(), return_tensors='pt', padding=True)
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=256)
        translated = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # STRICT CLEANUP: purge model immediately!
        del model
        del tokenizer
        del inputs
        del outputs
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return translated.strip()

    except Exception as e:
        print(f"[Aether Prompt-Magier] Neural translation fallback to dictionary: {e}")
        return dictionary_fallback_translate(text)


def expand_prompt_creative(english_prompt: str) -> str:
    """
    Uses local Fooocus GPT-2 prompt expansion engine or curated visual tags to enrich the prompt.
    """
    if not english_prompt or not english_prompt.strip():
        return english_prompt
    
    # Try using FooocusExpansion if already initialized in default_pipeline
    try:
        if pipeline.final_expansion is not None:
            expanded = pipeline.final_expansion(english_prompt, 42)
            if expanded and len(expanded) > len(english_prompt):
                return f"{english_prompt}, {expanded}"
    except Exception:
        pass

    # High-grade artistic enrichment fallback
    lower = english_prompt.lower()
    additions = [kw for kw in PROMPT_EXPANSION_KEYWORDS if kw not in lower]
    if additions:
        return f"{english_prompt}, {', '.join(additions[:4])}"
    return english_prompt


def boost_quality_english(prompt: str) -> str:
    """Adds high-quality visual and lighting tags without translation."""
    if not prompt or not prompt.strip():
        return prompt
    cleaned = prompt.strip()
    lower = cleaned.lower()
    additions = [kw for kw in PROMPT_EXPANSION_KEYWORDS[:4] if kw not in lower]
    if additions:
        return f"{cleaned.rstrip(',')}, {', '.join(additions)}"
    return cleaned


def expand_prompt_english(prompt: str) -> str:
    """Creative expansion on existing English prompt without translation."""
    if not prompt or not prompt.strip():
        return prompt
    return expand_prompt_creative(prompt.strip())


def translate_and_enhance_prompt(prompt: str, mode: str = "neural_auto") -> str:
    """
    Main entry point for translation & prompt creation.
    Modes:
    - 'neural_auto': Neural KI-Übersetzung + Qualitäts-Boost (Beleuchtung & Schärfe).
    - 'neural_expand': Neural KI-Übersetzung + KI-Prompt-Ersteller (dichtet Details dazu).
    - 'neural_translate_only': Reine neuronale KI-Übersetzung ins Englische (ohne Zusätze).
    - 'enhance_only': Behält bestehenden Text bei und fügt nur Qualitäts-Tags hinzu (ohne Übersetzung).
    - 'expand_only': Dichtet kreative Details dazu (ohne Übersetzung).
    """
    if not prompt or not prompt.strip():
        return prompt

    cleaned = prompt.strip()

    if mode == "expand_only":
        return expand_prompt_english(cleaned)
    elif mode == "enhance_only":
        return boost_quality_english(cleaned)

    # Step 1: Translation
    if mode in ("neural_auto", "neural_expand", "neural_translate_only"):
        english_text = neural_translate_de_to_en(cleaned)
    else:
        english_text = cleaned

    # Step 2: Prompt Enhancement
    if mode == "neural_expand":
        return expand_prompt_creative(english_text)
    elif mode == "neural_auto":
        return boost_quality_english(english_text)
    elif mode == "neural_translate_only":
        return english_text

    return english_text
