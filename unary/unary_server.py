import grpc
from concurrent import futures
import time
import unary.unary_pb2_grpc as pb2_grpc
import unary.unary_pb2 as pb2


class UnaryService(pb2_grpc.UnaryServicer):
    """
        gRPC service
        """
    def __init__(self, *args, **kwargs):
        self.server_port = 46001

    def GetServerResponse(self, request, context):
        # get the string from the incoming request

        message = request.message
        result = f'Hello I am up and running received "{message}" message from you'
        result = {'message': result, 'received': True}

        return pb2.MessageResponse(**result)

    def start_server(self):
        # declare a server object with desired number
        # of thread pool workers.
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        pb2_grpc.add_UnaryServicer_to_server(UnaryService(), server)

        # bind the server to the port defined above
        server.add_insecure_port('[::]:{}'.format(self.server_port))

        # start the server
        server.start()

        try:
            while True:
                time.sleep(60*60*60)
        except KeyboardInterrupt:
            server.stop(0)
            print('Server Stopped ...')


curr_server = UnaryService()
curr_server.start_server()
