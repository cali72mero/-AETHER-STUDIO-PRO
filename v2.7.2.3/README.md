<div align="center">

# 🌌 Aether Diffusion Studio Pro 2.7.2.3 (Beta)
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
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.7.2.3-yellow.svg)](#-community-feedback--bug-reports)
[![Release: v2.7.2.3](https://img.shields.io/badge/Release-v2.7.2.3-cyan.svg)](v2.7.2.3/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-about-the-project--developer-note)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-aether-studio-pro-vs-standard-fooocus)

</div>

---

# 🇬🇧 English Documentation

## 🌌 About the Project & Developer Note

**Aether Diffusion Studio Pro** is an advanced, high-performance evolution of the popular open-source AI image generation software **Fooocus**.

> [!NOTE]
> This software is independently developed and maintained by a **single solo developer**. The software is currently in active **Beta phase (v2.7.2.3 Beta)**.
> 
> Because this is a continuous development process, community feedback is invaluable! If you encounter any bugs, unexpected behavior, or have ideas for exciting new features (models, workflows, UI improvements), please open an Issue on GitHub or join the discussions. I read every report and actively integrate user suggestions into new releases!

> [!WARNING]
> ### ⚠️ Stability & Compatibility Notice (Stable vs. Beta Releases)
> - **🟢 Stable Releases (All versions below v2.7):**  
>   All releases **below v2.7** (such as **v2.5**, **v2.6**, **v2.6.1**, **v2.6.2**, **v2.6.3**) are extensively tested, fully stable, and run reliably across almost all systems.
> - **🟡 Beta Releases (v2.7 and higher):**  
>   All versions **from v2.7 onwards** (v2.7.0, v2.7.1, v2.7.2, v2.7.2.1, v2.7.2.2, v2.7.2.3) are active **Beta versions** featuring cutting-edge features (Live Face Swap & Webcam Studio, Smartphone Wireless Camera, Precision Vision AI Studio, Custom Sampling Steps).  
>   *Please note: On certain devices or specific hardware configurations, beta versions may encounter unexpected issues or might not start properly. If you run into problems, please file an issue or use a stable release below v2.7.*

---

## 🔄 Version Evolution: Fooocus ➔ v2.5 ➔ v2.6 ➔ v2.6.3 ➔ v2.7.0 ➔ v2.7.1 ➔ v2.7.2 ➔ v2.7.2.1 ➔ v2.7.2.2 ➔ v2.7.2.3

### 🆕 What's New in v2.7.2.3 (Current Patch - iPhone Safari HTTPS Cloud-Tunnel & 0.0.0.0 Wi-Fi Listen Fix)
1. **📱 iPhone & Safari Remote Webcam HTTPS Cloud-Tunnel Fix**:
   - Fixed `TypeError: expected str, bytes or os.PathLike object, not NoneType` in `start_public_tunnel()` by providing a valid 32-byte secret token (`secrets.token_urlsafe(32)`) to Gradio's tunneling subsystem.
   - Provides a real, trusted HTTPS cloud URL (`https://....gradio.live`) with valid SSL certificates, allowing Apple iOS Safari to grant camera permissions (Apple strictly blocks camera access on unencrypted HTTP in Wi-Fi).
   - Added automatic iOS/Safari environment detection and user-friendly notice banner inside `REMOTE_CAM_HTML`.
2. **🌐 Default LAN Network Binding (`listen="0.0.0.0"`)**:
   - Set `listen="0.0.0.0"` default in `args_manager.py` and updated `run_lowvram.sh` with `--listen`, ensuring Fooocus binds to all network interfaces and accepts connections from other devices in the Wi-Fi.

---

### 🌟 What was added in v2.7.2.2 (Torch Import Fix in Model Management)
1. **🔧 Fixed Startup Crash (Torch Import in Model Management)**:
   - Resolved `NameError: name 'torch' is not defined` in `ldm_patched/modules/model_management.py`.
   - Tensor Core TF32 acceleration and cuDNN benchmark tuning on NVIDIA Ampere (RTX 3050+) initialize cleanly.

---

### 🌟 What was added in v2.7.2.1 (Custom Performance & Freely Configurable Sampling Steps)
1. **🎯 Custom Performance Mode (`Custom (Eigene Schritte)`)**:
   - Added a dedicated **Custom** setting directly to the Performance selector alongside Speed, Quality, Lightning, Hyper-SD, Extreme Speed, and Turbo.
   - Dynamically expands a sleek Obsidian Cyberpunk control panel right beneath the performance buttons.
2. **🎛️ Dual Slider & Precise Numeric Input for Steps (1–200 Steps)**:
   - Configure any desired sampling step count between 1 and 200 (e.g. 15, 20, 25, 40, 50, 75, 100 steps) with live synchronization.
3. **⚡ Seamless Diffusion Pipeline Execution**:
   - Accurately executes the custom step count across standard SDXL sampling pipelines.

---

### 🌟 What was added in v2.7.2 (Precision Vision AI: Anime vs. Realism & Target Model Selector)
1. **🎨 Anime vs. Photorealism Selector in Vision AI Studio**:
   - Explicit toggle between `🔍 Automatisch erkennen`, `📸 Realistisches Foto / Fotorealismus`, and `🎨 Anime / Manga / Illustration`.
   - Strips photographic jargon from anime prompts and prevents anime artifacts on realistic photos.
2. **🎯 Target Model Dropdown with Syntax Profiling**:
   - Adapts syntax dynamically for Pony (`score_9`), Animagine (`masterpiece`), and SDXL Photorealism (`dslr, raw photo`).
   - Instant 1ms reactive prompt re-calculation.

---

### 🌟 What was added in v2.7.1 (Smartphone Webcam, Instant Splash Launcher & Low-VRAM Speed Boost)
1. **📱 Wireless Smartphone & Tablet Webcam Integration**:
   - Use your iPhone, Android phone, iPad, or secondary tablet as a wireless camera via QR Code / PIN.
   - Streams to Fooocus, driving avatars in real time for OBS Studio, TikTok Live Studio, and Discord!
2. **⚡ Instant Browser Loading Screen**:
   - Browser opens within 1 second showing an obsidian dark loading screen with live progress.
3. **🚀 Low-VRAM & RTX 3050 Speed Boost**:
   - Tensor Core TF32 acceleration + optimized memory allocation for 6GB GPUs (15–25% faster).
4. **🐳 Fixed GitHub Actions Container Build**:
   - Fixed Docker tag format naming conflict in workflow.

---

### 🌟 What was added in v2.7.0 (Live Face Swap Studio & Direct English Prompt Enhancer)
1. **🎭 Live Face Swap & Avatar Studio (Beta - 100% Local & OBS Studio Ready)**:
   - **Realtime Facial Tracking**: Tracks your face via webcam or phone—measuring eye blinking, mouth motion, and head tilt/roll.
   - **Avatar Expression Retargeting**: Upload any reference portrait or character; the AI animates eyes, mouth, and head in real time!
   - **Multi-Tier Model Architecture**: Eco / Fast (0 MB VRAM, RTX 3050 & CPU) to LivePortrait HD.
   - **OBS Studio & Stream Integration**: Browser Source `http://127.0.0.1:7865/live_avatar` and MJPEG `http://127.0.0.1:7865/stream/avatar.mjpg`.
2. **🪄 Direct English Prompt Enhancer (Without Translation)**:
   - Button `🪄 Prompt Erweitern (Ohne Übersetzung)` to enrich English prompts without loading the translation model.

---

### 🌟 What was added in v2.6.3
1. **🧪 Official Beta Status Banner & UI Refinements**:
   - Prominent Beta banner inside the Vision AI Studio tab and clean unified action bars (`vision-action-bar`, `vision-res-row`).
2. **❌ Automatic Negative Prompt Synthesis**:
   - Analyzes detected style and artifacts to auto-compose a matching SDXL Negative Prompt with 1-click adoption.
3. **📐 Image Resolution Auto-Detection & 1-Click Adoption**:
   - Displays exact uploaded image dimensions and sets them as active generation size with 1 click.
4. **🎛️ ComfyUI-Style Free Custom Resolution Controls**:
   - Free pixel sliders for width and height (256 - 2048 px) with quick portrait/landscape swap.
   - Explains the difference between Fast 2x (ESRGAN without new details) and 1.5x/2x (SDXL Latent Diffusion with new micro-textures).

---

### 🌟 What was added in v2.6.2
1. **🔬 Precision Vision AI Studio & Reverse Prompting (100% Local)**:
   - Deep multi-modal image comprehension combining **BLIP natural captioning** with **WD14 multi-tagger interrogation** for exact 1:1 SDXL prompt reconstruction.
   - Completely offline execution with **0 MB lingering VRAM footprint** (models run and immediately purge memory).
2. **🖌️ Interactive Brush Masking (`tool='sketch'`)**:
   - **Ganzes Bild analysieren (Full Image)**: Analyzes the complete uploaded reference picture.
   - **Markierten Bereich ignorieren (ausschließen / Exclude Mask)**: User-drawn brush strokes are blanked out so the AI completely ignores masked objects or distractions.
   - **Nur markierten Bereich analysieren (Fokus / Focus Mask)**: Blacks out the background and isolates only the marked region for targeted inspection.
3. **🎛️ Selective Attribute Filtering (7 Semantic Categories)**:
   - Structured decomposition into Subject, Hair/Face, Clothing, Background, Lighting, Style, and Camera.
   - All 7 checked by default for instant 1:1 prompt recreation.
4. **🎯 Selective Prompt Merging & Attribute Swapping**:
   - Keep your existing typed prompt intact and swap or insert *only* specific attributes from the uploaded image (clothing, hair, background, lighting, art style).

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

| Feature | Standard Fooocus (v2.5) | Aether Studio Pro (v2.6) | Aether Studio Pro (v2.6.3) | 🌌 Aether Studio Pro (v2.7.2.2) |
| :--- | :--- | :--- | :--- | :--- |
| **🎨 User Interface** | Light standard theme | Dark Obsidian Cyberpunk UI | Dark Obsidian Glassmorphism | **Dark Obsidian Glassmorphism + Instant Browser Splash Screen** |
| **⚡ Performance & Steps** | Fixed presets only | Fixed presets only | Fixed presets only | **Presets (Quality, Speed, Turbo) + 🎯 Custom Steps (1-200 Slider & Input)** |
| **⚡ VRAM Control** | CLI flags only (`--lowvram`) | WebUI Dual-Engine Switch | WebUI Dual-Engine Switch | **Dual-Engine + Ampere TF32 & 6GB Optimized Headroom Boost** |
| **🧠 Memory Safety (OOM)**| Crashes on VRAM exhaustion | Smart RAM Offload (32 GB) | Smart RAM Offload (32 GB RAM Safe) | **Smart RAM Offload (32 GB RAM Safe)** |
| **⏱️ Stop & Pause** | Waits for full step finish | Instant Millisecond Stop | Instant Millisecond Stop & Pause | **Instant Millisecond Stop & Pause** |
| **🎭 Live Face Swap Studio**| None | None | None | **Live Face Swap & Realtime Avatar (Webcam + Smartphone Wireless, OBS, TikTok, Discord)** |
| **🔬 Vision AI Studio** | Simple describe button | Standard describe | Precision Vision Studio | **Precision Vision Studio: Anime vs. Realism, Target Model Profiling, Neg-Prompt, 7 Filters** |
| **📐 Aspect Ratios** | Fixed presets only | Fixed presets only | ComfyUI-Style Pixel Sliders | **ComfyUI-Style Custom Pixel Sliders + 1-Click Reference Adoption** |
| **🌐 Neural Translation** | None | Dictionary Matrix | Local Neural MarianMT (0 MB VRAM) | **Local Neural MarianMT (CPU, 0 MB VRAM, Instant Purge)** |
| **🪄 Prompt Creator** | Standard prompt expansion | Prompt Guide Presets | AI Prompt Creator & Enricher | **AI Prompt Magician + Direct English Enhancer (No Translation Required)** |
| **📥 Civitai Download** | None (manual) | None | Integrated 1-Click Downloader | **Integrated 1-Click Downloader (Beta)** |
| **🎚️ Image Comparison** | None | None | Interactive Drag Slider | **Interactive Before/After Drag Slider** |
| **🧬 Model Scope** | SDXL only | SDXL, Turbo, SD1.5, Flux | Universal Architecture | **Universal Model Architecture (`all_models_sdxl_flux/`)** |

---

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
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der **Beta-Phase (v2.7.2.3 Beta)**.
> 
> Da es sich um ein Solo-Projekt handelt, freue ich mich über jede Art von Feedback! Melde Fehler, unvollständige Funktionen oder schlage neue Ideen vor. Ich lese jeden Feedback-Eintrag und baue coole Vorschläge gerne in künftige Updates ein!

> [!WARNING]
> ### ⚠️ Wichtiger Hinweis zu Stabilität & Beta-Versionen
> - **🟢 Stabile Versionen (Alle Versionen unter 2.7):**  
>   Alle Versionen **unter 2.7** (wie **v2.5**, **v2.6**, **v2.6.1**, **v2.6.2**, **v2.6.3**) laufen stabil und zuverlässig auf allen unterstützten Systemen.
> - **🟡 Beta-Versionen (Ab Version 2.7 und höher):**  
>   Alle Versionen **ab 2.7** (v2.7.0, v2.7.1, v2.7.2, v2.7.2.1, v2.7.2.2, v2.7.2.3) sind **aktive Beta-Versionen** mit neuesten experimentellen Funktionen (Live Face Swap & Avatar Studio, kabellose Smartphone-Kamera, Precision Vision AI, Custom Performance Steps).  
>   *Hinweis: Auf einigen Geräten oder Hardware-Konfigurationen können Beta-Versionen zu Problemen führen oder gar nicht starten. Falls Probleme auftreten, nutze bitte eine stabile Version unter 2.7 oder melde den Fehler auf GitHub.*

---

## 🔄 Versions-Evolution: Was ist neu in v2.7.2.3?

1. **📱 iPhone & Safari Remote-Kamera HTTPS Cloud-Tunnel Fix**:
   - Fehler `TypeError: NoneType` im Gradio-Tunnel behoben, indem ein sicherer 32-Byte Secret Token erzeugt wird.
   - Der öffentliche HTTPS-Tunnel (`https://....gradio.live`) startet nun mit 1 Klick fehlerfrei und liefert echte SSL-Zertifikate, wodurch Apple Safari auf dem iPhone den Kamerazugriff sofort erlaubt.
   - Automatische Erkennung von iOS Safari bei unverschlüsseltem HTTP mit Hinweismeldung direkt im mobilen Browser.
2. **🌐 Standard LAN-Bindung (`listen="0.0.0.0"`)**:
   - Fooocus bindet standardmäßig an alle Netzwerkadressen (`0.0.0.0`), sodass Geräte im selben WLAN direkt zugreifen können.

---

### 🌟 Was wurde in v2.7.2.2 & v2.7.2.1 hinzugefügt?
1. **🔧 Start-Bugfix behoben**: `import torch` in `ldm_patched/modules/model_management.py` ergänzt.
2. **🎯 Custom Performance Modus (`Custom (Eigene Schritte)`)**:
   - Völlig freie Schrittanzahl (1–200 Steps) direkt per Schieberegler oder Direkteingabe festlegen.
2. **🎨 Anime vs. Fotorealismus Selektor im Vision AI Studio**:
   - Spezifische Umschaltung zwischen automatischer Erkennung, reinem Fotorealismus oder Anime/Manga.
3. **🎯 Ziel-Modell Profilierung**:
   - Auswahl des Ziel-Checkpoints aus den heruntergeladenen Modellen (z.B. Animagine, Juggernaut, Pony).

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
