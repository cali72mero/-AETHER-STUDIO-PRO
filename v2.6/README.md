<div align="center">

# 🌌 Aether Diffusion Studio Pro 2.6 (Beta)
### Next-Gen Autonomous Neural AI Image Synthesis • Built on Fooocus

<p align="center">
  <a href="#-english-documentation">
    <img src="https://img.shields.io/badge/Language-English%20(Default)-0284c7?style=for-the-badge&logo=googletranslate&logoColor=white" alt="English" />
  </a>
  <a href="#-deutsche-dokumentation">
    <img src="https://img.shields.io/badge/Sprache-Deutsch-10b981?style=for-the-badge&logo=googletranslate&logoColor=white" alt="Deutsch" />
  </a>
</p>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Base: Fooocus](https://img.shields.io/badge/Based%20on-Fooocus-orange.svg)](https://github.com/lllyasviel/Fooocus)
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.6-yellow.svg)](#-community-feedback--bug-reports)
[![Release: v2.6.0](https://img.shields.io/badge/Release-v2.6.0-cyan.svg)](v2.6/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-about-the-project--developer-note)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-aether-studio-pro-vs-standard-fooocus)

</div>

---

# 🇬🇧 English Documentation

## 🌌 About the Project & Developer Note

**Aether Diffusion Studio Pro** is an advanced, high-performance evolution of the popular open-source AI image generation software **Fooocus**.

> [!NOTE]
> This software is independently developed and maintained by a **single solo developer**. The software is currently in active **Beta phase (v2.6 Beta)**.

---

## 🔄 What's New from v2.5 to v2.6? (Changelog)

Below are all the features, improvements, and bug fixes introduced from the base version (v2.5.5) to the new **Version 2.6.0**:

1. **🧠 100% Local Neural AI Translator (`Helsinki-NLP/opus-mt-de-en`)**:
   - Accurately translates entire German sentences and expressions into English without any external API.
   - **Zero-VRAM Impact**: Executes on CPU, consuming **0.0 MB GPU VRAM**, and is **immediately purged** from memory (`torch.cuda.empty_cache()`) so all 6 GB VRAM remain 100% dedicated to SDXL.
2. **🪄 AI Prompt Creator & Enhancer**:
   - Automatically expands and enriches simple prompts with cinematic lighting, camera angles, and high-fidelity SDXL tags.
3. **📥 Civitai 1-Click Downloader (Beta)**:
   - Download checkpoints, LoRAs, and VAEs directly inside the WebUI via Civitai link or model ID.
   - Automatic classification and destination routing (`models/checkpoints/` or `models/loras/`) with built-in Beta safety warning.
4. **🎚️ Interactive Before / After Comparison Slider**:
   - Real-time split-screen slider widget to inspect original vs. upscaled/varied images. Includes 1-click import from Upscale/Variation and Gallery.
5. **📖 Performance Modes Documentation Accordion**:
   - In-depth UI guide explaining the trade-offs of Quality (60 steps), Speed (30 steps), Turbo (6-8 steps), Lightning (4-8 steps), Hyper-SD, and LCM.
6. **⚡ Dynamic Dual-Engine VRAM Switch**:
   - Seamlessly toggle between **🌱 Eco / Low-VRAM** and **🚀 Normal / Max Speed** modes directly in the WebUI with live status indicator.
7. **🧠 Smart RAM Offloading**:
   - Prevents CUDA Out-Of-Memory (OOM) crashes by dynamically offloading excess tensor weights into system RAM (up to 32 GB).
8. **⏱️ Instant Millisecond Stop & Pause Controls**:
   - Immediate abort and pause controls without waiting for full denoising step completion.
9. **🧬 Universal Model Directory (`models/all_models_sdxl_flux/`)**:
   - Centralized folder supporting SDXL, Turbo, SD 1.5, and Flux models with automatic scanning.
10. **📊 Hardware & VRAM Compatibility Calculator**:
    - Automatic hardware detection and predictive VRAM calculation from model names or Civitai links.
11. **🎨 3D Master & Anime Prompt Guide**:
    - Specialized prompt generator with 1-click preset injection for photorealistic 3D renders and anime scenes.
12. **💾 Quick-History & 1-Click Download**:
    - Instantly export generated images into your system Downloads folder.
13. **🛠️ Critical Bug Fixes**:
    - Resolved HuggingFace CLIP tensor mismatch on CUDA in Low-VRAM mode.
    - Resilient aspect ratio regex parser supporting `×`, `*`, and `x` delimiters.

---

## 🚀 Aether Studio Pro vs. Standard Fooocus

| Feature | Standard Fooocus | 🌌 Aether Diffusion Studio Pro 2.6 (Beta) |
| :--- | :--- | :--- |
| **🎨 User Interface** | Light standard Gradio theme | **Dark Obsidian Glassmorphism**: Cyber-dark aesthetics, glowing indicators, responsive controls, and dynamic status header |
| **⚡ VRAM Architecture** | Fixed at launch via CLI flags (`--lowvram`) | **Dynamic Dual-Engine VRAM Switch**: Seamlessly toggle between *🌱 Eco / Low-VRAM* and *🚀 Normal / Max Speed* directly inside the WebUI |
| **🧠 Memory Safety (OOM)** | Crashes with CUDA Out-Of-Memory when models exceed VRAM | **Smart RAM Offloading**: Dynamically offloads excess tensor layers to system RAM (up to 32 GB) to prevent OOM crashes |
| **⏱️ Stop & Pause Latency** | Often waits seconds until the full step completes | **Instant Millisecond Controls**: Near-zero latency abort and pause hooks built into the inner diffusion loop |
| **🌐 Neural Translation** | None | **Local MarianMT Neural Engine**: 100% offline, zero VRAM usage, instant memory purge |
| **📥 Civitai Download** | None (manual browsing and copying) | **Integrated 1-Click Downloader (Beta)** with auto-detection for Checkpoints and LoRAs |
| **🎚️ Image Comparison** | None | **Interactive Before/After Slider** for visual verification of upscales and variations |
| **🧬 Model Compatibility** | Primarily constrained to SDXL checkpoints | **Universal Model Architecture (`all_models_sdxl_flux/`)**: Centralized directory supporting SDXL, Turbo, SD 1.5, and Flux models |
| **📊 Hardware Calculator** | None | **Integrated Model & VRAM Calculator**: Predicts exact VRAM requirements and hardware compatibility from model names or Civitai links |
| **🎨 Prompt Engineering** | Basic style selection | **3D Master & Anime Prompt Guide**: Dedicated prompt builder with 1-click preset injection |
| **📖 Performance Guide** | Simple radio buttons without explanation | **Interactive Performance Accordion**: Full breakdown of Quality, Speed, Turbo, Lightning, Hyper-SD, and LCM |
| **💾 History & Quick Export** | Manual browsing in outputs directory | **Quick-History & 1-Click Download**: Instantly export generated images into your system Downloads folder |

---

## 💬 Community Feedback & Bug Reports

- 🐛 **Found a bug?** Please submit an issue on GitHub with your operating system, GPU model, and the error log.
- 💡 **Feature Requests?** Ideas for new models, styles, or tools are always welcome! As an independent developer, I will review all suggestions and do my best to incorporate them.

---

## 📜 License & Compliance (GPL-3.0)

> [!IMPORTANT]
> **Aether Diffusion Studio Pro** is built on top of **[Fooocus](https://github.com/lllyasviel/Fooocus)** (created by **lllyasviel** and maintained by **mashb1t**).
>
> In accordance with the **GNU General Public License v3.0 (GPLv3)**, this software remains 100% free and open-source. All original copyright notices and licenses are fully preserved. The original [LICENSE](LICENSE) is included without alterations.

---

## 💻 System Requirements

- **Operating System**: Linux (Arch, CachyOS, Ubuntu, Debian, Fedora, etc.) or Windows 10/11
- **GPU**: NVIDIA Graphics Card with 4 GB – 6 GB+ VRAM (e.g. RTX 3050, 2060, 3060, 40-series)
- **System Memory (RAM)**: 16 GB minimum (32 GB recommended for Smart RAM Offloading on massive checkpoints)
- **Dependencies**: Python 3.10, PyTorch 2.1+, CUDA Toolkit

---

## 🛠️ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/cali72mero/-AETHER-STUDIO-PRO.git
cd -AETHER-STUDIO-PRO
```

### 2. Launching

**Standard Mode (Full GPU Acceleration):**
```bash
./venv/bin/python entry_with_update.py
```

**Low-VRAM / Eco Mode (Recommended for 4 GB – 6 GB GPUs):**
```bash
./venv/bin/python entry_with_update.py --lowvram
# or:
./run_lowvram.sh
```

Access the studio in your browser at: `http://127.0.0.1:7865`

---
---

# 🇩🇪 Deutsche Dokumentation

## 🌌 Über das Projekt & Entwickler-Hinweis

**Aether Diffusion Studio Pro** ist eine eigenständige, hochmoderne Weiterentwicklung des beliebten Open-Source-Tools **Fooocus**.

> [!NOTE]
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der **Beta-Phase (v2.6 Beta)**.

---

## 🔄 Was wurde von Version 2.5 auf Version 2.6 geändert? (Changelog)

Hier sind alle Neuerungen, die von der alten Basisversion (v2.5.5) auf die neue **Version 2.6.0** entwickelt und hinzugefügt wurden:

1. **🧠 100% Lokaler Neuronaler KI-Übersetzer (`Helsinki-NLP/opus-mt-de-en`)**:
   - Übersetzt ganze deutsche Sätze flüssig und akkurat ins Englische – komplett ohne Cloud und ohne externe API!
   - **0 MB VRAM-Verbrauch**: Läuft auf der CPU, schont die Grafikkarte zu 100% und wird nach der Übersetzung **sofort aus dem Speicher gelöscht**.
2. **🪄 KI-Prompt-Ersteller & Magier**:
   - Erweitert einfache Stichworte automatisch mit filmischen Details, Lichtstimmungen und Qualitäts-Tags.
3. **📥 Civitai 1-Klick Downloader (Beta)**:
   - Checkpoints und LoRAs direkt über die WebUI per Civitai-Link herunterladen.
   - Automatische Erkennung des Modelltyps und Zielordners mit integrierter Beta-Sicherheitswarnung.
4. **🎚️ Interaktiver Vorher / Nachher Bildvergleichs-Slider**:
   - Neuer Reiter im Eingabebereich für direkten Vorher/Nachher-Vergleich mit stufenlosem Schieberegler.
   - 1-Klick-Übernahme aus Upscale / Variation und Galerie.
5. **📖 Interaktives Performance-Akkordeon**:
   - Detaillierte Tabelle in der UI über die Unterschiede zwischen **Quality** (60 Steps), **Speed** (30 Steps), **Turbo** (6-8 Steps), **Lightning** (4-8 Steps), **Hyper-SD** und **Extreme Speed (LCM)**.
6. **⚡ Dynamischer Dual-Engine VRAM Switch**:
   - Umschaltung zwischen **🌱 VRAM-Sparmodus (Eco / Low-VRAM)** und **🚀 Normalmodus (Max GPU-Speed)** direkt in der WebUI mit Live-Header-Statusbadge.
7. **🧠 Smart RAM Offloading**:
   - Verhindert CUDA Out-Of-Memory (OOM) Abstürze: Lagert überzählige Modellschichten automatisch in den 32 GB System-RAM aus, wenn der VRAM (z. B. 6 GB) voll ist.
8. **⏱️ Millisekunden Stop & Pause Kontrollen**:
   - Reagiert sofort und ohne Verzögerung auf den Stop- und Pause-Button, ohne den laufenden Step abzuwarten.
9. **🧬 Universeller Modell-Ordner (`models/all_models_sdxl_flux/`)**:
   - Zentraler Ordner für alle SDXL-, Turbo-, SD 1.5- und FLUX-Checkpoints mit automatischer Scanner-Erkennung.
10. **📊 Integrierter VRAM- & Hardware-Rechner**:
    - Automatische Hardware-Erkennung (GPU & RAM) und Kompatibilitätsrechner für Civitai-Modelle.
11. **🎨 3D Master & Anime Prompt Guide**:
    - Spezialisierte Prompt-Generatoren mit 1-Klick-Injektion für fotorealistische 3D-Renders und Anime-Motive.
12. **💾 Quick-History & 1-Klick Download**:
    - Generierte Bilder können sofort mit einem Klick in den System-Download-Ordner exportiert werden.
13. **🛠️ Kritische Bugfixes**:
    - HuggingFace CLIP Device-Mismatch im Low-VRAM Modus behoben (`Expected all tensors to be on the same device`).
    - Flexibler Aspect-Ratio-Parser für Formate mit `×`, `*` und `x`.

---

## 🚀 Vergleich: Standard Fooocus vs. Aether Studio Pro 2.6

| Funktion | Normales Fooocus | 🌌 Aether Diffusion Studio Pro 2.6 (Beta) |
| :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles, simples Standard-Design | **Dark Obsidian Glassmorphism**: Hochmodernes Dark-UI mit tiefem Schwarz, Neon-Akzenten und Live-Status-Header |
| **⚡ VRAM-Verwaltung** | Feste Einstellung nur über Start-Flags (`--lowvram`) | **Dual-Engine VRAM Switch**: Direkt in der WebUI zwischen *🌱 Sparmodus* und *🚀 Normalmodus* umschalten |
| **🧠 RAM-Schutz (OOM)** | Programm stürzt bei Speicherüberlauf (CUDA OOM) ab | **Smart RAM Offload**: Lagert überzählige Schichten dynamisch in den System-RAM (bis 32 GB) aus |
| **⏱️ Stop & Pause** | Braucht oft Sekunden bis zum Ende eines Denoising-Steps | **Instant Millisecond Controls**: Nahezu verzögerungsfreies Abbrechen und Pausieren direkt im Iterationszyklus |
| **🌐 KI-Übersetzung** | Keine | **Lokaler neuronaler MarianMT-Übersetzer**: 100% offline, 0 MB VRAM, sofortige Speicherentladung |
| **📥 Civitai Download** | Nicht vorhanden (alles manuell) | **Integrierter 1-Klick Downloader (Beta)** mit Auto-Erkennung für Checkpoints und LoRAs |
| **🎚️ Bild-Vergleich** | Nicht vorhanden | **Interaktiver Vorher/Nachher-Slider** zur optischen Überprüfung von Upscales und Variationen |
| **🧬 Modell-Unterstützung** | Nahezu ausschließlich auf Standard-SDXL fokussiert | **Universeller Modellordner (`all_models_sdxl_flux/`)**: Zentraler Checkpoint-Ordner für SDXL, Turbo, SD 1.5 und Flux-Modelle |
| **📊 Modell- & VRAM-Rechner** | Nicht vorhanden | **Integrierter VRAM-Checker**: Berechnet per Modellname oder Civitai-Link exakt den VRAM-Bedarf |
| **🎨 Prompting-Assistenz** | Nur generische Styles | **3D Master & Anime Prompt Guide**: Spezialisierter Generator mit 1-Klick-Injektion |
| **📖 Performance-Erklärung** | Nur Radio-Buttons ohne Erklärung | **Interaktives Erklärungs-Menü**: Detaillierte Tabelle über Quality, Speed, Turbo, Lightning, Hyper-SD, LCM |
| **💾 Bild-Verlauf & Export** | Manuelles Suchen im Ausgabeordner | **Quick-History & 1-Klick Download**: Generierte Bilder sofort in den System-Download-Ordner exportieren |

---

## 💬 Community Feedback & Fehler melden

- 🐛 **Fehler gefunden?** Bitte erstelle ein Issue auf GitHub oder melde Bugs mit einer kurzen Beschreibung deines Setups.
- 💡 **Ideen für neue Funktionen?** Schreib es gerne in das Feedback – ich werde mein Bestes tun, um sinnvolle Vorschläge in kommenden Versionen einzubauen!

---

## 📜 Lizenz & Urheberrecht (GPL-3.0 Compliance)

> [!IMPORTANT]
> **Aether Diffusion Studio Pro** basiert auf dem Open-Source-Projekt **[Fooocus](https://github.com/lllyasviel/Fooocus)** (entwickelt von **lllyasviel** und gepflegt von **mashb1t**). 
> 
> Das Projekt steht gemäß der **GNU General Public License v3.0 (GPLv3)** vollständig als freie Open-Source-Software zur Verfügung. Sämtliche Urheberrechte der ursprünglichen Entwickler von Fooocus, PyTorch, Gradio und ldm_patched bleiben vollumfänglich gewahrt. Die originale Lizenzdatei [LICENSE](LICENSE) ist unverändert enthalten.

---

## 🌟 Danksagung & Credits
- **Fooocus Core Engine**: [lllyasviel](https://github.com/lllyasviel) & [mashb1t](https://github.com/mashb1t)
- **Stable Diffusion XL**: [Stability AI](https://stability.ai)
- **ComfyUI Architecture**: [comfyanonymous](https://github.com/comfyanonymous)
- **Gradio Framework**: [Gradio Team](https://gradio.app)
