import string

from kubeManager.settings import BASE_DIR, CLUSTER_NAME
from kubernetes import client, config
from kubernetes.client import V1Node, V1Deployment


class Kubernetes:
    def __init__(self, cluster_name=CLUSTER_NAME):
        self.__config_path = BASE_DIR.joinpath('kube')
        self.__configfile_path = self.__config_path.joinpath(cluster_name).as_posix()
        print(self.__configfile_path)

        config.kube_config.load_kube_config(self.__configfile_path)
        self.__client = client
        self.__api_instance = client.CoreV1Api()

    @property
    def configfile_path(self):
        return self.__configfile_path

    @property
    def api_instance(self):
        return self.__api_instance

    @api_instance.setter
    def api_instance(self, api_group):
        if api_group == 'v1':
            pass
        if api_group == 'v1/apps':
            self.__api_instance = client.AppsV1Api()


kube_cluster = Kubernetes()


class NodeStats:
    __state: str
    __name: str
    __address: str

    def __init__(self):
        self.__name = ''
        self.__address = ''
        self.__state = ''

    @staticmethod
    def format_node(node: V1Node):
        name = node.metadata.name
        ip_address = node.status.addresses[0].address
        if node.status.conditions[-1].type == 'Ready' and node.status.conditions[-1].status == 'True':
            conditions_ready = 'Ready'
        else:
            conditions_ready = 'Unready'
        return {
            'name': name,
            'address': ip_address,
            'conditions_ready': conditions_ready,
        }

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state


class PathDeployment:
    def __init__(self, deployment_name, namespace='default'):
        kube_cluster.api_instance = 'v1/apps'
        self.__api_instance = kube_cluster.api_instance
        self.__deployment_name = deployment_name
        self.__namespace = namespace
        self.__body = self.__api_instance.read_namespaced_deployment(deployment_name, namespace)

    def update_image(self, version, container_index=0):
        img_str = self.__body.spec.template.spec.containers[container_index].image
        image = img_str.split(':')
        if len(image) != 2:
            image.append('latest')
        image[-1] = version
        self.__body.spec.template.spec.containers[container_index].image = ':'.join(image)
        res = self.__apply()

        return {
            'deployment': res.metadata.name,
            'namespace': res.metadata.namespace,
            'image': res.spec.template.spec.containers[container_index].image,
        }

    def __apply(self):
        if isinstance(self.__body, V1Deployment):
            return self.__api_instance.patch_namespaced_deployment(self.__deployment_name, self.__namespace, self.__body)



