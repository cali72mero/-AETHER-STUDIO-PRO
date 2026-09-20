<div align="center">

# 🌌 Aether Diffusion Studio Pro 2.6.2 (Beta)
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
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.6.2-yellow.svg)](#-community-feedback--bug-reports)
[![Release: v2.6.2](https://img.shields.io/badge/Release-v2.6.2-cyan.svg)](v2.6.2/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-about-the-project--developer-note)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-aether-studio-pro-vs-standard-fooocus)

</div>

---

# 🇬🇧 English Documentation

## 🌌 About the Project & Developer Note

**Aether Diffusion Studio Pro** is an advanced, high-performance evolution of the popular open-source AI image generation software **Fooocus**.

> [!NOTE]
> This software is independently developed and maintained by a **single solo developer**. The software is currently in active **Beta phase (v2.6.2 Beta)**.
> 
> Because this is a continuous development process, community feedback is invaluable! If you encounter any bugs, unexpected behavior, or have ideas for exciting new features (models, workflows, UI improvements), please open an Issue on GitHub or join the discussions. I read every report and actively integrate user suggestions into new releases!

---

## 🔄 Version Evolution: Fooocus ➔ v2.5 ➔ v2.6 ➔ v2.6.1 ➔ v2.6.2

### 🆕 What's New in v2.6.2 (Current Release - Precision Vision AI Studio)
1. **🔬 Precision Vision AI Studio & Reverse Prompting (100% Local)**:
   - Deep multi-modal image comprehension combining **BLIP natural captioning** with **WD14 multi-tagger interrogation** for exact 1:1 SDXL prompt reconstruction.
   - Completely offline execution with **0 MB lingering VRAM footprint** (models run and immediately purge memory).
2. **🖌️ Interactive Brush Masking (`tool='sketch'`)**:
   - **Ganzes Bild analysieren (Full Image)**: Analyzes the complete uploaded reference picture.
   - **Markierten Bereich ignorieren (ausschließen / Exclude Mask)**: User-drawn brush strokes are blanked out so the AI completely ignores masked objects or distractions.
   - **Nur markierten Bereich analysieren (Fokus / Focus Mask)**: Blacks out the background and isolates only the marked region for targeted inspection.
3. **🎛️ Selective Attribute Filtering (7 Semantic Categories)**:
   - Structured decomposition into:
     - `👤 Subject & Person` (Subjekt/Motiv)
     - `💇 Hair & Face` (Haare/Gesicht)
     - `👗 Clothing & Outfit` (Kleidung)
     - `🏞️ Background & Scene` (Hintergrund)
     - `💡 Lighting & Atmosphere` (Beleuchtung)
     - `🎨 Art Style & Medium` (Kunststil)
     - `📐 Camera & Perspective` (Kamera)
   - **All 7 checked by default** for instant 1:1 prompt recreation.
   - Toggling checkmarks instantly re-composes the SDXL prompt without re-running heavy models.
4. **🎯 Selective Prompt Merging & Attribute Swapping**:
   - Keep your existing typed prompt intact and swap or insert *only* specific attributes from the uploaded image:
     - `👗 Nur Kleidung übertragen` (Swap only clothing)
     - `💇 Nur Haare & Gesicht übertragen` (Swap only hair/face)
     - `🏞️ Nur Hintergrund übertragen` (Swap only background)
     - `💡 Nur Licht übertragen` (Swap only lighting)
     - `🎨 Nur Stil übertragen` (Swap only art style)

---

### 🌟 What was added in v2.6.1
1. **🧠 100% Local Neural AI Translator (`Helsinki-NLP/opus-mt-de-en`)**:
   - Full German-to-English translation pipeline running on CPU/RAM with 0 MB VRAM footprint and automatic cache purge.
2. **🪄 AI Prompt Magician & Enhancer**:
   - Generates cinematic, highly detailed SDXL prompts automatically from translated concepts.
3. **📥 Civitai 1-Click Downloader (Beta)**:
   - Download checkpoints and LoRAs directly from Civitai URLs into the proper model directories with safety warning and auto-refresh.
4. **🎚️ Interactive Before / After Comparison Slider**:
   - Real-time split-screen slider widget to compare source vs. upscaled/varied images.
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

## 🚀 Comparison: Standard Fooocus vs. Aether Studio Pro

| Feature | Standard Fooocus (v2.5) | Aether Studio Pro (v2.6) | Aether Studio Pro (v2.6.1) | 🌌 Aether Studio Pro (v2.6.2) |
| :--- | :--- | :--- | :--- | :--- |
| **🎨 User Interface** | Light standard theme | Dark Obsidian Cyberpunk UI | Dark Obsidian Glassmorphism | **Dark Obsidian Glassmorphism + Live Status** |
| **⚡ VRAM Control** | CLI flags only (`--lowvram`) | WebUI Dual-Engine Switch | WebUI Dual-Engine Switch | **WebUI Dual-Engine Switch + Live Header Badge** |
| **🧠 Memory Safety (OOM)**| Crashes on VRAM exhaustion | Smart RAM Offload (32 GB) | Smart RAM Offload (32 GB RAM Safe) | **Smart RAM Offload (32 GB RAM Safe)** |
| **⏱️ Stop & Pause** | Waits for full step finish | Instant Millisecond Stop | Instant Millisecond Stop & Pause | **Instant Millisecond Stop & Pause** |
| **🔬 Vision AI Studio** | Simple describe button | Standard describe | Standard describe | **Precision Vision Studio: Brush Masking (Ignore/Focus), 7 Category Filters, Attribute Swapping** |
| **🌐 Neural Translation** | None | Dictionary Matrix | Local Neural MarianMT (0 MB VRAM) | **Local Neural MarianMT (CPU, 0 MB VRAM, Instant Purge)** |
| **🪄 Prompt Creator** | Standard prompt expansion | Prompt Guide Presets | AI Prompt Creator & Enricher | **AI Prompt Magician + Vision Prompt Builder** |
| **📥 Civitai Download** | None (manual) | None | Integrated 1-Click Downloader (Beta) | **Integrated 1-Click Downloader (Beta)** |
| **🎚️ Image Comparison** | None | None | Interactive Before/After Drag Slider | **Interactive Before/After Drag Slider** |
| **🧬 Model Scope** | SDXL only | SDXL, Turbo, SD1.5, Flux | Universal Model Architecture | **Universal Model Architecture (`all_models_sdxl_flux/`)** |

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
./venv/bin/python webui.py
```

**Low-VRAM Mode (Eco Mode for 4-6 GB GPUs):**
```bash
./run_lowvram.sh
```
*(Or simply toggle Eco Mode anytime inside the WebUI!)*

---

# 🇩🇪 Deutsche Dokumentation

## 🌌 Über das Projekt & Entwickler-Hinweis

**Aether Diffusion Studio Pro** ist eine eigenständige, hochmoderne Weiterentwicklung des beliebten Open-Source-Tools **Fooocus**.

> [!NOTE]
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der **Beta-Phase (v2.6.2 Beta)**.
> 
> Da es sich um ein Solo-Projekt handelt, freue ich mich über jede Art von Feedback! Melde Fehler, unvollständige Funktionen oder schlage neue Ideen vor. Ich lese jeden Feedback-Eintrag und baue coole Vorschläge gerne in künftige Updates ein!

---

## 🔄 Versions-Evolution: Was ist neu in v2.6.2?

1. **🔬 Precision Vision AI Studio (100% Lokal & Offline)**:
   - Detaillierte Bildanalyse durch Kombination aus natürlicher BLIP-Bildbeschreibung und tiefgehendem WD14-Tagging für eine exakte 1:1-Prompt-Rekonstruktion.
   - **0 MB dauerhafter VRAM-Verbrauch**: Alle Seh-Modelle entladen sich sofort nach der Erkennung vollständig aus dem Speicher.
2. **🖌️ Interaktives Pinsel-Maskierungswerkzeug**:
   - Zeichne direkt mit dem Pinsel auf das hochgeladene Bild:
     - **Ganzes Bild analysieren**: Komplette Bilderkennung.
     - **Markierten Bereich ignorieren (ausschließen)**: Übermalt störende Bildteile, sodass die KI sie vollständig ignoriert.
     - **Nur markierten Bereich analysieren (Fokus)**: Die KI konzentriert sich ausschließlich auf das markierte Objekt.
3. **🎛️ Selektive Attribut-Filterung in 7 Kategorien**:
   - `👤 Subjekt & Motiv`, `💇 Haare & Gesicht`, `👗 Kleidung & Outfit`, `🏞️ Hintergrund & Szene`, `💡 Licht & Atmosphäre`, `🎨 Kunststil & Medium`, `📐 Kamera & Perspektive`.
   - **Standardmäßig alle 7 aktiv** für vollständige 1:1-Prompt-Übernahme.
   - Abwählen einzelner Boxen aktualisiert den fertigen Prompt sofort ohne Neuanalyse.
4. **🎯 Gezielte Attribut-Ersetzung im bestehenden Prompt**:
   - Behalte deinen geschriebenen Prompt und ersetze gezielt nur einzelne Attribute:
     - `👗 Nur Kleidung übertragen` (z. B. nur das Outfit aus dem Bild übernehmen)
     - `💇 Nur Haare & Gesicht übertragen` (z. B. nur die Frisur/Haarfarbe übernehmen)
     - `🏞️ Nur Hintergrund übertragen` (z. B. nur die Umgebung übernehmen)
     - `💡 Nur Licht übertragen` / `🎨 Nur Stil übertragen`

---

## 💬 Community-Feedback & Fehler melden

- 🐛 **Fehler gefunden?** Öffne gerne ein Issue auf GitHub mit Betriebssystem, Grafikkarte und Fehlermeldung.
- 💡 **Feedback & Wünsche:** Schreibe mir gerne, was du dir als Nächstes im Programm wünschst!
