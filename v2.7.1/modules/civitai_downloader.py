# Aether Studio Pro - Civitai Model Downloader (Beta)
import os
import re
import time
import requests
import modules.config

CIVITAI_API_BASE = "https://civitai.com/api/v1"

def parse_civitai_input(url_or_id: str):
    """
    Extracts model_id and optional version_id from Civitai URL or raw ID.
    Supports formats:
    - 123456
    - https://civitai.com/models/123456
    - https://civitai.com/models/123456/model-name
    - https://civitai.com/models/123456?modelVersionId=78910
    - https://civitai.com/api/download/models/78910
    """
    url_or_id = url_or_id.strip()
    if not url_or_id:
        return None, None
    
    # Direct version download url: /api/download/models/(\d+)
    m_dl = re.search(r'/api/download/models/(\d+)', url_or_id)
    if m_dl:
        return None, m_dl.group(1)
    
    # Model URL with modelVersionId query param
    m_ver = re.search(r'modelVersionId=(\d+)', url_or_id)
    version_id = m_ver.group(1) if m_ver else None

    # Model ID from URL /models/(\d+)
    m_model = re.search(r'/models/(\d+)', url_or_id)
    if m_model:
        model_id = m_model.group(1)
        return model_id, version_id

    # If purely digits: check if it's model_id
    if url_or_id.isdigit():
        return url_or_id, None
    
    return None, None


def fetch_civitai_metadata(url_or_id: str, api_key: str = ""):
    """
    Fetches model metadata from Civitai API.
    Returns dictionary with details or error string.
    """
    model_id, version_id = parse_civitai_input(url_or_id)
    if not model_id and not version_id:
        return {"error": "Ungültige Civitai-URL oder Modell-ID eingegeben."}
    
    headers = {
        "User-Agent": "AetherStudio/2.6 (Linux; x86_64)"
    }
    if api_key and api_key.strip():
        headers["Authorization"] = f"Bearer {api_key.strip()}"

    try:
        if version_id and not model_id:
            # Direct version endpoint
            res = requests.get(f"{CIVITAI_API_BASE}/model-versions/{version_id}", headers=headers, timeout=12)
            if res.status_code == 404:
                return {"error": f"Modell-Version {version_id} wurde auf Civitai nicht gefunden."}
            if res.status_code in (401, 403):
                return {"error": "Zugriff verweigert (HTTP 401/403). Für dieses Modell wird ein Civitai-API-Key benötigt!"}
            res.raise_for_status()
            ver_data = res.json()
            model_name = ver_data.get("model", {}).get("name", f"Model_{version_id}")
            model_type = ver_data.get("model", {}).get("type", "Checkpoint")
            selected_version = ver_data
        else:
            # Model endpoint
            res = requests.get(f"{CIVITAI_API_BASE}/models/{model_id}", headers=headers, timeout=12)
            if res.status_code == 404:
                return {"error": f"Modell {model_id} wurde auf Civitai nicht gefunden."}
            if res.status_code in (401, 403):
                return {"error": "Zugriff verweigert (HTTP 401/403). Für dieses Modell wird ein Civitai-API-Key benötigt!"}
            res.raise_for_status()
            data = res.json()
            model_name = data.get("name", f"Model_{model_id}")
            model_type = data.get("type", "Checkpoint")
            
            versions = data.get("modelVersions", [])
            if not versions:
                return {"error": "Keine Modell-Dateien/Versionen gefunden."}
            
            # If specific version requested, find it, else take the latest (first)
            selected_version = None
            if version_id:
                for v in versions:
                    if str(v.get("id")) == str(version_id):
                        selected_version = v
                        break
            if not selected_version:
                selected_version = versions[0]

        files = selected_version.get("files", [])
        if not files:
            return {"error": "Keine herunterladbaren Dateien für diese Version hinterlegt."}
        
        # Select primary model file (.safetensors preferred)
        chosen_file = None
        for f in files:
            if f.get("primary", False):
                chosen_file = f
                break
        if not chosen_file:
            for f in files:
                if f.get("name", "").endswith(".safetensors"):
                    chosen_file = f
                    break
        if not chosen_file:
            chosen_file = files[0]

        filename = chosen_file.get("name", "model.safetensors")
        size_kb = chosen_file.get("sizeKB", 0)
        size_gb = round(size_kb / (1024 * 1024), 2)
        download_url = chosen_file.get("downloadUrl", selected_version.get("downloadUrl", ""))
        base_model = selected_version.get("baseModel", "SDXL 1.0")

        # Destination folder
        m_type_lower = model_type.lower()
        if "lora" in m_type_lower or "locon" in m_type_lower:
            target_dir = modules.config.paths_checkpoints[0].replace("checkpoints", "loras")
            detected_type = "LoRA"
        elif "vae" in m_type_lower:
            target_dir = modules.config.paths_checkpoints[0].replace("checkpoints", "vae")
            detected_type = "VAE"
        elif "embedding" in m_type_lower or "textual" in m_type_lower:
            target_dir = modules.config.paths_checkpoints[0].replace("checkpoints", "embeddings")
            detected_type = "Embedding"
        else:
            # Checkpoint
            if "flux" in str(base_model).lower() or "turbo" in model_name.lower():
                target_dir = getattr(modules.config, 'path_all_models_sdxl_flux', modules.config.paths_checkpoints[0])
            else:
                target_dir = modules.config.paths_checkpoints[0]
            detected_type = "Checkpoint"

        images = selected_version.get("images", [])
        preview_url = images[0].get("url", "") if images else ""

        return {
            "success": True,
            "model_name": model_name,
            "version_name": selected_version.get("name", "Default"),
            "model_type": detected_type,
            "base_model": base_model,
            "filename": filename,
            "size_gb": size_gb,
            "download_url": download_url,
            "target_dir": target_dir,
            "preview_url": preview_url,
        }

    except Exception as e:
        return {"error": f"Fehler beim Abrufen der Civitai-Daten: {str(e)}"}


