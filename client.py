import sys
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the subfolder
subfolder_path = os.path.join(current_dir, 'grpc_output')

# Add the subfolder path to sys.path
sys.path.append(subfolder_path)

import grpc
import quadratic_pb2
import quadratic_pb2_grpc


# Client side for the gRPC service and quadratic equation input from user
def run():
    # Create a gRPC channel to the server
    channel = grpc.insecure_channel("localhost:50181")  # using open port that was found from socket_finder.py
    stub = quadratic_pb2_grpc.QuadraticSolverStub(channel)

    # Get coefficients from user input
    print("Enter coefficients for the quadratic equation (ax^2 + bx + c = 0):")
    while True:
        try:
            a = float(input("Enter coefficient a: "))
            if a == 0:
                raise ValueError("Coefficient 'a' cannot be zero for a quadratic equation.")
            b = float(input("Enter coefficient b: "))
            if b == 0:
                raise ValueError("Coefficient 'b' cannot be zero for a quadratic equation.")
            # Coefficient 'c' can be zero for a quadratic equation
            c = float(input("Enter coefficient c: "))
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter numeric values.")
            continue
        break

    # Create a request object and call the gRPC method
    request = quadratic_pb2.QuadraticRequest(a=a, b=b, c=c)
    response = stub.SolveQuadratic(request)

    # Print the response from the server
    if response.roots:
        print(f"Roots of the equation: {response.roots}")
    else:
        print("No real roots found.")


if __name__ == "__main__":
    run()