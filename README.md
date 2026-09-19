# 🌌 Aether Diffusion Studio Pro 2.6 • Next-Gen Neural AI

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Base: Fooocus](https://img.shields.io/badge/Based%20on-Fooocus-orange.svg)](https://github.com/lllyasviel/Fooocus)
[![Version: v2.6](https://img.shields.io/badge/Version-2.6.0-cyan.svg)](#features)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-purple.svg)](#ui-redesign)

**Aether Diffusion Studio Pro** ist eine hochmoderne, erweiterte Next-Gen Bildgenerierungsplattform, entwickelt auf Basis des legendären Open-Source-Projekts **Fooocus**.

Das System kombiniert die Benutzerfreundlichkeit von Fooocus mit hochentwickelten Enterprise- und Power-User-Features: **Dual-Engine VRAM Management**, **intelligentes RAM-Offloading**, **Echtzeit Stop-/Pause-Reaktionszeiten**, **integrierter Modell- & VRAM-Rechner**, **3D/Anime Master Prompter** und ein komplett neu gestaltetes **Dark Obsidian Cyber-Design**.

---

## 📜 Lizenz & Urheberrechtshinweis (Attribution & Compliance)

> [!IMPORTANT]
> **Aether Diffusion Studio Pro** basiert auf dem Open-Source-Projekt **[Fooocus](https://github.com/lllyasviel/Fooocus)**, ursprünglich entwickelt von **lllyasviel** und weitergeführt von **mashb1t**.
> 
> Gemäß den Bestimmungen der **GNU General Public License v3.0 (GPLv3)** steht auch Aether Diffusion Studio Pro vollständig unter der **GPLv3**. Alle Urheberrechte der ursprünglichen Autoren von Fooocus, PyTorch, Gradio und ComfyUI-Komponenten bleiben vollumfänglich gewahrt. Die Original-Lizenzdatei [LICENSE](LICENSE) ist unverändert im Repository enthalten.

---

## 🚀 Was kann Aether Studio Pro, was Fooocus noch nicht konnte?

| Feature | Standard Fooocus | Aether Diffusion Studio Pro 2.6 |
| :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles Standard-Gradio Design | **Dark Obsidian Glassmorphism**: High-End Cyberpunk Dark UI, leuchtende Akzente, Live-Status-Badges und kompakte Menüs |
| **⚡ VRAM-Steuerung** | Nur über Konsolen-Flags (`--lowvram`) beim Start | **Dynamischer Dual-Engine Switch**: Umschalten zwischen *VRAM-Sparmodus (Eco)* und *Max-Speed Normalmodus* direkt in der WebUI im laufenden Betrieb mit Live-Badge |
| **🧠 Speicher-Überlauf (OOM)** | CUDA Out-of-Memory Absturz bei zu großen Modellen | **Smart RAM Offloading**: Erkennt GPU-Engpässe und lagert überzählige Schichten dynamisch in den System-RAM (bis 32 GB) aus – kein Absturz mehr! |
| **⏱️ Reaktionszeit Stop/Pause** | Wartet oft mehrere Sekunden bis zum Ende des aktuellen Steps | **Instant Millisecond Controls**: Sofortiger Abbruch und unterbrechungsfreie Pause-Funktion ohne Verzögerung |
| **🧬 Modell-Unterstützung** | Fast ausschließlich auf SDXL beschränkt | **Universal Model Architecture (`models/all_models_sdxl_flux/`)**: Zentraler Ordner für SDXL, Turbo, SD 1.5 und Flux-Checkpoints mit automatischer Erkennung |
| **📊 VRAM & Hardware-Rechner** | Nicht vorhanden | **Integrierter Modell-Rechner**: Berechnet anhand von Modellname oder Civitai-Link exakt benötigten VRAM und prüft Hardware-Kompatibilität |
| **🎨 Prompting-Assistenz** | Nur generische Styles | **3D Master & Anime Prompt Guide**: Spezialisierte Prompt-Builder und 1-Klick Preset-Injektion für fotorealistische 3D-Renders und Anime |
| **📖 Performance-Erklärung** | Nur Radio-Buttons ohne Erklärung | **Interaktives Performance-Akkordeon**: Detaillierte Tabelle über Quality (60 St.), Speed (30 St.), Turbo (6 St.), Lightning (4 St.), Hyper-SD und LCM |
| **💾 Bild-Verlauf & Export** | Manuelles Suchen im Ausgabeordner | **Quick-History & 1-Klick Download**: Generierte Bilder sofort mit einem Klick in den System-Download-Ordner exportieren |
| **🛠️ Bugfixes & Stabilität** | Bekannte Tensor-Mismatches bei Low-VRAM | **Low-VRAM Fix**: HuggingFace CLIP Tensor-Mismatch auf CUDA behoben; robuster Parser für alle Bildformate (`×`, `*`, `x`) |

---

## 💻 Systemanforderungen

- **Betriebssystem**: Linux (Arch, CachyOS, Ubuntu, Debian, Fedora) / Windows 10/11
- **GPU**: NVIDIA Grafikkarte mit mindestens 4–6 GB VRAM (z. B. RTX 3050, GTX 1660, RTX 2060, RTX 3060, RTX 40-Serie)
- **RAM**: 16 GB empfohlen (32 GB für Smart RAM Offload bei sehr großen Modellen)
- **Python**: Python 3.10 mit PyTorch 2.1+ und CUDA-Unterstützung

---

## 🛠️ Schnellstart & Ausführung

### 1. Repository klonen
```bash
git clone https://github.com/cali72mero/-AETHER-STUDIO-PRO.git
cd -AETHER-STUDIO-PRO
```

### 2. Starten

**Normaler High-Speed Modus:**
```bash
./venv/bin/python entry_with_update.py
```

**Direkt im VRAM-Sparmodus (für 4GB - 6GB GPUs):**
```bash
./venv/bin/python entry_with_update.py --lowvram
# oder:
./run_lowvram.sh
```

Öffne anschließend die Web-Oberfläche in deinem Browser unter:
`http://127.0.0.1:7865`

---

## 📁 Ordner-Struktur für Modelle

- `models/checkpoints/` : Standard-Checkpoints (SDXL, SD 1.5)
- `models/all_models_sdxl_flux/` : Erweiterte Modelle, Turbo-Modelle und experimentelle Checkpoints
- `models/loras/` : LoRA-Dateien (z. B. SDXL-Offset, LCM, Lightning, Hyper-SD)
- `models/vae/` : Optionale VAE-Dateien

---

## 🌟 Danksagung & Credits
- **Fooocus Core**: [lllyasviel](https://github.com/lllyasviel) & [mashb1t](https://github.com/mashb1t)
- **SDXL**: [Stability AI](https://stability.ai)
- **ComfyUI / ldm_patched**: [comfyanonymous](https://github.com/comfyanonymous)
- **Gradio**: [Gradio Team](https://gradio.app)
