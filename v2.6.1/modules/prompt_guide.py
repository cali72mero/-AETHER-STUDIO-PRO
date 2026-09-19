"""
Prompt Guide & Templates Module for Fooocus
Provides specialized 3D CGI and Anime Masterclass prompt templates and explanations.
"""

GUIDE_TEMPLATES = {
    # --- 3D & CGI TEMPLATES ---
    "3D: Sci-Fi Cyberpunk Mecha (Octane Render)": {
        "category": "3D",
        "title": "Sci-Fi Cyberpunk Mecha",
        "description": "Hyperdetaillierter 3D-Roboter mit Octane-Render, volumetrischem Licht & Raytracing.",
        "prompt": "intricate cyberpunk mecha robot standing in a futuristic hangar, glowing cyan LED optical sensors, exposed titanium hydraulic joints, carbon fiber armor plates, cinematic rim lighting, volumetric steam dust particles, Octane Render, 8k resolution, Unreal Engine 5, ray tracing reflections, hyperrealistic CGI masterpiece",
        "negative_prompt": "flat, 2d, illustration, cartoon, low poly, noisy, blurry, painting, sketch, low quality, deformed, bad proportions",
        "styles": ["Fooocus V2", "Fooocus Sharp", "SAI 3D Model"],
        "aspect_ratio": "896*1152",
        "guidance_scale": 6.0,
        "recommended_model": "juggernautXL_v8Rundiffusion.safetensors"
    },
    "3D: Isometrisches Cozy Raum-Diorama (Blender)": {
        "category": "3D",
        "title": "Isometrisches Cozy Zimmer",
        "description": "Niedliches 3D-Diorama mit warmen Neon-Lichtern, Tilt-Shift & Blender-Render.",
        "prompt": "isometric cute cozy cyberpunk gaming bedroom, miniature cutaway room diorama, glowing purple neon signs, multi-monitor gaming desk setup, plush sofa, rainy window, soft ambient occlusion, tilt-shift photography, Blender 3D render, clay render aesthetic, volumetric lighting, highly detailed 3d asset",
        "negative_prompt": "flat, 2d, drawing, sketches, low quality, blurry, human, cropped, worst quality",
        "styles": ["Fooocus V2", "SA-Isometric 3D", "SA-Claymation"],
        "aspect_ratio": "1024*1024",
        "guidance_scale": 5.0,
        "recommended_model": "juggernautXL_v8Rundiffusion.safetensors"
    },
    "3D: Niedlicher Pixar / Disney 3D Charakter": {
        "category": "3D",
        "title": "Pixar / Disney 3D Maskottchen",
        "description": "Niedlicher 3D-Charakter mit weichem Fell, Subsurface Scattering & Studiobeleuchtung.",
        "prompt": "adorable fluffy baby dragon sitting on a mossy fantasy rock, big sparkling expressive amber eyes, detailed soft scales and fur texture, Pixar 3D animation style, Disney 3D render, subsurface scattering, soft studio key light, shallow depth of field, 8k render, octane render, cheerful wholesome expression",
        "negative_prompt": "photo, realistic human, flat, 2d, scary, ugly, low quality, deformed, creepy, bad eyes",
        "styles": ["Fooocus V2", "Fooocus Masterpiece", "SAI 3D Model"],
        "aspect_ratio": "896*1152",
        "guidance_scale": 6.0,
        "recommended_model": "juggernautXL_v8Rundiffusion.safetensors"
    },
    "3D: Luxus-Architektur & Interior (Corona Render)": {
        "category": "3D",
        "title": "Moderne 3D Luxus-Villa",
        "description": "Fotorealistische architektonische 3D-Visualisierung mit realistischen Materialien.",
        "prompt": "luxury modern brutalist concrete villa surrounded by misty pine forest, floor-to-ceiling glass windows, warm architectural interior lighting, reflection pool with water ripples, overcast twilight sky, ArchDaily photography, Corona Render, photorealistic CGI, extremely detailed materials and textures",
        "negative_prompt": "drawing, painting, blurry, deformed structure, low resolution, cartoon, 2d, oversaturated",
        "styles": ["Fooocus V2", "Fooocus Sharp", "SAI 3D Model"],
        "aspect_ratio": "1152*896",
        "guidance_scale": 5.5,
        "recommended_model": "jedpointreal_v8VAE.safetensors"
    },

    # --- ANIME & MANGA TEMPLATES ---
    "Anime: Makoto Shinkai Cinematic Landschaft (Kimi no Na wa)": {
        "category": "Anime",
        "title": "Makoto Shinkai Cinematic Anime",
        "description": "Atemberaubender Himmelseffekt, goldene Wolken, Kirschblüten & Schultheater-Atmosphäre.",
        "prompt": "masterpiece, best quality, 1girl, solo, school uniform, beautiful detailed eyes, gentle smile, wind blowing long hair, standing on a hillside overlooking a coastal Japanese town, dramatic sunset sky, gigantic cumulus clouds with radiant golden rays, falling cherry blossom petals, Makoto Shinkai aesthetic, CoMix Wave Films style, vibrant anime colors, cinematic lighting",
        "negative_prompt": "worst quality, low quality, normal quality, lowres, bad anatomy, bad hands, text, watermark, signature, blurry, deformed, 3d, photo, realistic",
        "styles": ["Fooocus V2", "SAI Anime", "Fooocus Masterpiece"],
        "aspect_ratio": "1152*896",
        "guidance_scale": 5.5,
        "recommended_model": "animagineXL40_v4Opt.safetensors"
    },
    "Anime: Ufotable Action Szene (Demon Slayer / Fate)": {
        "category": "Anime",
        "title": "Ufotable Dynamische Action",
        "description": "Intensive Magie-Effekte, leuchtende Klingen, dynamischer Kamerawinkel & High-End Anime.",
        "prompt": "masterpiece, best quality, 1boy, anime warrior leaping with dual glowing energy katanas, dynamic action combat pose, swirling fire sparks, lightning arcs, dramatic motion blur, glowing neon aura, dark stormy battlefield, ufotable anime production style, Fate Stay Night aesthetic, intensely glowing sharp eyes, cinematic low angle, epic composition",
        "negative_prompt": "worst quality, low quality, lowres, bad hands, missing fingers, extra limbs, blurry, static, dull colors",
        "styles": ["Fooocus V2", "SAI Anime", "Fooocus Sharp"],
        "aspect_ratio": "1152*896",
        "guidance_scale": 6.0,
        "recommended_model": "animagineXL40_v4Opt.safetensors"
    },
    "Anime: 3D Cel-Shaded Anime (Genshin / Honkai Style)": {
        "category": "Anime 3D",
        "title": "3D Cel-Shaded Anime Charakter",
        "description": "Moderner 3D-Anime-Look im Stil von Genshin Impact / Honkai: Star Rail mit perfekten Konturen.",
        "prompt": "masterpiece, best quality, 1girl, solo, stylized 3d anime character model, Genshin Impact aesthetic, Honkai Star Rail style, cel-shaded 3d render, elegant fantasy adventurer outfit, glowing mystical crystal staff, floating energy particles, soft rim lighting, clean outline, beautiful detailed face, anime 3d CGI render, studio background",
        "negative_prompt": "low poly, ugly face, bad hands, photo, 2d sketch, flat, worst quality, low quality, realistic skin texture",
        "styles": ["Fooocus V2", "SAI 3D Model", "SAI Anime"],
        "aspect_ratio": "896*1152",
        "guidance_scale": 6.0,
        "recommended_model": "animagineXL40_v4Opt.safetensors"
    },
    "Anime: Ästhetische Bleistift / Manga Zeichnung (AnimaPencil)": {
        "category": "Anime",
        "title": "Traditionelle Manga & Bleistift-Zeichnung",
        "description": "Feine Linienführung, detaillierte Schraffur & klassischer Manga-Illustrationsstil.",
        "prompt": "masterpiece, finest quality, traditional media, delicate pencil lineart, detailed anime girl portrait, expressive emotional eyes, soft graphite shading, monochrome manga panel, fine crosshatching, artistic textured paper background, authentic manga illustration, ink contours",
        "negative_prompt": "low quality, messy, 3d, realistic photo, color, blurry, digital gradients, bad anatomy",
        "styles": ["Fooocus V2", "MRE Manga", "Fooocus Semi Realistic"],
        "aspect_ratio": "896*1152",
        "guidance_scale": 5.0,
        "recommended_model": "animaPencilXL_v500.safetensors"
    }
}


