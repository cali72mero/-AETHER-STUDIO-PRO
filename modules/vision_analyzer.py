# Aether Studio Pro - Precision Vision Analyzer & Reverse Prompting Studio
# 100% LOKAL: Detaillierte Bildanalyse mit Maskierungs-Ausschluss und selektiver Attribut-Filterung
import os
import re
import gc
import torch
import numpy as np
from PIL import Image

import ldm_patched.modules.model_management as model_management
from extras.interrogate import default_interrogator as blip_interrogator
from extras.wd14tagger import default_interrogator as wd14_interrogator

# Category Definition Dictionary for SDXL Tag Sorting
CATEGORIES = {
    "subject": [
        "1girl", "1boy", "1other", "2girls", "2boys", "woman", "man", "girl", "boy", "female", "male",
        "solo", "multiple girls", "multiple boys", "warrior", "knight", "queen", "king", "princess",
        "prince", "witch", "wizard", "mage", "cyborg", "robot", "cat", "dog", "dragon", "angel",
        "demon", "elf", "vampire", "samurai", "ninja", "astronaut", "soldier", "body", "athletic",
        "slender", "muscular", "mature", "teen", "fisherman", "hero", "villain", "person", "people"
    ],
    "face_hair": [
        "hair", "eyes", "face", "smile", "smiling", "lips", "eyelashes", "expression", "gaze",
        "blonde", "brunette", "black hair", "brown hair", "silver hair", "white hair", "red hair",
        "blue hair", "pink hair", "green hair", "purple hair", "long hair", "short hair", "medium hair",
        "ponytail", "twintails", "braid", "curly hair", "straight hair", "wavy hair", "blue eyes",
        "green eyes", "brown eyes", "red eyes", "amber eyes", "closed eyes", "open mouth", "blush",
        "freckles", "beard", "mustache", "pale skin", "tanned skin", "dark skin"
    ],
    "clothing": [
        "dress", "shirt", "pants", "skirt", "jacket", "coat", "boots", "shoes", "gloves", "armor",
        "plate armor", "cape", "hood", "cloak", "hat", "cap", "helmet", "crown", "tie", "suit",
        "tuxedo", "socks", "stockings", "tights", "bikini", "swimsuit", "uniform", "school uniform",
        "robe", "kimono", "jewelry", "necklace", "earrings", "belt", "leather", "corset", "sweater",
        "hoodie", "jeans", "scarf", "sleeves", "sleeveless", "strapless", "collar", "bare shoulders",
        "heels", "sandals", "trenchcoat", "vest"
    ],
    "background": [
        "background", "scenery", "outdoors", "indoors", "room", "nature", "tree", "forest", "grass",
        "flower", "flowers", "sky", "cloud", "clouds", "mountain", "mountains", "water", "sea",
        "ocean", "beach", "lake", "river", "city", "street", "building", "buildings", "architecture",
        "castle", "ruins", "room", "window", "wall", "bedroom", "night", "day", "sunset", "sunrise",
        "space", "stars", "galaxy", "rain", "snow", "fog", "cyberpunk", "futuristic", "medieval",
        "pier", "port", "harbor"
    ],
    "lighting": [
        "light", "lighting", "shadow", "shadows", "sunlight", "moonlight", "volumetric", "cinematic lighting",
        "soft lighting", "rim light", "rim lighting", "backlighting", "god rays", "neon", "glowing",
        "dramatic lighting", "ambient", "studio lighting", "lens flare", "reflection", "reflections",
        "dramatic shadows", "golden hour"
    ],
    "style": [
        "photo", "photograph", "photorealistic", "hyperrealistic", "realistic", "anime", "manga",
        "comic", "illustration", "digital art", "oil painting", "watercolor", "3d render", "octane render",
        "unreal engine", "8k", "masterpiece", "best quality", "vintage", "retro", "monochrome", "greyscale",
        "concept art"
    ],
    "camera": [
        "portrait", "close-up", "extreme close-up", "upper body", "cowboy shot", "full body", "wide shot",
        "macro", "fisheye", "looking at viewer", "looking away", "profile", "from side", "from behind",
        "from above", "from below", "dutch angle", "depth of field", "bokeh", "blurry background"
    ]
}

