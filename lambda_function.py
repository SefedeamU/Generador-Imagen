import json, os, base64, traceback, re
from diagrams import Diagram, Cluster

from diagrams.aws.analytics import (
    AmazonOpensearchService, Analytics, Athena, Cloudsearch, DataLakeResource,
    EMRCluster, EMREngine, EMR, GlueCrawlers, GlueDataCatalog, Glue,
    KinesisDataAnalytics, KinesisDataFirehose, KinesisDataStreams,
    KinesisVideoStreams, LakeFormation, ManagedStreamingForKafka, Quicksight,
    RedshiftDenseComputeNode, RedshiftDenseStorageNode, Redshift
)
from diagrams.aws.ar import ArVr, Sumerian
from diagrams.aws.blockchain import BlockchainResource, Blockchain, ManagedBlockchain, QuantumLedgerDatabaseQldb
from diagrams.aws.business import AlexaForBusiness, BusinessApplications, Chime, Workmail
from diagrams.aws.compute import *
from diagrams.aws.cost import Budgets, CostAndUsageReport, CostExplorer, CostManagement, ReservedInstanceReporting, SavingsPlans
from diagrams.aws.database import *
from diagrams.aws.devtools import *
from diagrams.aws.enablement import *
from diagrams.aws.enduser import *
from diagrams.aws.engagement import *
from diagrams.aws.game import *
from diagrams.aws.general import *
from diagrams.aws.integration import *
from diagrams.aws.iot import *
from diagrams.aws.management import *
from diagrams.aws.media import *
from diagrams.aws.migration import *
from diagrams.aws.ml import *
from diagrams.aws.mobile import *
from diagrams.aws.network import *
from diagrams.aws.quantum import *
from diagrams.aws.robotics import *
from diagrams.aws.satellite import *
from diagrams.aws.security import *
from diagrams.aws.storage import *

from diagrams.gcp.analytics import *
from diagrams.gcp.api import *
from diagrams.gcp.compute import *
from diagrams.gcp.database import *
from diagrams.gcp.devtools import *
from diagrams.gcp.iot import IotCore
from diagrams.gcp.migration import *
from diagrams.gcp.ml import *
from diagrams.gcp.network import *
from diagrams.gcp.operations import *
from diagrams.gcp.security import *
from diagrams.gcp.storage import *


def indent(text, prefix):
    return "\n".join(prefix + line if line.strip() else line for line in text.splitlines())

def replace_local_images_with_base64(svg_text):
    pattern = r'xlink:href=["\']([^"\']+\.png)["\']'
    matches = re.findall(pattern, svg_text)
    for img_path in set(matches):
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
            svg_text = svg_text.replace(img_path, f'data:image/png;base64,{img_b64}')
    return svg_text

def handler(event, context):
    try:
        parsed = json.loads(event.get("body", event) or "{}")
        user_code = parsed.get("body", "")
        if not isinstance(user_code, str) or not user_code.strip():
            return {"statusCode":400, "body":"El campo 'body' debe ser un string con código válido."}

        diagram_code = f"""
from diagrams import Diagram, Cluster
# (import statements omitted)
with Diagram("Mi Diagrama", show=False, outformat=["png", "svg"], filename="/tmp/diagram"):
{indent(user_code, "    ")}
"""
        exec(diagram_code, globals())

        result = {}
        with open("/tmp/diagram.png", "rb") as f:
            result["png_image"] = "data:image/png;base64," + base64.b64encode(f.read()).decode()
        os.remove("/tmp/diagram.png")

        with open("/tmp/diagram.svg", "r", encoding="utf-8") as f:
            svg_text = f.read()
        os.remove("/tmp/diagram.svg")

        result["svg_image"] = replace_local_images_with_base64(svg_text)

        return {"statusCode":200, "headers":{"Content-Type":"application/json"},
                "body": json.dumps(result, ensure_ascii=False)}

    except Exception:
        return {"statusCode":500, "body":"Error al generar diagrama:\n" + traceback.format_exc()}
