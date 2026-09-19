"""
Model Compatibility & VRAM Calculator for Fooocus
Analyzes Civitai URLs and model names to determine VRAM requirements
and compatibility with the user's hardware (e.g. RTX 3050 + 32GB RAM).
"""

import os
import re
import urllib.parse
import psutil
import torch


def get_hardware_specs() -> dict:
    """Detects available GPU VRAM and System RAM."""
    gpu_name = "CPU / Unbekannte GPU"
    vram_gb = 0.0
    has_cuda = torch.cuda.is_available()

    if has_cuda:
        try:
            device = torch.cuda.current_device()
            gpu_name = torch.cuda.get_device_name(device)
            vram_gb = round(torch.cuda.get_device_properties(device).total_memory / (1024 ** 3), 2)
        except Exception:
            gpu_name = "NVIDIA CUDA GPU"
            vram_gb = 6.0

    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)

    return {
        "has_cuda": has_cuda,
        "gpu_name": gpu_name,
        "vram_gb": vram_gb,
        "ram_gb": ram_gb,
        "display": f"🎮 **GPU:** `{gpu_name}` ({vram_gb} GB VRAM)  |  🧠 **System-RAM:** `{ram_gb} GB`"
    }


# Known models and architecture profiles
MODEL_DATABASE = {
    "flux_dev_fp16": {
        "name": "FLUX.1 [dev] (FP16 / Standard)",
        "arch": "FLUX.1",
        "size_gb": 23.8,
        "precision": "FP16 / BF16",
        "min_vram": 16.0,
        "rec_vram": 24.0,
        "needs_ram_offload": True,
        "description": "Black Forest Labs 12B DiT Modell im Originalzustand. Extrem hohe Qualität, benötigt sehr viel Speicher."
    },
    "flux_dev_fp8": {
        "name": "FLUX.1 [dev] (FP8 / NF4 / GGUF)",
        "arch": "FLUX.1",
        "size_gb": 11.9,
        "precision": "FP8 / NF4",
        "min_vram": 5.5,
        "rec_vram": 8.0,
        "needs_ram_offload": True,
        "description": "FLUX.1 Dev quantisiert auf 8-Bit. Perfekt für 6GB/8GB GPUs mit viel System-RAM (z.B. 32 GB RAM)."
    },
    "flux_schnell_fp8": {
        "name": "FLUX.1 [schnell] (FP8 / 4-Step Turbo)",
        "arch": "FLUX.1",
        "size_gb": 11.8,
        "precision": "FP8 / NF4",
        "min_vram": 5.5,
        "rec_vram": 8.0,
        "needs_ram_offload": True,
        "description": "Ultra-schnelles FLUX Modell (benötigt nur 4 Steps). Optimal für schnelle hochwertige Generierung."
    },
    "sdxl_standard": {
        "name": "SDXL 1.0 (Standard Checkpoint, z.B. Juggernaut XL, Animagine XL)",
        "arch": "SDXL 1.0",
        "size_gb": 6.6,
        "precision": "FP16",
        "min_vram": 5.0,
        "rec_vram": 8.0,
        "needs_ram_offload": False,
        "description": "Standard SDXL Modell für 1024x1024 Auflösung. Voll kompatibel mit allen Fooocus-Funktionen."
    },
    "sdxl_turbo": {
        "name": "SDXL Turbo / Lightning / Hyper-SD",
        "arch": "SDXL Turbo",
        "size_gb": 6.6,
        "precision": "FP16 / FP8",
        "min_vram": 4.5,
        "rec_vram": 6.0,
        "needs_ram_offload": False,
        "description": "Schnelle SDXL Destillierung (4 bis 8 Sampling-Steps). Hohe Qualität in wenigen Sekunden."
    },
    "sd15": {
        "name": "Stable Diffusion 1.5 (z.B. Realistic Vision, DreamShaper 1.5)",
        "arch": "SD 1.5",
        "size_gb": 2.1,
        "precision": "FP16",
        "min_vram": 3.0,
        "rec_vram": 4.0,
        "needs_ram_offload": False,
        "description": "Klassisches 512x512 Modell. Extrem ressourcenschonend und rasant schnell."
    },
    "pony_v6": {
        "name": "Pony Diffusion V6 XL",
        "arch": "SDXL 1.0 (Pony)",
        "size_gb": 6.7,
        "precision": "FP16",
        "min_vram": 5.0,
        "rec_vram": 8.0,
        "needs_ram_offload": False,
        "description": "Spezialisiertes SDXL Anime/Cartoon Modell basierend auf Danbooru/Score Tags."
    }
}


