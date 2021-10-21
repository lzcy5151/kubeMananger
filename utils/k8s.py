import string

from kubeManager.settings import BASE_DIR, CLUSTER_NAME
from kubernetes import client, config
from kubernetes.client import V1Node


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
