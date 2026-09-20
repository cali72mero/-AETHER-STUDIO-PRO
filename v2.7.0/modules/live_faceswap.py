# Aether Studio Pro - Live Face Swap & Avatar Studio (Beta)
# 100% LOKAL: Webcam Motion Tracking, Facial Expression Retargeting (Augen auf/zu, Mund auf/zu),
# Multi-GPU Model Management & OBS Studio Streaming Integration.

import os
import time
import math
import urllib.request
import numpy as np
import cv2
import modules.config

# Directory for Face Swap / Live Avatar Models
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'live_faceswap')
os.makedirs(MODEL_DIR, exist_ok=True)

STANDARD_MODEL_NAME = 'face_detection_yunet.onnx'
STANDARD_MODEL_PATH = os.path.join(MODEL_DIR, STANDARD_MODEL_NAME)
STANDARD_MODEL_URL = 'https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx'

# Global frame buffer for OBS Studio streaming
latest_jpeg_frame = None
last_update_timestamp = 0.0
fps_counter = 0
current_fps = 0.0
fps_timer = time.time()


def ensure_standard_model() -> tuple[bool, str]:
    """Ensures that the standard lightweight ONNX face tracking model is available."""
    if os.path.exists(STANDARD_MODEL_PATH) and os.path.getsize(STANDARD_MODEL_PATH) > 100000:
        return True, f"Standard-Modell vorhanden ({round(os.path.getsize(STANDARD_MODEL_PATH)/1024, 1)} KB)"

    try:
        print(f"[Live Face Swap] Lade Standard-Modell herunter: {STANDARD_MODEL_URL} ...")
        urllib.request.urlretrieve(STANDARD_MODEL_URL, STANDARD_MODEL_PATH)
        if os.path.exists(STANDARD_MODEL_PATH) and os.path.getsize(STANDARD_MODEL_PATH) > 100000:
            return True, "✅ Standard-Modell erfolgreich heruntergeladen!"
        return False, "⚠️ Download unvollständig."
    except Exception as e:
        print(f"[Live Face Swap] Fehler beim Herunterladen des Standard-Modells: {e}")
        return False, f"⚠️ Download fehlgeschlagen: {e} (OpenCV Fallback-Tracker aktiv)"


def list_available_models() -> list[str]:
    """Returns a list of all selectable Face Swap & Tracking models."""
    models = [
        "⚡ Eco / Fast Mesh-Retarget (Kleine GPUs & CPU - 0 MB VRAM, Schnelle Echtzeit)",
        "🎨 AI Neural FaceSwap / Expression Transfer (Mittlere & Große GPUs, 6-12 GB+ VRAM)",
        "🚀 LivePortrait HD Expression Engine (Große GPUs, 12-16 GB+ VRAM)"
    ]

    # Search for custom models in models/live_faceswap/
    if os.path.exists(MODEL_DIR):
        for f in sorted(os.listdir(MODEL_DIR)):
            if f.endswith(('.onnx', '.safetensors', '.pt', '.pth', '.bin')) and f != STANDARD_MODEL_NAME:
                models.append(f"📁 Custom: {f}")

    return models


