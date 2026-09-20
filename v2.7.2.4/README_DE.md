<div align="center">

# 🌌 Aether Diffusion Studio Pro 2.7.2.4 (Beta)
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
[![Status: Beta](https://img.shields.io/badge/Status-Beta%20v2.7.2.4-yellow.svg)](#-community-feedback--fehler-melden)
[![Release: v2.7.2.4](https://img.shields.io/badge/Release-v2.7.2.4-cyan.svg)](v2.7.2.4/)
[![Developer: Solo Project](https://img.shields.io/badge/Developer-Solo%20Dev-purple.svg)](#-uber-das-projekt--entwickler-hinweis)
[![UI: Dark Obsidian](https://img.shields.io/badge/UI-Dark%20Obsidian%20Glass-cyan.svg)](#-vergleich-standard-fooocus-vs-aether-studio-pro-2722)

</div>

---

# 🇩🇪 Deutsche Dokumentation

## 🌌 Über das Projekt & Entwickler-Hinweis

**Aether Diffusion Studio Pro** ist eine eigenständige, hochmoderne Weiterentwicklung des beliebten Open-Source-Tools **Fooocus**.

> [!NOTE]
> Dieses Projekt wird von einem **einzelnen, unabhängigen Entwickler** mit viel Leidenschaft aufgebaut und weiterentwickelt. Das Projekt befindet sich aktuell in der aktiven **Beta-Phase (v2.7.2.4 Beta)**.
> 
> Da ich dieses Projekt alleine entwickle, ist Community-Feedback extrem wertvoll! Falls du Fehler findest, Verbesserungswünsche hast oder neue Ideen einbringen möchtest, eröffne bitte gerne ein Issue auf GitHub oder hinterlasse Feedback. Ich lese jeden Vorschlag und versuche, neue Features zügig einzubauen!

> [!WARNING]
> ### ⚠️ Wichtiger Hinweis zu Stabilität & Beta-Versionen
> - **🟢 Stabile Versionen (Alle Versionen unter 2.7):**  
>   Alle Versionen **unter 2.7** (wie **v2.5**, **v2.6**, **v2.6.1**, **v2.6.2**, **v2.6.3**) laufen stabil und zuverlässig auf allen unterstützten Systemen.
> - **🟡 Beta-Versionen (Ab Version 2.7 und höher):**  
>   Alle Versionen **ab 2.7** (v2.7.0, v2.7.1, v2.7.2, v2.7.2.1, v2.7.2.2, v2.7.2.3, v2.7.2.4) sind **aktive Beta-Versionen** mit neuesten experimentellen Funktionen.  
>   *Hinweis: Auf einigen Geräten oder Hardware-Konfigurationen können Beta-Versionen zu Problemen führen oder gar nicht starten.*
> 
> ### ⚠️ Status des Face Swap Features (Aktuell fehlerhaft / In Überarbeitung)
> **Wichtiger Hinweis zum Live Face Swap & Smartphone-Kamera-Feature:**  
> Die Funktion **Live Face Swap & Live Avatar Studio** ist derzeit **nicht stabil nutzbar bzw. läuft nur mit Fehlern** (insbesondere bei der Video-Erfassung und Smartphone-Übertragung auf mobilen Endgeräten).  
> **Dieser Fehler ist bekannt und wird in Kürze in einem kommenden Update behoben!**  
> Alle Standard-Funktionen von Aether Studio Pro (Text-to-Image Bildgenerierung, Inpainting, Outpainting, Vision AI Studio, Custom Steps) sind davon nicht betroffen und laufen gewohnt stabil.

---

## 🔄 Was wurde in Version 2.7.2.4 neu hinzugefügt? (Changelog)

1. **📱 iOS Safari & WebKit Inline-Video Autoplay Fix**:
   - `webkit-playsinline`, `playsinline` und explizites `muted = true` / `defaultMuted = true` ergänzt, damit iOS Safari das Kamerabild nicht mehr blockiert oder beim Abspielen einfriert.
2. **🎛️ Visuelle In-Page Fehler- & Diagnosekarte**:
   - `alert()` (wird von Safari-Pop-up-Blockern stumm unterdrückt) durch eine interaktive Informationskarte direkt auf der Seite ersetzt.
   - Sofortiges Button-Feedback (`⌛ Kamera wird gestartet...`) und `touchend`-Unterstützung für verzögerungsfreies Antippen auf Mobilgeräten.
3. **⚡ Überlastungsschutz im Frame-Loop**:
   - Verhindert Netzwerkstau bei der Bildübertragung vom Handy an den PC.

---

## 🔄 Was wurde in Version 2.7.2.3 hinzugefügt?

1. **📱 iPhone & Safari Remote-Kamera HTTPS Cloud-Tunnel Fix**:
   - Fehler `TypeError: expected str, bytes or os.PathLike object, not NoneType` im Gradio-Tunnel behoben, indem ein sicherer 32-Byte Secret Token erzeugt wird.
   - Der öffentliche HTTPS-Tunnel (`https://....gradio.live`) startet nun mit 1 Klick fehlerfrei und liefert echte SSL-Zertifikate, wodurch Apple Safari auf dem iPhone den Kamerazugriff sofort erlaubt.
2. **🌐 Standard LAN-Bindung (`listen="0.0.0.0"`)**:
   - Fooocus bindet standardmäßig an alle Netzwerkadressen (`0.0.0.0`), sodass Geräte im selben WLAN direkt zugreifen können.

1. **🔧 Startfehler behoben (Torch Import in Model Management)**:
   - Behoben: `NameError: name 'torch' is not defined` beim Start des Studios in `ldm_patched/modules/model_management.py`.
   - Die Tensor Core TF32 Beschleunigung und das cuDNN Auto-Tuning für NVIDIA Ampere (RTX 3050+) initialisieren nun fehlerfrei.

---

## 🔄 Was wurde in Version 2.7.2.1 hinzugefügt?

1. **🎯 Benutzerdefinierte Performance & freie Step-Einstellung (`Custom (Eigene Schritte)`)**:
   - Neuer Performance-Modus **Custom (Eigene Schritte)** direkt neben Speed, Quality, Lightning, Hyper-SD, Extreme Speed und Turbo.
   - Öffnet ein edles Obsidian-Cyberpunk Bedienfeld direkt unter der Performance-Auswahl.
2. **🎛️ Dualer Schieberegler & Direkteingabe für Sampling Steps (1–200 Steps)**:
   - Frei wählbare Schrittanzahl von **1 bis 200 Schritten** (z. B. 15, 20, 25, 40, 50, 75, 100 Steps).
   - Schieberegler und Zahlenfeld sind live synchronisiert: Du kannst bequem ziehen oder die exakte Zahl per Tastatur eintippen!
3. **⚡ Nahtlose Diffusions-Pipeline Übernahme**:
   - Die KI generiert Bilder exakt mit deiner gewählten Schrittzahl.
   - Volle Kompatibilität mit allen Samplern, LoRAs, Refinern und Bild-Stilen.

---

## 🔄 Was wurde in Version 2.7.2 hinzugefügt?

1. **🎨 Anime vs. Fotorealismus Bild-Typ Selektor**:
   - Manuelle Umschaltung im Vision AI Studio zwischen:
     - `🔍 Automatisch erkennen` (Intelligente Erkennung anhand visueller Deskriptoren)
     - `📸 Realistisches Foto / Fotorealismus` (Fokus auf Hauttextur, Licht, Fotografie)
     - `🎨 Anime / Manga / Illustration` (Fokus auf Danbooru-Tags, Cel-Shading, Lineart)
   - **Anime-Modus**: Entfernt fotorealistische Kamera-Termini (`dslr, 35mm, f/1.8 lens, raw photo`), die bei Anime-Modellen zu Bildfehlern führen, und injiziert saubere Danbooru-Struktur.
   - **Fotorealismus-Modus**: Entfernt Anime-Tags (`1girl, flat color, 2d`), priorisiert natürliche BLIP-Bildbeschreibungen und hochwertige Fotodetails (`raw photo, 8k uhd, dslr, soft cinematic lighting, film grain`).

2. **🎯 Ziel-Modell Profilierung & automatische Prompt-Anpassung**:
   - Dropdown mit allen aktuell heruntergeladenen Checkpoint-Modellen (z. B. `animagineXL40_v4Opt`, `juggernautXL_v8Rundiffusion`, `animaPencilXL`, `jedpointreal` oder `[Automatisch anpassen]`).
   - Die KI passt die Prompt-Syntax vollautomatisch an die Besonderheiten des Zielmodells an:
     - **Pony Diffusion Modelle**: Fügt automatisch `score_9, score_8_up, score_7_up, rating_safe` sowie angepasste Negativ-Scores ein.
     - **Animagine Modelle**: Ergänzt `masterpiece, best quality, ultra-detailed anime, aesthetic`.
     - **Fotorealistische SDXL Modelle**: Ergänzt Kamera- und Beleuchtungs-Modifier.
   - **Blitzschnelle Reaktion**: Ändert man Ziel-Modell oder Bild-Typ, werden Positiv- und Negativ-Prompt in **1 Millisekunde** neu berechnet – ohne das Bild erneut analysieren zu müssen!

---

## 🔄 Was wurde in Version 2.7.1 hinzugefügt?

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

## 🚀 Vergleich: Standard Fooocus vs. Aether Studio Pro 2.7.2.2

| Funktion | Standard Fooocus (v2.5) | Aether Studio Pro (v2.6) | Aether Studio Pro (v2.6.3) | 🌌 Aether Studio Pro (v2.7.2.2) |
| :--- | :--- | :--- | :--- | :--- |
| **🎨 Benutzeroberfläche** | Helles Standard-Thema | Dark Obsidian Cyber-UI | Dark Obsidian Glassmorphism | **Dark Obsidian Glassmorphism + Sofort-Browser-Ladebildschirm** |
| **⚡ Performance & Steps** | Nur feste Presets | Nur feste Presets | Nur feste Presets | **Presets (Quality, Speed, Turbo) + 🎯 Eigene Steps (1-200 Schieberegler)** |
| **⚡ VRAM-Verwaltung** | Nur per CLI-Flag (`--lowvram`) | WebUI Dual-Engine Switch | WebUI Dual-Engine Switch | **Dual-Engine + Ampere TF32 & 6GB VRAM-Headroom Boost** |
| **🧠 RAM-Schutz (OOM)**| Stürzt bei VRAM-Überlauf ab | Smart RAM Offload (32 GB) | Smart RAM Offload (32 GB) | **Smart RAM Offload (32 GB RAM Safe)** |
| **⏱️ Stop & Pause** | Wartet auf vollen Step | Sofort-Stop (Millisekunden) | Sofort-Stop & Pause | **Sofort-Stop & Pause ohne Latenz** |
| **🎭 Live Face Swap Studio**| Nicht vorhanden | Nicht vorhanden | Nicht vorhanden | **Live Face Swap (Webcam + Smartphone drahtlos, OBS, TikTok, Discord)** |
| **🔬 Vision AI Studio** | Simpler Describe-Button | Simpler Describe-Button | Precision Vision Studio | **Precision Vision Studio: Anime vs. Realismus, Ziel-Modell Profilierung, Neg-Prompt, 7 Filter** |
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