CATEGORY_LABELS = [
    '👤 Subjekt & Motiv',
    '💇 Haare & Gesicht',
    '👗 Kleidung & Outfit',
    '🏞️ Hintergrund & Szene',
    '💡 Licht & Atmosphäre',
    '🎨 Kunststil & Medium',
    '📐 Kamera & Perspektive'
]

CAT_LABEL_MAP = {
    '👤 Subjekt & Motiv': 'subject',
    '💇 Haare & Gesicht': 'face_hair',
    '👗 Kleidung & Outfit': 'clothing',
    '🏞️ Hintergrund & Szene': 'background',
    '💡 Licht & Atmosphäre': 'lighting',
    '🎨 Kunststil & Medium': 'style',
    '📐 Kamera & Perspektive': 'camera'
}

# Reverse map for convenience
CAT_KEY_TO_LABEL = {v: k for k, v in CAT_LABEL_MAP.items()}


def apply_mask_to_image(image_rgb: np.ndarray, mask: np.ndarray, mode: str) -> np.ndarray:
    """
    Applies user drawn brush mask to the image.
    - 'full' / 'Ganzes Bild analysieren': whole image untouched.
    - 'ignore_mask' / 'Markierten Bereich ignorieren (ausschließen)': user marked areas are blacked out.
    - 'focus_mask' / 'Nur markierten Bereich analysieren (Fokus)': areas outside mask are blacked out.
    """
    if image_rgb is None:
        return None
    
    # Check if mask exists and actually contains drawings
    if mask is None:
        return image_rgb

    if isinstance(mask, np.ndarray) and np.max(mask) < 10:
        return image_rgb

    mode_clean = str(mode).lower()
    if 'ganz' in mode_clean or mode_clean == 'full':
        return image_rgb

    processed = image_rgb.copy()
    if len(mask.shape) == 3:
        mask_2d = mask[:, :, 0]
    else:
        mask_2d = mask

    # Resize mask if shape differs from image
    if mask_2d.shape[:2] != processed.shape[:2]:
        mask_pil = Image.fromarray(mask_2d).resize((processed.shape[1], processed.shape[0]), Image.NEAREST)
        mask_2d = np.array(mask_pil)

    is_marked = mask_2d > 128

    if 'ignor' in mode_clean or mode_clean == 'ignore_mask':
        # Blank out user marked area so AI ignores it completely
        processed[is_marked] = [15, 15, 15]
    elif 'fokus' in mode_clean or 'nur' in mode_clean or mode_clean == 'focus_mask':
        # Blank out everything EXCEPT user marked area
        processed[~is_marked] = [15, 15, 15]

    return processed


def classify_tag(tag: str) -> str:
    """Classifies an extracted tag into one of the 7 semantic categories."""
    tag_clean = tag.lower().strip()
    for cat_name, kw_list in CATEGORIES.items():
        for kw in kw_list:
            if kw in tag_clean:
                return cat_name
    return "other"


def analyze_image_deep(image_input, mask_mode: str = 'Ganzes Bild analysieren'):
    """
    Deep Vision Analysis combining BLIP captioner + WD14 tagger.
    Extracts structured attributes and returns category breakdown.
    Immediately frees GPU memory.
    """
    image_rgb = None
    mask = None

    if isinstance(image_input, dict):
        image_rgb = image_input.get('image', None)
        mask = image_input.get('mask', None)
    elif isinstance(image_input, np.ndarray):
        image_rgb = image_input
    elif hasattr(image_input, '__array__'):
        image_rgb = np.array(image_input)

    if image_rgb is None:
        return {"error": "Kein Bild zum Analysieren übergeben."}

    # Step 1: Apply brush mask according to user mode
    target_img = apply_mask_to_image(image_rgb, mask, mask_mode)

    caption = ""
    try:
        # Run BLIP natural captioner
        caption = blip_interrogator(target_img)
    except Exception as e:
        print(f"[Vision Analyzer] BLIP caption error: {e}")

    wd14_tags = []
    try:
        # Run WD14 multi-tagger
        raw_tags = wd14_interrogator(target_img, threshold=0.32)
        if raw_tags:
            wd14_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
    except Exception as e:
        print(f"[Vision Analyzer] WD14 tagger error: {e}")

    # Memory cleanup: ensure VRAM is immediately purged
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # Step 2: Categorize tags into semantic groups
    categorized = {
        "subject": [],
        "face_hair": [],
        "clothing": [],
        "background": [],
        "lighting": [],
        "style": [],
        "camera": [],
        "other": []
    }

    seen_tags = set()

    for tag in wd14_tags:
        if tag.lower() in seen_tags:
            continue
        seen_tags.add(tag.lower())
        cat = classify_tag(tag)
        categorized[cat].append(tag)

    return {
        "success": True,
        "caption": caption,
        "categorized": categorized,
        "all_tags": wd14_tags
    }


