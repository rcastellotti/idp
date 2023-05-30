import logging

from google.protobuf.descriptor_pool import DescriptorPool
import grpc
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import \
    ProtoReflectionDescriptorDatabase

from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc


def run():
    print("Will try to greet world ...")
    with grpc.insecure_channel('192.168.100.1:9200') as channel:
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)

        # Create the gRPC request message to get the service descriptor
        file_descriptor_request = reflection_pb2.ServerReflectionRequest()
        file_descriptor_request.host = '192.168.100.1:9200'
        file_descriptor_request.file_by_filename = "Handle"

        # Retrieve the service descriptor using server reflection
        file_descriptor_response = stub.ServerReflectionInfo(file_descriptor_request)

        # Extract the file descriptor
        file_descriptor_proto = file_descriptor_response.file_descriptor_response.file_descriptor_proto[0]

        # Create the dynamic stub using the file descriptor
    dynamic_stub = grpc.dynamic.stub(channel, file_descriptor_proto)
if __name__ == '__main__':
    logging.basicConfig()
    run()