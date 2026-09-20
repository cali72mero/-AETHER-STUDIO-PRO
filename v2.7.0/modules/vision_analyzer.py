# Aether Studio Pro - Precision Vision Analyzer & Reverse Prompting Studio
# 100% LOKAL: Detaillierte Bildanalyse mit Körperhaltung, Posen, Möbeln/Objekten, Maskierungs-Ausschluss & Filterung
import os
import re
import gc
import torch
import numpy as np
from PIL import Image

import ldm_patched.modules.model_management as model_management
from extras.interrogate import default_interrogator as blip_interrogator
from extras.wd14tagger import default_interrogator as wd14_interrogator

# Comprehensive Semantic Category Dictionaries for High-Precision SDXL Reverse Prompting
CATEGORIES = {
    "subject_pose": [
        # Subject & Count
        "1girl", "1boy", "1other", "2girls", "2boys", "woman", "man", "girl", "boy", "female", "male",
        "solo", "multiple girls", "multiple boys", "people", "person", "lady", "guy", "warrior", "knight",
        "queen", "king", "princess", "prince", "witch", "wizard", "mage", "cyborg", "robot", "cat", "dog",
        "animal", "dragon", "angel", "demon", "elf", "vampire", "samurai", "ninja", "astronaut", "soldier",
        "body", "athletic", "slender", "muscular", "mature", "teen", "hero", "villain",
        # Poses & Posture (Wie die Person sitzt, steht oder posiert)
        "sitting", "sitting on chair", "sitting on bed", "sitting on floor", "sitting on couch",
        "sitting on bench", "sitting on ground", "standing", "lying", "lying on back", "lying on stomach",
        "reclining", "kneeling", "crouching", "squatting", "leaning", "leaning back", "leaning forward",
        "crossed legs", "crossed arms", "arms crossed", "arms behind back", "hands in pockets", "hands on lap",
        "hands on hips", "hands on head", "arms up", "reaching", "holding", "walking", "running", "jumping",
        "looking at viewer", "looking away", "looking back", "profile", "head tilt", "curled up", "pose",
        "dynamic pose", "action pose", "contrapposto", "full body", "upper body", "cowboy shot"
    ],
    "face_hair": [
        "hair", "eyes", "face", "smile", "smiling", "smirk", "laughing", "lips", "parted lips", "open mouth",
        "closed eyes", "gaze", "expression", "eyelashes", "eyebrows", "blonde hair", "blonde", "brunette",
        "black hair", "brown hair", "silver hair", "white hair", "red hair", "blue hair", "pink hair",
        "green hair", "purple hair", "long hair", "short hair", "medium hair", "very long hair", "ponytail",
        "twintails", "braid", "braided hair", "curly hair", "straight hair", "wavy hair", "bob cut", "bangs",
        "messy hair", "tied hair", "hair bun", "blue eyes", "green eyes", "brown eyes", "red eyes",
        "amber eyes", "dark eyes", "slit pupils", "blush", "freckles", "pale skin", "tanned skin", "dark skin",
        "beard", "mustache", "mole", "makeup", "eyeshadow", "lipstick", "detailed face", "detailed eyes"
    ],
    "clothing": [
        "dress", "skirt", "shirt", "t-shirt", "pants", "jeans", "trousers", "jacket", "leather jacket",
        "coat", "trenchcoat", "sweater", "hoodie", "cardigan", "blouse", "top", "crop top", "boots",
        "shoes", "sneakers", "high heels", "heels", "sandals", "socks", "stockings", "thighhighs", "tights",
        "gloves", "fingerless gloves", "hat", "cap", "beret", "beanie", "scarf", "tie", "necktie", "bow",
        "bowtie", "suit", "tuxedo", "formal wear", "armor", "plate armor", "shoulder armor", "cape",
        "cloak", "hood", "belt", "corset", "vest", "swimsuit", "bikini", "one-piece swimsuit", "uniform",
        "school uniform", "maid", "maid uniform", "robe", "kimono", "yukata", "jewelry", "necklace",
        "earrings", "pendant", "bracelet", "ring", "choker", "glasses", "sunglasses", "hair ribbon",
        "hair ornament", "bare shoulders", "sleeveless", "short sleeves", "long sleeves", "cleavage",
        "collar", "lace", "leather", "denim", "silk", "cotton", "wool", "buttons", "zipper"
    ],
    "background_objects": [
        # Scenery & Environment
        "background", "simple background", "scenery", "outdoors", "indoors", "inside", "outside", "room",
        "nature", "forest", "tree", "trees", "grass", "flower", "flowers", "plants", "garden", "sky",
        "cloud", "clouds", "blue sky", "sunset", "sunrise", "night", "day", "starry sky", "space", "mountain",
        "mountains", "water", "sea", "ocean", "beach", "lake", "river", "city", "street", "cityscape",
        "building", "buildings", "architecture", "castle", "ruins", "cyberpunk", "futuristic", "medieval",
        "bedroom", "living room", "kitchen", "office", "cafe", "library", "classroom", "corridor", "hallway",
        # Furniture, Room & Props (Möbel & Gegenstände)
        "chair", "wooden chair", "armchair", "sofa", "couch", "bench", "stool", "bed", "table", "wooden table",
        "desk", "window", "large window", "wall", "floor", "wooden floor", "tiled floor", "carpet", "rug",
        "curtain", "curtains", "door", "bookshelf", "shelf", "books", "book", "lamp", "lantern", "chandelier",
        "light fixture", "pillow", "cushion", "blanket", "houseplant", "potted plant", "vase", "mirror",
        "painting", "picture frame", "clock", "cup", "coffee cup", "mug", "glass", "wine glass", "bottle",
        "plate", "food", "phone", "smartphone", "laptop", "computer", "screen", "keyboard", "papers",
        "pen", "bag", "backpack", "candle", "fireplace", "balcony", "patio", "stairs", "railing"
    ],
    "lighting": [
        "light", "lighting", "shadow", "shadows", "sunlight", "sunbeams", "sun glare", "moonlight",
        "volumetric lighting", "volumetric", "cinematic lighting", "soft lighting", "rim light", "rim lighting",
        "backlighting", "backlit", "god rays", "neon", "neon lights", "glowing", "glow", "dramatic lighting",
        "ambient light", "ambient", "studio lighting", "lens flare", "reflection", "reflections", "dramatic shadows",
        "soft shadows", "golden hour", "warm light", "cool light", "dimly lit", "brightly lit", "natural light",
        "candlelight", "firelight", "chiaroscuro"
    ],
    "style": [
        "photo", "photograph", "photorealistic", "hyperrealistic", "realistic", "raw photo", "dslr", "film",
        "film grain", "anime", "manga", "comic", "illustration", "digital art", "oil painting", "watercolor",
        "acrylic painting", "3d render", "octane render", "unreal engine", "8k", "uhd", "masterpiece",
        "best quality", "high quality", "extremely detailed", "highly detailed", "sharp", "vintage",
        "retro", "monochrome", "greyscale", "concept art", "matte painting", "cinematic", "artstation"
    ],
    "camera": [
        "portrait", "close-up", "extreme close-up", "medium shot", "upper body", "cowboy shot", "full body",
        "wide shot", "long shot", "establishing shot", "macro", "fisheye", "looking at viewer", "looking away",
        "profile", "three-quarter view", "from side", "from behind", "from above", "high angle", "from below",
        "low angle", "dutch angle", "depth of field", "dof", "bokeh", "blurry background", "blurry foreground",
        "sharp focus", "soft focus", "telephoto", "wide angle", "centered", "rule of thirds", "composition"
    ]
}

