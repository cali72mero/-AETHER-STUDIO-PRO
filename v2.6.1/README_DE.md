<div align="center">

# 🌌 Aether Diffusion Studio Pro 2.6 (Beta)
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
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.6-yellow.svg)](#-community-feedback--fehler-melden)
[![Release: v2.6.0](https://img.shields.io/badge/Release-v2.6.0-cyan.svg)](v2.6/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-uber-das-projekt--entwickler-hinweis)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-vergleich-standard-fooocus-vs-aether-studio-pro-26)

</div>

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
