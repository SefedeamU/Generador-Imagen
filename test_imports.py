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
print("✅ Todos los imports se realizaron correctamente.")