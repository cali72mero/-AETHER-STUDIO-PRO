<div align="center">

# 🌌 Aether Diffusion Studio Pro 2.7.0 (Beta)
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
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.7.0-yellow.svg)](#-community-feedback--fehler-melden)
[![Release: v2.7.0](https://img.shields.io/badge/Release-v2.7.0-cyan.svg)](v2.7.0/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-uber-das-projekt--entwickler-hinweis)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-vergleich-standard-fooocus-vs-aether-studio-pro-270)

</div>

---

# 🇩🇪 Deutsche Dokumentation

## 🌌 Über das Projekt & Entwickler-Hinweis

**Aether Diffusion Studio Pro** ist eine eigenständige, hochmoderne Weiterentwicklung des beliebten Open-Source-Tools **Fooocus**.

> [!NOTE]
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der aktiven **Beta-Phase (v2.7.0 Beta)**.
> 
> Da ich dieses Projekt alleine entwickle, ist Community-Feedback extrem wertvoll! Falls du Fehler findest, Verbesserungswünsche hast oder neue Ideen einbringen möchtest, eröffne bitte gerne ein Issue auf GitHub oder hinterlasse Feedback. Ich lese jeden Vorschlag und versuche, neue Features zügig einzubauen!

---

## 🔄 Was wurde in Version 2.7.0 neu hinzugefügt? (Changelog)

1. **🎭 Live Face Swap & Avatar Studio (Beta - 100% Lokal & OBS-Ready)**:
   - **Echtzeit-Webcam-Tracking**: Erkennt deine Mimik (Augen auf/zu beim Blinzeln, Mund-Öffnung beim Sprechen, Kopfneigung) direkt über die Webcam im Browser.
   - **Avatar-Mimik-Übertragung**: Lade ein beliebiges Porträt, eine Figur oder einen Körper hoch – die KI animiert Augen, Mund und Kopfbewegungen der Figur live passend zu dir!
   - **Nahtloser Face-Swap**: Tausche das Gesicht des Avatars auf deine Live-Webcam oder dein Gesicht auf den Avatar-Körper.
   - **Multi-Modell-Architektur für kleine & große GPUs**:
     - `⚡ Eco / Fast Mesh-Retarget`: Extrem ressourcenschonend, 0 MB Rest-VRAM (perfekt für RTX 3050 6GB & CPU).
     - `🎨 AI Neural FaceSwap / Expression Transfer`: Erweiterte Mimik-Erkennung für mittlere GPUs (6-12 GB VRAM).
     - `🚀 LivePortrait HD Expression Engine`: Studioqualität für große GPUs (12-16 GB+ VRAM).
     - **Automatischer 1-Klick-Download**: Lädt das Standard-Modell (`face_detection_yunet.onnx`) bei Bedarf mit einem Klick automatisch herunter.
     - **Eigener Modellordner (`models/live_faceswap/`)**: Eigene `.onnx` oder `.safetensors` Modelle einfach im Ordner ablegen; sie werden sofort erkannt.
   - **Direkte OBS Studio Einbindung**:
     - Browser-Source URL: `http://127.0.0.1:7865/live_avatar`
     - MJPEG Video-Stream: `http://127.0.0.1:7865/stream/avatar.mjpg`
     - Mit integrierter 10-Sekunden-Anleitung für OBS Studio.
   - **Beta-Status-Banner**: Transparentes Entwicklungs-Banner mit Hinweis auf experimentelle Funktion.

2. **🪄 Prompt-Magier Direkt-Erweiterung (Ohne Übersetzung)**:
   - Neuer Button `🪄 Prompt Erweitern (Ohne Übersetzung)` direkt unter dem Eingabefeld.
   - Englische Prompts können nun ohne neuronale Übersetzung direkt veredelt und detailreich ausgebaut werden.

---

## 🔄 Rückblick: Was wurde von v2.5 auf v2.6, v2.6.1, v2.6.2 und v2.6.3 geändert?

- **v2.6.3:**
  - 🧪 Offizielles Beta-Warnbanner & aufgeräumte Aktionsleisten im Vision AI Studio.
  - ❌ Automatische Negativ-Prompt-Generierung mit 1-Klick-Übernahme.
  - 📐 Bildauflösungs-Erkennung & 1-Klick-Übernahme aus Vorlage.
  - 🎛️ Eigene freie Bildauflösung mit Schiebereglern (wie in ComfyUI).
  - 💡 Detaillierter Upscale-Ratgeber (Fast 2x vs. 1.5x/2x SDXL Diffusion).
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

## 🚀 Vergleich: Standard Fooocus vs. Aether Studio Pro 2.7.0

| Funktion | Standard Fooocus (v2.5) | Aether Studio Pro (v2.6) | Aether Studio Pro (v2.6.3) | 🌌 Aether Studio Pro (v2.7.0) |
| :--- | :--- | :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles Standard-Thema | Dark Obsidian Cyber-UI | Dark Obsidian Glassmorphism | **Dark Obsidian Glassmorphism + Live-Status & Aktionsleisten** |
| **⚡ VRAM-Verwaltung** | Nur per CLI-Flag (`--lowvram`) | WebUI Dual-Engine Switch | WebUI Dual-Engine Switch | **WebUI Dual-Engine Switch + Live-Header-Badge** |
| **🧠 RAM-Schutz (OOM)**| Stürzt bei VRAM-Überlauf ab | Smart RAM Offload (32 GB) | Smart RAM Offload (32 GB) | **Smart RAM Offload (32 GB RAM Safe)** |
| **⏱️ Stop & Pause** | Wartet auf vollen Step | Sofort-Stop (Millisekunden) | Sofort-Stop & Pause | **Sofort-Stop & Pause ohne Latenz** |
| **🎭 Live Face Swap Studio**| Nicht vorhanden | Nicht vorhanden | Nicht vorhanden | **Live Face Swap & Realtime Avatar Tracking (Webcam, Augen/Mund, OBS-Stream)** |
| **🔬 Vision AI Studio** | Simpler Describe-Button | Simpler Describe-Button | Precision Vision Studio | **Precision Vision Studio: Beta-Banner, Negativ-Prompt, Res-Erkennung, 7 Filter** |
| **📐 Auflösungen** | Nur feste Presets | Nur feste Presets | ComfyUI-Style Pixel-Slider | **ComfyUI-Style Pixel-Slider + 1-Klick-Übernahme aus Vorlage** |
| **🌐 KI-Übersetzung** | Keine | Wörterbuch-Matrix | Lokaler MarianMT (0 MB VRAM) | **Lokaler neuronaler MarianMT (CPU, 0 MB VRAM)** |
| **🪄 Prompt-Ersteller**| Standard Style-Tags | Prompt-Guide Presets | KI-Prompt Magier | **KI-Prompt Magier + Direkt-Erweiterung (Ohne Übersetzung)** |
| **📥 Civitai Download** | Manuell | Manuell | 1-Klick Downloader (Beta) | **1-Klick Downloader (Beta)** |
| **🎚️ Bild-Vergleich** | Nicht vorhanden | Nicht vorhanden | Vorher/Nachher Slider | **Vorher/Nachher Slider** |
| **🧬 Modell-Ordner** | Nur SDXL | SDXL, Turbo, Flux | Universeller Ordner | **Universeller Modellordner (`all_models_sdxl_flux/`)** |

---

## 💬 Community-Feedback & Fehler melden

- 🐛 **Fehler gefunden?** Öffne gerne ein Issue auf GitHub mit Betriebssystem, Grafikkarte und Log.
- 💡 **Feedback & Wünsche:** Schreibe mir gerne, was du dir als Nächstes im Programm wünschst!
