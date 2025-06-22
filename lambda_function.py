import json
import os
import base64
import traceback

from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

def indent(text, prefix):
    return "\n".join(
        prefix + line if line.strip() else line
        for line in text.splitlines()
    )

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

        # Crear archivo Python temporal para ejecutar el diagrama
        diagram_template = f"""
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Mi Diagrama", show=False, outformat=["png", "svg"], filename="/tmp/diagram"):
{indent(user_code, "    ")}
"""
        exec(diagram_template, {})

        # Leer el archivo SVG como texto (sin codificar)
        with open("/tmp/diagram.svg", "r", encoding="utf-8") as f:
            svg_raw = f.read()
        os.remove("/tmp/diagram.svg")

        # Leer el archivo PNG y codificar en base64
        with open("/tmp/diagram.png", "rb") as f:
            png_encoded = base64.b64encode(f.read()).decode("utf-8")
        os.remove("/tmp/diagram.png")

        # Construir respuesta JSON
        result = {
            "svg_image_raw": svg_raw,
            "png_image": f"data:image/png;base64,{png_encoded}"
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(result)
        }

    except Exception:
        return {
            "statusCode": 500,
            "body": "Error al generar diagrama:\n" + traceback.format_exc()
        }