CATEGORY_LABELS = [
    '👤 Subjekt & Körperhaltung (Pose/Sitzen/Stehen)',
    '💇 Haare, Gesicht & Ausdruck',
    '👗 Kleidung, Schuhe & Accessoires',
    '🏞️ Hintergrund, Umgebung & Objekte (Möbel/Raum)',
    '💡 Licht, Schatten & Atmosphäre',
    '🎨 Kunststil & Medium',
    '📐 Kamera, Bildausschnitt & Schärfe'
]

CAT_LABEL_MAP = {
    '👤 Subjekt & Körperhaltung (Pose/Sitzen/Stehen)': 'subject_pose',
    '💇 Haare, Gesicht & Ausdruck': 'face_hair',
    '👗 Kleidung, Schuhe & Accessoires': 'clothing',
    '🏞️ Hintergrund, Umgebung & Objekte (Möbel/Raum)': 'background_objects',
    '💡 Licht, Schatten & Atmosphäre': 'lighting',
    '🎨 Kunststil & Medium': 'style',
    '📐 Kamera, Bildausschnitt & Schärfe': 'camera',
    # Legacy alias mappings for backwards compatibility
    '👤 Subjekt & Motiv': 'subject_pose',
    '💇 Haare & Gesicht': 'face_hair',
    '👗 Kleidung & Outfit': 'clothing',
    '🏞️ Hintergrund & Szene': 'background_objects',
    '💡 Licht & Atmosphäre': 'lighting'
}

