import json, os, base64, traceback, re
from diagrams import Diagram, Cluster

# AWS
from diagrams.aws.compute import EC2, ECS, EKS, Lambda
from diagrams.aws.database import RDS, DynamoDB, Redshift, ElastiCache
from diagrams.aws.network import ELB, VPC, Route53, CloudFront
from diagrams.aws.storage import S3, EFS
from diagrams.aws.integration import SQS, SNS
# Azure
from diagrams.azure.compute import VirtualMachines, FunctionApps, AppServices
from diagrams.azure.database import Cosmosdb, Sqldatabase
from diagrams.azure.network import AppGateway, VirtualNetworks
from diagrams.azure.storage import BlobStorage, StorageAccounts
# GCP
from diagrams.gcp.compute import AppEngine, GCE, Functions
from diagrams.gcp.database import SQL, Spanner, Bigquery
from diagrams.gcp.analytics import PubSub, Dataflow
from diagrams.gcp.storage import GCS, Storage
from diagrams.gcp.ml import AutoML
# Kubernetes
from diagrams.k8s.compute import Pod, Deployment, StatefulSet
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.k8s.clusterconfig import HPA
# Alibaba Cloud
from diagrams.alibabacloud.compute import ECS as AlibabaECS
from diagrams.alibabacloud.storage import ObjectTableStore
# Oracle Cloud (OCI)
from diagrams.oci.compute import VirtualMachine, Container
from diagrams.oci.network import Firewall
from diagrams.oci.storage import FileStorage, StorageGateway
# OpenStack
from diagrams.openstack.compute import Nova
from diagrams.openstack.network import Neutron
from diagrams.openstack.storage import Cinder
# IBM
from diagrams.ibm.compute import IKS, CloudFoundry
# Firebase
from diagrams.firebase.database import Firestore
from diagrams.firebase.storage import Storage as FBStorage
# DigitalOcean
from diagrams.digitalocean.compute import Droplet
from diagrams.digitalocean.database import Database
from diagrams.digitalocean.storage import Volume
# Elastic
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.elastic.kibana import Kibana
# Outscale
from diagrams.outscale.compute import VM
from diagrams.outscale.network import Net
# On‑Premises / Generic
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
# SaaS / Programming / C4
from diagrams.saas.database import MySQL
from diagrams.programming.language import Python
from diagrams.c4 import Person, SystemBoundary

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
