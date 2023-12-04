"""
This module calls the gRPC api and returns JSON data, offers:
+ `api.get_status()`
+ `api.reboot()`
+ `api.get_obstruction_map()`

It should be straightforward to extend to call [other gRPC endpoints](https://gist.github.com/rcastellotti/e20630366dfeaeada6cc2680f562f6ac)
"""
import warnings
import grpc

try:
    from spacex.api.device import device_pb2_grpc  # pylint: disable=import-error
    from spacex.api.device import device_pb2  # pylint: disable=import-error
except ImportError:
    pass

from yagrc import importer
from google.protobuf.json_format import MessageToJson

importer.add_lazy_packages(["spacex.api.device"])

warnings.filterwarnings("ignore")


def setup():
    """
    Setup stuff
    """
    channel = grpc.insecure_channel("192.168.100.1:9200")
    importer.resolve_lazy_imports(channel)
    stub = device_pb2_grpc.DeviceStub(channel)
    return stub


def get_status():
    """
    grpcurl -plaintext -d '{"get_status":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
    """
    stub = setup()
    status = stub.Handle(device_pb2.Request(get_status={}), timeout=5)
    return MessageToJson(status)


def reboot():
    """
    grpcurl -plaintext -d '{"reboot":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
    """
    stub = setup()
    reboot_value = stub.Handle(device_pb2.Request(reboot={}), timeout=5)
    return MessageToJson(reboot_value)


def get_obstruction_map():
    """
    grpcurl -plaintext -d '{"dish_get_obstruction_map":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
    """
    stub = setup()
    obstruction_map = stub.Handle(
        device_pb2.Request(dish_get_obstruction_map={}), timeout=5
    )
    return MessageToJson(obstruction_map)
