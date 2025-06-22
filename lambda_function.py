import json, os, base64, traceback
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

def indent(text, prefix):
    return "\n".join(prefix + line if line.strip() else line
                     for line in text.splitlines())

def handler(event, context):
    try:
        raw_body = event.get("body", "")
        parsed = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
        user_code = parsed.get("body", "")
        if not isinstance(user_code, str) or not user_code.strip():
            return {"statusCode": 400,
                    "body": "Error: El campo 'body' debe ser un string con el código del diagrama."}

        diagram_template = f'''
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Mi Diagrama", show=False, outformat=["png","svg"], filename="/tmp/diagram"):
{indent(user_code, "    ")}
'''

        exec(diagram_template, {})

        result = {}

        # Leer SVG como texto plano
        svg_path = "/tmp/diagram.svg"
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_text = f.read()
        os.remove(svg_path)
        result["svg_image"] = svg_text

        # Leer PNG y codificar
        png_path = "/tmp/diagram.png"
        with open(png_path, "rb") as f:
            png_b64 = base64.b64encode(f.read()).decode("utf-8")
        os.remove(png_path)
        result["png_image"] = f"data:image/png;base64,{png_b64}"

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result)
        }

    except Exception:
        return {
            "statusCode": 500,
            "body": "Error al generar diagrama:\n" + traceback.format_exc()
        }