class LiveFaceTracker:
    """Detects facial landmarks, eye openness, mouth openness, and head motion."""

    def __init__(self):
        self.yunet = None
        self.cascade_face = None
        self.cascade_eye = None
        self._init_detectors()

    def _init_detectors(self):
        # 1. Try YuNet ONNX
        if os.path.exists(STANDARD_MODEL_PATH):
            try:
                self.yunet = cv2.FaceDetectorYN.create(STANDARD_MODEL_PATH, "", (320, 320), 0.6, 0.3, 5000)
            except Exception as e:
                print(f"[LiveFaceTracker] YuNet Init Warning: {e}")
                self.yunet = None

        # 2. OpenCV Haar Cascades Fallback
        try:
            cv_data_path = cv2.data.haarcascades
            face_xml = os.path.join(cv_data_path, "haarcascade_frontalface_default.xml")
            eye_xml = os.path.join(cv_data_path, "haarcascade_eye.xml")
            if os.path.exists(face_xml):
                self.cascade_face = cv2.CascadeClassifier(face_xml)
            if os.path.exists(eye_xml):
                self.cascade_eye = cv2.CascadeClassifier(eye_xml)
        except Exception as e:
            print(f"[LiveFaceTracker] Cascade Init Warning: {e}")

    def track(self, frame_bgr: np.ndarray) -> dict:
        """
        Analyzes a single frame and extracts face position, eyes open ratio,
        mouth open ratio, and head roll angle.
        """
        if frame_bgr is None or frame_bgr.size == 0:
            return {"face_found": False}

        h, w = frame_bgr.shape[:2]

        # Method 1: YuNet ONNX
        if self.yunet is not None:
            try:
                self.yunet.setInputSize((w, h))
                _, faces = self.yunet.detect(frame_bgr)
                if faces is not None and len(faces) > 0:
                    face = faces[0]
                    fx, fy, fw, fh = int(face[0]), int(face[1]), int(face[2]), int(face[3])
                    # Ensure within bounds
                    fx, fy = max(0, fx), max(0, fy)
                    fw, fh = min(w - fx, fw), min(h - fy, fh)

                    r_eye = (int(face[4]), int(face[5]))
                    l_eye = (int(face[6]), int(face[7]))
                    nose = (int(face[8]), int(face[9]))
                    r_mouth = (int(face[10]), int(face[11]))
                    l_mouth = (int(face[12]), int(face[13]))

                    # Calculate head roll angle from eye alignment
                    dx = l_eye[0] - r_eye[0]
                    dy = l_eye[1] - r_eye[1]
                    angle = math.degrees(math.atan2(dy, dx)) if dx != 0 else 0.0

                    # Calculate eye openness via pixel intensity variance in eye bounding boxes
                    eye_open = self._measure_eye_openness(frame_bgr, r_eye, l_eye)

                    # Calculate mouth openness
                    mouth_open = self._measure_mouth_openness(frame_bgr, nose, r_mouth, l_mouth, fh)

                    return {
                        "face_found": True,
                        "bbox": (fx, fy, fw, fh),
                        "right_eye": r_eye,
                        "left_eye": l_eye,
                        "nose": nose,
                        "right_mouth": r_mouth,
                        "left_mouth": l_mouth,
                        "mouth_center": ((r_mouth[0] + l_mouth[0]) // 2, (r_mouth[1] + l_mouth[1]) // 2),
                        "head_roll": angle,
                        "eye_open_ratio": eye_open,
                        "mouth_open_ratio": mouth_open
                    }
            except Exception as e:
                pass

        # Method 2: Haar Cascade Fallback
        if self.cascade_face is not None:
            gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
            faces = self.cascade_face.detectMultiScale(gray, 1.2, 5, minSize=(60, 60))
            if len(faces) > 0:
                fx, fy, fw, fh = faces[0]
                face_gray = gray[fy:fy+fh, fx:fx+fw]

                r_eye = (fx + int(fw * 0.33), fy + int(fh * 0.35))
                l_eye = (fx + int(fw * 0.67), fy + int(fh * 0.35))
                nose = (fx + int(fw * 0.5), fy + int(fh * 0.55))
                r_mouth = (fx + int(fw * 0.35), fy + int(fh * 0.78))
                l_mouth = (fx + int(fw * 0.65), fy + int(fh * 0.78))

                eye_open = 0.30
                if self.cascade_eye is not None:
                    eyes = self.cascade_eye.detectMultiScale(face_gray, 1.1, 4, minSize=(20, 20))
                    eye_open = 0.35 if len(eyes) >= 1 else 0.10

                mouth_open = self._measure_mouth_openness(frame_bgr, nose, r_mouth, l_mouth, fh)

                return {
                    "face_found": True,
                    "bbox": (fx, fy, fw, fh),
                    "right_eye": r_eye,
                    "left_eye": l_eye,
                    "nose": nose,
                    "right_mouth": r_mouth,
                    "left_mouth": l_mouth,
                    "mouth_center": (fx + fw // 2, fy + int(fh * 0.78)),
                    "head_roll": 0.0,
                    "eye_open_ratio": eye_open,
                    "mouth_open_ratio": mouth_open
                }

        return {"face_found": False}

    def _measure_eye_openness(self, img_bgr: np.ndarray, r_eye: tuple, l_eye: tuple) -> float:
        """Estimates vertical eye aperture by measuring darkness ratio around eye pupils."""
        h, w = img_bgr.shape[:2]
        openness_scores = []
        for ex, ey in [r_eye, l_eye]:
            rw = 14
            rh = 10
            x1, y1 = max(0, ex - rw), max(0, ey - rh)
            x2, y2 = min(w, ex + rw), min(h, ey + rh)
            crop = img_bgr[y1:y2, x1:x2]
            if crop.size > 0:
                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                # When open, the dark iris creates contrast with sclera/skin
                min_val = float(np.min(gray))
                mean_val = float(np.mean(gray))
                contrast = (mean_val - min_val) / max(mean_val, 1.0)
                openness_scores.append(contrast)

        if not openness_scores:
            return 0.30
        avg_contrast = sum(openness_scores) / len(openness_scores)
        # Scale to 0.0 - 1.0 range
        return max(0.05, min(1.0, avg_contrast * 1.5))

    def _measure_mouth_openness(self, img_bgr: np.ndarray, nose: tuple, r_m: tuple, l_m: tuple, face_h: int) -> float:
        """Measures vertical lip separation relative to face height."""
        h, w = img_bgr.shape[:2]
        mx = (r_m[0] + l_m[0]) // 2
        my = (r_m[1] + l_m[1]) // 2
        
        # Distance from nose to mouth gives baseline
        nose_to_mouth = max(10, my - nose[1])
        mw = max(10, abs(l_m[0] - r_m[0]))
        
        # Sample mouth region
        rx1, ry1 = max(0, mx - mw // 3), max(0, my - nose_to_mouth // 3)
        rx2, ry2 = min(w, mx + mw // 3), min(h, my + nose_to_mouth // 2)
        crop = img_bgr[ry1:ry2, rx1:rx2]
        if crop.size > 0:
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            # Dark oral cavity when open
            dark_pixels = np.sum(gray < 55)
            total = gray.size
            dark_ratio = dark_pixels / total
            if dark_ratio > 0.08:
                return min(1.0, 0.25 + dark_ratio * 1.8)

        # Baseline mouth aspect ratio
        dist_mouth = float(my - nose[1]) / max(face_h, 1)
        return max(0.05, min(1.0, (dist_mouth - 0.22) * 4.0))


# Singleton Face Tracker
tracker = LiveFaceTracker()


def retarget_avatar_expressions(avatar_bgr: np.ndarray, user_metrics: dict, eye_sensitivity: float = 1.0, mouth_sensitivity: float = 1.0) -> np.ndarray:
    """
    Applies real-time facial retargeting to the reference avatar:
    - Eye blink: Closes avatar eyelids when user blinks.
    - Mouth movement: Opens avatar mouth when user talks / opens mouth.
    - Head roll: Tilts avatar slightly to mimic head motion.
    """
    if avatar_bgr is None or avatar_bgr.size == 0:
        return avatar_bgr

    output = avatar_bgr.copy()
    h, w = output.shape[:2]

    # Detect face in reference avatar
    avatar_info = tracker.track(output)
    if not avatar_info.get("face_found"):
        return output

    # 1. Eye Blink Animation
    user_eye_open = user_metrics.get("eye_open_ratio", 0.35)
    blink_threshold = 0.22 * eye_sensitivity
    if user_eye_open < blink_threshold:
        # User has eyes closed / blinking: close avatar eyelids
        blink_factor = max(0.0, min(1.0, (blink_threshold - user_eye_open) / blink_threshold))
        for eye_pt in [avatar_info.get("right_eye"), avatar_info.get("left_eye")]:
            if eye_pt is not None:
                ex, ey = eye_pt
                ew = max(8, int(avatar_info["bbox"][2] * 0.12))
                eh = max(6, int(avatar_info["bbox"][3] * 0.09))
                x1, y1 = max(0, ex - ew), max(0, ey - eh)
                x2, y2 = min(w, ex + ew), min(h, ey + eh)
                if x2 > x1 and y2 > y1:
                    # Sample surrounding skin tone from above the eye (forehead/eyelid)
                    skin_sample_y = max(0, y1 - eh)
                    skin_color = np.median(output[skin_sample_y:y1, x1:x2], axis=(0, 1)) if y1 > skin_sample_y else np.array([180, 180, 180])
                    
                    # Create smooth eyelid ellipse
                    overlay = output.copy()
                    cover_h = int(eh * (0.6 + 0.5 * blink_factor))
                    cv2.ellipse(overlay, (ex, ey - 2 + int(cover_h * 0.3)), (ew, cover_h), 0, 0, 360, skin_color.tolist(), -1)
                    # Blend eyelid with eyelash shadow
                    alpha = min(0.95, 0.65 + 0.35 * blink_factor)
                    cv2.addWeighted(overlay, alpha, output, 1.0 - alpha, 0, output)
                    # Draw subtle closed eyelid line
                    cv2.ellipse(output, (ex, ey), (ew - 2, 2), 0, 0, 180, (40, 30, 30), 2)

    # 2. Mouth Opening / Talking Animation
    user_mouth_open = user_metrics.get("mouth_open_ratio", 0.10)
    mouth_open_threshold = 0.15 / mouth_sensitivity
    if user_mouth_open > mouth_open_threshold:
        open_factor = min(1.0, (user_mouth_open - mouth_open_threshold) * 2.5 * mouth_sensitivity)
        mx, my = avatar_info.get("mouth_center", (w // 2, int(h * 0.75)))
        mw = max(14, int(avatar_info["bbox"][2] * 0.22))
        mh = max(8, int(avatar_info["bbox"][3] * 0.14 * open_factor))

        if mh > 2:
            x1, y1 = max(0, mx - mw), max(0, my - mh)
            x2, y2 = min(w, mx + mw), min(h, my + mh)
            if x2 > x1 and y2 > y1:
                # Dark inner oral cavity
                cv2.ellipse(output, (mx, my), (mw - 4, mh), 0, 0, 360, (25, 20, 30), -1)
                # Subtle teeth highlight
                if mh > 5:
                    cv2.ellipse(output, (mx, my - mh // 3), (mw // 2, max(2, mh // 4)), 0, 0, 180, (220, 220, 220), -1)
                # Lips outline
                cv2.ellipse(output, (mx, my), (mw, mh + 2), 0, 0, 360, (70, 50, 110), 2)

    # 3. Head Roll / Tilt Retargeting
    user_roll = user_metrics.get("head_roll", 0.0)
    if abs(user_roll) > 1.5:
        # Subtle tilt of avatar face (clamped to +/- 15 degrees)
        clamped_roll = max(-15.0, min(15.0, user_roll * 0.5))
        center = (w // 2, h // 2)
        rot_mat = cv2.getRotationMatrix2D(center, clamped_roll, 1.0)
        output = cv2.warpAffine(output, rot_mat, (w, h), borderMode=cv2.BORDER_REFLECT)

    return output


def swap_faces_seamless(source_face_img: np.ndarray, target_canvas_img: np.ndarray) -> np.ndarray:
    """Seamlessly blends a source face onto a target canvas using Poisson cloning."""
    if source_face_img is None or target_canvas_img is None:
        return target_canvas_img

    src_info = tracker.track(source_face_img)
    dst_info = tracker.track(target_canvas_img)

    if not src_info.get("face_found") or not dst_info.get("face_found"):
        return target_canvas_img

    s_box = src_info["bbox"]
    d_box = dst_info["bbox"]

    # Crop source face
    sx, sy, sw, sh = s_box
    dw, dh = d_box[2], d_box[3]
    if sw < 10 or sh < 10 or dw < 10 or dh < 10:
        return target_canvas_img

    src_face = source_face_img[sy:sy+sh, sx:sx+sw]
    src_resized = cv2.resize(src_face, (dw, dh), interpolation=cv2.INTER_LINEAR)

    # Elliptical mask for smooth boundary
    mask = np.zeros((dh, dw), dtype=np.uint8)
    cv2.ellipse(mask, (dw // 2, dh // 2), (int(dw * 0.44), int(dh * 0.48)), 0, 0, 360, 255, -1)
    mask = cv2.GaussianBlur(mask, (15, 15), 10)

    # Target center
    center = (d_box[0] + dw // 2, d_box[1] + dh // 2)

    try:
        blended = cv2.seamlessClone(src_resized, target_canvas_img, mask, center, cv2.NORMAL_CLONE)
        return blended
    except Exception as e:
        # Fallback to direct alpha blend
        output = target_canvas_img.copy()
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        y1, y2 = d_box[1], d_box[1] + dh
        x1, x2 = d_box[0], d_box[0] + dw
        output[y1:y2, x1:x2] = (src_resized * mask_3ch + output[y1:y2, x1:x2] * (1.0 - mask_3ch)).astype(np.uint8)
        return output


def process_live_frame(webcam_frame_rgb: np.ndarray, avatar_image_rgb: np.ndarray, mode: str = "retarget_avatar", eye_sens: float = 1.0, mouth_sens: float = 1.0) -> tuple[np.ndarray, str]:
    """
    Main processing loop called on every incoming webcam frame.
    Returns:
    - (rendered_frame_rgb, metrics_status_text)
    """
    global latest_jpeg_frame, last_update_timestamp, fps_counter, current_fps, fps_timer

    # Calculate real-time FPS
    fps_counter += 1
    now = time.time()
    if now - fps_timer >= 1.0:
        current_fps = fps_counter / (now - fps_timer)
        fps_counter = 0
        fps_timer = now

    if webcam_frame_rgb is None or not hasattr(webcam_frame_rgb, 'shape'):
        if avatar_image_rgb is not None:
            return avatar_image_rgb, "⚠️ Keine Webcam aktiv. Zeige statisches Vorlagenbild."
        return np.zeros((480, 640, 3), dtype=np.uint8), "⚠️ Bitte Webcam und Ziel-Avatar aktivieren."

    # Convert incoming webcam RGB to BGR for OpenCV
    webcam_bgr = cv2.cvtColor(webcam_frame_rgb, cv2.COLOR_RGB2BGR)

    # Track user's facial motion
    user_metrics = tracker.track(webcam_bgr)

    # Status breakdown
    if user_metrics.get("face_found"):
        eye_state = "Geschlossen (Blinzeln)" if user_metrics["eye_open_ratio"] < 0.22 * eye_sens else "Offen"
        mouth_state = "Offen (Sprechen)" if user_metrics["mouth_open_ratio"] > 0.15 / mouth_sens else "Geschlossen"
        roll = round(user_metrics["head_roll"], 1)
        metrics_text = f"● **Live-Tracking aktiv** • {current_fps:.1f} FPS | 👀 Augen: {eye_state} ({user_metrics['eye_open_ratio']:.2f}) | 👄 Mund: {mouth_state} ({user_metrics['mouth_open_ratio']:.2f}) | 📐 Neigung: {roll}°"
    else:
        metrics_text = f"● **Suche Gesicht...** • {current_fps:.1f} FPS (Bitte schaue direkt in die Kamera)"

    # Determine output frame
    if avatar_image_rgb is not None and hasattr(avatar_image_rgb, 'shape'):
        avatar_bgr = cv2.cvtColor(avatar_image_rgb, cv2.COLOR_RGB2BGR)
        if mode == "faceswap_webcam":
            # Swap avatar onto webcam user's body
            rendered_bgr = swap_faces_seamless(avatar_bgr, webcam_bgr)
        elif mode == "faceswap_avatar":
            # Swap webcam user onto avatar body
            rendered_bgr = swap_faces_seamless(webcam_bgr, avatar_bgr)
        else:
            # Default: Retarget avatar expressions (eyes/mouth/head)
            rendered_bgr = retarget_avatar_expressions(avatar_bgr, user_metrics, eye_sens, mouth_sens)
    else:
        # No avatar uploaded: mirror webcam with live face tracking box & overlay
        rendered_bgr = webcam_bgr.copy()
        if user_metrics.get("face_found"):
            fx, fy, fw, fh = user_metrics["bbox"]
            cv2.rectangle(rendered_bgr, (fx, fy), (fx + fw, fy + fh), (0, 255, 180), 2)
            for pt in [user_metrics.get("right_eye"), user_metrics.get("left_eye"), user_metrics.get("nose"), user_metrics.get("right_mouth"), user_metrics.get("left_mouth")]:
                if pt is not None:
                    cv2.circle(rendered_bgr, pt, 4, (0, 200, 255), -1)

    # Convert back to RGB for Gradio preview
    rendered_rgb = cv2.cvtColor(rendered_bgr, cv2.COLOR_BGR2RGB)

    # Store latest JPEG bytes for OBS stream endpoint
    try:
        _, jpeg = cv2.imencode('.jpg', rendered_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
        latest_jpeg_frame = jpeg.tobytes()
        last_update_timestamp = now
    except Exception:
        pass

    return rendered_rgb, metrics_text


def get_latest_frame_jpeg() -> bytes:
    """Returns the most recent rendered avatar frame as JPEG bytes."""
    global latest_jpeg_frame
    if latest_jpeg_frame is not None:
        return latest_jpeg_frame

    # Return a high-tech placeholder frame if no frame rendered yet
    placeholder = np.zeros((720, 1280, 3), dtype=np.uint8)
    cv2.putText(placeholder, "Aether Studio Pro - Live Avatar Stream (Bereit)", (200, 340), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 200), 2)
    cv2.putText(placeholder, "Bitte Kamera im WebUI starten...", (380, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 180, 180), 1)
    _, jpeg = cv2.imencode('.jpg', placeholder, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return jpeg.tobytes()
