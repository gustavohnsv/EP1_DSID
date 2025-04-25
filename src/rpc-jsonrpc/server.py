import math
import random
import logging
# from socketserver import ThreadingMixIn
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

# class ThreadingSimpleServer(ThreadingMixIn, SimpleJSONRPCServer):
#     pass

def VoidOP():
    return {}

def LongOP(value):
    prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if value == 0:
        raise ValueError("Value cannot be zero")
    result = value * random.choice(prime_numbers)
    return {"value": result}

def MultLongOP(values):
    result = 1
    if len(values) != 8:
        raise ValueError("Invalid number of arguments. Expected 8.")
    else:
        for value in values:
            if value == 0:
                result *= 1
            else:
                result *= value
    return {"value": result}

def StringOP(value):
    size = len(value)
    if size == 0:
        raise ValueError("String cannot be empty")
    elif size > pow(2, 20):
        raise ValueError("String is too long")
    result = ""
    for i in range(size):
        result += chr(ord(value[i]) + 17)
    return {"value": result}

def rotate_vector(dx, dy, angle): # For ClassOP function
    angle_deg = math.radians(angle)
    cos_theta = math.cos(angle_deg)
    sin_theta = math.sin(angle_deg)
    rot_x = dx * cos_theta - dy * sin_theta
    rot_y = dx * sin_theta + dy * cos_theta
    return rot_x, rot_y

def ClassOP(start, end):
    if start['color'] != end['color']:
        raise ValueError("Start and end points must have the same color")
    if start['xAxis'] == end['xAxis'] and start['yAxis'] == end['yAxis'] and start['zAxis'] == end['zAxis']:
        raise ValueError("Start and end points cannot be the same")
    
    dx = end['xAxis'] - start['xAxis']
    dy = end['yAxis'] - start['yAxis']

    magnitude = math.sqrt(dx ** 2 + dy ** 2)
    if magnitude == 0:
        dx_norm, dy_norm = 0, 0
    else:
        dx_norm = dx / magnitude
        dy_norm = dy / magnitude

    rotated_dx, rotated_dy = rotate_vector(dx_norm, dy_norm, 45)

    shadow_offset_x = int(rotated_dx * 2)
    shadow_offset_y = int(rotated_dy * 2)

    shadow_start = {
        "xAxis": start['xAxis'],
        "yAxis": start['yAxis'],
        "zAxis": start['zAxis'],
        "color": "Red"
    }

    shadow_end = {
        "xAxis": (end['xAxis'] + shadow_offset_x),
        "yAxis": (end['yAxis'] + shadow_offset_y),
        "zAxis": min(start['zAxis'], end['zAxis']),
        "color": "Red"
    }
    return {
        "start": shadow_start,
        "end": shadow_end
    }

try:
    # server = ThreadingSimpleServer(('0.0.0.0', 50050))
    server = SimpleJSONRPCServer(('0.0.0.0', 50050))
    server.register_function(VoidOP, 'VoidOP')
    server.register_function(LongOP, 'LongOP')
    server.register_function(MultLongOP, 'MultLongOP')
    server.register_function(StringOP, 'StringOP')
    server.register_function(ClassOP, 'ClassOP')
    logging.basicConfig(level=logging.INFO)
    logging.info("[jsonRPC Server] Starting server on port 50050")
    server.serve_forever()
except KeyboardInterrupt as e:
    print("\r")
    logging.info("[jsonRPC Server] 🛑 Server stopped by user.")
    server.server_close()