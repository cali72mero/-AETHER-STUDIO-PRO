import gradio as gr
import random
import os
import json
import time
import shared
import modules.config
import fooocus_version
import modules.html
import modules.async_worker as worker
import modules.constants as constants
import modules.flags as flags
import modules.gradio_hijack as grh
import modules.style_sorter as style_sorter
import modules.meta_parser
import args_manager
import copy
import launch
from extras.inpaint_mask import SAMOptions

from modules.sdxl_styles import legal_style_names
from modules.private_logger import get_current_html_path
from modules.ui_gradio_extensions import reload_javascript
from modules.auth import auth_enabled, check_auth
from modules.util import is_json
import glob
import modules.history_manager as history_manager
import modules.prompt_guide as prompt_guide
import modules.model_checker as model_checker
import modules.civitai_downloader as civitai_downloader
import modules.prompt_magier as prompt_magier
import modules.comparison_slider as comparison_slider
from PIL import Image

def get_task(*args):
    args = list(args)
    args.pop(0)

    return worker.AsyncTask(args=args)

def generate_clicked(task: worker.AsyncTask):
    import ldm_patched.modules.model_management as model_management

    model_management.set_paused(False)
    with model_management.interrupt_processing_mutex:
        model_management.interrupt_processing = False
    # outputs=[progress_html, progress_window, progress_gallery, gallery]

    if len(task.args) == 0:
        return

    execution_start_time = time.perf_counter()
    finished = False

    yield gr.update(visible=True, value=modules.html.make_progress_html(1, 'Waiting for task to start ...')), \
        gr.update(visible=True, value=None), \
        gr.update(visible=False, value=None), \
        gr.update(visible=False)

    worker.async_tasks.append(task)

    while not finished:
        time.sleep(0.01)
        if len(task.yields) > 0:
            flag, product = task.yields.pop(0)
            if flag == 'preview':

                # help bad internet connection by skipping duplicated preview
                if len(task.yields) > 0:  # if we have the next item
                    if task.yields[0][0] == 'preview':   # if the next item is also a preview
                        # print('Skipped one preview for better internet connection.')
                        continue

                percentage, title, image = product
                yield gr.update(visible=True, value=modules.html.make_progress_html(percentage, title)), \
                    gr.update(visible=True, value=image) if image is not None else gr.update(), \
                    gr.update(), \
                    gr.update(visible=False)
            if flag == 'results':
                yield gr.update(visible=True), \
                    gr.update(visible=True), \
                    gr.update(visible=True, value=product), \
                    gr.update(visible=False)
            if flag == 'finish':
                if not args_manager.args.disable_enhance_output_sorting:
                    product = sort_enhance_images(product, task)

                yield gr.update(visible=False), \
                    gr.update(visible=False), \
                    gr.update(visible=False), \
                    gr.update(visible=True, value=product)
                finished = True

                # delete Fooocus temp images, only keep gradio temp images
                if args_manager.args.disable_image_log:
                    for filepath in product:
                        if isinstance(filepath, str) and os.path.exists(filepath):
                            os.remove(filepath)

    execution_time = time.perf_counter() - execution_start_time
    print(f'Total time: {execution_time:.2f} seconds')
    return


def sort_enhance_images(images, task):
    if not task.should_enhance or len(images) <= task.images_to_enhance_count:
        return images

    sorted_images = []
    walk_index = task.images_to_enhance_count

    for index, enhanced_img in enumerate(images[:task.images_to_enhance_count]):
        sorted_images.append(enhanced_img)
        if index not in task.enhance_stats:
            continue
        target_index = walk_index + task.enhance_stats[index]
        if walk_index < len(images) and target_index <= len(images):
            sorted_images += images[walk_index:target_index]
        walk_index += task.enhance_stats[index]

    return sorted_images


def inpaint_mode_change(mode, inpaint_engine_version):
    assert mode in modules.flags.inpaint_options

    # inpaint_additional_prompt, outpaint_selections, example_inpaint_prompts,
    # inpaint_disable_initial_latent, inpaint_engine,
    # inpaint_strength, inpaint_respective_field

    if mode == modules.flags.inpaint_option_detail:
        return [
            gr.update(visible=True), gr.update(visible=False, value=[]),
            gr.Dataset.update(visible=True, samples=modules.config.example_inpaint_prompts),
            False, 'None', 0.5, 0.0
        ]

    if inpaint_engine_version == 'empty':
        inpaint_engine_version = modules.config.default_inpaint_engine_version

    if mode == modules.flags.inpaint_option_modify:
        return [
            gr.update(visible=True), gr.update(visible=False, value=[]),
            gr.Dataset.update(visible=False, samples=modules.config.example_inpaint_prompts),
            True, inpaint_engine_version, 1.0, 0.0
        ]

    return [
        gr.update(visible=False, value=''), gr.update(visible=True),
        gr.Dataset.update(visible=False, samples=modules.config.example_inpaint_prompts),
        False, inpaint_engine_version, 1.0, 0.618
    ]


reload_javascript()

import ldm_patched.modules.model_management as model_management

def render_header_bar(is_eco: bool = True):
    if is_eco:
        vram_badge = '<span class="aether-hw-badge aether-badge-eco"><strong class="aether-hw-tag" style="color: #34d399;">🌱 VRAM-SPARMODUS:</strong> <span style="color:#a7f3d0; font-weight:700;">AKTIV</span> (Eco-VRAM)</span>'
    else:
        vram_badge = '<span class="aether-hw-badge aether-badge-speed"><strong class="aether-hw-tag" style="color: #38bdf8;">⚡ NORMALMODUS:</strong> <span style="color:#bae6fd; font-weight:700;">MAX SPEED</span> (Sparmodus AUS)</span>'

    return f"""
        <div class="aether-header-bar-inner">
            <div class="aether-brand-title-group">
                <span class="aether-symbol">◈</span>
                <span class="aether-studio-title">AETHER <span class="aether-accent-text">STUDIO PRO</span></span>
                <span class="aether-studio-version">v2.6.1 NEXT-GEN</span>
                <span class="aether-divider-pipe">|</span>
                <span class="aether-hw-badge"><strong class="aether-hw-tag">GPU</strong> RTX 3050 (6GB)</span>
                <span class="aether-hw-badge"><strong class="aether-hw-tag">RAM</strong> 32 GB Hybrid</span>
                {vram_badge}
            </div>
            <div class="aether-status-group">
                <span class="aether-online-pulse"></span>
                <span class="aether-status-badge-text">SYSTEM BEREIT</span>
            </div>
        </div>
    """

def render_vram_info(is_eco: bool = True):
    if is_eco:
        return """### 🟢 Status: 🌱 VRAM-Sparmodus ist AKTIV
*Das System spart maximal Grafikspeicher, damit selbst große Modelle stabil laufen.*

- **📊 VRAM-Verbrauch:** Stark reduziert (~2 bis 3 GB VRAM).
- **⚙️ Funktionsweise:** Gewichte des Modells werden in kleineren Teilmengen auf der GPU berechnet und bei Bedarf dynamisch im 32 GB RAM abgelegt.
- **✨ Vorteile:**
  - Kein VRAM Out-of-Memory (OOM) Absturz.
  - Lässt große SDXL-, Turbo- und FLUX-Modelle sowie mehrere LoRAs problemlos auf der 6 GB RTX 3050 laufen.
- **⚠️ Einschränkungen:**
  - Durch das kontinuierliche Hin- und Herladen über die PCIe-Schnittstelle in den RAM ist die Bildberechnung **etwas langsamer** als im Normalmodus.
"""
    else:
        return """### ⚡ Status: ⚡ Normalmodus ist AKTIV (Maximales Tempo)
*Das System nutzt die volle Geschwindigkeit der RTX 3050 ohne Drosselung oder RAM-Transfer.*

- **📊 VRAM-Verbrauch:** Vollständig / Normal (Gesamtes Modell wird im GPU-VRAM gehalten).
- **⚙️ Funktionsweise:** Keine Auslagerungs-Latenzen während des Samplings; das Modell läuft dauerhaft auf voller GPU-Bandbreite.
- **✨ Vorteile:**
  - **Maximale Generierungsgeschwindigkeit!** Keine Verzögerungen durch RAM-Speichertransfers.
- **⚠️ Einschränkungen:**
  - Das Modell muss komplett in den 5,72 GB VRAM deiner RTX 3050 passen.
  - Wenn ein Modell zu groß ist (z.B. große Checkpoints mit vielen LoRAs), bricht die Generierung ab bzw. benötigt die Option 'Modell in RAM mitladen'.
"""

title = 'Aether Diffusion Studio Pro 2.6.1 • Autonomous Neural AI'

if isinstance(args_manager.args.preset, str):
    title += ' [' + args_manager.args.preset + ']'

shared.gradio_root = gr.Blocks(title=title).queue()