def get_template_names() -> list[str]:
    return list(GUIDE_TEMPLATES.keys())


def load_template_data(template_name: str):
    """Returns prompt, negative_prompt, styles, aspect_ratio, guidance_scale, model for the given template."""
    tmpl = GUIDE_TEMPLATES.get(template_name)
    if not tmpl:
        return "", "", [], "1024*1024", 6.0, ""
    return (
        tmpl["prompt"],
        tmpl["negative_prompt"],
        tmpl["styles"],
        tmpl["aspect_ratio"],
        tmpl["guidance_scale"],
        tmpl["recommended_model"]
    )


GUIDE_MARKDOWN_TEXT = """
## 🎓 Masterclass: Wie du perfekte 3D- & Anime-Bilder erstellst

### 🌟 Die 4 goldenen Grundregeln für SDXL:

1. **🇬🇧 Immer auf Englisch prompten:**
   * SDXL Text-Encoder wurden mit englischen Texten trainiert.
   * ❌ *Schlecht:* `"ein mädchen am strand im bikini"`
   * ✅ *Perfekt:* `"1girl, beautiful anime girl, standing on a sunny beach, swimsuit, ocean waves, cinematic lighting"`

2. **🚫 Midjourney-Befehle weglassen:**
   * Parameter wie `--ar 2:3` oder `--stylize 250` versteht SDXL nicht und platziert sie als störende Textelemente.
   * Seitenverhältnis wählst du direkt bei **Aspect Ratios** (z. B. `896*1152` für Hochformat).
   * Die Stilisierung wird über **Guidance Scale (CFG)** geregelt (optimal: 4.0 - 6.5).

3. **💎 Das Geheimnis für echte 3D- & CGI-Bilder:**
   * **Stile aktivieren:** Wähle unter `Styles` die Option **SAI 3D Model** und **Fooocus V2** & **Fooocus Sharp**.
   * **Magische 3D-Keywords im Prompt:**
     * `Octane Render`, `Unreal Engine 5`, `ray tracing reflections`
     * `subsurface scattering` *(lässt Haut/Materialien realistisch transluzent wirken)*
     * `cinematic rim lighting`, `volumetric lighting`, `ambient occlusion`
     * `hyperrealistic 3d CGI render, 8k resolution`
   * **Negativer Prompt:** `flat, 2d, illustration, cartoon, low poly, painting, sketch`

4. **🌸 Das Geheimnis für atemberaubende Anime-Bilder:**
   * **Bestes Modell wählen:** Wähle unter `Models` **animagineXL40_v4Opt.safetensors** *(bereits installiert!)* oder **animaPencilXL_v500.safetensors**.
   * **Danbooru-Tags verwenden:**
     * `masterpiece, best quality, 1girl, solo`
     * Studios / Künstler: `Makoto Shinkai style`, `ufotable`, `Kyoto Animation`
   * **Stile aktivieren:** **SAI Anime** & **Fooocus V2**.
   * **3D-Anime (Genshin / Honkai Look):**
     * Kombiniere Tags: `stylized 3d anime character model, Genshin Impact aesthetic, cel-shaded 3d render, octane render anime`.
   * **Negativer Prompt:** `worst quality, low quality, normal quality, lowres, bad anatomy, bad hands, blurry, 3d, photo` *(bzw. für 3D-Anime 2D ausschließen)*.
"""
