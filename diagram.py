#!/usr/bin/env python3

from diagrams import Diagram, Cluster
from diagrams.custom import Custom

with Diagram('Architecture'):
    with Cluster('AWS'):
        fastapi = Custom('fastapi', 'images/fastapi.png')