def download_file_stream(download_url: str, target_filepath: str, api_key: str = "", progress_callback=None):
    """
    Downloads file with chunk streaming and progress updates.
    """
    headers = {
        "User-Agent": "AetherStudio/2.6 (Linux; x86_64)"
    }
    if api_key and api_key.strip():
        headers["Authorization"] = f"Bearer {api_key.strip()}"
        if "?" in download_url:
            download_url += f"&token={api_key.strip()}"
        else:
            download_url += f"?token={api_key.strip()}"

    temp_filepath = target_filepath + ".downloading"
    os.makedirs(os.path.dirname(target_filepath), exist_ok=True)

    try:
        response = requests.get(download_url, headers=headers, stream=True, timeout=30, allow_redirects=True)
        if response.status_code in (401, 403):
            return False, "Fehler 401/403: Für diesen Download ist ein Civitai-API-Key erforderlich!"
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 1024 * 1024  # 1 MB chunk
        start_time = time.time()
        last_update = time.time()

        with open(temp_filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    now = time.time()
                    if now - last_update >= 0.5 or downloaded == total_size:
                        last_update = now
                        elapsed = max(now - start_time, 0.001)
                        speed_mb = (downloaded / (1024 * 1024)) / elapsed
                        percent = (downloaded / total_size * 100) if total_size > 0 else 0
                        done_mb = downloaded / (1024 * 1024)
                        total_mb = total_size / (1024 * 1024)
                        if progress_callback:
                            progress_callback(percent, done_mb, total_mb, speed_mb)

        # Download completed, rename to final file
        if os.path.exists(target_filepath):
            os.remove(target_filepath)
        os.rename(temp_filepath, target_filepath)
        return True, f"Erfolgreich heruntergeladen: {os.path.basename(target_filepath)}"

    except Exception as e:
        if os.path.exists(temp_filepath):
            try:
                os.remove(temp_filepath)
            except Exception:
                pass
        return False, f"Download-Fehler: {str(e)}"
