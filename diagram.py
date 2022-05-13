from diagrams import Cluster, Diagram
from diagrams.custom import Custom

from diagrams.onprem.monitoring import Grafana, Prometheus

with Diagram('Architecture'):
    # prometheus = Prometheus('metrics')
    grafana = Grafana('monitoring')
    loki = Custom('logs', 'images/loki.png')
    fastapi = Custom('fastapi', 'images/fastapi.png')

    # fastapi << prometheus << grafana
    fastapi >> loki << grafana
