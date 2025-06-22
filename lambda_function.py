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
        # parseo igual que antes...
        
        diagram_template = f'''
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Mi Diagrama", show=False, outformat=["png","svg"], filename="/tmp/diagram"):
{indent(user_code, "    ")}
'''
        exec(diagram_template, {})

        # Leer SVG como texto
        with open("/tmp/diagram.svg", "r", encoding="utf-8") as f:
            svg_text = f.read()
        os.remove("/tmp/diagram.svg")

        # Leer PNG codificado
        with open("/tmp/diagram.png", "rb") as f:
            png_b64 = base64.b64encode(f.read()).decode("utf-8")
        os.remove("/tmp/diagram.png")

        # Armar JSON
        result = {
            "svg_image_raw": svg_text,
            "png_image": f"data:image/png;base64,{png_b64}"
        }

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
