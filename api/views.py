from django.shortcuts import render
from utils import kube_cluster
from utils.k8s import NodeStats
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
# Create your views here.


@api_view(['GET'])
def list_node_stats(request):
    nodes = kube_cluster.api_instance.list_node()
    data = []

    for node in nodes.items:
        node_s = NodeStats()
        node_stats = NodeStats.format_node(node)
        node_s.name = node_stats['name']
        node_s.address = node_stats['address']
        node_s.state = node_stats['conditions_ready']

        data.append(node_s.__dict__)

    response = {
        'data': data,
    }

    return Response(response)
