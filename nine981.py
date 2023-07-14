import grpc
from yagrc import importer
import json
from google.protobuf.json_format import MessageToJson
importer.add_lazy_packages(["spacex.api.device"])
from spacex.api.device import device_pb2
from spacex.api.device import device_pb2_grpc
import warnings

warnings.filterwarnings("ignore")


def setup():
    channel = grpc.insecure_channel("192.168.100.1:9200")
    importer.resolve_lazy_imports(channel)
    stub = device_pb2_grpc.DeviceStub(channel)
    return stub


def get_status():
    stub = setup()
    return json.loads(stub.Handle(device_pb2.Request(get_status={}), timeout=5))

def reboot():
    stub = setup()
    return stub.Handle(device_pb2.Request(reboot={}), timeout=5)

def get_obstruction_map():
    stub = setup()
    map=stub.Handle(device_pb2.Request(dish_get_obstruction_map={}), timeout=5)
    return MessageToJson(map)
          