with shared.gradio_root:
    currentTask = gr.State(worker.AsyncTask(args=[]))
    inpaint_engine_state = gr.State('empty')
    with gr.Row(elem_classes=['aether-header-bar']):
        header_bar_html = gr.HTML(value=render_header_bar(is_eco=model_management.is_vram_sparmodus()))
    with gr.Row():
        with gr.Column(scale=2):
            with gr.Row():
                progress_window = grh.Image(label='Preview', show_label=True, visible=False, height=768,
                                            elem_classes=['main_view'])
                progress_gallery = gr.Gallery(label='Finished Images', show_label=True, object_fit='contain',
                                              height=768, visible=False, elem_classes=['main_view', 'image_gallery'])
            progress_html = gr.HTML(value=modules.html.make_progress_html(32, 'Progress 32%'), visible=False,
                                    elem_id='progress-bar', elem_classes='progress-bar')
            gallery = gr.Gallery(label='Gallery', show_label=False, object_fit='contain', visible=True, height=768,
                                 elem_classes=['resizable_area', 'main_view', 'final_gallery', 'image_gallery'],
                                 elem_id='final_gallery')
            with gr.Row(elem_classes=['quick_download_row']):
                quick_download_btn = gr.Button(value="💾 In Downloads speichern", elem_classes=['comfy-quick-download-btn'], scale=1)
                quick_download_status = gr.Markdown(value="", elem_id='quick_download_status', scale=3)
            last_selected_main_image = gr.State("")
            with gr.Row():
                with gr.Column(scale=17):
                    prompt = gr.Textbox(show_label=False, placeholder="Prompt hier eingeben oder Bildbeschreibung verfassen...", elem_id='positive_prompt',
                                        autofocus=True, lines=3)

                    with gr.Row(elem_classes=['prompt_magier_row'], visible=False) as prompt_magier_row:
                        prompt_magier_btn = gr.Button(value="✨ Prompt verzaubern (Deutsch ➔ Magisches Englisch)", variant="secondary", elem_classes=['prompt_magier_btn'], scale=1)

                    default_prompt = modules.config.default_prompt
                    if isinstance(default_prompt, str) and default_prompt != '':
                        shared.gradio_root.load(lambda: default_prompt, outputs=prompt)

                with gr.Column(scale=3, min_width=0):
                    generate_button = gr.Button(label="Generate", value="⚡ Generieren", elem_classes=['type_row', 'aether_btn_generate'], elem_id='generate_button', visible=True)
                    reset_button = gr.Button(label="Reconnect", value="🔄 Neu verbinden", elem_classes=['type_row', 'aether_btn_reconnect'], elem_id='reset_button', visible=False)
                    load_parameter_button = gr.Button(label="Load Parameters", value="Parameter laden", elem_classes=['type_row', 'aether_btn_params'], elem_id='load_parameter_button', visible=False)
                    with gr.Row(elem_classes=['aether_action_subrow']):
                        pause_button = gr.Button(label="Pause", value="⏸️ Pause", elem_classes=['type_row_half', 'aether_btn_pause'], elem_id='pause_button', visible=False)
                        skip_button = gr.Button(label="Skip", value="⏭️ Skip", elem_classes=['type_row_half', 'aether_btn_skip'], elem_id='skip_button', visible=False)
                    stop_button = gr.Button(label="Stop", value="⏹️ Sofort-Stopp", elem_classes=['type_row_half', 'aether_btn_stop'], elem_id='stop_button', visible=False)

                    def stop_clicked(currentTask):
                        import ldm_patched.modules.model_management as model_management
                        currentTask.last_stop = 'stop'
                        model_management.set_paused(False)
                        if currentTask.processing:
                            model_management.interrupt_current_processing(True)
                        return currentTask

                    def skip_clicked(currentTask):
                        import ldm_patched.modules.model_management as model_management
                        currentTask.last_stop = 'skip'
                        model_management.set_paused(False)
                        if currentTask.processing:
                            model_management.interrupt_current_processing(True)
                        return currentTask

                    def pause_clicked():
                        import ldm_patched.modules.model_management as model_management
                        now_paused = model_management.toggle_paused()
                        new_label = "▶️ Weiter" if now_paused else "⏸️ Pause"
                        return gr.update(value=new_label)

                    stop_button.click(stop_clicked, inputs=currentTask, outputs=currentTask, queue=False, show_progress=False, _js='cancelGenerateForever')
                    skip_button.click(skip_clicked, inputs=currentTask, outputs=currentTask, queue=False, show_progress=False)
                    pause_button.click(pause_clicked, inputs=[], outputs=[pause_button], queue=False, show_progress=False)
            with gr.Row(elem_classes='advanced_check_row'):
                input_image_checkbox = gr.Checkbox(label='Input Image', value=modules.config.default_image_prompt_checkbox, container=False, elem_classes='min_check')
                enhance_checkbox = gr.Checkbox(label='Enhance', value=modules.config.default_enhance_checkbox, container=False, elem_classes='min_check')
                advanced_checkbox = gr.Checkbox(label='Advanced', value=modules.config.default_advanced_checkbox, container=False, elem_classes='min_check')
            with gr.Row(visible=modules.config.default_image_prompt_checkbox) as image_input_panel:
                with gr.Tabs(selected=modules.config.default_selected_image_input_tab_id):
                    with gr.Tab(label='Upscale or Variation', id='uov_tab') as uov_tab:
                        with gr.Row():
                            with gr.Column():
                                uov_input_image = grh.Image(label='Image', source='upload', type='numpy', show_label=False)
                            with gr.Column():
                                uov_method = gr.Radio(label='Upscale or Variation:', choices=flags.uov_list, value=modules.config.default_uov_method)
                                gr.HTML('<a href="https://github.com/lllyasviel/Fooocus/discussions/390" target="_blank">\U0001F4D4 Documentation</a>')
                    with gr.Tab(label='Image Prompt', id='ip_tab') as ip_tab:
                        with gr.Row():
                            ip_images = []
                            ip_types = []
                            ip_stops = []
                            ip_weights = []
                            ip_ctrls = []
                            ip_ad_cols = []
                            for image_count in range(modules.config.default_controlnet_image_count):
                                image_count += 1
                                with gr.Column():
                                    ip_image = grh.Image(label='Image', source='upload', type='numpy', show_label=False, height=300, value=modules.config.default_ip_images[image_count])
                                    ip_images.append(ip_image)
                                    ip_ctrls.append(ip_image)
                                    with gr.Column(visible=modules.config.default_image_prompt_advanced_checkbox) as ad_col:
                                        with gr.Row():
                                            ip_stop = gr.Slider(label='Stop At', minimum=0.0, maximum=1.0, step=0.001, value=modules.config.default_ip_stop_ats[image_count])
                                            ip_stops.append(ip_stop)
                                            ip_ctrls.append(ip_stop)

                                            ip_weight = gr.Slider(label='Weight', minimum=0.0, maximum=2.0, step=0.001, value=modules.config.default_ip_weights[image_count])
                                            ip_weights.append(ip_weight)
                                            ip_ctrls.append(ip_weight)

                                        ip_type = gr.Radio(label='Type', choices=flags.ip_list, value=modules.config.default_ip_types[image_count], container=False)
                                        ip_types.append(ip_type)
                                        ip_ctrls.append(ip_type)

                                        ip_type.change(lambda x: flags.default_parameters[x], inputs=[ip_type], outputs=[ip_stop, ip_weight], queue=False, show_progress=False)
                                    ip_ad_cols.append(ad_col)
                        ip_advanced = gr.Checkbox(label='Advanced', value=modules.config.default_image_prompt_advanced_checkbox, container=False)
                        gr.HTML('* \"Image Prompt\" is powered by Aether Neural Mixture Engine (v2.6.1).')

                        def ip_advance_checked(x):
                            return [gr.update(visible=x)] * len(ip_ad_cols) + \
                                [flags.default_ip] * len(ip_types) + \
                                [flags.default_parameters[flags.default_ip][0]] * len(ip_stops) + \
                                [flags.default_parameters[flags.default_ip][1]] * len(ip_weights)

                        ip_advanced.change(ip_advance_checked, inputs=ip_advanced,
                                           outputs=ip_ad_cols + ip_types + ip_stops + ip_weights,
                                           queue=False, show_progress=False)

                    with gr.Tab(label='Inpaint or Outpaint', id='inpaint_tab') as inpaint_tab:
                        with gr.Row():
                            with gr.Column():
                                inpaint_input_image = grh.Image(label='Image', source='upload', type='numpy', tool='sketch', height=500, brush_color="#FFFFFF", elem_id='inpaint_canvas', show_label=False)
                                inpaint_advanced_masking_checkbox = gr.Checkbox(label='Enable Advanced Masking Features', value=modules.config.default_inpaint_advanced_masking_checkbox)
                                inpaint_mode = gr.Dropdown(choices=modules.flags.inpaint_options, value=modules.config.default_inpaint_method, label='Method')
                                inpaint_additional_prompt = gr.Textbox(placeholder="Describe what you want to inpaint.", elem_id='inpaint_additional_prompt', label='Inpaint Additional Prompt', visible=False)
                                outpaint_selections = gr.CheckboxGroup(choices=['Left', 'Right', 'Top', 'Bottom'], value=[], label='Outpaint Direction')
                                example_inpaint_prompts = gr.Dataset(samples=modules.config.example_inpaint_prompts,
                                                                     label='Additional Prompt Quick List',
                                                                     components=[inpaint_additional_prompt],
                                                                     visible=False)
                                gr.HTML('* Powered by Aether Neural Inpaint Studio Engine')
                                example_inpaint_prompts.click(lambda x: x[0], inputs=example_inpaint_prompts, outputs=inpaint_additional_prompt, show_progress=False, queue=False)

                            with gr.Column(visible=modules.config.default_inpaint_advanced_masking_checkbox) as inpaint_mask_generation_col:
                                inpaint_mask_image = grh.Image(label='Mask Upload', source='upload', type='numpy', tool='sketch', height=500, brush_color="#FFFFFF", mask_opacity=1, elem_id='inpaint_mask_canvas')
                                invert_mask_checkbox = gr.Checkbox(label='Invert Mask When Generating', value=modules.config.default_invert_mask_checkbox)
                                inpaint_mask_model = gr.Dropdown(label='Mask generation model',
                                                                 choices=flags.inpaint_mask_models,
                                                                 value=modules.config.default_inpaint_mask_model)
                                inpaint_mask_cloth_category = gr.Dropdown(label='Cloth category',
                                                             choices=flags.inpaint_mask_cloth_category,
                                                             value=modules.config.default_inpaint_mask_cloth_category,
                                                             visible=False)
                                inpaint_mask_dino_prompt_text = gr.Textbox(label='Detection prompt', value='', visible=False, info='Use singular whenever possible', placeholder='Describe what you want to detect.')
                                example_inpaint_mask_dino_prompt_text = gr.Dataset(
                                    samples=modules.config.example_enhance_detection_prompts,
                                    label='Detection Prompt Quick List',
                                    components=[inpaint_mask_dino_prompt_text],
                                    visible=modules.config.default_inpaint_mask_model == 'sam')
                                example_inpaint_mask_dino_prompt_text.click(lambda x: x[0],
                                                                            inputs=example_inpaint_mask_dino_prompt_text,
                                                                            outputs=inpaint_mask_dino_prompt_text,
                                                                            show_progress=False, queue=False)

                                with gr.Accordion("Advanced options", visible=False, open=False) as inpaint_mask_advanced_options:
                                    inpaint_mask_sam_model = gr.Dropdown(label='SAM model', choices=flags.inpaint_mask_sam_model, value=modules.config.default_inpaint_mask_sam_model)
                                    inpaint_mask_box_threshold = gr.Slider(label="Box Threshold", minimum=0.0, maximum=1.0, value=0.3, step=0.05)
                                    inpaint_mask_text_threshold = gr.Slider(label="Text Threshold", minimum=0.0, maximum=1.0, value=0.25, step=0.05)
                                    inpaint_mask_sam_max_detections = gr.Slider(label="Maximum number of detections", info="Set to 0 to detect all", minimum=0, maximum=10, value=modules.config.default_sam_max_detections, step=1, interactive=True)
                                generate_mask_button = gr.Button(value='Generate mask from image')

                                def generate_mask(image, mask_model, cloth_category, dino_prompt_text, sam_model, box_threshold, text_threshold, sam_max_detections, dino_erode_or_dilate, dino_debug):
                                    from extras.inpaint_mask import generate_mask_from_image

                                    extras = {}
                                    sam_options = None
                                    if mask_model == 'u2net_cloth_seg':
                                        extras['cloth_category'] = cloth_category
                                    elif mask_model == 'sam':
                                        sam_options = SAMOptions(
                                            dino_prompt=dino_prompt_text,
                                            dino_box_threshold=box_threshold,
                                            dino_text_threshold=text_threshold,
                                            dino_erode_or_dilate=dino_erode_or_dilate,
                                            dino_debug=dino_debug,
                                            max_detections=sam_max_detections,
                                            model_type=sam_model
                                        )

                                    mask, _, _, _ = generate_mask_from_image(image, mask_model, extras, sam_options)

                                    return mask


                                inpaint_mask_model.change(lambda x: [gr.update(visible=x == 'u2net_cloth_seg')] +
                                                                    [gr.update(visible=x == 'sam')] * 2 +
                                                                    [gr.Dataset.update(visible=x == 'sam',
                                                                                       samples=modules.config.example_enhance_detection_prompts)],
                                                          inputs=inpaint_mask_model,
                                                          outputs=[inpaint_mask_cloth_category,
                                                                   inpaint_mask_dino_prompt_text,
                                                                   inpaint_mask_advanced_options,
                                                                   example_inpaint_mask_dino_prompt_text],
                                                          queue=False, show_progress=False)

                    with gr.Tab(label='Describe', id='describe_tab') as describe_tab:
                        with gr.Row():
                            with gr.Column():
                                describe_input_image = grh.Image(label='Image', source='upload', type='numpy', show_label=False)
                            with gr.Column():
                                describe_methods = gr.CheckboxGroup(
                                    label='Content Type',
                                    choices=flags.describe_types,
                                    value=modules.config.default_describe_content_type)
                                describe_apply_styles = gr.Checkbox(label='Apply Styles', value=modules.config.default_describe_apply_prompts_checkbox)
                                describe_btn = gr.Button(value='Describe this Image into Prompt')
                                describe_image_size = gr.Textbox(label='Image Size and Recommended Size', elem_id='describe_image_size', visible=False)
                                gr.HTML('<a href="https://github.com/lllyasviel/Fooocus/discussions/1363" target="_blank">\U0001F4D4 Documentation</a>')

                                def trigger_show_image_properties(image):
                                    value = modules.util.get_image_size_info(image, modules.flags.sdxl_aspect_ratios)
                                    return gr.update(value=value, visible=True)

                                describe_input_image.upload(trigger_show_image_properties, inputs=describe_input_image,
                                                            outputs=describe_image_size, show_progress=False, queue=False)

                    with gr.Tab(label='Enhance', id='enhance_tab') as enhance_tab:
                        with gr.Row():
                            with gr.Column():
                                enhance_input_image = grh.Image(label='Use with Enhance, skips image generation', source='upload', type='numpy')
                                gr.HTML('<a href="https://github.com/lllyasviel/Fooocus/discussions/3281" target="_blank">\U0001F4D4 Documentation</a>')

                    with gr.Tab(label='Metadata', id='metadata_tab') as metadata_tab:
                        with gr.Column():
                            metadata_input_image = grh.Image(label='For images created by Aether Diffusion Studio', source='upload', type='pil')
                            metadata_json = gr.JSON(label='Metadata')
                            metadata_import_button = gr.Button(value='Apply Metadata')

                        def trigger_metadata_preview(file):
                            parameters, metadata_scheme = modules.meta_parser.read_info_from_image(file)

                            results = {}
                            if parameters is not None:
                                results['parameters'] = parameters

                            if isinstance(metadata_scheme, flags.MetadataScheme):
                                results['metadata_scheme'] = metadata_scheme.value

                            return results

                        metadata_input_image.upload(trigger_metadata_preview, inputs=metadata_input_image,
                                                    outputs=metadata_json, queue=False, show_progress=True)

                    with gr.Tab(label='🎚️ Vorher/Nachher Vergleich', id='comparison_tab') as comparison_tab:
                        with gr.Row():
                            with gr.Column(scale=1):
                                comp_before_img = grh.Image(label='1. Bild Vorher (Original)', source='upload', type='pil')
                                comp_after_img = grh.Image(label='2. Bild Nachher (Bearbeitet)', source='upload', type='pil')
                                with gr.Row():
                                    comp_update_btn = gr.Button('🔄 Slider aktualisieren', variant='primary')
                                    comp_load_uov_btn = gr.Button('📥 Von Upscale/Vary übernehmen', variant='secondary')
                            with gr.Column(scale=2):
                                comp_html_viewer = gr.HTML(value=comparison_slider.generate_comparison_html(None, None))

                        def on_comp_update(b, a):
                            return comparison_slider.generate_comparison_html(b, a)

                        def on_comp_load_uov(uov_img, gal):
                            after_img = None
                            if gal and len(gal) > 0:
                                try:
                                    first_item = gal[0]
                                    if isinstance(first_item, dict) and 'name' in first_item:
                                        after_img = Image.open(first_item['name'])
                                    elif isinstance(first_item, str):
                                        after_img = Image.open(first_item)
                                except Exception:
                                    pass
                            before_pil = None
                            if uov_img is not None:
                                try:
                                    before_pil = Image.fromarray(uov_img) if not isinstance(uov_img, Image.Image) else uov_img
                                except Exception:
                                    before_pil = None
                            html = comparison_slider.generate_comparison_html(before_pil, after_img)
                            return before_pil, after_img, html

                        comp_update_btn.click(on_comp_update, inputs=[comp_before_img, comp_after_img], outputs=comp_html_viewer, queue=False)
                        comp_before_img.change(on_comp_update, inputs=[comp_before_img, comp_after_img], outputs=comp_html_viewer, queue=False)
                        comp_after_img.change(on_comp_update, inputs=[comp_before_img, comp_after_img], outputs=comp_html_viewer, queue=False)
                        comp_load_uov_btn.click(on_comp_load_uov, inputs=[uov_input_image, gallery], outputs=[comp_before_img, comp_after_img, comp_html_viewer], queue=False)

            with gr.Row(visible=modules.config.default_enhance_checkbox) as enhance_input_panel:
                with gr.Tabs():
                    with gr.Tab(label='Upscale or Variation'):
                        with gr.Row():
                            with gr.Column():
                                enhance_uov_method = gr.Radio(label='Upscale or Variation:', choices=flags.uov_list,
                                                              value=modules.config.default_enhance_uov_method)
                                enhance_uov_processing_order = gr.Radio(label='Order of Processing',
                                                                        info='Use before to enhance small details and after to enhance large areas.',
                                                                        choices=flags.enhancement_uov_processing_order,
                                                                        value=modules.config.default_enhance_uov_processing_order)
                                enhance_uov_prompt_type = gr.Radio(label='Prompt',
                                                                   info='Choose which prompt to use for Upscale or Variation.',
                                                                   choices=flags.enhancement_uov_prompt_types,
                                                                   value=modules.config.default_enhance_uov_prompt_type,
                                                                   visible=modules.config.default_enhance_uov_processing_order == flags.enhancement_uov_after)

                                enhance_uov_processing_order.change(lambda x: gr.update(visible=x == flags.enhancement_uov_after),
                                                                    inputs=enhance_uov_processing_order,
                                                                    outputs=enhance_uov_prompt_type,
                                                                    queue=False, show_progress=False)
                                gr.HTML('<a href="https://github.com/lllyasviel/Fooocus/discussions/3281" target="_blank">\U0001F4D4 Documentation</a>')
                    enhance_ctrls = []
                    enhance_inpaint_mode_ctrls = []
                    enhance_inpaint_engine_ctrls = []
                    enhance_inpaint_update_ctrls = []
                    for index in range(modules.config.default_enhance_tabs):
                        with gr.Tab(label=f'#{index + 1}') as enhance_tab_item:
                            enhance_enabled = gr.Checkbox(label='Enable', value=False, elem_classes='min_check',
                                                          container=False)

                            enhance_mask_dino_prompt_text = gr.Textbox(label='Detection prompt',
                                                                       info='Use singular whenever possible',
                                                                       placeholder='Describe what you want to detect.',
                                                                       interactive=True,
                                                                       visible=modules.config.default_enhance_inpaint_mask_model == 'sam')
                            example_enhance_mask_dino_prompt_text = gr.Dataset(
                                samples=modules.config.example_enhance_detection_prompts,
                                label='Detection Prompt Quick List',
                                components=[enhance_mask_dino_prompt_text],
                                visible=modules.config.default_enhance_inpaint_mask_model == 'sam')
                            example_enhance_mask_dino_prompt_text.click(lambda x: x[0],
                                                                        inputs=example_enhance_mask_dino_prompt_text,
                                                                        outputs=enhance_mask_dino_prompt_text,
                                                                        show_progress=False, queue=False)

                            enhance_prompt = gr.Textbox(label="Enhancement positive prompt",
                                                        placeholder="Uses original prompt instead if empty.",
                                                        elem_id='enhance_prompt')
                            enhance_negative_prompt = gr.Textbox(label="Enhancement negative prompt",
                                                                 placeholder="Uses original negative prompt instead if empty.",
                                                                 elem_id='enhance_negative_prompt')

                            with gr.Accordion("Detection", open=False):
                                enhance_mask_model = gr.Dropdown(label='Mask generation model',
                                                                 choices=flags.inpaint_mask_models,
                                                                 value=modules.config.default_enhance_inpaint_mask_model)
                                enhance_mask_cloth_category = gr.Dropdown(label='Cloth category',
                                                                          choices=flags.inpaint_mask_cloth_category,
                                                                          value=modules.config.default_inpaint_mask_cloth_category,
                                                                          visible=modules.config.default_enhance_inpaint_mask_model == 'u2net_cloth_seg',
                                                                          interactive=True)

                                with gr.Accordion("SAM Options",
                                                  visible=modules.config.default_enhance_inpaint_mask_model == 'sam',
                                                  open=False) as sam_options:
                                    enhance_mask_sam_model = gr.Dropdown(label='SAM model',
                                                                         choices=flags.inpaint_mask_sam_model,
                                                                         value=modules.config.default_inpaint_mask_sam_model,
                                                                         interactive=True)
                                    enhance_mask_box_threshold = gr.Slider(label="Box Threshold", minimum=0.0,
                                                                           maximum=1.0, value=0.3, step=0.05,
                                                                           interactive=True)
                                    enhance_mask_text_threshold = gr.Slider(label="Text Threshold", minimum=0.0,
                                                                            maximum=1.0, value=0.25, step=0.05,
                                                                            interactive=True)
                                    enhance_mask_sam_max_detections = gr.Slider(label="Maximum number of detections",
                                                                                info="Set to 0 to detect all",
                                                                                minimum=0, maximum=10,
                                                                                value=modules.config.default_sam_max_detections,
                                                                                step=1, interactive=True)

                            with gr.Accordion("Inpaint", visible=True, open=False):
                                enhance_inpaint_mode = gr.Dropdown(choices=modules.flags.inpaint_options,
                                                                   value=modules.config.default_inpaint_method,
                                                                   label='Method', interactive=True)
                                enhance_inpaint_disable_initial_latent = gr.Checkbox(
                                    label='Disable initial latent in inpaint', value=False)
                                enhance_inpaint_engine = gr.Dropdown(label='Inpaint Engine',
                                                                     value=modules.config.default_inpaint_engine_version,
                                                                     choices=flags.inpaint_engine_versions,
                                                                     info='Version of Aether inpaint model. If set, use performance Quality or Speed (no performance LoRAs) for best results.')
                                enhance_inpaint_strength = gr.Slider(label='Inpaint Denoising Strength',
                                                                     minimum=0.0, maximum=1.0, step=0.001,
                                                                     value=1.0,
                                                                     info='Same as the denoising strength in A1111 inpaint. '
                                                                          'Only used in inpaint, not used in outpaint. '
                                                                          '(Outpaint always use 1.0)')
                                enhance_inpaint_respective_field = gr.Slider(label='Inpaint Respective Field',
                                                                             minimum=0.0, maximum=1.0, step=0.001,
                                                                             value=0.618,
                                                                             info='The area to inpaint. '
                                                                                  'Value 0 is same as "Only Masked" in A1111. '
                                                                                  'Value 1 is same as "Whole Image" in A1111. '
                                                                                  'Only used in inpaint, not used in outpaint. '
                                                                                  '(Outpaint always use 1.0)')
                                enhance_inpaint_erode_or_dilate = gr.Slider(label='Mask Erode or Dilate',
                                                                            minimum=-64, maximum=64, step=1, value=0,
                                                                            info='Positive value will make white area in the mask larger, '
                                                                                 'negative value will make white area smaller. '
                                                                                 '(default is 0, always processed before any mask invert)')
                                enhance_mask_invert = gr.Checkbox(label='Invert Mask', value=False)

                            gr.HTML('<a href="https://github.com/lllyasviel/Fooocus/discussions/3281" target="_blank">\U0001F4D4 Documentation</a>')

                        enhance_ctrls += [
                            enhance_enabled,
                            enhance_mask_dino_prompt_text,
                            enhance_prompt,
                            enhance_negative_prompt,
                            enhance_mask_model,
                            enhance_mask_cloth_category,
                            enhance_mask_sam_model,
                            enhance_mask_text_threshold,
                            enhance_mask_box_threshold,
                            enhance_mask_sam_max_detections,
                            enhance_inpaint_disable_initial_latent,
                            enhance_inpaint_engine,
                            enhance_inpaint_strength,
                            enhance_inpaint_respective_field,
                            enhance_inpaint_erode_or_dilate,
                            enhance_mask_invert
                        ]

                        enhance_inpaint_mode_ctrls += [enhance_inpaint_mode]
                        enhance_inpaint_engine_ctrls += [enhance_inpaint_engine]

                        enhance_inpaint_update_ctrls += [[
                            enhance_inpaint_mode, enhance_inpaint_disable_initial_latent, enhance_inpaint_engine,
                            enhance_inpaint_strength, enhance_inpaint_respective_field
                        ]]

                        enhance_inpaint_mode.change(inpaint_mode_change, inputs=[enhance_inpaint_mode, inpaint_engine_state], outputs=[
                            inpaint_additional_prompt, outpaint_selections, example_inpaint_prompts,
                            enhance_inpaint_disable_initial_latent, enhance_inpaint_engine,
                            enhance_inpaint_strength, enhance_inpaint_respective_field
                        ], show_progress=False, queue=False)

                        enhance_mask_model.change(
                            lambda x: [gr.update(visible=x == 'u2net_cloth_seg')] +
                                      [gr.update(visible=x == 'sam')] * 2 +
                                      [gr.Dataset.update(visible=x == 'sam',
                                                         samples=modules.config.example_enhance_detection_prompts)],
                            inputs=enhance_mask_model,
                            outputs=[enhance_mask_cloth_category, enhance_mask_dino_prompt_text, sam_options,
                                     example_enhance_mask_dino_prompt_text],
                            queue=False, show_progress=False)

            switch_js = "(x) => {if(x){viewer_to_bottom(100);viewer_to_bottom(500);}else{viewer_to_top();} return x;}"
            down_js = "() => {viewer_to_bottom();}"

            input_image_checkbox.change(lambda x: gr.update(visible=x), inputs=input_image_checkbox,
                                        outputs=image_input_panel, queue=False, show_progress=False, _js=switch_js)
            ip_advanced.change(lambda: None, queue=False, show_progress=False, _js=down_js)

            current_tab = gr.Textbox(value='uov', visible=False)
            uov_tab.select(lambda: 'uov', outputs=current_tab, queue=False, _js=down_js, show_progress=False)
            inpaint_tab.select(lambda: 'inpaint', outputs=current_tab, queue=False, _js=down_js, show_progress=False)
            ip_tab.select(lambda: 'ip', outputs=current_tab, queue=False, _js=down_js, show_progress=False)
            describe_tab.select(lambda: 'desc', outputs=current_tab, queue=False, _js=down_js, show_progress=False)
            enhance_tab.select(lambda: 'enhance', outputs=current_tab, queue=False, _js=down_js, show_progress=False)
            metadata_tab.select(lambda: 'metadata', outputs=current_tab, queue=False, _js=down_js, show_progress=False)
            enhance_checkbox.change(lambda x: gr.update(visible=x), inputs=enhance_checkbox,
                                        outputs=enhance_input_panel, queue=False, show_progress=False, _js=switch_js)

        with gr.Column(scale=1, visible=modules.config.default_advanced_checkbox) as advanced_column:
            with gr.Tab(label='⚙️ Settings & Performance'):
                if not args_manager.args.disable_preset_selection:
                    preset_selection = gr.Dropdown(label='Preset',
                                                   choices=modules.config.available_presets,
                                                   value=args_manager.args.preset if args_manager.args.preset else "initial",
                                                   interactive=True)

                with gr.Group(elem_classes=['vram_mode_group']):
                    init_eco = model_management.is_vram_sparmodus()
                    vram_mode_radio = gr.Radio(
                        label='💾 GPU VRAM-Betriebsmodus',
                        choices=['🌱 VRAM-Sparmodus (Eco / Low-VRAM)', '⚡ Normalmodus (Max Speed / Normal-VRAM)'],
                        value='🌱 VRAM-Sparmodus (Eco / Low-VRAM)' if init_eco else '⚡ Normalmodus (Max Speed / Normal-VRAM)',
                        elem_classes=['vram_mode_radio']
                    )
                    vram_mode_info = gr.Markdown(value=render_vram_info(init_eco), elem_classes=['vram_info_box'])

                    def on_vram_mode_change(choice):
                        is_eco = (choice == '🌱 VRAM-Sparmodus (Eco / Low-VRAM)')
                        model_management.set_vram_sparmodus(is_eco)
                        return render_header_bar(is_eco), render_vram_info(is_eco)

                    vram_mode_radio.change(on_vram_mode_change, inputs=[vram_mode_radio], outputs=[header_bar_html, vram_mode_info], queue=False)

                with gr.Accordion(label='🔮 Prompt-Magier & Übersetzer Einstellungen', open=False):
                    enable_prompt_magier = gr.Checkbox(
                        label='✨ Prompt-Magier & Deutsch-Übersetzer aktivieren',
                        value=False,
                        info='Schaltet einen Schnell-Button unter dem Prompt frei, um deutsche Prompts automatisch ins Englische zu übersetzen und mit Detail- und Qualitäts-Tags zu optimieren.'
                    )
                    prompt_magier_mode = gr.Radio(
                        label='Magier-Modus',
                        choices=[
                            '🧠 KI-Übersetzung + Qualitäts-Boost (Empfohlen)',
                            '✨ KI-Übersetzung + KI-Prompt-Ersteller (Erweitert Details)',
                            '🌐 Nur KI-Übersetzung (Deutsch ➔ Englisch)',
                            '🎨 Nur Qualitäts-Boost (Englisch beibehalten)'
                        ],
                        value='🧠 KI-Übersetzung + Qualitäts-Boost (Empfohlen)'
                    )

                    enable_prompt_magier.change(lambda en: gr.update(visible=en), inputs=enable_prompt_magier, outputs=prompt_magier_row, queue=False)

                    def on_prompt_magier_click(current_prompt, mode_choice):
                        mode_map = {
                            '🧠 KI-Übersetzung + Qualitäts-Boost (Empfohlen)': 'neural_auto',
                            '✨ KI-Übersetzung + KI-Prompt-Ersteller (Erweitert Details)': 'neural_expand',
                            '🌐 Nur KI-Übersetzung (Deutsch ➔ Englisch)': 'neural_translate_only',
                            '🎨 Nur Qualitäts-Boost (Englisch beibehalten)': 'enhance_only'
                        }
                        mode = mode_map.get(mode_choice, 'neural_auto')
                        return prompt_magier.translate_and_enhance_prompt(current_prompt, mode=mode)

                    prompt_magier_btn.click(on_prompt_magier_click, inputs=[prompt, prompt_magier_mode], outputs=prompt, queue=False)

                performance_selection = gr.Radio(label='Performance',
                                                 choices=flags.Performance.values(),
                                                 value=modules.config.default_performance,
                                                 elem_classes=['performance_selection'])

                with gr.Accordion(label='📖 Performance-Modi erklärt (Unterschiede & Details)', open=False, elem_id='performance_accordion'):
                    gr.Markdown("""
### ⚡ Die Performance-Modi im Vergleich

| Modus | Schritte | Sampler / CFG | Renderzeit | Empfohlen für |
| :--- | :---: | :---: | :---: | :--- |
| **🏆 Quality** | **60 Steps** | dpmpp_2m_sde (CFG ~4–7) | Gründlich & detailliert | Maximale Bildschärfe, feine Texturen & fotorealistische Details |
| **🚀 Speed** | **30 Steps** | dpmpp_2m_sde (CFG ~4–7) | Standard (sehr schnell) | Der beste Allrounder: Hohe Qualität bei halber Renderzeit |
| **⚡ Turbo** | **6–8 Steps** | euler (CFG 1.5–2.0) | **Extrem rasant (Sekunden)** | Schnelle Entwürfe & Modelle mit SDXL-Turbo Architektur |
| **🌩️ Lightning** | **4–8 Steps** | euler (CFG 1.0) | **Ultra-Speed** | ByteDance SDXL-Lightning Beschleunigung (automatische LoRA) |
| **💎 Hyper-SD** | **4–12 Steps** | dpmpp_sde (CFG 1.0) | Sehr schnell & stabil | Neueste ByteDance Hyper-SD Technologie mit hoher Wiedergabetreue |
| **🏎️ Extreme Speed** | **8 Steps** | lcm (CFG 1.0) | Nahezu Echtzeit | Latent Consistency Models (LCM LoRA) für blitzschnelle Previews |

---
#### 💡 Wann nutze ich welchen Modus?
- **Speed (30 Steps):** Standard für fast alle SDXL-Modelle (Juggernaut, RealVis, Animagine) – perfektes Verhältnis aus Detail und Renderzeit.
- **Quality (60 Steps):** Wenn du feinste Haare, komplexe Hintergründe oder maximale Detailtiefe suchst.
- **Turbo / Lightning / Hyper-SD:** Wenn du in wenigen Sekunden neue Bildideen ausprobieren möchtest.
                    """)

                with gr.Accordion(label='Aspect Ratios', open=False, elem_id='aspect_ratios_accordion') as aspect_ratios_accordion:
                    aspect_ratios_selection = gr.Radio(label='Aspect Ratios', show_label=False,
                                                       choices=modules.config.available_aspect_ratios_labels,
                                                       value=modules.config.default_aspect_ratio,
                                                       info='width × height',
                                                       elem_classes='aspect_ratios')

                    aspect_ratios_selection.change(lambda x: None, inputs=aspect_ratios_selection, queue=False, show_progress=False, _js='(x)=>{refresh_aspect_ratios_label(x);}')
                    shared.gradio_root.load(lambda x: None, inputs=aspect_ratios_selection, queue=False, show_progress=False, _js='(x)=>{refresh_aspect_ratios_label(x);}')

                image_number = gr.Slider(label='Image Number', minimum=1, maximum=modules.config.default_max_image_number, step=1, value=modules.config.default_image_number)

                output_format = gr.Radio(label='Output Format',
                                         choices=flags.OutputFormat.list(),
                                         value=modules.config.default_output_format)

                negative_prompt = gr.Textbox(label='Negative Prompt', show_label=True, placeholder="Type prompt here.",
                                             info='Describing what you do not want to see.', lines=2,
                                             elem_id='negative_prompt',
                                             value=modules.config.default_prompt_negative)
                seed_random = gr.Checkbox(label='Random', value=True)
                image_seed = gr.Textbox(label='Seed', value=0, max_lines=1, visible=False) # workaround for https://github.com/gradio-app/gradio/issues/5354

                def random_checked(r):
                    return gr.update(visible=not r)

                def refresh_seed(r, seed_string):
                    if r:
                        return random.randint(constants.MIN_SEED, constants.MAX_SEED)
                    else:
                        try:
                            seed_value = int(seed_string)
                            if constants.MIN_SEED <= seed_value <= constants.MAX_SEED:
                                return seed_value
                        except ValueError:
                            pass
                        return random.randint(constants.MIN_SEED, constants.MAX_SEED)

                seed_random.change(random_checked, inputs=[seed_random], outputs=[image_seed],
                                   queue=False, show_progress=False)

                def update_history_link():
                    if args_manager.args.disable_image_log:
                        return gr.update(value='')

                    return gr.update(value=f'<a href="file={get_current_html_path(output_format)}" target="_blank">\U0001F4DA History Log</a>')

                history_link = gr.HTML()
                shared.gradio_root.load(update_history_link, outputs=history_link, queue=False, show_progress=False)

            with gr.Tab(label='Styles', elem_classes=['style_selections_tab']):
                style_sorter.try_load_sorted_styles(
                    style_names=legal_style_names,
                    default_selected=modules.config.default_styles)

                style_search_bar = gr.Textbox(show_label=False, container=False,
                                              placeholder="\U0001F50E Type here to search styles ...",
                                              value="",
                                              label='Search Styles')
                style_selections = gr.CheckboxGroup(show_label=False, container=False,
                                                    choices=copy.deepcopy(style_sorter.all_styles),
                                                    value=copy.deepcopy(modules.config.default_styles),
                                                    label='Selected Styles',
                                                    elem_classes=['style_selections'])
                gradio_receiver_style_selections = gr.Textbox(elem_id='gradio_receiver_style_selections', visible=False)

                shared.gradio_root.load(lambda: gr.update(choices=copy.deepcopy(style_sorter.all_styles)),
                                        outputs=style_selections)

                style_search_bar.change(style_sorter.search_styles,
                                        inputs=[style_selections, style_search_bar],
                                        outputs=style_selections,
                                        queue=False,
                                        show_progress=False).then(
                    lambda: None, _js='()=>{refresh_style_localization();}')

                gradio_receiver_style_selections.input(style_sorter.sort_styles,
                                                       inputs=style_selections,
                                                       outputs=style_selections,
                                                       queue=False,
                                                       show_progress=False).then(
                    lambda: None, _js='()=>{refresh_style_localization();}')

            with gr.Tab(label='🧠 Models & VRAM-Hybrid'):
                with gr.Group():
                    with gr.Row():
                        base_model = gr.Dropdown(label='Base Model (SDXL only)', choices=modules.config.model_filenames, value=modules.config.default_base_model_name, show_label=True)
                        refiner_model = gr.Dropdown(label='Refiner (SDXL or SD 1.5)', choices=['None'] + modules.config.model_filenames, value=modules.config.default_refiner_model_name, show_label=True)

                    custom_folder_models = ['None'] + [f for f in os.listdir(modules.config.path_all_models_sdxl_flux) if f.endswith(('.safetensors', '.ckpt', '.pt', '.bin', '.gguf'))] if os.path.exists(modules.config.path_all_models_sdxl_flux) else ['None']
                    all_models_dropdown = gr.Dropdown(
                        label='📁 Alternativ: Modelle aus all_models_sdxl_flux (SDXL / Turbo / FLUX / SD 1.5)',
                        choices=custom_folder_models,
                        value='None',
                        info='Wenn ausgewählt, wird dieses Modell als Basis-Modell geladen.'
                    )

                    smart_ram_offload_cb = gr.Checkbox(
                        label='⚡ Modell in RAM mitladen (Smart Hybrid VRAM + RAM Offload)',
                        value=True,
                        info='AUTOMATISCH AKTIV: Große Modelle (SDXL, FLUX), die nicht komplett in den RTX 3050 VRAM (~6 GB) passen, lagern Ebenen dynamisch in deinen 32 GB Arbeitsspeicher aus. DEAKTIVIERT: Modell muss zu 100% in die GPU passen – Generierung bricht sofort ab, falls der VRAM nicht ausreicht!',
                        elem_classes=['smart_ram_checkbox']
                    )

                    def toggle_smart_ram(enabled):
                        import ldm_patched.modules.model_management as mm
                        mm.set_smart_ram_offload(enabled)
                        print(f"[Aether Studio] Smart RAM Offload: {'AKTIV' if enabled else 'DEAKTIVIERT'}")

                    smart_ram_offload_cb.change(toggle_smart_ram, inputs=[smart_ram_offload_cb], outputs=[], queue=False)

                    refiner_switch = gr.Slider(label='Refiner Switch At', minimum=0.1, maximum=1.0, step=0.0001,
                                               info='Use 0.4 for SD1.5 realistic models; '
                                                    'or 0.667 for SD1.5 anime models; '
                                                    'or 0.8 for XL-refiners; '
                                                    'or any value for switching two SDXL models.',
                                               value=modules.config.default_refiner_switch,
                                               visible=modules.config.default_refiner_model_name != 'None')

                    refiner_model.change(lambda x: gr.update(visible=x != 'None'),
                                         inputs=refiner_model, outputs=refiner_switch, show_progress=False, queue=False)

                with gr.Group():
                    lora_ctrls = []

                    for i, (enabled, filename, weight) in enumerate(modules.config.default_loras):
                        with gr.Row():
                            lora_enabled = gr.Checkbox(label='Enable', value=enabled,
                                                       elem_classes=['lora_enable', 'min_check'], scale=1)
                            lora_model = gr.Dropdown(label=f'LoRA {i + 1}',
                                                     choices=['None'] + modules.config.lora_filenames, value=filename,
                                                     elem_classes='lora_model', scale=5)
                            lora_weight = gr.Slider(label='Weight', minimum=modules.config.default_loras_min_weight,
                                                    maximum=modules.config.default_loras_max_weight, step=0.01, value=weight,
                                                     elem_classes='lora_weight', scale=5)
                            lora_ctrls += [lora_enabled, lora_model, lora_weight]

                with gr.Row():
                    refresh_files = gr.Button(label='Refresh', value='\U0001f504 Refresh All Files', variant='secondary', elem_classes='refresh_button')

            with gr.Tab(label='🌐 Modell-Manager & VRAM-Rechner'):
                hardware_specs = model_checker.get_hardware_specs()
                gr.Markdown(f"### 🖥️ Deine Hardware-Erkennung\n{hardware_specs['display']}")

                with gr.Group():
                    gr.Markdown("### 🧮 VRAM- & Kompatibilitäts-Rechner (Civitai Check)")
                    with gr.Row():
                        model_calc_input = gr.Textbox(
                            label='Civitai-URL oder Modellname eingeben',
                            placeholder='z.B. https://civitai.com/models/618692/flux1-dev oder flux schnell fp8 oder dreamshaper 1.5',
                            scale=4
                        )
                        model_calc_btn = gr.Button('🔍 Kompatibilität berechnen', variant='primary', elem_classes=['comfy-quick-download-btn'], scale=1)

                    with gr.Row():
                        btn_test_flux_schnell = gr.Button("⚡ FLUX.1 [schnell] FP8", scale=1)
                        btn_test_flux_dev = gr.Button("⚡ FLUX.1 [dev] FP8", scale=1)
                        btn_test_flux_fp16 = gr.Button("🔥 FLUX.1 [dev] FP16", scale=1)
                        btn_test_turbo = gr.Button("🚀 SDXL Turbo", scale=1)
                        btn_test_sd15 = gr.Button("🎨 SD 1.5 Realistic", scale=1)

                    model_calc_result = gr.Markdown(value="*Gib oben einen Modellnamen oder eine URL ein, um zu berechnen, ob und wie das Modell auf deiner RTX 3050 läuft.*")

                with gr.Accordion(label="📂 Eigener Ordner: models/all_models_sdxl_flux", open=True):
                    gr.Markdown(f"**Pfad:** `{modules.config.path_all_models_sdxl_flux}`\n\n*Alle Modelle in diesem Ordner werden automatisch von Aether Studio erkannt!*")
                    def get_custom_folder_files():
                        p = modules.config.path_all_models_sdxl_flux
                        if os.path.exists(p):
                            files = [f for f in os.listdir(p) if f.endswith(('.safetensors', '.ckpt', '.pt', '.bin', '.gguf'))]
                            if files:
                                return "📁 **Gefundene Modelle im Ordner:**\n" + "\n".join([f"- `{f}`" for f in files])
                        return "*(Ordner ist momentan noch leer. Kopiere deine SDXL-, Turbo-, SD 1.5- oder FLUX-Modelle hier hinein!)*"
                    custom_folder_file_list = gr.Markdown(value=get_custom_folder_files())
                    refresh_custom_folder_btn = gr.Button("🔄 Ordnerinhalt aktualisieren")

                with gr.Accordion(label="📋 Übersicht: Welche Modelle werden unterstützt?", open=False):
                    gr.Markdown("""
| Modell-Familie | Auflösung | Steps | Benötigter VRAM | Läuft auf RTX 3050? |
| :--- | :--- | :--- | :--- | :--- |
| **SDXL 1.0 (Standard)** | 1024x1024 | 30 | 5-6 GB | 🟢 Ja (mit `./run_lowvram.sh`) |
| **SDXL Turbo / Lightning** | 1024x1024 | 4-6 | 5-6 GB | 🟢 Ja, extrem schnell (4-8s pro Bild) |
| **Stable Diffusion 1.5** | 512x512 | 20-30 | 3-4 GB | 🟢 Ja, superschnell (2-5s pro Bild) |
| **Pony Diffusion V6 XL** | 1024x1024 | 25-30 | 5-6 GB | 🟢 Ja (mit `./run_lowvram.sh`) |
| **FLUX.1 [schnell] FP8** | 1024x1024 | 4 | ~6 GB VRAM + 16GB RAM | 🟡 Ja, dank deinen **32 GB RAM**! |
| **FLUX.1 [dev] FP8 / GGUF** | 1024x1024 | 20 | ~6 GB VRAM + 24GB RAM | 🟡 Ja, dank deinen **32 GB RAM**! |
| **FLUX.1 [dev] FP16** | 1024x1024 | 20 | 24 GB VRAM | 🔴 Nein (nur FP8/GGUF empfohlen) |
""")

            with gr.Tab(label='📥 Civitai Downloader (Beta)'):
                gr.HTML("""
                <div class="civitai-beta-warning" style="background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.45); border-radius: 10px; padding: 14px 16px; margin-bottom: 16px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <span style="font-size: 20px;">⚠️</span>
                        <h4 style="color: #f87171; margin: 0; font-size: 15px; font-weight: 700;">ACHTUNG: EXPERIMENTELLE BETA-FUNKTION!</h4>
                    </div>
                    <p style="color: #fca5a5; margin: 0; font-size: 13px; line-height: 1.5;">
                        Dieser integrierte Civitai-Downloader ist ein <b>Beta-Feature</b>. Bei großen Dateien (z. B. 6 GB Checkpoints) oder instabiler Internetverbindung kann es zu Timeouts oder Netzwerkabbrüchen kommen.<br>
                        <b>💡 Empfehlung:</b> Bei sehr großen Modellen wird empfohlen, die Dateien regulär im Webbrowser herunterzuladen und in den jeweiligen Modell-Ordner zu legen.
                    </p>
                </div>
                """)

                with gr.Group():
                    with gr.Row():
                        civitai_input = gr.Textbox(
                            label='Civitai Modell-URL oder Version-ID',
                            placeholder='z.B. https://civitai.com/models/123456 oder https://civitai.com/models/123456?modelVersionId=78910',
                            scale=4
                        )
                        civitai_api_key = gr.Textbox(
                            label='Civitai API-Key (Optional)',
                            placeholder='Nur nötig für geschützte Modelle mit Login-Pflicht',
                            type='password',
                            scale=2
                        )
                    
                    with gr.Row():
                        civitai_inspect_btn = gr.Button('🔍 1. Modell-Details prüfen', variant='secondary', scale=1)
                        civitai_dl_btn = gr.Button('⬇️ 2. Modell jetzt herunterladen', variant='primary', elem_classes=['comfy-quick-download-btn'], scale=1)

                civitai_cached_info = gr.State({})
                civitai_info_box = gr.Markdown(value="*Gib oben eine Civitai-URL ein und klicke auf '1. Modell-Details prüfen'.*")
                civitai_status_box = gr.Markdown(value="")

                def on_civitai_inspect(url_or_id, api_key):
                    if not url_or_id or not url_or_id.strip():
                        return {}, "*Bitte gib zuerst eine Civitai-URL oder Modell-ID ein.*", ""
                    data = civitai_downloader.fetch_civitai_metadata(url_or_id, api_key=api_key)
                    if "error" in data:
                        return {}, f"❌ **Fehler:** {data['error']}", ""
                    
                    md = f"""
### 📦 Gefundenes Modell: **{data['model_name']}**
- **Version:** `{data['version_name']}`
- **Modell-Typ:** `{data['model_type']}` (Basis: `{data['base_model']}`)
- **Dateiname:** `{data['filename']}`
- **Größe:** **{data['size_gb']} GB**
- **Zielordner:** `{data['target_dir']}`
                    """
                    return data, md, "✅ Modell gefunden! Klicke jetzt auf **'2. Modell jetzt herunterladen'**."

                def on_civitai_download(cached_data, api_key):
                    if not cached_data or not cached_data.get("success"):
                        return "❌ **Fehler:** Bitte prüfe zuerst das Modell mit '1. Modell-Details prüfen', bevor du den Download startest."
                    
                    dl_url = cached_data["download_url"]
                    target_dir = cached_data["target_dir"]
                    filename = cached_data["filename"]
                    target_filepath = os.path.join(target_dir, filename)

                    if os.path.exists(target_filepath):
                        return f"ℹ️ **Datei existiert bereits:** `{filename}` in `{target_dir}`!"

                    success, msg = civitai_downloader.download_file_stream(
                        download_url=dl_url,
                        target_filepath=target_filepath,
                        api_key=api_key
                    )
                    if success:
                        modules.config.update_files()
                        return f"🎉 **Fertig:** {msg}\n\n*Das Modell steht nun sofort in deinen Checkpoints / LoRAs zur Verfügung!*"
                    else:
                        return f"❌ **Fehler beim Download:** {msg}"

                civitai_inspect_btn.click(
                    on_civitai_inspect,
                    inputs=[civitai_input, civitai_api_key],
                    outputs=[civitai_cached_info, civitai_info_box, civitai_status_box],
                    queue=False
                )
                civitai_dl_btn.click(
                    on_civitai_download,
                    inputs=[civitai_cached_info, civitai_api_key],
                    outputs=[civitai_status_box]
                )

            with gr.Tab(label='Advanced'):
                guidance_scale = gr.Slider(label='Guidance Scale', minimum=1.0, maximum=30.0, step=0.01,
                                           value=modules.config.default_cfg_scale,
                                           info='Higher value means style is cleaner, vivider, and more artistic.')
                sharpness = gr.Slider(label='Image Sharpness', minimum=0.0, maximum=30.0, step=0.001,
                                      value=modules.config.default_sample_sharpness,
                                      info='Higher value means image and texture are sharper.')
                gr.HTML('<a href="https://github.com/lllyasviel/Fooocus/discussions/117" target="_blank">\U0001F4D4 Documentation</a>')
                dev_mode = gr.Checkbox(label='Developer Debug Mode', value=modules.config.default_developer_debug_mode_checkbox, container=False)

                with gr.Column(visible=modules.config.default_developer_debug_mode_checkbox) as dev_tools:
                    with gr.Tab(label='Debug Tools'):
                        adm_scaler_positive = gr.Slider(label='Positive ADM Guidance Scaler', minimum=0.1, maximum=3.0,
                                                        step=0.001, value=1.5, info='The scaler multiplied to positive ADM (use 1.0 to disable). ')
                        adm_scaler_negative = gr.Slider(label='Negative ADM Guidance Scaler', minimum=0.1, maximum=3.0,
                                                        step=0.001, value=0.8, info='The scaler multiplied to negative ADM (use 1.0 to disable). ')
                        adm_scaler_end = gr.Slider(label='ADM Guidance End At Step', minimum=0.0, maximum=1.0,
                                                   step=0.001, value=0.3,
                                                   info='When to end the guidance from positive/negative ADM. ')

                        refiner_swap_method = gr.Dropdown(label='Refiner swap method', value=flags.refiner_swap_method,
                                                          choices=['joint', 'separate', 'vae'])

                        adaptive_cfg = gr.Slider(label='CFG Mimicking from TSNR', minimum=1.0, maximum=30.0, step=0.01,
                                                 value=modules.config.default_cfg_tsnr,
                                                 info='Enabling Aether\'s implementation of CFG mimicking for TSNR '
                                                      '(effective when real CFG > mimicked CFG).')
                        clip_skip = gr.Slider(label='CLIP Skip', minimum=1, maximum=flags.clip_skip_max, step=1,
                                                 value=modules.config.default_clip_skip,
                                                 info='Bypass CLIP layers to avoid overfitting (use 1 to not skip any layers, 2 is recommended).')
                        sampler_name = gr.Dropdown(label='Sampler', choices=flags.sampler_list,
                                                   value=modules.config.default_sampler)
                        scheduler_name = gr.Dropdown(label='Scheduler', choices=flags.scheduler_list,
                                                     value=modules.config.default_scheduler)
                        vae_name = gr.Dropdown(label='VAE', choices=[modules.flags.default_vae] + modules.config.vae_filenames,
                                                     value=modules.config.default_vae, show_label=True)

                        generate_image_grid = gr.Checkbox(label='Generate Image Grid for Each Batch',
                                                          info='(Experimental) This may cause performance problems on some computers and certain internet conditions.',
                                                          value=False)

                        overwrite_step = gr.Slider(label='Forced Overwrite of Sampling Step',
                                                   minimum=-1, maximum=200, step=1,
                                                   value=modules.config.default_overwrite_step,
                                                   info='Set as -1 to disable. For developer debugging.')
                        overwrite_switch = gr.Slider(label='Forced Overwrite of Refiner Switch Step',
                                                     minimum=-1, maximum=200, step=1,
                                                     value=modules.config.default_overwrite_switch,
                                                     info='Set as -1 to disable. For developer debugging.')
                        overwrite_width = gr.Slider(label='Forced Overwrite of Generating Width',
                                                    minimum=-1, maximum=2048, step=1, value=-1,
                                                    info='Set as -1 to disable. For developer debugging. '
                                                         'Results will be worse for non-standard numbers that SDXL is not trained on.')
                        overwrite_height = gr.Slider(label='Forced Overwrite of Generating Height',
                                                     minimum=-1, maximum=2048, step=1, value=-1,
                                                     info='Set as -1 to disable. For developer debugging. '
                                                          'Results will be worse for non-standard numbers that SDXL is not trained on.')
                        overwrite_vary_strength = gr.Slider(label='Forced Overwrite of Denoising Strength of "Vary"',
                                                            minimum=-1, maximum=1.0, step=0.001, value=-1,
                                                            info='Set as negative number to disable. For developer debugging.')
                        overwrite_upscale_strength = gr.Slider(label='Forced Overwrite of Denoising Strength of "Upscale"',
                                                               minimum=-1, maximum=1.0, step=0.001,
                                                               value=modules.config.default_overwrite_upscale,
                                                               info='Set as negative number to disable. For developer debugging.')

                        disable_preview = gr.Checkbox(label='Disable Preview', value=modules.config.default_black_out_nsfw,
                                                      interactive=not modules.config.default_black_out_nsfw,
                                                      info='Disable preview during generation.')
                        disable_intermediate_results = gr.Checkbox(label='Disable Intermediate Results',
                                                      value=flags.Performance.has_restricted_features(modules.config.default_performance),
                                                      info='Disable intermediate results during generation, only show final gallery.')

                        disable_seed_increment = gr.Checkbox(label='Disable seed increment',
                                                             info='Disable automatic seed increment when image number is > 1.',
                                                             value=False)
                        read_wildcards_in_order = gr.Checkbox(label="Read wildcards in order", value=False)

                        black_out_nsfw = gr.Checkbox(label='Black Out NSFW', value=modules.config.default_black_out_nsfw,
                                                     interactive=not modules.config.default_black_out_nsfw,
                                                     info='Use black image if NSFW is detected.')

                        black_out_nsfw.change(lambda x: gr.update(value=x, interactive=not x),
                                              inputs=black_out_nsfw, outputs=disable_preview, queue=False,
                                              show_progress=False)

                        if not args_manager.args.disable_image_log:
                            save_final_enhanced_image_only = gr.Checkbox(label='Save only final enhanced image',
                                                                         value=modules.config.default_save_only_final_enhanced_image)

                        if not args_manager.args.disable_metadata:
                            save_metadata_to_images = gr.Checkbox(label='Save Metadata to Images', value=modules.config.default_save_metadata_to_images,
                                                                  info='Adds parameters to generated images allowing manual regeneration.')
                            metadata_scheme = gr.Radio(label='Metadata Scheme', choices=flags.metadata_scheme, value=modules.config.default_metadata_scheme,
                                                       info='Image Prompt parameters are not included. Use png and a1111 for compatibility with Civitai.',
                                                       visible=modules.config.default_save_metadata_to_images)

                            save_metadata_to_images.change(lambda x: gr.update(visible=x), inputs=[save_metadata_to_images], outputs=[metadata_scheme],
                                                           queue=False, show_progress=False)

                    with gr.Tab(label='Control'):
                        debugging_cn_preprocessor = gr.Checkbox(label='Debug Preprocessors', value=False,
                                                                info='See the results from preprocessors.')
                        skipping_cn_preprocessor = gr.Checkbox(label='Skip Preprocessors', value=False,
                                                               info='Do not preprocess images. (Inputs are already canny/depth/cropped-face/etc.)')

                        mixing_image_prompt_and_vary_upscale = gr.Checkbox(label='Mixing Image Prompt and Vary/Upscale',
                                                                           value=False)
                        mixing_image_prompt_and_inpaint = gr.Checkbox(label='Mixing Image Prompt and Inpaint',
                                                                      value=False)

                        controlnet_softness = gr.Slider(label='Softness of ControlNet', minimum=0.0, maximum=1.0,
                                                        step=0.001, value=0.25,
                                                        info='Similar to the Control Mode in A1111 (use 0.0 to disable). ')

                        with gr.Tab(label='Canny'):
                            canny_low_threshold = gr.Slider(label='Canny Low Threshold', minimum=1, maximum=255,
                                                            step=1, value=64)
                            canny_high_threshold = gr.Slider(label='Canny High Threshold', minimum=1, maximum=255,
                                                             step=1, value=128)

                    with gr.Tab(label='Inpaint'):
                        debugging_inpaint_preprocessor = gr.Checkbox(label='Debug Inpaint Preprocessing', value=False)
                        debugging_enhance_masks_checkbox = gr.Checkbox(label='Debug Enhance Masks', value=False,
                                                                       info='Show enhance masks in preview and final results')
                        debugging_dino = gr.Checkbox(label='Debug GroundingDINO', value=False,
                                                     info='Use GroundingDINO boxes instead of more detailed SAM masks')
                        inpaint_disable_initial_latent = gr.Checkbox(label='Disable initial latent in inpaint', value=False)
                        inpaint_engine = gr.Dropdown(label='Inpaint Engine',
                                                     value=modules.config.default_inpaint_engine_version,
                                                     choices=flags.inpaint_engine_versions,
                                                     info='Version of Aether inpaint model. If set, use performance Quality or Speed (no performance LoRAs) for best results.')
                        inpaint_strength = gr.Slider(label='Inpaint Denoising Strength',
                                                     minimum=0.0, maximum=1.0, step=0.001, value=1.0,
                                                     info='Same as the denoising strength in A1111 inpaint. '
                                                          'Only used in inpaint, not used in outpaint. '
                                                          '(Outpaint always use 1.0)')
                        inpaint_respective_field = gr.Slider(label='Inpaint Respective Field',
                                                             minimum=0.0, maximum=1.0, step=0.001, value=0.618,
                                                             info='The area to inpaint. '
                                                                  'Value 0 is same as "Only Masked" in A1111. '
                                                                  'Value 1 is same as "Whole Image" in A1111. '
                                                                  'Only used in inpaint, not used in outpaint. '
                                                                  '(Outpaint always use 1.0)')
                        inpaint_erode_or_dilate = gr.Slider(label='Mask Erode or Dilate',
                                                            minimum=-64, maximum=64, step=1, value=0,
                                                            info='Positive value will make white area in the mask larger, '
                                                                 'negative value will make white area smaller. '
                                                                 '(default is 0, always processed before any mask invert)')
                        dino_erode_or_dilate = gr.Slider(label='GroundingDINO Box Erode or Dilate',
                                                         minimum=-64, maximum=64, step=1, value=0,
                                                         info='Positive value will make white area in the mask larger, '
                                                              'negative value will make white area smaller. '
                                                              '(default is 0, processed before SAM)')

                        inpaint_mask_color = gr.ColorPicker(label='Inpaint brush color', value='#FFFFFF', elem_id='inpaint_brush_color')

                        inpaint_ctrls = [debugging_inpaint_preprocessor, inpaint_disable_initial_latent, inpaint_engine,
                                         inpaint_strength, inpaint_respective_field,
                                         inpaint_advanced_masking_checkbox, invert_mask_checkbox, inpaint_erode_or_dilate]

                        inpaint_advanced_masking_checkbox.change(lambda x: [gr.update(visible=x)] * 2,
                                                                 inputs=inpaint_advanced_masking_checkbox,
                                                                 outputs=[inpaint_mask_image, inpaint_mask_generation_col],
                                                                 queue=False, show_progress=False)

                        inpaint_mask_color.change(lambda x: gr.update(brush_color=x), inputs=inpaint_mask_color,
                                                  outputs=inpaint_input_image,
                                                  queue=False, show_progress=False)

                    with gr.Tab(label='FreeU'):
                        freeu_enabled = gr.Checkbox(label='Enabled', value=False)
                        freeu_b1 = gr.Slider(label='B1', minimum=0, maximum=2, step=0.01, value=1.01)
                        freeu_b2 = gr.Slider(label='B2', minimum=0, maximum=2, step=0.01, value=1.02)
                        freeu_s1 = gr.Slider(label='S1', minimum=0, maximum=4, step=0.01, value=0.99)
                        freeu_s2 = gr.Slider(label='S2', minimum=0, maximum=4, step=0.01, value=0.95)
                        freeu_ctrls = [freeu_enabled, freeu_b1, freeu_b2, freeu_s1, freeu_s2]

                def dev_mode_checked(r):
                    return gr.update(visible=r)

                dev_mode.change(dev_mode_checked, inputs=[dev_mode], outputs=[dev_tools],
                                queue=False, show_progress=False)

                def refresh_files_clicked():
                    modules.config.update_files()
                    custom_folder_models = ['None'] + [f for f in os.listdir(modules.config.path_all_models_sdxl_flux) if f.endswith(('.safetensors', '.ckpt', '.pt', '.bin', '.gguf'))] if os.path.exists(modules.config.path_all_models_sdxl_flux) else ['None']
                    results = [gr.update(choices=modules.config.model_filenames)]
                    results += [gr.update(choices=['None'] + modules.config.model_filenames)]
                    results += [gr.update(choices=custom_folder_models)]
                    results += [gr.update(choices=[flags.default_vae] + modules.config.vae_filenames)]
                    if not args_manager.args.disable_preset_selection:
                        results += [gr.update(choices=modules.config.available_presets)]
                    for i in range(modules.config.default_max_lora_number):
                        results += [gr.update(interactive=True),
                                    gr.update(choices=['None'] + modules.config.lora_filenames), gr.update()]
                    return results

                refresh_files_output = [base_model, refiner_model, all_models_dropdown, vae_name]
                if not args_manager.args.disable_preset_selection:
                    refresh_files_output += [preset_selection]
                refresh_files.click(refresh_files_clicked, [], refresh_files_output + lora_ctrls,
                                    queue=False, show_progress=False)

            with gr.Tab(label='🖼️ Verlauf & Downloads', elem_id='history_tab'):
                with gr.Row():
                    history_refresh_btn = gr.Button(value="🔄 Verlauf aktualisieren", scale=1)
                    history_download_all_today_btn = gr.Button(value="📥 Alle von heute in Downloads speichern", scale=2)
                history_status = gr.Markdown(value="", elem_id="history_status")
                with gr.Row():
                    with gr.Column(scale=3):
                        history_gallery = gr.Gallery(
                            label='Generierungs-Verlauf (Klicke auf ein Bild für Details & Download)',
                            show_label=True,
                            columns=3,
                            height=560,
                            object_fit='contain',
                            elem_classes=['history_gallery']
                        )
                        history_image_paths = gr.State([])
                    with gr.Column(scale=2):
                        history_selected_preview = grh.Image(label='Vorschau', show_label=True, height=260)
                        history_selected_path = gr.State("")
                        with gr.Row():
                            history_download_btn = gr.Button(value="💾 In Downloads speichern", elem_classes=['comfy-quick-download-btn'], scale=1)
                            history_load_prompt_btn = gr.Button(value="📋 Prompt laden", scale=1)
                        history_load_input_btn = gr.Button(value="🔄 In Input Image (Upscale) senden")
                        history_info_box = gr.Markdown(value="*Klicke auf ein Bild links, um Details & Prompt anzuzeigen.*")

            with gr.Tab(label='📚 Guide (3D & Anime)', elem_id='guide_tab'):
                gr.Markdown(prompt_guide.GUIDE_MARKDOWN_TEXT)
                gr.Markdown("### ⚡ 1-Klick Vorlagen (Templates)")
                with gr.Row():
                    guide_template_dropdown = gr.Dropdown(
                        label="Wähle eine Vorlage aus:",
                        choices=prompt_guide.get_template_names(),
                        value=prompt_guide.get_template_names()[0]
                    )
                guide_template_info = gr.Markdown(value="")
                guide_apply_btn = gr.Button(value="📥 Vorlage in Prompt & Generator laden", variant='primary', elem_classes=['comfy-quick-download-btn'])
                guide_apply_status = gr.Markdown(value="")

        state_is_generating = gr.State(False)

        load_data_outputs = [advanced_checkbox, image_number, prompt, negative_prompt, style_selections,
                             performance_selection, overwrite_step, overwrite_switch, aspect_ratios_selection,
                             overwrite_width, overwrite_height, guidance_scale, sharpness, adm_scaler_positive,
                             adm_scaler_negative, adm_scaler_end, refiner_swap_method, adaptive_cfg, clip_skip,
                             base_model, refiner_model, refiner_switch, sampler_name, scheduler_name, vae_name,
                             seed_random, image_seed, inpaint_engine, inpaint_engine_state,
                             inpaint_mode] + enhance_inpaint_mode_ctrls + [generate_button,
                             load_parameter_button] + freeu_ctrls + lora_ctrls

        if not args_manager.args.disable_preset_selection:
            def preset_selection_change(preset, is_generating, inpaint_mode):
                preset_content = modules.config.try_get_preset_content(preset) if preset != 'initial' else {}
                preset_prepared = modules.meta_parser.parse_meta_from_preset(preset_content)

                default_model = preset_prepared.get('base_model')
                previous_default_models = preset_prepared.get('previous_default_models', [])
                checkpoint_downloads = preset_prepared.get('checkpoint_downloads', {})
                embeddings_downloads = preset_prepared.get('embeddings_downloads', {})
                lora_downloads = preset_prepared.get('lora_downloads', {})
                vae_downloads = preset_prepared.get('vae_downloads', {})

                preset_prepared['base_model'], preset_prepared['checkpoint_downloads'] = launch.download_models(
                    default_model, previous_default_models, checkpoint_downloads, embeddings_downloads, lora_downloads,
                    vae_downloads)

                if 'prompt' in preset_prepared and preset_prepared.get('prompt') == '':
                    del preset_prepared['prompt']

                return modules.meta_parser.load_parameter_button_click(json.dumps(preset_prepared), is_generating, inpaint_mode)


            def inpaint_engine_state_change(inpaint_engine_version, *args):
                if inpaint_engine_version == 'empty':
                    inpaint_engine_version = modules.config.default_inpaint_engine_version

                result = []
                for inpaint_mode in args:
                    if inpaint_mode != modules.flags.inpaint_option_detail:
                        result.append(gr.update(value=inpaint_engine_version))
                    else:
                        result.append(gr.update())

                return result

            preset_selection.change(preset_selection_change, inputs=[preset_selection, state_is_generating, inpaint_mode], outputs=load_data_outputs, queue=False, show_progress=True) \
                .then(fn=style_sorter.sort_styles, inputs=style_selections, outputs=style_selections, queue=False, show_progress=False) \
                .then(lambda: None, _js='()=>{refresh_style_localization();}') \
                .then(inpaint_engine_state_change, inputs=[inpaint_engine_state] + enhance_inpaint_mode_ctrls, outputs=enhance_inpaint_engine_ctrls, queue=False, show_progress=False)

        performance_selection.change(lambda x: [gr.update(interactive=not flags.Performance.has_restricted_features(x))] * 11 +
                                               [gr.update(visible=not flags.Performance.has_restricted_features(x))] * 1 +
                                               [gr.update(value=flags.Performance.has_restricted_features(x))] * 1,
                                     inputs=performance_selection,
                                     outputs=[
                                         guidance_scale, sharpness, adm_scaler_end, adm_scaler_positive,
                                         adm_scaler_negative, refiner_switch, refiner_model, sampler_name,
                                         scheduler_name, adaptive_cfg, refiner_swap_method, negative_prompt, disable_intermediate_results
                                     ], queue=False, show_progress=False)

        output_format.input(lambda x: gr.update(output_format=x), inputs=output_format)

        advanced_checkbox.change(lambda x: gr.update(visible=x), advanced_checkbox, advanced_column,
                                 queue=False, show_progress=False) \
            .then(fn=lambda: None, _js='refresh_grid_delayed', queue=False, show_progress=False)

        inpaint_mode.change(inpaint_mode_change, inputs=[inpaint_mode, inpaint_engine_state], outputs=[
            inpaint_additional_prompt, outpaint_selections, example_inpaint_prompts,
            inpaint_disable_initial_latent, inpaint_engine,
            inpaint_strength, inpaint_respective_field
        ], show_progress=False, queue=False)

        # load configured default_inpaint_method
        default_inpaint_ctrls = [inpaint_mode, inpaint_disable_initial_latent, inpaint_engine, inpaint_strength, inpaint_respective_field]
        for mode, disable_initial_latent, engine, strength, respective_field in [default_inpaint_ctrls] + enhance_inpaint_update_ctrls:
            shared.gradio_root.load(inpaint_mode_change, inputs=[mode, inpaint_engine_state], outputs=[
                inpaint_additional_prompt, outpaint_selections, example_inpaint_prompts, disable_initial_latent,
                engine, strength, respective_field
            ], show_progress=False, queue=False)

        generate_mask_button.click(fn=generate_mask,
                                   inputs=[inpaint_input_image, inpaint_mask_model, inpaint_mask_cloth_category,
                                           inpaint_mask_dino_prompt_text, inpaint_mask_sam_model,
                                           inpaint_mask_box_threshold, inpaint_mask_text_threshold,
                                           inpaint_mask_sam_max_detections, dino_erode_or_dilate, debugging_dino],
                                   outputs=inpaint_mask_image, show_progress=True, queue=True)

        ctrls = [currentTask, generate_image_grid]
        ctrls += [
            prompt, negative_prompt, style_selections,
            performance_selection, aspect_ratios_selection, image_number, output_format, image_seed,
            read_wildcards_in_order, sharpness, guidance_scale
        ]

        ctrls += [base_model, refiner_model, refiner_switch] + lora_ctrls
        ctrls += [input_image_checkbox, current_tab]
        ctrls += [uov_method, uov_input_image]
        ctrls += [outpaint_selections, inpaint_input_image, inpaint_additional_prompt, inpaint_mask_image]
        ctrls += [disable_preview, disable_intermediate_results, disable_seed_increment, black_out_nsfw]
        ctrls += [adm_scaler_positive, adm_scaler_negative, adm_scaler_end, adaptive_cfg, clip_skip]
        ctrls += [sampler_name, scheduler_name, vae_name]
        ctrls += [overwrite_step, overwrite_switch, overwrite_width, overwrite_height, overwrite_vary_strength]
        ctrls += [overwrite_upscale_strength, mixing_image_prompt_and_vary_upscale, mixing_image_prompt_and_inpaint]
        ctrls += [debugging_cn_preprocessor, skipping_cn_preprocessor, canny_low_threshold, canny_high_threshold]
        ctrls += [refiner_swap_method, controlnet_softness]
        ctrls += freeu_ctrls
        ctrls += inpaint_ctrls

        if not args_manager.args.disable_image_log:
            ctrls += [save_final_enhanced_image_only]

        if not args_manager.args.disable_metadata:
            ctrls += [save_metadata_to_images, metadata_scheme]

        ctrls += ip_ctrls
        ctrls += [debugging_dino, dino_erode_or_dilate, debugging_enhance_masks_checkbox,
                  enhance_input_image, enhance_checkbox, enhance_uov_method, enhance_uov_processing_order,
                  enhance_uov_prompt_type]
        ctrls += enhance_ctrls

        def parse_meta(raw_prompt_txt, is_generating):
            loaded_json = None
            if is_json(raw_prompt_txt):
                loaded_json = json.loads(raw_prompt_txt)

            if loaded_json is None:
                if is_generating:
                    return gr.update(), gr.update(), gr.update()
                else:
                    return gr.update(), gr.update(visible=True), gr.update(visible=False)

            return json.dumps(loaded_json), gr.update(visible=False), gr.update(visible=True)

        prompt.input(parse_meta, inputs=[prompt, state_is_generating], outputs=[prompt, generate_button, load_parameter_button], queue=False, show_progress=False)

        load_parameter_button.click(modules.meta_parser.load_parameter_button_click, inputs=[prompt, state_is_generating, inpaint_mode], outputs=load_data_outputs, queue=False, show_progress=False)

        def trigger_metadata_import(file, state_is_generating):
            parameters, metadata_scheme = modules.meta_parser.read_info_from_image(file)
            if parameters is None:
                print('Could not find metadata in the image!')
                parsed_parameters = {}
            else:
                metadata_parser = modules.meta_parser.get_metadata_parser(metadata_scheme)
                parsed_parameters = metadata_parser.to_json(parameters)

            return modules.meta_parser.load_parameter_button_click(parsed_parameters, state_is_generating, inpaint_mode)

        metadata_import_button.click(trigger_metadata_import, inputs=[metadata_input_image, state_is_generating], outputs=load_data_outputs, queue=False, show_progress=True) \
            .then(style_sorter.sort_styles, inputs=style_selections, outputs=style_selections, queue=False, show_progress=False)

        # Quick download below main gallery
        def quick_download_clicked(selected_img, task):
            target = None
            if selected_img and os.path.exists(selected_img):
                target = selected_img
            elif task and hasattr(task, 'results') and task.results:
                for res in reversed(task.results):
                    if isinstance(res, str) and os.path.exists(res):
                        target = res
                        break
            if not target:
                recent = history_manager.scan_history_images(limit=1)
                if recent:
                    target = recent[0]

            if target:
                ok, msg = history_manager.copy_image_to_downloads(target)
                return msg
            return "❌ Noch kein Bild vorhanden."

        def on_main_gallery_select(evt: gr.SelectData, task):
            if task and hasattr(task, 'results') and task.results:
                idx = evt.index
                if 0 <= idx < len(task.results):
                    res = task.results[idx]
                    if isinstance(res, str) and os.path.exists(res):
                        return res
            if evt.value and isinstance(evt.value, str) and os.path.exists(evt.value):
                return evt.value
            return ""

        gallery.select(on_main_gallery_select, inputs=[currentTask], outputs=[last_selected_main_image], queue=False, show_progress=False)
        quick_download_btn.click(quick_download_clicked, inputs=[last_selected_main_image, currentTask], outputs=[quick_download_status], queue=False)

        # History and Downloads Manager
        def reload_history_gallery():
            imgs = history_manager.scan_history_images(limit=80)
            return gr.update(value=imgs), imgs

        history_refresh_btn.click(reload_history_gallery, outputs=[history_gallery, history_image_paths], queue=False)
        shared.gradio_root.load(reload_history_gallery, outputs=[history_gallery, history_image_paths], queue=False)

        def on_history_select(evt: gr.SelectData, paths):
            if not paths or evt.index >= len(paths):
                return None, "", "*Keine Details gefunden.*"
            selected = paths[evt.index]
            details = history_manager.get_image_details(selected)
            return selected, selected, details["info_markdown"]

        history_gallery.select(on_history_select, inputs=[history_image_paths], outputs=[history_selected_preview, history_selected_path, history_info_box], queue=False)

        def on_history_download(selected_path):
            if not selected_path:
                return "❌ Bitte wähle zuerst ein Bild aus dem Verlauf aus."
            ok, msg = history_manager.copy_image_to_downloads(selected_path)
            return msg

        history_download_btn.click(on_history_download, inputs=[history_selected_path], outputs=[history_status], queue=False)

        def on_history_load_prompt(selected_path):
            if not selected_path:
                return gr.update(), gr.update()
            details = history_manager.get_image_details(selected_path)
            return gr.update(value=details["prompt"]), gr.update(value=details["negative_prompt"])

        history_load_prompt_btn.click(on_history_load_prompt, inputs=[history_selected_path], outputs=[prompt, negative_prompt], queue=False)

        def on_history_load_input(selected_path):
            if not selected_path or not os.path.exists(selected_path):
                return gr.update(), gr.update()
            import cv2
            img = cv2.imread(selected_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img, True

        history_load_input_btn.click(on_history_load_input, inputs=[history_selected_path], outputs=[uov_input_image, input_image_checkbox], queue=False)

        def on_download_all_today():
            today_str = time.strftime("%Y-%m-%d")
            today_folder = os.path.join(modules.config.path_outputs, today_str)
            if not os.path.exists(today_folder):
                return f"❌ Heute ({today_str}) wurden noch keine Bilder generiert."
            images = []
            for ext in ('*.png', '*.jpg', '*.jpeg', '*.webp'):
                images.extend(glob.glob(os.path.join(today_folder, ext)))
            if not images:
                return f"❌ Keine Bilder für heute ({today_str}) gefunden."
            ok, msg = history_manager.copy_multiple_to_downloads(images)
            return msg

        history_download_all_today_btn.click(on_download_all_today, outputs=[history_status], queue=False)

        # Guide (3D & Anime)
        def on_guide_template_change(name):
            tmpl = prompt_guide.GUIDE_TEMPLATES.get(name, {})
            if not tmpl:
                return ""
            return f"**Kategorie:** `{tmpl.get('category')}` | **Empfohlenes Modell:** `{tmpl.get('recommended_model')}`\n\n**Beschreibung:** {tmpl.get('description')}\n\n**Prompt-Vorschau:**\n> {tmpl.get('prompt')}\n\n**Stile:** `{tmpl.get('styles')}` | **CFG:** `{tmpl.get('guidance_scale')}` | **Format:** `{tmpl.get('aspect_ratio')}`"

        guide_template_dropdown.change(on_guide_template_change, inputs=[guide_template_dropdown], outputs=[guide_template_info], queue=False)
        shared.gradio_root.load(lambda: on_guide_template_change(prompt_guide.get_template_names()[0]), outputs=[guide_template_info], queue=False)

        def on_guide_apply(name):
            prompt_val, neg_prompt_val, styles_val, ar_val, cfg_val, model_val = prompt_guide.load_template_data(name)
            status_msg = f"✅ Vorlage **{name}** geladen! Prompt, Stile und Einstellungen wurden übernommen."
            model_update = gr.update()
            if model_val and model_val in modules.config.model_filenames:
                model_update = gr.update(value=model_val)
                status_msg += f" Basis-Modell auf `{model_val}` gesetzt."
            ar_update = gr.update()
            if ar_val:
                try:
                    ar_formatted = modules.config.add_ratio(ar_val)
                    ar_update = gr.update(value=ar_formatted)
                except Exception:
                    ar_update = gr.update(value=ar_val)
            return [
                gr.update(value=prompt_val),
                gr.update(value=neg_prompt_val),
                gr.update(value=styles_val),
                ar_update,
                gr.update(value=cfg_val),
                model_update,
                status_msg
            ]

        guide_apply_btn.click(
            on_guide_apply,
            inputs=[guide_template_dropdown],
            outputs=[prompt, negative_prompt, style_selections, aspect_ratios_selection, guidance_scale, base_model, guide_apply_status],
            queue=False
        ).then(fn=style_sorter.sort_styles, inputs=style_selections, outputs=style_selections, queue=False, show_progress=False)

        # Model Compatibility & VRAM Calculator handlers
        model_calc_btn.click(fn=model_checker.calculate_compatibility, inputs=[model_calc_input], outputs=[model_calc_result], queue=False)
        model_calc_input.submit(fn=model_checker.calculate_compatibility, inputs=[model_calc_input], outputs=[model_calc_result], queue=False)

        btn_test_flux_schnell.click(lambda: ("flux schnell fp8", model_checker.calculate_compatibility("flux schnell fp8")), outputs=[model_calc_input, model_calc_result], queue=False)
        btn_test_flux_dev.click(lambda: ("flux dev fp8", model_checker.calculate_compatibility("flux dev fp8")), outputs=[model_calc_input, model_calc_result], queue=False)
        btn_test_flux_fp16.click(lambda: ("flux dev fp16", model_checker.calculate_compatibility("flux dev fp16")), outputs=[model_calc_input, model_calc_result], queue=False)
        btn_test_turbo.click(lambda: ("sdxl turbo", model_checker.calculate_compatibility("sdxl turbo")), outputs=[model_calc_input, model_calc_result], queue=False)
        btn_test_sd15.click(lambda: ("sd 1.5", model_checker.calculate_compatibility("sd 1.5")), outputs=[model_calc_input, model_calc_result], queue=False)

        refresh_custom_folder_btn.click(fn=get_custom_folder_files, outputs=[custom_folder_file_list], queue=False)

        def on_custom_model_select(m):
            if m and m != 'None':
                return gr.update(value=m)
            return gr.update()

        all_models_dropdown.change(on_custom_model_select, inputs=[all_models_dropdown], outputs=[base_model], queue=False)

        generate_button.click(lambda: (gr.update(visible=True, interactive=True),
                                      gr.update(visible=True, interactive=True),
                                      gr.update(visible=True, interactive=True, value="⏸️ Pause"),
                                      gr.update(visible=False, interactive=False), [], True),
                              outputs=[stop_button, skip_button, pause_button, generate_button, gallery, state_is_generating]) \
            .then(fn=refresh_seed, inputs=[seed_random, image_seed], outputs=image_seed) \
            .then(fn=get_task, inputs=ctrls, outputs=currentTask) \
            .then(fn=generate_clicked, inputs=currentTask, outputs=[progress_html, progress_window, progress_gallery, gallery]) \
            .then(lambda: (gr.update(visible=True, interactive=True),
                           gr.update(visible=False, interactive=False),
                           gr.update(visible=False, interactive=False),
                           gr.update(visible=False, interactive=False), False),
                  outputs=[generate_button, stop_button, skip_button, pause_button, state_is_generating]) \
            .then(fn=update_history_link, outputs=history_link) \
            .then(reload_history_gallery, outputs=[history_gallery, history_image_paths], queue=False) \
            .then(fn=lambda: None, _js='playNotification').then(fn=lambda: None, _js='refresh_grid_delayed')

        def reset_clicked():
            import ldm_patched.modules.model_management as mm
            mm.set_paused(False)
            mm.interrupt_current_processing(False)
            return [worker.AsyncTask(args=[]), False, gr.update(visible=True, interactive=True)] + \
                   [gr.update(visible=False)] * 7 + \
                   [gr.update(visible=True, value=[])]

        reset_button.click(reset_clicked,
                           outputs=[currentTask, state_is_generating, generate_button,
                                    reset_button, stop_button, skip_button, pause_button,
                                    progress_html, progress_window, progress_gallery, gallery],
                           queue=False)

        for notification_file in ['notification.ogg', 'notification.mp3']:
            if os.path.exists(notification_file):
                gr.Audio(interactive=False, value=notification_file, elem_id='audio_notification', visible=False)
                break

        def trigger_describe(modes, img, apply_styles):
            describe_prompts = []
            styles = set()

            if flags.describe_type_photo in modes:
                from extras.interrogate import default_interrogator as default_interrogator_photo
                describe_prompts.append(default_interrogator_photo(img))
                styles.update(["Fooocus V2", "Fooocus Enhance", "Fooocus Sharp"])

            if flags.describe_type_anime in modes:
                from extras.wd14tagger import default_interrogator as default_interrogator_anime
                describe_prompts.append(default_interrogator_anime(img))
                styles.update(["Fooocus V2", "Fooocus Masterpiece"])

            if len(styles) == 0 or not apply_styles:
                styles = gr.update()
            else:
                styles = list(styles)

            if len(describe_prompts) == 0:
                describe_prompt = gr.update()
            else:
                describe_prompt = ', '.join(describe_prompts)

            return describe_prompt, styles

        describe_btn.click(trigger_describe, inputs=[describe_methods, describe_input_image, describe_apply_styles],
                           outputs=[prompt, style_selections], show_progress=True, queue=True) \
            .then(fn=style_sorter.sort_styles, inputs=style_selections, outputs=style_selections, queue=False, show_progress=False) \
            .then(lambda: None, _js='()=>{refresh_style_localization();}')

        if args_manager.args.enable_auto_describe_image:
            def trigger_auto_describe(mode, img, prompt, apply_styles):
                # keep prompt if not empty
                if prompt == '':
                    return trigger_describe(mode, img, apply_styles)
                return gr.update(), gr.update()

            uov_input_image.upload(trigger_auto_describe, inputs=[describe_methods, uov_input_image, prompt, describe_apply_styles],
                                   outputs=[prompt, style_selections], show_progress=True, queue=True) \
                .then(fn=style_sorter.sort_styles, inputs=style_selections, outputs=style_selections, queue=False, show_progress=False) \
                .then(lambda: None, _js='()=>{refresh_style_localization();}')

            enhance_input_image.upload(lambda: gr.update(value=True), outputs=enhance_checkbox, queue=False, show_progress=False) \
                .then(trigger_auto_describe, inputs=[describe_methods, enhance_input_image, prompt, describe_apply_styles],
                      outputs=[prompt, style_selections], show_progress=True, queue=True) \
                .then(fn=style_sorter.sort_styles, inputs=style_selections, outputs=style_selections, queue=False, show_progress=False) \
                .then(lambda: None, _js='()=>{refresh_style_localization();}')

def dump_default_english_config():
    from modules.localization import dump_english_config
    dump_english_config(grh.all_components)


# dump_default_english_config()

shared.gradio_root.launch(
    inbrowser=args_manager.args.in_browser,
    server_name=args_manager.args.listen,
    server_port=args_manager.args.port,
    share=args_manager.args.share,
    auth=check_auth if (args_manager.args.share or args_manager.args.listen) and auth_enabled else None,
    allowed_paths=[modules.config.path_outputs],
    blocked_paths=[constants.AUTH_FILENAME]
)
