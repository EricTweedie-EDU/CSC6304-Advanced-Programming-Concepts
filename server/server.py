import grpc
from concurrent import futures
import time

import quadratic_pb2
import quadratic_pb2_grpc

# Server side response for the gRPC service and quadratic equation function
def quadratic(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        root1 = (-b + discriminant**0.5) / (2*a)
        root2 = (-b - discriminant**0.5) / (2*a)
        return root1, root2
    elif discriminant == 0:
        root = -b / (2*a)
        return root,
    else:
        return None
    
# gRPC service implementation
class QuadraticSolver(quadratic_pb2_grpc.QuadraticSolver):
    def SolveQuadratic(self, request, context):
        a = request.a
        b = request.b
        c = request.c
        roots = quadratic(a, b, c)
        if roots is None:
            return quadratic_pb2.QuadraticResponse(roots=[])
        else:
            return quadratic_pb2.QuadraticResponse(roots=list(roots))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    quadratic_pb2_grpc.add_QuadraticSolverServicer_to_server(QuadraticSolver(), server)
    server.add_insecure_port("[::]:50181") # bind to port that is open, checked with socket_finder.py
    server.start()
    print("gRPC Server running on port 50181...") # will need to update port depending on what is open on local machine
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