def build_filtered_prompt(analysis_result: dict, selected_categories: list) -> str:
    """
    Builds a coherent, high-detail SDXL prompt containing ONLY the selected categories.
    """
    if not analysis_result or not analysis_result.get("success"):
        return ""

    if not selected_categories:
        return ""

    active_keys = []
    for item in selected_categories:
        if item in CAT_LABEL_MAP:
            active_keys.append(CAT_LABEL_MAP[item])
        elif item in CATEGORIES:
            active_keys.append(item)

    prompt_parts = []
    categorized = analysis_result.get("categorized", {})

    # If subject & full caption are active, start with BLIP caption base
    caption = analysis_result.get("caption", "")
    if 'subject' in active_keys and caption:
        prompt_parts.append(caption)

    # Order of priority for prompt composition:
    order = ['subject', 'face_hair', 'clothing', 'background', 'lighting', 'camera', 'style']

    for key in order:
        if key in active_keys and key in categorized:
            tags = categorized[key]
            if tags:
                chunk = ", ".join(tags[:6])
                if chunk and chunk not in prompt_parts:
                    prompt_parts.append(chunk)

    final_prompt = ", ".join(prompt_parts)
    # Clean redundant commas and spaces
    final_prompt = re.sub(r',\s*,', ',', final_prompt).strip(" ,")
    return final_prompt


def replace_category_in_existing_prompt(existing_prompt: str, analysis_result: dict, category_key: str) -> str:
    """
    Replaces or appends a specific category (e.g. clothing, hair) in an existing prompt.
    """
    if not analysis_result or not analysis_result.get("success"):
        return existing_prompt

    categorized = analysis_result.get("categorized", {})
    new_tags = categorized.get(category_key, [])

    if not new_tags:
        return existing_prompt

    replacement_str = ", ".join(new_tags[:6])

    if not existing_prompt or not existing_prompt.strip():
        return replacement_str

    # Attempt to remove previous keywords of this category
    cleaned_prompt = existing_prompt
    kw_list = CATEGORIES.get(category_key, [])
    for kw in kw_list:
        pattern = re.compile(rf'\b{re.escape(kw)}[^,]*[,]*', re.IGNORECASE)
        cleaned_prompt = pattern.sub('', cleaned_prompt)

    cleaned_prompt = re.sub(r',\s*,', ',', cleaned_prompt).strip(" ,")

    if cleaned_prompt:
        return f"{cleaned_prompt}, {replacement_str}"
    return replacement_str


def format_breakdown_markdown(analysis_result: dict) -> str:
    """
    Formats a user-friendly overview of detected attributes.
    """
    if not analysis_result or not analysis_result.get("success"):
        return "*(Noch keine Analyse durchgeführt oder Bild enthält keine erkannten Merkmale)*"

    lines = ["**✨ Detaillierte Erkennungsübersicht:**\n"]
    caption = analysis_result.get("caption", "")
    if caption:
        lines.append(f"• **Natürliche Beschreibung (BLIP):** *{caption}*\n")

    categorized = analysis_result.get("categorized", {})
    lines.append("| Attribut-Kategorie | Erkannte Merkmale / SDXL Tags |")
    lines.append("| :--- | :--- |")

    for label in CATEGORY_LABELS:
        key = CAT_LABEL_MAP[label]
        tags = categorized.get(key, [])
        tag_str = ", ".join(f"`{t}`" for t in tags[:7]) if tags else "—"
        lines.append(f"| **{label}** | {tag_str} |")

    other = categorized.get("other", [])
    if other:
        lines.append(f"\n*Zusätzliche Merkmale:* {', '.join(f'`{t}`' for t in other[:10])}")

    return "\n".join(lines)