def parse_query_or_url(input_str: str) -> dict:
    """Extracts model metadata and matches model architecture."""
    input_str = input_str.strip()
    slug = ""
    model_id = ""

    # Check Civitai URL
    civitai_match = re.search(r'civitai\.com/models/(\d+)(?:/([^/?#]+))?', input_str)
    if civitai_match:
        model_id = civitai_match.group(1)
        slug = civitai_match.group(2) or ""

    # Check Hugging Face URL
    hf_match = re.search(r'huggingface\.co/([^/]+)/([^/?#]+)', input_str)
    if hf_match:
        slug = hf_match.group(2).lower()

    text_to_search = (slug + " " + input_str).lower().replace('-', ' ').replace('_', ' ')

    # Match architecture
    if "flux" in text_to_search:
        if "schnell" in text_to_search:
            return MODEL_DATABASE["flux_schnell_fp8"]
        if any(w in text_to_search for w in ["fp8", "nf4", "gguf", "q4", "q8", "quant"]):
            return MODEL_DATABASE["flux_dev_fp8"]
        if "fp16" in text_to_search or "dev" in text_to_search:
            return MODEL_DATABASE["flux_dev_fp16"]
        # Default Flux to FP8 as recommended
        return MODEL_DATABASE["flux_dev_fp8"]

    if "turbo" in text_to_search or "lightning" in text_to_search or "hyper" in text_to_search:
        return MODEL_DATABASE["sdxl_turbo"]

    if "pony" in text_to_search:
        return MODEL_DATABASE["pony_v6"]

    if any(w in text_to_search for w in ["1.5", "v1 5", "v1-5", "sd15", "dreamshaper 1", "realistic vision"]):
        return MODEL_DATABASE["sd15"]

    # Default to SDXL Standard
    return MODEL_DATABASE["sdxl_standard"]


