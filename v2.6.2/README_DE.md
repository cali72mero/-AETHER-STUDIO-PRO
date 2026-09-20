<div align="center">

# 🌌 Aether Diffusion Studio Pro 2.6.2 (Beta)
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
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.6.2-yellow.svg)](#-community-feedback--fehler-melden)
[![Release: v2.6.2](https://img.shields.io/badge/Release-v2.6.2-cyan.svg)](v2.6.2/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-uber-das-projekt--entwickler-hinweis)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-vergleich-standard-fooocus-vs-aether-studio-pro-262)

</div>

---

# 🇩🇪 Deutsche Dokumentation

## 🌌 Über das Projekt & Entwickler-Hinweis

**Aether Diffusion Studio Pro** ist eine eigenständige, hochmoderne Weiterentwicklung des beliebten Open-Source-Tools **Fooocus**.

> [!NOTE]
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der aktiven **Beta-Phase (v2.6.2 Beta)**.
> 
> Da ich dieses Projekt alleine entwickle, ist Community-Feedback extrem wertvoll! Falls du Fehler findest, Verbesserungswünsche hast oder neue Ideen einbringen möchtest, eröffne bitte gerne ein Issue auf GitHub oder hinterlasse Feedback. Ich lese jeden Vorschlag und versuche, neue Features zügig einzubauen!

---

## 🔄 Was wurde in Version 2.6.2 neu hinzugefügt? (Changelog)

1. **🔬 Precision Vision AI Studio & Reverse Prompting (100% Lokal)**:
   - Hochdetaillierte Bildanalyse durch die Kombination von natürlicher Sprachbeschreibung (BLIP) und tiefgehender SDXL-Tag-Erkennung (WD14).
   - Erstellt fertige, hochpräzise Prompts für eine 1:1-Bildrekonstruktion in SDXL.
   - **0 MB dauerhafter VRAM-Verbrauch**: Alle Seh-Modelle entladen ihren Grafikspeicher direkt nach Abschluss der Analyse (`torch.cuda.empty_cache()` + `gc.collect()`), sodass der volle GPU-Speicher für die Bilderzeugung frei bleibt.
2. **🖌️ Interaktives Pinsel- & Maskierungswerkzeug (`tool='sketch'`)**:
   - Zeichne direkt mit dem Pinsel auf das hochgeladene Bild:
     - **Ganzes Bild analysieren**: Vollständige Bildauswertung ohne Maskierung.
     - **Markierten Bereich ignorieren (ausschließen)**: Pinselstriche maskieren Bildbereiche schwarz aus, sodass die KI sie vollständig ignoriert.
     - **Nur markierten Bereich analysieren (Fokus)**: Die Umgebung wird ausgeblendet – die KI analysiert gezielt nur das eingemalte Detail.
3. **🎛️ Selektive Attribut-Filterung in 7 Kategorien**:
   - Strukturierte Zerlegung des Bildes in:
     - `👤 Subjekt & Motiv` (Personen, Hauptmotive)
     - `💇 Haare & Gesicht` (Haarfarbe, Schnitt, Blick)
     - `👗 Kleidung & Outfit` (Kleidung, Accessoires, Rüstung)
     - `🏞️ Hintergrund & Szene` (Landschaft, Räume, Details)
     - `💡 Licht & Atmosphäre` (Lichtführung, Schatten, Farben)
     - `🎨 Kunststil & Medium` (3D, Foto, Comic, Anime)
     - `📐 Kamera & Perspektive` (Nahaufnahme, Weitwinkel, Winkel)
   - **Standardmäßig sind alle 7 Kategorien ausgewählt** (für 1:1 Prompt-Generierung).
   - Einzelne Kategorien können per Checkbox abgewählt werden; der finale Prompt passt sich in Echtzeit an.
4. **🎯 Gezielte Attribut-Ersetzung im bestehenden Prompt**:
   - Behalte deinen geschriebenen Prompt und ersetze gezielt nur einzelne Merkmale aus dem Bild:
     - `👗 Nur Kleidung übertragen`
     - `💇 Nur Haare & Gesicht übertragen`
     - `🏞️ Nur Hintergrund übertragen`
     - `💡 Nur Licht übertragen`
     - `🎨 Nur Stil übertragen`

---

## 🔄 Rückblick: Was wurde von v2.5 auf v2.6 und v2.6.1 geändert?

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

## 🚀 Vergleich: Standard Fooocus vs. Aether Studio Pro 2.6.2

| Funktion | Standard Fooocus (v2.5) | Aether Studio Pro (v2.6) | Aether Studio Pro (v2.6.1) | 🌌 Aether Studio Pro (v2.6.2) |
| :--- | :--- | :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles Standard-Thema | Dark Obsidian Cyber-UI | Dark Obsidian Glassmorphism | **Dark Obsidian Glassmorphism + Live-Status** |
| **⚡ VRAM-Verwaltung** | Nur per CLI-Flag (`--lowvram`) | WebUI Dual-Engine Switch | WebUI Dual-Engine Switch | **WebUI Dual-Engine Switch + Live-Header-Badge** |
| **🧠 RAM-Schutz (OOM)**| Stürzt bei VRAM-Überlauf ab | Smart RAM Offload (32 GB) | Smart RAM Offload (32 GB) | **Smart RAM Offload (32 GB RAM Safe)** |
| **⏱️ Stop & Pause** | Wartet auf vollen Step | Sofort-Stop (Millisekunden) | Sofort-Stop & Pause | **Sofort-Stop & Pause ohne Latenz** |
| **🔬 Vision AI Studio** | Simpler Describe-Button | Simpler Describe-Button | Simpler Describe-Button | **Precision Vision Studio: Pinsel-Maske (Ignorieren/Fokus), 7 Attribut-Filter, Gezielte Ersetzung** |
| **🌐 KI-Übersetzung** | Keine | Wörterbuch-Matrix | Lokaler MarianMT (0 MB VRAM) | **Lokaler neuronaler MarianMT (CPU, 0 MB VRAM)** |
| **🪄 Prompt-Ersteller**| Standard Style-Tags | Prompt-Guide Presets | KI-Prompt Magier | **KI-Prompt Magier + Vision Prompt Builder** |
| **📥 Civitai Download** | Manuell | Manuell | 1-Klick Downloader (Beta) | **1-Klick Downloader (Beta)** |
| **🎚️ Bild-Vergleich** | Nicht vorhanden | Nicht vorhanden | Vorher/Nachher Slider | **Vorher/Nachher Slider** |
| **🧬 Modell-Ordner** | Nur SDXL | SDXL, Turbo, Flux | Universeller Ordner | **Universeller Modellordner (`all_models_sdxl_flux/`)** |

---

## 💬 Community-Feedback & Fehler melden

- 🐛 **Fehler gefunden?** Öffne gerne ein Issue auf GitHub mit Betriebssystem, Grafikkarte und Log.
- 💡 **Feedback & Wünsche:** Schreibe mir gerne, was du dir als Nächstes im Programm wünschst!
