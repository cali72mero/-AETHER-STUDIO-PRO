<div align="center">

# 🌌 Aether Diffusion Studio Pro 2.6.1 (Beta)
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
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.6.1-yellow.svg)](#-community-feedback--bug-reports)
[![Release: v2.6.1](https://img.shields.io/badge/Release-v2.6.1-cyan.svg)](v2.6.1/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-about-the-project--developer-note)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-aether-studio-pro-vs-standard-fooocus)

</div>

---

# 🇬🇧 English Documentation

## 🌌 About the Project & Developer Note

**Aether Diffusion Studio Pro** is an advanced, high-performance evolution of the popular open-source AI image generation software **Fooocus**.

> [!NOTE]
> This software is independently developed and maintained by a **single solo developer**. The software is currently in active **Beta phase (v2.6.1 Beta)**.

---

## 🔄 Version Evolution: Fooocus ➔ v2.5 ➔ v2.6 ➔ v2.6.1

### 🆕 What's New in v2.6.1 (Latest Patch)
1. **🧠 100% Local Neural AI Translator (`Helsinki-NLP/opus-mt-de-en`)**:
   - Upgraded from simple dictionary to a full neural translation model. Translates complete, complex German sentences fluently into English.
   - **Zero-VRAM Architecture**: Runs purely on CPU/RAM, consuming **0.0 MB GPU VRAM**, and is **instantly purged** from memory (`torch.cuda.empty_cache()`) so all 6 GB VRAM remain 100% dedicated to SDXL.
2. **🪄 AI Prompt Creator & Enhancer**:
   - Generates cinematic, highly detailed SDXL prompts automatically from translated text.
3. **📥 Civitai 1-Click Downloader (Beta)**:
   - Download checkpoints and LoRAs directly from Civitai URLs into `models/checkpoints/` or `models/loras/` with safety warning and auto-refresh.
4. **🎚️ Interactive Before / After Comparison Slider**:
   - Real-time split-screen slider widget to inspect original vs. upscaled/varied images.
5. **🌐 Bilingual Language Bar**:
   - Default English view for global GitHub audience with 1-click German toggle.

---

### 🌟 What was added in v2.6 (Major Upgrade over Fooocus v2.5)
- **Dark Obsidian Cyber-UI**: Modern cyber-dark glassmorphism redesign.
- **Dual-Engine VRAM Switch**: Dynamic toggle between *Eco/Low-VRAM* and *Normal Max Speed* directly inside the WebUI.
- **Smart RAM Offloading**: Prevents CUDA OOM crashes by dynamically sharing layers with 32 GB system RAM.
- **Instant Millisecond Controls**: Near-zero latency abort and pause hooks in the diffusion loop.
- **Universal Model Directory (`models/all_models_sdxl_flux/`)**: Auto-detection of SDXL, Turbo, and Flux checkpoints.
- **VRAM & Civitai Calculator**: Predicts hardware compatibility before loading models.
- **3D Master & Anime Prompt Guide**: Built-in 1-click preset injectors.
- **Performance Modes Guide Accordion**: Explains Quality (60), Speed (30), Turbo (6), Lightning (4), Hyper-SD, and LCM.
- **Quick-History & 1-Click Download**: Direct export to system Downloads directory.
- **Critical Bugfixes**: Low-VRAM CLIP tensor mismatch on CUDA and aspect ratio parsing with `×`, `*`, `x`.

---

## 🚀 Comparison: Standard Fooocus vs. Aether Studio Pro 2.6.1

| Feature | Standard Fooocus (v2.5) | Aether Studio Pro (v2.6) | 🌌 Aether Studio Pro (v2.6.1) |
| :--- | :--- | :--- | :--- |
| **🎨 User Interface** | Light standard theme | Dark Obsidian Cyberpunk UI | **Dark Obsidian Glassmorphism + v2.6.1 Branding** |
| **⚡ VRAM Control** | CLI flags only (`--lowvram`) | WebUI Dual-Engine Switch | **WebUI Dual-Engine Switch + Live Header Badge** |
| **🧠 Memory Safety (OOM)** | Crashes on VRAM exhaustion | Smart RAM Offload (32 GB) | **Smart RAM Offload (32 GB RAM Safe)** |
| **⏱️ Stop & Pause** | Waits for full step finish | Instant Millisecond Stop | **Instant Millisecond Stop & Pause** |
| **🌐 Neural Translation** | None | Dictionary Matrix | **Local Neural MarianMT (CPU, 0 MB VRAM, Instant Purge)** |
| **🪄 Prompt Creator** | Standard prompt expansion | Prompt Guide Presets | **AI Prompt Creator & Enricher** |
| **📥 Civitai Download** | None (manual) | None | **Integrated 1-Click Downloader (Beta)** |
| **🎚️ Image Comparison** | None | None | **Interactive Before/After Drag Slider** |
| **🧬 Model Scope** | SDXL only | SDXL, Turbo, SD1.5, Flux | **Universal Model Architecture (`all_models_sdxl_flux/`)** |

---

## 💬 Community Feedback & Bug Reports

- 🐛 **Found a bug?** Please submit an issue on GitHub with your operating system, GPU model, and error log.
- 💡 **Feature Requests?** Ideas for new models, styles, or tools are always welcome! As a solo developer, I review all feedback and implement great suggestions in upcoming patches.

---

## 📜 License & Compliance (GPL-3.0)

> [!IMPORTANT]
> **Aether Diffusion Studio Pro** is built on top of **[Fooocus](https://github.com/lllyasviel/Fooocus)** (originally created by **lllyasviel** and maintained by **mashb1t**).
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
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der **Beta-Phase (v2.6.1 Beta)**.

---

## 🔄 Versions-Entwicklung: Fooocus ➔ v2.5 ➔ v2.6 ➔ v2.6.1

### 🆕 Was ist neu in v2.6.1 (Neuestes Update)?
1. **🧠 100% Lokaler Neuronaler KI-Übersetzer (`Helsinki-NLP/opus-mt-de-en`)**:
   - Ersetzt das einfache Wörterbuch durch ein echtes neuronales KI-Übersetzungsmodell. Übersetzt ganze, freie deutsche Sätze flüssig und sinngemäß ins Englische – komplett offline und ohne externe API!
   - **0 MB VRAM-Verbrauch**: Läuft auf der CPU, verbraucht **0 MB VRAM** deiner RTX 3050 und wird direkt nach der Übersetzung **sofort restlos aus dem Speicher gelöscht** (`del model`, `torch.cuda.empty_cache()`).
2. **🪄 KI-Prompt-Ersteller & Magier**:
   - Verwandelt kurze Stichworte automatisch in cinematische, hochdetaillierte SDXL-Prompts mit passender Beleuchtung und Kameraperspektive.
3. **📥 Civitai 1-Klick Downloader (Beta)**:
   - Checkpoints und LoRAs direkt über die WebUI per Civitai-Link herunterladen mit Typ-Erkennung und rotem Beta-Sicherheitswarnkasten.
4. **🎚️ Interaktiver Vorher / Nachher Bildvergleichs-Slider**:
   - Neuer Reiter im Eingabebereich für direkten Vorher/Nachher-Vergleich mit stufenlosem Schieberegler.
5. **🌐 Zweisprachige Readme-Button-Bar**:
   - Englisch als weltweiter Standard mit 1-Klick-Umschalter auf Deutsch.

---

### 🌟 Was wurde in v2.6 gegenüber der Fooocus-Basis hinzugefügt?
- **Dark Obsidian Cyber-UI**: Modernes Cyberpunk-Design mit Glassmorphism und Status-Header.
- **Dual-Engine VRAM Switch**: Direktes Umschalten zwischen *🌱 Sparmodus* und *🚀 Normalmodus* in der WebUI.
- **Smart RAM Offloading**: Auslagern in 32 GB RAM schützt vor CUDA Out-Of-Memory Abstürzen.
- **Millisekunden Stop & Pause**: Sofortiges Abbrechen und Pausieren ohne Wartezeit.
- **Universeller Modellordner (`models/all_models_sdxl_flux/`)**: Zentraler Ordner für alle Modell-Arten.
- **VRAM- & Hardware-Rechner**: Prüft Hardware-Tauglichkeit für RTX 3050.
- **3D Master & Anime Prompt Guide**: Spezialisierte Prompt-Generatoren.
- **Interaktives Performance-Akkordeon**: Detaillierte Tabelle über Quality, Speed, Turbo, Lightning, Hyper-SD, LCM.
- **Quick-History & 1-Klick Download**: Direkt-Export in den Download-Ordner.
- **Bugfixes**: Low-VRAM CLIP Tensor Mismatch & robuster Aspect Ratio Parser (`×`, `*`, `x`).

---

## 🚀 Der Unterschied: Original Fooocus vs. v2.5 vs. v2.6 vs. v2.6.1

| Funktion | Original Fooocus (v2.5) | Aether Studio Pro (v2.6) | 🌌 Aether Studio Pro (v2.6.1) |
| :--- | :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles Standard-Design | Dark Obsidian Cyberpunk UI | **Dark Obsidian Glassmorphism + v2.6.1 Branding** |
| **⚡ VRAM-Steuerung** | Nur beim Start (`--lowvram`) | WebUI Dual-Engine Switch | **WebUI Dual-Engine Switch + Live-Badge** |
| **🧠 RAM-Schutz (OOM)** | Stürzt bei Speicherüberlauf ab | Smart RAM Offload (32 GB) | **Smart RAM Offload (32 GB RAM Safe)** |
| **⏱️ Stop & Pause** | Wartet bis Step-Ende | Sofort-Stopp in Millisekunden | **Sofort-Stopp & Pause ohne Verzögerung** |
| **🌐 KI-Übersetzung** | Keine | Wörterbuch-Matrix | **Lokales neuronales MarianMT-Modell (CPU, 0 MB VRAM)** |
| **🪄 Prompt-Ersteller** | Nur simple Expansion | Prompt Guide Presets | **KI-Prompt-Ersteller & Detail-Anreicherung** |
| **📥 Civitai Download** | Keiner (alles manuell) | Keiner | **Integrierter 1-Klick Downloader (Beta)** |
| **🎚️ Bild-Vergleich** | Keiner | Keiner | **Interaktiver Vorher/Nachher Drag-Slider** |
| **🧬 Modell-Unterstützung** | Fast nur Standard-SDXL | SDXL, Turbo, SD1.5, Flux | **Universeller Modellordner (`all_models_sdxl_flux/`)** |

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
