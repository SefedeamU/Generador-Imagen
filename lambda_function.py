import json, os, base64, traceback, re
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

def indent(text, prefix):
    return "\n".join(prefix + line if line.strip() else line for line in text.splitlines())

def replace_local_images_with_base64(svg_text):
    pattern = r'xlink:href=["\']([^"\']+\.png)["\']'
    matches = re.findall(pattern, svg_text)
    for img_path in set(matches):
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
                data_uri = f'data:image/png;base64,{img_b64}'
                svg_text = svg_text.replace(img_path, data_uri)
    return svg_text

def handler(event, context):
    try:
        raw_body = event.get("body", "")
        parsed = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
        user_code = parsed.get("body", "")

        if not isinstance(user_code, str) or not user_code.strip():
            return {
                "statusCode": 400,
                "body": "Error: El campo 'body' debe ser un string con el código del diagrama."
            }

        # Generar el código completo del diagrama
        diagram_code = f"""
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Mi Diagrama", show=False, outformat=["png", "svg"], filename="/tmp/diagram"):
{indent(user_code, "    ")}
"""
        exec(diagram_code, {})

        result = {}

        # PNG como Base64
        with open("/tmp/diagram.png", "rb") as f:
            result["png_image"] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        os.remove("/tmp/diagram.png")

        # Leer el SVG y reemplazar imágenes locales por base64
        with open("/tmp/diagram.svg", "r", encoding="utf-8") as f:
            svg_text = f.read()
        os.remove("/tmp/diagram.svg")

        svg_inlined = replace_local_images_with_base64(svg_text)
        result["svg_image"] = svg_inlined  # SVG sin escapar, útil para pegar directamente

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result, ensure_ascii=False)
        }

    except Exception:
        return {
            "statusCode": 500,
            "body": "Error al generar diagrama:\n" + traceback.format_exc()
        }
