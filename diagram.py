#!/usr/bin/env python3

from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki

with Diagram('Architecture', show=False):
    with Cluster('AWS'):
        fastapi = Custom('app', 'images/fastapi.png')
        loki = Loki('logging')
        grafana = Grafana('visualization')
        prometheus = Prometheus('metrics')
        
        # logging
        fastapi >> loki
        
        # metrics
        prometheus >> [ loki, grafana, prometheus, fastapi ]
        
        # visualization
        grafana >> [ prometheus, loki ]
        