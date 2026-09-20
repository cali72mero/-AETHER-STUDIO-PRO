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
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der aktiven **Beta-Phase (v2.7.1 Beta)**.
> 
> Da ich dieses Projekt alleine entwickle, ist Community-Feedback extrem wertvoll! Falls du Fehler findest, Verbesserungswünsche hast oder neue Ideen einbringen möchtest, eröffne bitte gerne ein Issue auf GitHub oder hinterlasse Feedback. Ich lese jeden Vorschlag und versuche, neue Features zügig einzubauen!

---

## 🔄 Was wurde in Version 2.7.1 neu hinzugefügt? (Changelog)

1. **📱 Kabellose Smartphone- & Tablet-Webcam Einbindung**:
   - **Keine PC-Webcam erforderlich!** Nutze dein iPhone, Android-Smartphone, iPad oder Zweit-Gerät als vollwertige HD-Kamera.
   - Einfach den angezeigten **QR-Code scannen** oder die Web-Adresse `http://<WLAN-IP>:7865/remote_cam` im Handy-Browser öffnen.
   - Geschützt mit automatischer **Benutzer- (`aether`) & PIN-Authentifizierung**.
   - Optionaler **1-Klick-Cloud-Tunnel** für Verbindungen über mobile Daten (4G/5G).
   - Das Smartphone streamt direkt in Fooocus: Die KI erkennt deine Mimik (Augen blinzeln, Mund bewegen, Sprechen) und animiert deinen Avatar live auf dem PC!
   - Über OBS Studio (Virtuelle Kamera) nahtlos in **OBS Studio**, **TikTok Live Studio**, **Discord**, **Zoom** & **Teams** nutzbar!

2. **⚡ Sofortiger Browser-Start mit Cyberpunk-Ladebildschirm**:
   - Beim Start öffnet sich der Browser **sofort innerhalb von 1 Sekunde** mit einem edlen Obsidian-Dark Ladebildschirm.
   - Kein langes, stummes Warten mehr im schwarzen Terminal!
   - Zeigt animierten Pulse-Spinner und Live-Fortschritt (`[1/3] System prüfen`, `[2/3] Modelle & VRAM laden`, `[3/3] Bereit`).
   - Sobald das Studio einsatzbereit ist, schaltet die Seite vollautomatisch direkt ins WebUI um.

3. **🚀 Low-VRAM & RTX 3050 Performance-Update**:
   - **Tensor Core TF32 Beschleunigung** und **cuDNN Auto-Tuning** für Ampere-Architekturen (RTX 30xx Reihe) aktiviert.
   - Optimierte VRAM-Speicherzuteilung für 6-GB-Grafikkarten: Bis zu 4,2 GB Modellgewichte bleiben direkt im VRAM, wodurch ständiges Auslagern über den PCIe-Bus in den RAM spürbar reduziert und die Bildgenerierung um 15–25 % beschleunigt wird!

4. **🐳 GitHub Actions Docker-Fix**:
   - OCI-Tag-Namenskonflikt beim automatischen GitHub-Container-Build behoben.

---

## 🔄 Was wurde in Version 2.7.0 hinzugefügt?
1. **🎭 Live Face Swap & Avatar Studio (Beta - 100% Lokal & OBS-Ready)**:
   - **Echtzeit-Webcam-Tracking**: Erkennt deine Mimik (Augen auf/zu beim Blinzeln, Mund-Öffnung beim Sprechen, Kopfneigung) direkt über die Webcam oder das Smartphone im Browser.
   - **Avatar-Mimik-Übertragung**: Lade ein beliebiges Porträt hoch – die KI animiert Augen, Mund und Kopfbewegungen der Figur synchron zu dir!
   - **Nahtloser Face-Swap**: Tausche das Gesicht des Avatars auf deine Live-Webcam oder dein Gesicht auf den Avatar-Körper.
   - **Multi-Modell-Architektur**: Eco / Fast (0 MB VRAM, RTX 3050 & CPU) bis LivePortrait HD.
   - **Direkte OBS Studio Einbindung**: `/live_avatar` (Browser-Quelle) und `/stream/avatar.mjpg` (Video-Stream).
2. **🪄 Prompt-Magier Direkt-Erweiterung (Ohne Übersetzung)**:
   - Button `🪄 Prompt Erweitern (Ohne Übersetzung)` zur schnellen Veredelung englischer Prompts.

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

## 🚀 Vergleich: Standard Fooocus vs. Aether Studio Pro 2.7.1

| Funktion | Standard Fooocus (v2.5) | Aether Studio Pro (v2.6) | Aether Studio Pro (v2.6.3) | 🌌 Aether Studio Pro (v2.7.1) |
| :--- | :--- | :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles Standard-Thema | Dark Obsidian Cyber-UI | Dark Obsidian Glassmorphism | **Dark Obsidian Glassmorphism + Sofort-Browser-Ladebildschirm** |
| **⚡ VRAM-Verwaltung** | Nur per CLI-Flag (`--lowvram`) | WebUI Dual-Engine Switch | WebUI Dual-Engine Switch | **Dual-Engine + Ampere TF32 & 6GB VRAM-Headroom Boost** |
| **🧠 RAM-Schutz (OOM)**| Stürzt bei VRAM-Überlauf ab | Smart RAM Offload (32 GB) | Smart RAM Offload (32 GB) | **Smart RAM Offload (32 GB RAM Safe)** |
| **⏱️ Stop & Pause** | Wartet auf vollen Step | Sofort-Stop (Millisekunden) | Sofort-Stop & Pause | **Sofort-Stop & Pause ohne Latenz** |
| **🎭 Live Face Swap Studio**| Nicht vorhanden | Nicht vorhanden | Nicht vorhanden | **Live Face Swap (Webcam + Smartphone drahtlos, OBS, TikTok, Discord)** |
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