CAT_KEY_TO_LABEL = {
    'subject_pose': '👤 Subjekt & Körperhaltung (Pose/Sitzen/Stehen)',
    'face_hair': '💇 Haare, Gesicht & Ausdruck',
    'clothing': '👗 Kleidung, Schuhe & Accessoires',
    'background_objects': '🏞️ Hintergrund, Umgebung & Objekte (Möbel/Raum)',
    'lighting': '💡 Licht, Schatten & Atmosphäre',
    'style': '🎨 Kunststil & Medium',
    'camera': '📐 Kamera, Bildausschnitt & Schärfe',
    'details': '✨ Erkannte Feinheiten & Details'
}


def apply_mask_to_image(image_rgb: np.ndarray, mask: np.ndarray, mode: str) -> np.ndarray:
    """
    Applies user drawn brush mask to the image.
    - 'full' / 'Ganzes Bild analysieren': whole image untouched.
    - 'ignore_mask' / 'Markierten Bereich ignorieren': user marked areas are blacked out.
    - 'focus_mask' / 'Nur markierten Bereich analysieren': areas outside mask are blacked out.
    """
    if image_rgb is None:
        return None

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

    if mask_2d.shape[:2] != processed.shape[:2]:
        mask_pil = Image.fromarray(mask_2d).resize((processed.shape[1], processed.shape[0]), Image.NEAREST)
        mask_2d = np.array(mask_pil)

    is_marked = mask_2d > 128

    if 'ignor' in mode_clean or mode_clean == 'ignore_mask':
        processed[is_marked] = [15, 15, 15]
    elif 'fokus' in mode_clean or 'nur' in mode_clean or mode_clean == 'focus_mask':
        processed[~is_marked] = [15, 15, 15]

    return processed


def classify_tag(tag: str) -> str:
    """Classifies an extracted tag into one of the semantic categories."""
    tag_clean = tag.lower().strip()
    for cat_name, kw_list in CATEGORIES.items():
        for kw in kw_list:
            if kw == tag_clean or f" {kw} " in f" {tag_clean} " or tag_clean.startswith(f"{kw} ") or tag_clean.endswith(f" {kw}"):
                return cat_name
    return "details"


def analyze_image_deep(image_input, mask_mode: str = 'Ganzes Bild analysieren'):
    """
    High-Precision Vision Analysis combining:
    1. BLIP natural language captioning (with device mismatch fixes).
    2. WD14 multi-tagger with sensitive threshold (0.20) for full posture, objects & nuances.
    Immediately purges GPU VRAM after inference.
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

    orig_h, orig_w = image_rgb.shape[:2]

    # Step 1: Apply brush mask according to user mode
    target_img = apply_mask_to_image(image_rgb, mask, mask_mode)

    # Step 2: Natural scene description via BLIP
    caption = ""
    try:
        caption = blip_interrogator(target_img)
    except Exception as e:
        print(f"[Vision Analyzer] BLIP caption warning: {e}")

    # Step 3: Granular tag extraction via WD14 (Threshold 0.20 captures postures & scene objects)
    wd14_tags = []
    try:
        raw_tags = wd14_interrogator(target_img, threshold=0.20)
        if raw_tags:
            wd14_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
    except Exception as e:
        print(f"[Vision Analyzer] WD14 tagger warning: {e}")

    # Immediate GPU/RAM purge
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # Step 4: Categorize tags into rich semantic groups
    categorized = {
        "subject_pose": [],
        "face_hair": [],
        "clothing": [],
        "background_objects": [],
        "lighting": [],
        "style": [],
        "camera": [],
        "details": []
    }

    seen_tags = set()
    for tag in wd14_tags:
        clean = tag.lower()
        if clean in seen_tags:
            continue
        seen_tags.add(clean)
        cat = classify_tag(tag)
        categorized[cat].append(tag)

    res = {
        "success": True,
        "caption": caption.strip(),
        "categorized": categorized,
        "all_tags": wd14_tags,
        "width": int(orig_w),
        "height": int(orig_h)
    }
    res["negative_prompt"] = generate_negative_prompt(res)
    return res


def generate_negative_prompt(analysis_result: dict) -> str:
    """
    Generates a tailored negative prompt according to image style, quality filters,
    and undesirable artifacts.
    """
    if not analysis_result or not analysis_result.get("success"):
        return "blurry, bad anatomy, bad hands, low quality, worst quality, distorted, extra limbs"

    categorized = analysis_result.get("categorized", {})
    style_tags = [t.lower() for t in categorized.get("style", [])]

    is_anime = any(s in style_tags for s in ["anime", "manga", "comic", "illustration", "lineart"])
    is_photo = any(s in style_tags for s in ["photo", "photograph", "photorealistic", "raw photo"]) or not is_anime

    base_neg = [
        "ugly", "deformed", "bad anatomy", "bad proportions", "bad limbs", "missing arms", "missing legs",
        "extra arms", "extra legs", "mutated hands", "extra fingers", "missing fingers", "poorly drawn hands",
        "poorly drawn face", "mutation", "blurry", "out of focus", "low resolution", "low quality",
        "worst quality", "watermark", "signature", "username", "text", "error"
    ]

    if is_photo:
        base_neg += ["cartoon", "cgi", "render", "illustration", "plastic skin", "oversaturated", "amateur photo"]
    elif is_anime:
        base_neg += ["photorealistic", "realistic", "3d render", "grayscale"]

    return ", ".join(base_neg)


def build_filtered_prompt(analysis_result: dict, selected_categories: list) -> str:
    """
    Builds a coherent, high-detail SDXL prompt containing ALL details of selected categories.
    Combines the natural sentence from BLIP with the exact conditioning tags.
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
    caption = analysis_result.get("caption", "")

    # If subject_pose is active, start with the full natural BLIP description
    if ('subject_pose' in active_keys or 'subject' in active_keys) and caption:
        prompt_parts.append(caption)

    # Order of priority for prompt composition:
    order = [
        'subject_pose',
        'face_hair',
        'clothing',
        'background_objects',
        'lighting',
        'camera',
        'style'
    ]

    for key in order:
        if key in active_keys and key in categorized:
            tags = categorized[key]
            if tags:
                # Include all recognized tags in this category (up to 16 for rich SDXL coverage)
                chunk = ", ".join(tags[:16])
                if chunk and chunk not in prompt_parts:
                    prompt_parts.append(chunk)

    # If all 7 categories are selected, also append additional detected scene details!
    if len(active_keys) >= 6 and categorized.get("details"):
        extra_details = ", ".join(categorized["details"][:10])
        if extra_details:
            prompt_parts.append(extra_details)

    final_prompt = ", ".join(prompt_parts)
    # Deduplicate and clean up spacing
    final_prompt = re.sub(r',\s*,', ',', final_prompt).strip(" ,")
    return final_prompt


