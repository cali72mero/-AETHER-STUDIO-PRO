# Aether Studio Pro - Interactive Before / After Comparison Slider
import base64
import io
from PIL import Image

def pil_to_base64(image):
    if image is None:
        return ""
    if not isinstance(image, Image.Image):
        try:
            image = Image.fromarray(image)
        except Exception:
            return ""
    
    buffered = io.BytesIO()
    # Convert RGBA to RGB if saving as JPEG or preserve PNG
    if image.mode in ("RGBA", "P"):
        image.save(buffered, format="PNG")
        mime = "image/png"
    else:
        image.save(buffered, format="JPEG", quality=92)
        mime = "image/jpeg"
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:{mime};base64,{img_str}"


def generate_comparison_html(img_before, img_after) -> str:
    """
    Renders an interactive Before / After slider widget in HTML/CSS/JS.
    Drag the slider left and right to compare before & after images.
    """
    if img_before is None or img_after is None:
        return """
        <div style="text-align: center; padding: 40px; border: 2px dashed rgba(255,255,255,0.15); border-radius: 12px; background: rgba(15,23,42,0.6); color: #94a3b8;">
            <div style="font-size: 32px; margin-bottom: 10px;">🎚️</div>
            <div style="font-size: 16px; font-weight: 600; color: #f8fafc;">Vorher / Nachher Bildvergleich</div>
            <div style="font-size: 13px; margin-top: 5px;">Lade zwei Bilder (Vorher & Nachher) hoch oder generiere eine Bildvariante / Upscale, um sie hier interaktiv zu vergleichen.</div>
        </div>
        """

    b64_before = pil_to_base64(img_before)
    b64_after = pil_to_base64(img_after)

    if not b64_before or not b64_after:
        return "<div style='color: #ef4444;'>Fehler beim Laden der Bilddaten für den Vergleich.</div>"

    html = f"""
    <div class="aether-compare-wrapper" style="position: relative; width: 100%; max-width: 900px; margin: 0 auto; user-select: none;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px; font-weight: 700; color: #94a3b8;">
            <span style="color: #38bdf8;">◀ 1. Vorher (Original / Vorbereitung)</span>
            <span style="color: #a855f7;">2. Nachher (Aether Generierung / Upscale) ▶</span>
        </div>
        
        <div class="aether-compare-container" style="position: relative; width: 100%; height: 550px; overflow: hidden; border-radius: 14px; border: 1px solid rgba(255,255,255,0.15); background: #090d16; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
            <!-- After image (Base) -->
            <img src="{b64_after}" alt="Nachher" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; display: block;" />
            
            <!-- Before image (Clipped Overlay) -->
            <div class="compare-overlay" style="position: absolute; top: 0; left: 0; width: 50%; height: 100%; overflow: hidden; border-right: 2px solid #38bdf8; box-shadow: 2px 0 12px rgba(56, 189, 248, 0.6); pointer-events: none;">
                <img src="{b64_before}" alt="Vorher" style="position: absolute; top: 0; left: 0; width: 900px; max-width: none; height: 100%; object-fit: contain;" />
                <div style="position: absolute; top: 12px; left: 12px; background: rgba(15,23,42,0.85); color: #38bdf8; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; border: 1px solid rgba(56, 189, 248, 0.4); backdrop-filter: blur(4px);">VORHER</div>
            </div>
            
            <div style="position: absolute; top: 12px; right: 12px; background: rgba(15,23,42,0.85); color: #c084fc; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; border: 1px solid rgba(192, 132, 252, 0.4); backdrop-filter: blur(4px); pointer-events: none;">NACHHER</div>

            <!-- Draggable divider handle -->
            <div class="compare-handle" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0ea5e9, #a855f7); box-shadow: 0 0 15px rgba(56,189,248,0.8); display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 14px; pointer-events: none; z-index: 5;">
                &#10231;
            </div>

            <!-- Invisible range input for dragging -->
            <input type="range" min="0" max="100" value="50" 
                   oninput="
                     var p = this.parentElement;
                     var overlay = p.querySelector('.compare-overlay');
                     var handle = p.querySelector('.compare-handle');
                     var img = overlay.querySelector('img');
                     overlay.style.width = this.value + '%';
                     handle.style.left = this.value + '%';
                     img.style.width = p.clientWidth + 'px';
                   "
                   style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: ew-resize; z-index: 10; margin: 0; padding: 0;" />
        </div>
        <div style="text-align: center; margin-top: 8px; font-size: 11px; color: #64748b;">
            💡 Ziehe den Schieberegler mit der Maus nach links und rechts, um die Details zu vergleichen.
        </div>
    </div>
    """
    return html
