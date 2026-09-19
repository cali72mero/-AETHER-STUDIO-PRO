# 🌌 Aether Diffusion Studio Pro 2.6 (Beta)

<div align="center">

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Base: Fooocus](https://img.shields.io/badge/Based%20on-Fooocus-orange.svg)](https://github.com/lllyasviel/Fooocus)
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.6-yellow.svg)](#-status--community-feedback)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-uber-das-projekt--about-the-project)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-features--unterschiede-zu-fooocus)

**[🇩🇪 Deutsch](#-deutsche-dokumentation)** &nbsp;|&nbsp; **[🇬🇧 English](#-english-documentation)**

</div>

---

# 🇩🇪 Deutsche Dokumentation

## 🌌 Über das Projekt & Entwickler-Hinweis

**Aether Diffusion Studio Pro** ist eine eigenständige Weiterentwicklung des beliebten Open-Source-Tools **Fooocus**. 

> [!NOTE]
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der **Beta-Phase (v2.6 Beta)**.

---

## 💡 Feedback, Fehler melden & Feature-Wünsche

Da dieses Tool aktiv weiterentwickelt wird, ist deine Meinung und Unterstützung extrem wertvoll:
- 🐛 **Fehler gefunden?** Bitte erstelle ein Issue auf GitHub oder melde Bugs mit einer kurzen Beschreibung deines Setups.
- 💡 **Ideen für neue Funktionen?** Du hast eine Idee, was Aether Studio noch können sollte (neue Sampler, UI-Ideen, Modellunterstützungen etc.)? Schreib es gerne in das Feedback – ich werde mein Bestes tun, um sinnvolle Vorschläge in kommenden Versionen einzubauen!

---

## 📜 Lizenz & Urheberrecht (GPL-3.0 Compliance)

> [!IMPORTANT]
> **Aether Diffusion Studio Pro** basiert auf dem Code von **[Fooocus](https://github.com/lllyasviel/Fooocus)** (entwickelt von **lllyasviel** und gepflegt von **mashb1t**). 
> 
> Das Projekt steht gemäß der **GNU General Public License v3.0 (GPLv3)** vollständig als freie Open-Source-Software zur Verfügung. Sämtliche Urheberrechte der ursprünglichen Entwickler von Fooocus, PyTorch, Gradio und ldm_patched bleiben vollumfänglich gewahrt. Die originale Lizenzdatei [LICENSE](LICENSE) ist unverändert enthalten.

---

## 🚀 Was kann Aether Studio Pro mehr als das normale Fooocus?

Hier ist die Übersicht aller Neuerungen und Erweiterungen im Vergleich zur Basis-Version von Fooocus:

| Funktion | Normales Fooocus | 🌌 Aether Diffusion Studio Pro 2.6 (Beta) |
| :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles, simples Standard-Design | **Dark Obsidian Glassmorphism**: Hochmodernes Dark-UI mit tiefem Schwarz, subtilen Glass-Effekten, Neon-Akzenten und Live-Status-Header |
| **⚡ VRAM-Verwaltung** | Feste Einstellung nur über Start-Flags (`--lowvram`) | **Dual-Engine VRAM Switch**: Direkt in der WebUI im laufenden Betrieb zwischen *🌱 VRAM-Sparmodus (Eco)* und *🚀 Normalmodus (Max GPU)* umschalten |
| **🧠 RAM-Schutz (OOM)** | Programm stürzt bei Speicherüberlauf (CUDA OOM) ab | **Smart RAM Offload**: Wenn der VRAM der GPU (z. B. 6 GB) voll ist, lagert das System Schichten dynamisch in den System-RAM (bis 32 GB) aus |
| **⏱️ Stop & Pause** | Braucht oft Sekunden bis zum Ende eines Denoising-Steps | **Instant Millisecond Controls**: Nahezu verzögerungsfreies Abbrechen und Pausieren direkt im Iterationszyklus |
| **🧬 Modell-Unterstützung** | Nahezu ausschließlich auf Standard-SDXL fokussiert | **Universeller Modellordner (`all_models_sdxl_flux/`)**: Zentraler Checkpoint-Ordner für SDXL, Turbo, SD 1.5 und Flux-Modelle mit automatischer Erkennung |
| **📊 Modell- & VRAM-Rechner** | Nicht vorhanden | **Integrierter VRAM-Checker**: Berechnet per Modellname oder Civitai-Link exakt den VRAM-Bedarf und prüft die Hardware-Tauglichkeit |
| **🎨 Prompting-Assistenz** | Nur generische Styles | **3D Master & Anime Prompt Guide**: Spezialisierter Generator mit 1-Klick-Injektion für fotorealistische 3D-Renders & detailreiche Anime-Motive |
| **📖 Performance-Erklärung** | Nur Radio-Buttons ohne Erklärung | **Interaktives Erklärungs-Menü**: Detaillierte Tabelle über Quality (60 Steps), Speed (30), Turbo (6), Lightning (4), Hyper-SD und LCM |
| **💾 Bild-Verlauf & Export** | Manuelles Suchen im Ausgabeordner | **Quick-History & 1-Klick Download**: Generierte Bilder sofort mit einem Klick in den System-Download-Ordner exportieren |
| **🛠️ Low-VRAM Bugfix** | Absturz `RuntimeError: Expected all tensors on same device` | **Gefixt**: HuggingFace CLIP Text-Encoder Embeddings werden im Sparmodus synchron auf CUDA gehalten |
| **📐 Aspect Ratio Bugfix** | Absturz bei Asterisk-Format (`ValueError: not enough values to unpack`) | **Gefixt**: Universeller Regex-Parser für Formate mit `×`, `*` oder `x` |

---

## 💻 Systemanforderungen

- **Betriebssystem**: Linux (Arch, CachyOS, Ubuntu, Debian, etc.) oder Windows 10/11
- **Grafikkarte (GPU)**: NVIDIA RTX/GTX mit mind. 4 GB – 6 GB VRAM (z. B. RTX 3050, 2060, 3060, 40-Serie)
- **Arbeitsspeicher (RAM)**: 16 GB empfohlen (32 GB für Smart RAM Offload bei großen Modellen)
- **Software**: Python 3.10 mit PyTorch 2.1+ und CUDA-Treiber

---

## 🛠️ Schnellstart

### 1. Repository klonen
```bash
git clone https://github.com/cali72mero/-AETHER-STUDIO-PRO.git
cd -AETHER-STUDIO-PRO
```

### 2. Starten

**Im Standard-Modus (Maximale GPU-Geschwindigkeit):**
```bash
./venv/bin/python entry_with_update.py
```

**Im VRAM-Sparmodus (für 4 GB – 6 GB Grafikkarten empfohlen):**
```bash
./venv/bin/python entry_with_update.py --lowvram
# oder:
./run_lowvram.sh
```

Öffne im Browser: `http://127.0.0.1:7865`

---
---

# 🇬🇧 English Documentation

## 🌌 About the Project & Developer Note

**Aether Diffusion Studio Pro** is an advanced evolution of the acclaimed open-source AI image generation platform **Fooocus**.

> [!NOTE]
> This software is independently developed and maintained by a **single solo developer**. It is currently in active **Beta phase (v2.6 Beta)**.

---

## 💡 Feedback, Bug Reports & Feature Requests

Community feedback is essential to making Aether Studio the best it can be:
- 🐛 **Found a bug?** Please submit an issue on GitHub with a brief description of your operating system, GPU, and error log.
- 💡 **Feature Ideas?** Have an idea for new workflows, models, or UI features? Share your thoughts – I will gladly review all feedback and try my best to implement community suggestions in upcoming releases!

---

## 📜 License & Compliance (GPL-3.0)

> [!IMPORTANT]
> **Aether Diffusion Studio Pro** is built on top of **[Fooocus](https://github.com/lllyasviel/Fooocus)** (originally created by **lllyasviel** and maintained by **mashb1t**).
>
> In accordance with the **GNU General Public License v3.0 (GPLv3)**, this software remains 100% free and open-source. All intellectual property and copyright rights of the original Fooocus, PyTorch, Gradio, and ldm_patched contributors are fully preserved. The original [LICENSE](LICENSE) is included without alterations.

---

## 🚀 Key Enhancements (Aether Studio Pro vs. Standard Fooocus)

| Feature | Standard Fooocus | 🌌 Aether Diffusion Studio Pro 2.6 (Beta) |
| :--- | :--- | :--- |
| **🎨 User Interface** | Light standard Gradio theme | **Dark Obsidian Glassmorphism**: Cyber-dark aesthetics, glowing indicators, responsive controls, and dynamic status header |
| **⚡ VRAM Architecture** | Fixed at launch via CLI flags (`--lowvram`) | **Dynamic Dual-Engine VRAM Switch**: Seamlessly toggle between *🌱 Eco / Low-VRAM* and *🚀 Normal / Max Speed* directly inside the WebUI |
| **🧠 Memory Safety (OOM)** | Crashes with CUDA Out-Of-Memory when models exceed VRAM | **Smart RAM Offloading**: Dynamically offloads excess tensor layers to system RAM (up to 32 GB) to prevent OOM crashes |
| **⏱️ Stop & Pause Latency** | Often waits seconds until the full step completes | **Instant Millisecond Controls**: Near-zero latency abort and pause hooks built into the inner diffusion loop |
| **🧬 Model Compatibility** | Primarily constrained to SDXL checkpoints | **Universal Model Architecture (`all_models_sdxl_flux/`)**: Centralized directory supporting SDXL, Turbo, SD 1.5, and Flux models |
| **📊 Hardware Calculator** | None | **Integrated Model & VRAM Calculator**: Predicts exact VRAM requirements and hardware compatibility from model names or Civitai links |
| **🎨 Prompt Engineering** | Basic style selection | **3D Master & Anime Prompt Guide**: Dedicated prompt builder with 1-click preset injection for photorealistic 3D and anime artwork |
| **📖 Performance Guide** | Simple radio buttons without explanation | **Interactive Performance Accordion**: Full breakdown of Quality (60 steps), Speed (30), Turbo (6), Lightning (4), Hyper-SD, and LCM |
| **💾 History & Quick Export** | Manual browsing in outputs directory | **Quick-History & 1-Click Download**: Instantly export generated images into your system Downloads folder |
| **🛠️ Low-VRAM Bugfix** | `RuntimeError: Expected all tensors on same device` | **Resolved**: Synchronized HuggingFace CLIP embeddings and position IDs on CUDA devices during offloading |
| **📐 Aspect Ratio Parser** | Crashes on asterisk format (`ValueError: not enough values to unpack`) | **Resolved**: Resilient regex parser supporting `×`, `*`, and `x` delimiters |

---

## 💻 System Requirements

- **Operating System**: Linux (Arch, CachyOS, Ubuntu, Debian, Fedora, etc.) or Windows 10/11
- **GPU**: NVIDIA Graphics Card with 4 GB – 6 GB+ VRAM (e.g. RTX 3050, 2060, 3060, 40-series)
- **System Memory (RAM)**: 16 GB minimum (32 GB recommended for Smart RAM Offloading on massive checkpoints)
- **Dependencies**: Python 3.10, PyTorch 2.1+, CUDA Toolkit

---

## 🛠️ Getting Started

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

## 🌟 Acknowledgements & Credits
- **Fooocus Core Engine**: [lllyasviel](https://github.com/lllyasviel) & [mashb1t](https://github.com/mashb1t)
- **Stable Diffusion XL**: [Stability AI](https://stability.ai)
- **ComfyUI Architecture**: [comfyanonymous](https://github.com/comfyanonymous)
- **Gradio Framework**: [Gradio Team](https://gradio.app)
