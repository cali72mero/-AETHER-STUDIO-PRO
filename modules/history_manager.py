import os
import glob
import shutil
import re
import json
import urllib.parse
from datetime import datetime
from pathlib import Path
from PIL import Image

import modules.config


def get_downloads_dir() -> str:
    """Returns the user's Downloads directory, creating it if needed."""
    # Check XDG user dir config if present
    xdg_file = Path.home() / ".config" / "user-dirs.dirs"
    if xdg_file.exists():
        try:
            with open(xdg_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("XDG_DOWNLOAD_DIR"):
                        parts = line.strip().split('=', 1)
                        if len(parts) == 2:
                            val = parts[1].strip('"').replace('$HOME', str(Path.home()))
                            p = Path(val)
                            p.mkdir(parents=True, exist_ok=True)
                            return str(p)
        except Exception:
            pass

    downloads_dir = Path.home() / "Downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    return str(downloads_dir)


def scan_history_images(limit: int = 100) -> list[str]:
    """Scans Fooocus outputs folder for generated images, newest first."""
    outputs_path = modules.config.path_outputs
    if not os.path.exists(outputs_path):
        return []

    images = []
    for ext in ('*.png', '*.jpg', '*.jpeg', '*.webp'):
        images.extend(glob.glob(os.path.join(outputs_path, '**', ext), recursive=True))

    # Sort descending by modification time
    images.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    if limit > 0:
        images = images[:limit]
    return images


def get_image_details(image_path: str) -> dict:
    """Extracts prompt, negative prompt, model, resolution, seed, styles, and date from log.html or metadata."""
    if not image_path or not os.path.exists(image_path):
        return {
            "filename": "",
            "filepath": "",
            "date": "",
            "prompt": "",
            "negative_prompt": "",
            "styles": "[]",
            "model": "",
            "steps": "",
            "seed": "",
            "sampler": "",
            "resolution": "",
            "info_markdown": "*Kein Bild ausgewählt.*"
        }

    filename = os.path.basename(image_path)
    mtime = os.path.getmtime(image_path)
    date_str = datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M:%S")
    folder = os.path.dirname(image_path)
    log_file = os.path.join(folder, "log.html")

    data = {}
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                html = f.read()
            pattern = re.compile(rf'<a href=\"{re.escape(filename)}\"[^>]*>.*?to_clipboard\(\'([^\']+)\'\)', re.DOTALL)
            m = pattern.search(html)
            if m:
                data = json.loads(urllib.parse.unquote(m.group(1)))
        except Exception as e:
            print(f"[HistoryManager] Error reading log.html: {e}")

    # Fallback to PIL Image info if log.html didn't contain parameters
    if not data:
        try:
            with Image.open(image_path) as img:
                info = img.info or {}
                if 'parameters' in info and info['parameters']:
                    params = info['parameters']
                    try:
                        data = json.loads(params)
                    except Exception:
                        data = {'prompt': str(params)}
        except Exception:
            pass

    prompt = data.get('prompt', '')
    negative_prompt = data.get('negative_prompt', '')
    styles = str(data.get('styles', '[]'))
    base_model = data.get('base_model', 'Unbekannt')
    steps = str(data.get('steps', ''))
    seed = str(data.get('seed', ''))
    sampler = data.get('sampler', '')
    resolution = str(data.get('resolution', ''))
    guidance_scale = str(data.get('guidance_scale', ''))

    # Build sleek markdown summary card
    md_lines = [
        f"### 🖼️ `{filename}`",
        f"**📅 Datum:** {date_str}  |  **📐 Auflösung:** {resolution}  |  **🎯 Seed:** `{seed}`",
        f"**🤖 Modell:** `{base_model}`  |  **⚡ Steps:** {steps}  |  **🎛️ CFG:** {guidance_scale}",
        f"**🎨 Stile:** {styles}",
        "",
        f"**📝 Prompt:**",
        f"> {prompt}" if prompt else "> *(Kein Prompt gespeichert)*",
    ]
    if negative_prompt:
        md_lines.extend([
            "",
            f"**🚫 Negativer Prompt:**",
            f"> {negative_prompt}"
        ])

    return {
        "filename": filename,
        "filepath": image_path,
        "date": date_str,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "styles": styles,
        "model": base_model,
        "steps": steps,
        "seed": seed,
        "sampler": sampler,
        "resolution": resolution,
        "info_markdown": "\n".join(md_lines)
    }


def copy_image_to_downloads(image_path: str) -> tuple[bool, str]:
    """Copies single image to ~/Downloads without overwriting existing files."""
    if not image_path or not os.path.exists(image_path):
        return False, "❌ Kein Bild ausgewählt oder Datei nicht gefunden."

    try:
        downloads_dir = get_downloads_dir()
        filename = os.path.basename(image_path)
        dest_path = os.path.join(downloads_dir, filename)

        # Avoid collision
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(downloads_dir, f"{base}_{counter}{ext}")):
                counter += 1
            dest_path = os.path.join(downloads_dir, f"{base}_{counter}{ext}")

        shutil.copy2(image_path, dest_path)
        dest_filename = os.path.basename(dest_path)
        return True, f"✅ Bild erfolgreich im Downloads-Ordner gespeichert!\n📁 `{dest_path}`"
    except Exception as e:
        return False, f"❌ Fehler beim Speichern: {e}"


def copy_multiple_to_downloads(image_paths: list[str]) -> tuple[bool, str]:
    """Copies list of images to ~/Downloads."""
    if not image_paths:
        return False, "❌ Keine Bilder zum Speichern vorhanden."

    downloads_dir = get_downloads_dir()
    saved_count = 0
    errors = 0

    for path in image_paths:
        if isinstance(path, (tuple, list)):
            path = path[0]
        if not path or not os.path.exists(path):
            continue
        try:
            filename = os.path.basename(path)
            dest_path = os.path.join(downloads_dir, filename)
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(downloads_dir, f"{base}_{counter}{ext}")):
                    counter += 1
                dest_path = os.path.join(downloads_dir, f"{base}_{counter}{ext}")
            shutil.copy2(path, dest_path)
            saved_count += 1
        except Exception:
            errors += 1

    return True, f"✅ {saved_count} Bild(er) erfolgreich in `{downloads_dir}` gespeichert!"
