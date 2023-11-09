#!/usr/bin/env python3

from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.logging import Loki
from diagrams.onprem.monitoring import Grafana

with Diagram('Architesture', show=False):
    with Cluster('AWS'):
        fastapi = Custom('worldtime', 'images/fastapi.png')
        loki = Loki('logging')
        grafana = Grafana('monitoring')

        fastapi >> loki >> grafana
