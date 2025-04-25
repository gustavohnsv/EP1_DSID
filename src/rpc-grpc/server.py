import grpc
import math
import random
import logging
from concurrent import futures

# Import the generated classes
import service_pb2
import service_pb2_grpc

class BenchmarkServices(service_pb2_grpc.BenchmarkServicesServicer):

    def VoidOP(self, request, context):
        return service_pb2.Empty()
    
    def LongOP(self, request, context):
        prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        if request.value == 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Value cannot be zero")
        result = request.value * random.choice(prime_numbers)
        return service_pb2.LongValue(value=result)
    
    def MultLongOP(self, request, context):
        result = 1
        if len(request.values) != 8:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid number of arguments. Expected 8.")
        else:
            for value in request.values:
                if (value == 0):
                    result *= 1
                else:
                    result *= value.value
        return service_pb2.LongValue(value=result)
    
    def StringOP(self, request, context):
        size = len(request.value)
        if size == 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "String cannot be empty")
        elif size > pow(2, 20):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "String is too long")
        result = ""
        for i in range(size):
            result += chr(ord(request.value[i]) + 17)
        return service_pb2.StringValue(value=result)
    
    def rotate_vector(self, dx, dy, angle): # For ClassOP function
        angle_deg = math.radians(angle)
        cos_theta = math.cos(angle_deg)
        sin_theta = math.sin(angle_deg)
        rot_x = dx * cos_theta - dy * sin_theta
        rot_y = dx * sin_theta + dy * cos_theta
        return rot_x, rot_y
    
    def ClassOP(self, request, context):
        if request.start.color != request.end.color:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Start and end points must have the same color")
        if request.start.xAxis == request.end.xAxis and request.start.yAxis == request.end.yAxis and request.start.zAxis == request.end.zAxis:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Start and end points cannot be the same")

        dx = request.end.xAxis - request.start.xAxis
        dy = request.end.yAxis - request.start.yAxis

        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        if magnitude == 0:
            dx_norm, dy_norm = 0, 0
        else:
            dx_norm = dx / magnitude
            dy_norm = dy / magnitude

        rotated_dx, rotated_dy = self.rotate_vector(dx_norm, dy_norm, 45)

        shadow_offset_x = int(rotated_dx * 2)
        shadow_offset_y = int(rotated_dy * 2)

        shadow_start = service_pb2.PointValue(
            xAxis=request.start.xAxis,
            yAxis=request.start.yAxis,
            zAxis=request.start.zAxis,
            color="Red"
        )
        shadow_end = service_pb2.PointValue(
            xAxis=(request.end.xAxis + shadow_offset_x),
            yAxis=(request.end.yAxis + shadow_offset_y),
            zAxis=min(request.start.zAxis, request.end.zAxis),
            color="Red"
        )
        return service_pb2.VectorValue(start=shadow_start, end=shadow_end)
        
    
def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))
        service_pb2_grpc.add_BenchmarkServicesServicer_to_server(BenchmarkServices(), server)
        server.add_insecure_port('0.0.0.0:50051')
        logging.basicConfig(level=logging.INFO)
        logging.info("[gRPC Server] Starting server on port 50051")
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\r")
        logging.info("[gRPC Server] 🛑 Server stopped by user.")

if __name__ == '__main__':
    serve()