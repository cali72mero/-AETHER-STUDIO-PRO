<div align="center">

# 🌌 Aether Diffusion Studio Pro 2.6.3 (Beta)
### Autonome KI-Bildgenerierungsplattform der nächsten Generation • Basiert auf Fooocus

<p align="center">
  <a href="README.md">
    <img src="https://img.shields.io/badge/Switch%20to-English%20Version-0284c7?style=for-the-badge&logo=googletranslate&logoColor=white" alt="English" />
  </a>
  <a href="README_DE.md">
    <img src="https://img.shields.io/badge/Aktuell-Deutsche%20Version-10b981?style=for-the-badge&logo=googletranslate&logoColor=white" alt="Deutsch" />
  </a>
</p>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Base: Fooocus](https://img.shields.io/badge/Based%20on-Fooocus-orange.svg)](https://github.com/lllyasviel/Fooocus)
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.6.3-yellow.svg)](#-community-feedback--fehler-melden)
[![Release: v2.6.3](https://img.shields.io/badge/Release-v2.6.3-cyan.svg)](v2.6.3/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-uber-das-projekt--entwickler-hinweis)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-vergleich-standard-fooocus-vs-aether-studio-pro-263)

</div>

---

# 🇩🇪 Deutsche Dokumentation

## 🌌 Über das Projekt & Entwickler-Hinweis

**Aether Diffusion Studio Pro** ist eine eigenständige, hochmoderne Weiterentwicklung des beliebten Open-Source-Tools **Fooocus**.

> [!NOTE]
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der aktiven **Beta-Phase (v2.6.3 Beta)**.
> 
> Da ich dieses Projekt alleine entwickle, ist Community-Feedback extrem wertvoll! Falls du Fehler findest, Verbesserungswünsche hast oder neue Ideen einbringen möchtest, eröffne bitte gerne ein Issue auf GitHub oder hinterlasse Feedback. Ich lese jeden Vorschlag und versuche, neue Features zügig einzubauen!

---

## 🔄 Was wurde in Version 2.6.3 neu hinzugefügt? (Changelog)

1. **🧪 Offizielles Beta-Banner & aufgeräumte Aktionsleisten**:
   - Ein klares, leuchtendes Beta-Statusbanner direkt im Vision AI Studio signalisiert die aktive Weiterentwicklung und lädt zum Feedback ein.
   - Alle Buttons wurden in aufgeräumten, zusammenhängenden Aktionsleisten strukturiert (`vision-action-bar`, `vision-res-row`).
2. **❌ Automatische Negativ-Prompt-Generierung**:
   - Die Vision-KI analysiert Bildmedium, Zeichenstil und mögliche Bildartefakte und erzeugt automatisch einen passenden SDXL-Negativ-Prompt.
   - Per 1-Klick-Button `❌ Als Negativ-Prompt` wird dieser direkt in das Fooocus-Eingabefeld übernommen.
3. **📐 Bildauflösungs-Erkennung & 1-Klick-Übernahme**:
   - Erkennt beim Hochladen oder Analysieren sofort die exakte Originalauflösung (Breite × Höhe) des Referenzbildes.
   - Zeigt die SDXL-Empfehlung (64er-Raster) an.
   - Mit dem Button `📐 Als Zielauflösung übernehmen` wird die Auflösung sofort als aktive Generierungsauflösung eingestellt.
4. **🎛️ Eigene freie Auflösung wie in ComfyUI**:
   - Echte stufenlose Freiheit bei den Bildauflösungen: Schieberegler für Breite und Höhe (256 – 2048 Pixel in 64er Schritten).
   - `🔄 Seitenverhältnis tauschen (Breite ⇄ Höhe)` für blitzschnellen Wechsel zwischen Hoch- und Querformat.
   - Vollständig kompatibel mit der SDXL-Generierungs-Pipeline.
5. **💡 Detaillierter Upscale-Ratgeber**:
   - Neues Info-Akkordeon unter Upscale erklärt den Unterschied:
     - **Fast 2x:** Schnelle reine CPU-ESRGAN-Skalierung (pixelgenau vergrößert, erfindet aber keine neuen Details).
     - **1.5x / 2x:** Echte SDXL-Latent-Diffusion mit Denoising Strength 0.382 – generiert rasiermesserscharfe neue Hautporen, Wimpern, Haare und Mikrostrukturen.

---

## 🔄 Rückblick: Was wurde von v2.5 auf v2.6, v2.6.1 und v2.6.2 geändert?

- **v2.6.2:**
  - 🔬 Precision Vision Studio & Reverse Prompting (BLIP + WD14 Tagger, 100% lokal, 0 MB Rest-VRAM).
  - 🖌️ Interaktives Pinsel- & Maskierungswerkzeug (Ganzes Bild, Bereich ignorieren, Fokus-Maske).
  - 🎛️ 7 semantische Merkmals-Kategorien (Subjekt, Haare/Gesicht, Kleidung, Hintergrund, Licht, Stil, Kamera).
  - 🎯 Gezielte Attribut-Ersetzung einzelner Elemente im bestehenden Prompt.
- **v2.6.1:**
  - 🧠 100% lokaler neuronaler Übersetzer (`Helsinki-NLP/opus-mt-de-en`) auf CPU (0 MB VRAM, sofortige Speicherbereinigung).
  - 🪄 KI-Prompt-Magier zur automatischen Prompt-Veredelung.
  - 📥 Civitai 1-Klick Downloader mit Beta-Sicherheitswarnung und Modell-Auto-Refresh.
  - 🎚️ Interaktiver Vorher/Nachher Bildvergleichs-Slider.
  - 🌐 Zweisprachige Benutzeroberfläche und Dokumentation.
- **v2.6.0:**
  - Dark Obsidian Glassmorphism UI Redesign.
  - Dual-Engine VRAM Switch (🌱 Sparmodus vs. 🚀 Normalmodus) direkt in der WebUI.
  - Smart RAM Offloading gegen CUDA Out-Of-Memory Abstürze mit 32 GB RAM.
  - Sofortige Millisekunden-Stop- und Pause-Steuerung.
  - Universeller Modell-Ordner (`models/all_models_sdxl_flux/`).
  - VRAM-Rechner und Performance-Erklärungs-Akkordeon.

---

## 🚀 Vergleich: Standard Fooocus vs. Aether Studio Pro 2.6.3

| Funktion | Standard Fooocus (v2.5) | Aether Studio Pro (v2.6) | Aether Studio Pro (v2.6.1) | 🌌 Aether Studio Pro (v2.6.3) |
| :--- | :--- | :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles Standard-Thema | Dark Obsidian Cyber-UI | Dark Obsidian Glassmorphism | **Dark Obsidian Glassmorphism + Live-Status & Aktionsleisten** |
| **⚡ VRAM-Verwaltung** | Nur per CLI-Flag (`--lowvram`) | WebUI Dual-Engine Switch | WebUI Dual-Engine Switch | **WebUI Dual-Engine Switch + Live-Header-Badge** |
| **🧠 RAM-Schutz (OOM)**| Stürzt bei VRAM-Überlauf ab | Smart RAM Offload (32 GB) | Smart RAM Offload (32 GB) | **Smart RAM Offload (32 GB RAM Safe)** |
| **⏱️ Stop & Pause** | Wartet auf vollen Step | Sofort-Stop (Millisekunden) | Sofort-Stop & Pause | **Sofort-Stop & Pause ohne Latenz** |
| **🔬 Vision AI Studio** | Simpler Describe-Button | Simpler Describe-Button | Simpler Describe-Button | **Precision Vision Studio: Beta-Banner, Negativ-Prompt, Res-Erkennung, Pinsel, 7 Filter** |
| **📐 Auflösungen** | Nur feste Presets | Nur feste Presets | Nur feste Presets | **ComfyUI-Style Pixel-Slider + 1-Klick-Übernahme aus Vorlage** |
| **🌐 KI-Übersetzung** | Keine | Wörterbuch-Matrix | Lokaler MarianMT (0 MB VRAM) | **Lokaler neuronaler MarianMT (CPU, 0 MB VRAM)** |
| **🪄 Prompt-Ersteller**| Standard Style-Tags | Prompt-Guide Presets | KI-Prompt Magier | **KI-Prompt Magier + Vision Prompt & Negativ-Generator** |
| **📥 Civitai Download** | Manuell | Manuell | 1-Klick Downloader (Beta) | **1-Klick Downloader (Beta)** |
| **🎚️ Bild-Vergleich** | Nicht vorhanden | Nicht vorhanden | Vorher/Nachher Slider | **Vorher/Nachher Slider** |
| **🧬 Modell-Ordner** | Nur SDXL | SDXL, Turbo, Flux | Universeller Ordner | **Universeller Modellordner (`all_models_sdxl_flux/`)** |

---

## 💬 Community-Feedback & Fehler melden

- 🐛 **Fehler gefunden?** Öffne gerne ein Issue auf GitHub mit Betriebssystem, Grafikkarte und Log.
- 💡 **Feedback & Wünsche:** Schreibe mir gerne, was du dir als Nächstes im Programm wünschst!