def calculate_compatibility(input_str: str) -> str:
    """Calculates compatibility and returns rich markdown report."""
    if not input_str or len(input_str.strip()) < 2:
        return "*Bitte gib einen Modell-Namen oder eine Civitai-URL oben ein.*"

    specs = get_hardware_specs()
    vram = specs["vram_gb"]
    ram = specs["ram_gb"]

    profile = parse_query_or_url(input_str)

    name = profile["name"]
    arch = profile["arch"]
    size_gb = profile["size_gb"]
    precision = profile["precision"]
    min_vram = profile["min_vram"]
    rec_vram = profile["rec_vram"]
    needs_ram_offload = profile["needs_ram_offload"]

    # Calculate status
    if arch == "FLUX.1" and precision.startswith("FP16"):
        status_badge = "🔴 **Nicht empfohlen in FP16** (VRAM-Limit überschritten)"
        status_color = "#ef4444"
        verdict = f"""
> ⚠️ **Achtung:** FLUX.1 im unkomprimierten FP16-Format benötigt ca. **24 GB VRAM** und wird auf deiner RTX 3050 (5.7 GB VRAM) mit einem `Out of Memory (OOM)` Fehler abstürzen.
> 
> 💡 **Empfehlung:** Lade stattdessen die **FP8-** oder **GGUF-**Version von FLUX.1 (z. B. `flux1-dev-fp8.safetensors`). Diese läuft dank deinen **32 GB System-RAM** hervorragend!
"""
        recommended_cmd = "./run_lowvram.sh --unet-in-fp8-e4m3fn"
    elif arch == "FLUX.1":
        # FP8 / NF4 / GGUF
        if ram >= 24.0 and vram >= 5.0:
            status_badge = "🟡 **Läuft dank 32 GB System-RAM!** (Offload-Modus)"
            status_color = "#f59e0b"
            verdict = f"""
> ✅ **Kompatibel:** Dieses FLUX.1 Modell ist ca. **{size_gb} GB** groß. Da deine RTX 3050 {vram} GB VRAM besitzt, nutzt das System automatisches **VRAM-Offloading** in deinen riesigen **{ram} GB Arbeitsspeicher**.
> 
> ⏱️ **Geschwindigkeit:** Ca. 30 bis 60 Sekunden pro Bild.
"""
            recommended_cmd = "./run_lowvram.sh --unet-in-fp8-e4m3fn"
        else:
            status_badge = "🔴 **Arbeitsspeicher knapp**"
            status_color = "#ef4444"
            verdict = "> Mindestens 24 GB System-RAM erforderlich."
            recommended_cmd = "./run_lowvram.sh"
    elif arch == "SDXL Turbo":
        status_badge = "🟢 **Optimal & rasend schnell!** (4-6 Steps)"
        status_color = "#10b981"
        verdict = f"""
> 🚀 **Hervorragend:** SDXL Turbo läuft auf deiner RTX 3050 flüssig und benötigt nur **4 bis 6 Steps**.
> 
> ⏱️ **Geschwindigkeit:** Nur ca. **4 bis 8 Sekunden** pro Bild!
"""
        recommended_cmd = "./run_lowvram.sh (Preset 'Turbo' wählen)"
    elif arch == "SD 1.5":
        status_badge = "🟢 **Läuft extrem leicht & schnell!**"
        status_color = "#10b981"
        verdict = f"""
> ⚡ **Sehr sparsam:** SD 1.5 Modelle sind nur ca. 2 GB groß und passen vollständig in deinen Grafikspeicher ({vram} GB VRAM).
> 
> ⏱️ **Geschwindigkeit:** Ca. **2 bis 5 Sekunden** pro Bild.
"""
        recommended_cmd = "./venv/bin/python launch.py"
    else:
        # Standard SDXL
        if vram >= 5.0:
            status_badge = "🟢 **Voll kompatibel mit Low-VRAM Modus**"
            status_color = "#10b981"
            verdict = f"""
> ✅ **Getestet & empfohlen:** SDXL Modelle (wie Juggernaut XL oder Animagine XL) laufen stabil auf deiner RTX 3050 im Low-VRAM Modus.
> 
> ⏱️ **Geschwindigkeit:** Ca. **18 bis 35 Sekunden** pro Bild.
"""
            recommended_cmd = "./run_lowvram.sh"
        else:
            status_badge = "🟡 **Läuft mit starker Auslagerung**"
            status_color = "#f59e0b"
            verdict = "> Low-VRAM Modus zwingend erforderlich."
            recommended_cmd = "./run_lowvram.sh --always-low-vram"

    report = f"""
### 📊 Kompatibilitäts-Ergebnis: {status_badge}

| Eigenschaft | Modell-Wert | Dein PC |
| :--- | :--- | :--- |
| **Erkanntes Modell** | **{name}** | - |
| **Architektur** | `{arch}` ({precision}) | - |
| **Dateigröße** | **ca. {size_gb} GB** | Festplatte OK |
| **VRAM Mindestbedarf** | **{min_vram} GB VRAM** | **{vram} GB VRAM** (RTX 3050) |
| **RAM Mindestbedarf** | **16 GB RAM** | **{ram} GB RAM** |

{verdict}

---

### 📂 Speicherort für dieses Modell:
Kopiere die heruntergeladene `.safetensors`-Datei in diesen neu eingerichteten Ordner:
📁 `/run/media/milo/55411029-8ea3-4451-9248-71dfd9562056/Fooocus/Fooocus/models/all_models_sdxl_flux/`

### 💻 Empfohlener Start-Befehl:
```bash
{recommended_cmd}
```
"""
    return report
