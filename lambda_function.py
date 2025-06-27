import json, os, base64, traceback, re
from diagrams import Diagram, Cluster

from diagrams.aws.analytics import (
    ElasticsearchService, EMRCluster, EMREngine, EMR,
    GlueCrawlers, GlueDataCatalog, Glue,
    KinesisDataAnalytics, KinesisDataFirehose, KinesisDataStreams, KinesisVideoStreams,
    LakeFormation, ManagedStreamingForKafka, Quicksight,
    RedshiftDenseComputeNode, RedshiftDenseStorageNode, Redshift
)
from diagrams.aws.ar import ArVr, Sumerian
from diagrams.aws.blockchain import BlockchainResource, Blockchain, ManagedBlockchain, QuantumLedgerDatabaseQldb
from diagrams.aws.business import AlexaForBusiness, BusinessApplications, Chime, Workmail
from diagrams.aws.compute import (
    AppRunner, ApplicationAutoScaling, Batch, ComputeOptimizer, Compute,
    EC2Ami, EC2AutoScaling, EC2ContainerRegistryImage, EC2ContainerRegistryRegistry,
    EC2ContainerRegistry, EC2ElasticIpAddress, EC2ImageBuilder,
    EC2Instance, EC2Instances, EC2Rescue, EC2SpotInstance, EC2,
    ElasticBeanstalkApplication, ElasticBeanstalkDeployment, ElasticBeanstalk,
    ElasticContainerServiceContainer, ElasticContainerServiceService, ElasticContainerService,
    ElasticKubernetesService, Fargate, LambdaFunction, Lambda, Lightsail,
    LocalZones, Outposts, ServerlessApplicationRepository, ThinkboxDeadline,
    ThinkboxDraft, ThinkboxFrost, ThinkboxKrakatoa, ThinkboxSequoia, ThinkboxStoke,
    ThinkboxXmesh, VmwareCloudOnAWS, Wavelength
)
from diagrams.aws.cost import (
    Budgets, CostAndUsageReport, CostExplorer, CostManagement,
    ReservedInstanceReporting, SavingsPlans
)
from diagrams.aws.database import (
    AuroraInstance, Aurora,
    DatabaseMigrationServiceDatabaseMigrationWorkflow, DatabaseMigrationService,
    Database, DocumentdbMongodbCompatibility, DynamodbAttribute, DynamodbAttributes,
    DynamodbDax, DynamodbGlobalSecondaryIndex, DynamodbItem, DynamodbItems,
    DynamodbStreams, DynamodbTable, Dynamodb,
    ElasticacheCacheNode, ElasticacheForMemcached, ElasticacheForRedis, Elasticache,
    KeyspacesManagedApacheCassandraService, Neptune,
    QuantumLedgerDatabaseQldb, RDSInstance, RDSMariadbInstance, RDSMysqlInstance,
    RDSOnVmware, RDSOracleInstance, RDSPostgresqlInstance, RDSSqlServerInstance,
    RDS, RedshiftDenseComputeNode, RedshiftDenseStorageNode, Redshift, Timestream
)
from diagrams.aws.devtools import (
    CloudDevelopmentKit, Cloud9Resource, Cloud9,
    Codeartifact, Codebuild, Codecommit, Codedeploy, Codepipeline, Codestar,
    CommandLineInterface, DeveloperTools, ToolsAndSdks, XRay
)
from diagrams.aws.integration import SQS, SNS, EventBridge, StepFunctions  # ajusta según versión instalada
from diagrams.aws.iot import IoTCore, IoTPipeline, IoTSiteWise  # etc.
from diagrams.aws.management import Cloudwatch, Config, Cloudtrail, GuardDuty  # ajusta según versión
from diagrams.aws.media import MediaConvert, MediaLive, MediaPackage, MediaStore  # etc.
from diagrams.aws.ml import SageMaker, Comprehend, Rekognition, Translate  # etc.
from diagrams.aws.mobile import MobileAnalytics, Pinpoint, CognitoIdentity  # etc.
from diagrams.aws.network import (
    ELB, Route53, VPC, CloudFront, VPN, DirectConnect, API, TransitGateway  # etc.
)
from diagrams.aws.security import IAM, KMS, Shield, WAF, SecurityHub  # etc.
from diagrams.aws.storage import S3, EFS, Glacier, StorageGateway, Snowball, SnowballEdge, Snowmobile

from diagrams.gcp.analytics import Bigquery, Composer, DataCatalog, DataFusion, Dataflow, Datalab, Dataprep, Dataproc, Genomics, Pubsub
from diagrams.gcp.api import APIGateway, Apigee, Endpoints
from diagrams.gcp.compute import AppEngine, ComputeEngine, ContainerOptimizedOS, Functions, GKEOnPrem, GPU, KubernetesEngine, Run
from diagrams.gcp.database import Bigtable, Datastore, Firestore, Memorystore, Spanner, SQL
from diagrams.gcp.devtools import Build, CodeForIntellij, Code, ContainerRegistry, Scheduler, SDK, SourceRepositories, Tasks, TestLab, ToolsForEclipse, ToolsForPowershell
from diagrams.gcp.iot import IotCore
from diagrams.gcp.migration import TransferAppliance
from diagrams.gcp.ml import (
    AdvancedSolutionsLab, AIHub, AIPlatformDataLabelingService, AIPlatform,
    AutomlNaturalLanguage, AutomlTables, AutomlTranslation, AutomlVideoIntelligence,
    AutomlVision, Automl, DialogFlowEnterpriseEdition, InferenceAPI, JobsAPI,
    NaturalLanguageAPI, RecommendationsAI, SpeechToText, TextToSpeech, TPU,
    TranslationAPI, VideoIntelligenceAPI, VisionAPI
)
from diagrams.gcp.network import (
    Armor, CDN, DedicatedInterconnect, DNS, ExternalIpAddresses,
    FirewallRules, LoadBalancing, NAT, Network, PartnerInterconnect,
    PremiumNetworkTier, Router, Routes, StandardNetworkTier, TrafficDirector,
    VirtualPrivateCloud, VPN
)
from diagrams.gcp.operations import Logging, Monitoring
from diagrams.gcp.security import Iam, IAP, KeyManagementService, ResourceManager, SecurityCommandCenter, SecurityScanner
from diagrams.gcp.storage import Filestore, PersistentDisk, Storage


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
