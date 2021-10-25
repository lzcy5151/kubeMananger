from django.shortcuts import render
from utils import kube_cluster
from utils.k8s import NodeStats, PathDeployment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import json


# Create your views here.

@swagger_auto_schema(methods=['GET'], deprecated=True)
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


@swagger_auto_schema(methods=['GET'], deprecated=True)
@api_view(['GET'])
def update_image_version(request, dep_name, namespace, new_version, container_index=0):
    path_deployment = PathDeployment(dep_name, namespace)
    data = path_deployment.update_image(new_version, container_index)

    return Response({'data': data})


@swagger_auto_schema(methods=['POST'], request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['new_version', 'container_index'],
    properties={
        'new_version': openapi.Schema(type=openapi.TYPE_STRING),
        'container_index': openapi.Schema(type=openapi.TYPE_INTEGER)
    },
))
@api_view(['POST'])
def update_image(request, namespace, deployment_name):
    if request.method == 'POST':
        data = json.loads(request.body)
        path_deployment = PathDeployment(deployment_name, namespace)
        res = path_deployment.update_image(data['new_version'], data['container_index'])

        return Response({
            'data': res,
        })
