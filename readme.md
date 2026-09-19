# 🌌 Aether Diffusion Studio Pro 2.6 (Beta)

<div align="center">

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Base: Fooocus](https://img.shields.io/badge/Based%20on-Fooocus-orange.svg)](https://github.com/lllyasviel/Fooocus)
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.6-yellow.svg)](#-status--community-feedback)
[![Version: v2.6](https://img.shields.io/badge/Release-v2.6.0-cyan.svg)](v2.6/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-uber-das-projekt--about-the-project)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-features--unterschiede-zu-fooocus)

**[🇩🇪 Deutsch](#-deutsche-dokumentation)** &nbsp;|&nbsp; **[🇬🇧 English](#-english-documentation)**

</div>

---

# 🇩🇪 Deutsche Dokumentation

## 🌌 Über das Projekt & Entwickler-Hinweis

**Aether Diffusion Studio Pro** ist eine eigenständige, leistungsstarke Weiterentwicklung des beliebten Open-Source-Tools **Fooocus**.

> [!NOTE]
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der **Beta-Phase (v2.6 Beta)**.

---

## 🔄 Was wurde von Version 2.5 auf Version 2.6 geändert? (Changelog)

Hier sind alle Neuerungen, die von der alten Basisversion (v2.5.5) auf die neue **Version 2.6.0** entwickelt und hinzugefügt wurden:

1. **📥 Civitai 1-Klick Downloader (Beta)**:
   - Modelle und LoRAs können nun direkt über die WebUI per Civitai-Link oder Modell-ID heruntergeladen werden.
   - Automatische Erkennung von Modellname, Version, Basismodell (SDXL, SD 1.5, Flux) und Zielordner (`checkpoints/` oder `loras/`).
   - Integrierte Beta-Warnung bei sehr großen Dateien.
2. **🪄 Prompt-Magier & Deutsch-Übersetzer**:
   - Erkennt deutsche Prompts und übersetzt sie automatisch ins Englische.
   - Optionaler Qualitäts-Boost: Ergänzt fotorealistische und filmische SDXL-Keywords (*masterpiece, best quality, cinematic lighting, sharp focus*).
   - In den Einstellungen aktivierbar (`Auto`, `Nur Übersetzen`, `Nur Qualitäts-Boost`).
3. **🎚️ Interaktiver Vorher / Nachher Bildvergleichs-Slider**:
   - Neuer Reiter im Eingabebereich für direkten Vorher/Nachher-Vergleich mit stufenlosem Schieberegler.
   - 1-Klick-Übernahme aus Upscale / Variation und Galerie.
4. **📖 Interaktives Performance-Akkordeon**:
   - Detaillierte Tabelle in der UI über die Unterschiede zwischen **Quality** (60 Steps), **Speed** (30 Steps), **Turbo** (6-8 Steps), **Lightning** (4-8 Steps), **Hyper-SD** und **Extreme Speed (LCM)**.
5. **⚡ Dynamischer Dual-Engine VRAM Switch**:
   - Umschaltung zwischen **🌱 VRAM-Sparmodus (Eco / Low-VRAM)** und **🚀 Normalmodus (Max GPU-Speed)** direkt in der WebUI mit Live-Header-Statusbadge.
6. **🧠 Smart RAM Offloading**:
   - Verhindert CUDA Out-Of-Memory (OOM) Abstürze: Lagert überzählige Modellschichten automatisch in den 32 GB System-RAM aus, wenn der VRAM (z. B. 6 GB) voll ist.
7. **⏱️ Millisekunden Stop & Pause Kontrollen**:
   - Reagiert sofort und ohne Verzögerung auf den Stop- und Pause-Button, ohne den laufenden Step abzuwarten.
8. **🧬 Universeller Modell-Ordner (`models/all_models_sdxl_flux/`)**:
   - Zentraler Ordner für alle SDXL-, Turbo-, SD 1.5- und FLUX-Checkpoints mit automatischer Scanner-Erkennung.
9. **📊 Integrierter VRAM- & Hardware-Rechner**:
   - Automatische Hardware-Erkennung (GPU & RAM) und Kompatibilitätsrechner für Civitai-Modelle.
10. **🎨 3D Master & Anime Prompt Guide**:
    - Spezialisierte Prompt-Generatoren mit 1-Klick-Injektion für fotorealistische 3D-Renders und Anime-Motive.
11. **💾 Quick-History & 1-Klick Download**:
    - Generierte Bilder können sofort mit einem Klick in den System-Download-Ordner exportiert werden.
12. **🛠️ Kritische Bugfixes**:
    - HuggingFace CLIP Device-Mismatch im Low-VRAM Modus behoben (`Expected all tensors to be on the same device`).
    - Flexibler Aspect-Ratio-Parser für Formate mit `×`, `*` und `x`.

---

## 💡 Feedback, Fehler melden & Feature-Wünsche

Da dieses Tool aktiv weiterentwickelt wird, ist deine Meinung extrem wertvoll:
- 🐛 **Fehler gefunden?** Bitte erstelle ein Issue auf GitHub oder melde Bugs mit einer kurzen Beschreibung deines Setups.
- 💡 **Ideen für neue Funktionen?** Du hast eine Idee, was Aether Studio noch können sollte? Schreib es gerne in das Feedback – ich werde mein Bestes tun, um sinnvolle Vorschläge in kommenden Versionen einzubauen!

---

## 📜 Lizenz & Urheberrecht (GPL-3.0 Compliance)

> [!IMPORTANT]
> **Aether Diffusion Studio Pro** basiert auf dem Open-Source-Projekt **[Fooocus](https://github.com/lllyasviel/Fooocus)** (entwickelt von **lllyasviel** und gepflegt von **mashb1t**). 
> 
> Das Projekt steht gemäß der **GNU General Public License v3.0 (GPLv3)** vollständig als freie Open-Source-Software zur Verfügung. Sämtliche Urheberrechte der ursprünglichen Entwickler von Fooocus, PyTorch, Gradio und ldm_patched bleiben vollumfänglich gewahrt. Die originale Lizenzdatei [LICENSE](LICENSE) ist unverändert enthalten.

---

## 🚀 Vergleich: Standard Fooocus vs. Aether Studio Pro 2.6

| Funktion | Normales Fooocus | 🌌 Aether Diffusion Studio Pro 2.6 (Beta) |
| :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles, simples Standard-Design | **Dark Obsidian Glassmorphism**: Hochmodernes Dark-UI mit tiefem Schwarz, Neon-Akzenten und Live-Status-Header |
| **⚡ VRAM-Verwaltung** | Feste Einstellung nur über Start-Flags (`--lowvram`) | **Dual-Engine VRAM Switch**: Direkt in der WebUI zwischen *🌱 Sparmodus* und *🚀 Normalmodus* umschalten |
| **🧠 RAM-Schutz (OOM)** | Programm stürzt bei Speicherüberlauf (CUDA OOM) ab | **Smart RAM Offload**: Lagert überzählige Schichten dynamisch in den System-RAM (bis 32 GB) aus |
| **⏱️ Stop & Pause** | Braucht oft Sekunden bis zum Ende eines Denoising-Steps | **Instant Millisecond Controls**: Nahezu verzögerungsfreies Abbrechen und Pausieren direkt im Iterationszyklus |
| **📥 Civitai Download** | Nicht vorhanden (alles manuell) | **Integrierter 1-Klick Downloader (Beta)** mit Auto-Erkennung für Checkpoints und LoRAs |
| **🪄 Prompt-Übersetzer** | Nur Englisch, kein Übersetzer | **Prompt-Magier**: Übersetzt deutsche Prompts und reichert sie mit Top-Qualitätsbegriffen an |
| **🎚️ Bild-Vergleich** | Nicht vorhanden | **Interaktiver Vorher/Nachher-Slider** zur optischen Überprüfung von Upscales und Variationen |
| **🧬 Modell-Unterstützung** | Nahezu ausschließlich auf Standard-SDXL fokussiert | **Universeller Modellordner (`all_models_sdxl_flux/`)**: Zentraler Checkpoint-Ordner für SDXL, Turbo, SD 1.5 und Flux-Modelle |
| **📊 Modell- & VRAM-Rechner** | Nicht vorhanden | **Integrierter VRAM-Checker**: Berechnet per Modellname oder Civitai-Link exakt den VRAM-Bedarf |
| **🎨 Prompting-Assistenz** | Nur generische Styles | **3D Master & Anime Prompt Guide**: Spezialisierter Generator mit 1-Klick-Injektion |
| **📖 Performance-Erklärung** | Nur Radio-Buttons ohne Erklärung | **Interaktives Erklärungs-Menü**: Detaillierte Tabelle über Quality, Speed, Turbo, Lightning, Hyper-SD, LCM |
| **💾 Bild-Verlauf & Export** | Manuelles Suchen im Ausgabeordner | **Quick-History & 1-Klick Download**: Generierte Bilder sofort in den System-Download-Ordner exportieren |

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

## 🔄 What's New from v2.5 to v2.6? (Changelog)

1. **📥 Civitai 1-Click Downloader (Beta)**:
   - Download checkpoints and LoRAs directly from Civitai URLs or model IDs with automatic model classification and folder routing.
   - Built-in Beta safety warning for large files.
2. **🪄 Prompt Magier & Translator**:
   - Translates German prompt descriptions into fluent English and enhances them with SDXL quality keywords (*masterpiece, cinematic lighting, sharp focus*).
   - Configurable in Settings (`Auto`, `Translate Only`, `Quality Boost Only`).
3. **🎚️ Interactive Before / After Comparison Slider**:
   - Interactive slider tab comparing original input and generated upscale/variations side-by-side.
   - 1-click import from Upscale/Vary and Gallery.
4. **📖 Interactive Performance Modes Guide**:
   - Detailed accordion breaking down Quality (60 steps), Speed (30 steps), Turbo (6-8 steps), Lightning (4-8 steps), Hyper-SD, and LCM.
5. **⚡ Dynamic Dual-Engine VRAM Switch**:
   - Seamlessly toggle between **🌱 Eco / Low-VRAM** and **🚀 Normal / Max Speed** modes directly inside the UI with live status indicator.
6. **🧠 Smart RAM Offloading**:
   - Automatically offloads excess tensor weights into system RAM (up to 32 GB), preventing CUDA Out-Of-Memory crashes on 6 GB GPUs.
7. **⏱️ Millisecond Stop & Pause Response**:
   - Immediate abort and pause controls without waiting for full denoising step completion.
8. **🧬 Universal Model Architecture (`models/all_models_sdxl_flux/`)**:
   - Centralized directory for SDXL, Turbo, SD 1.5, and Flux models with automatic scanning.
9. **📊 Hardware & VRAM Compatibility Calculator**:
   - Hardware detection and predictive VRAM calculation from model names or Civitai links.
10. **🎨 3D Master & Anime Prompt Guide**:
    - Dedicated prompt generator with 1-click injection for 3D renders and anime scenes.
11. **💾 Quick-History & 1-Click Download**:
    - Instantly export generated images into your system Downloads folder.
12. **🛠️ Bugfixes**:
    - Resolved HuggingFace CLIP tensor mismatch on CUDA in Low-VRAM mode.
    - Resilient aspect ratio regex parser supporting `×`, `*`, and `x`.

---

## 💡 Feedback, Bug Reports & Feature Requests

- 🐛 **Found a bug?** Please submit an issue on GitHub with your setup details.
- 💡 **Feature Ideas?** Share your ideas – community suggestions are warmly welcome and will be reviewed for upcoming releases!

---

## 📜 License & Compliance (GPL-3.0)

> [!IMPORTANT]
> **Aether Diffusion Studio Pro** is built on top of **[Fooocus](https://github.com/lllyasviel/Fooocus)** (created by **lllyasviel** and maintained by **mashb1t**).
>
> In accordance with the **GNU General Public License v3.0 (GPLv3)**, this software remains 100% free and open-source. All original copyright notices and licenses are fully preserved.

---

## 🌟 Acknowledgements & Credits
- **Fooocus Core Engine**: [lllyasviel](https://github.com/lllyasviel) & [mashb1t](https://github.com/mashb1t)
- **Stable Diffusion XL**: [Stability AI](https://stability.ai)
- **ComfyUI Architecture**: [comfyanonymous](https://github.com/comfyanonymous)
- **Gradio Framework**: [Gradio Team](https://gradio.app)