def replace_category_in_existing_prompt(existing_prompt: str, analysis_result: dict, category_key: str) -> str:
    """
    Replaces or appends a specific category (e.g. clothing, hair, pose, background) in an existing prompt.
    """
    if not analysis_result or not analysis_result.get("success"):
        return existing_prompt

    # Handle alias keys
    resolved_key = CAT_LABEL_MAP.get(category_key, category_key)
    if resolved_key == 'subject':
        resolved_key = 'subject_pose'
    elif resolved_key == 'background':
        resolved_key = 'background_objects'

    categorized = analysis_result.get("categorized", {})
    new_tags = categorized.get(resolved_key, [])

    if not new_tags:
        return existing_prompt

    replacement_str = ", ".join(new_tags[:12])

    if not existing_prompt or not existing_prompt.strip():
        return replacement_str

    # Remove previous tags from this category in the prompt
    cleaned_prompt = existing_prompt
    kw_list = CATEGORIES.get(resolved_key, [])
    for kw in kw_list:
        pattern = re.compile(rf'\b{re.escape(kw)}[^,]*[,]*', re.IGNORECASE)
        cleaned_prompt = pattern.sub('', cleaned_prompt)

    cleaned_prompt = re.sub(r',\s*,', ',', cleaned_prompt).strip(" ,")

    if cleaned_prompt:
        return f"{cleaned_prompt}, {replacement_str}"
    return replacement_str


def format_breakdown_markdown(analysis_result: dict) -> str:
    """
    Formats a user-friendly overview of detected attributes and poses.
    """
    if not analysis_result or not analysis_result.get("success"):
        return "*(Noch keine Analyse durchgeführt oder Bild enthält keine erkannten Merkmale)*"

    lines = ["**✨ Detaillierte Erkennungsübersicht (100% Lokal):**\n"]
    caption = analysis_result.get("caption", "")
    if caption:
        lines.append(f"• **Natürliche Bildbeschreibung (BLIP):** *{caption}*\n")

    categorized = analysis_result.get("categorized", {})
    lines.append("| Attribut-Kategorie | Erkannte Merkmale / SDXL Tags |")
    lines.append("| :--- | :--- |")

    for label in CATEGORY_LABELS:
        key = CAT_LABEL_MAP[label]
        tags = categorized.get(key, [])
        tag_str = ", ".join(f"`{t}`" for t in tags[:10]) if tags else "—"
        lines.append(f"| **{label}** | {tag_str} |")

    details = categorized.get("details", [])
    if details:
        lines.append(f"\n*Zusätzliche Bilddetails:* {', '.join(f'`{t}`' for t in details[:12])}")

    return "\n".join(lines)
