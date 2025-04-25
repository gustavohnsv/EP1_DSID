import os
import grpc
import time
import random
import statistics

# Import the generated classes
import service_pb2
import service_pb2_grpc

logs = {
        "VoidOP": [],
        "LongOP": [],
        "MultLongOP": [],
        "ClassOP": [],
        "exp=0 StringOP": [],
        "exp=1 StringOP": [],
        "exp=2 StringOP": [],
        "exp=3 StringOP": [],
        "exp=4 StringOP": [],
        "exp=5 StringOP": [],
        "exp=6 StringOP": [],
        "exp=7 StringOP": [],
        "exp=8 StringOP": [],
        "exp=9 StringOP": [],
        "exp=10 StringOP": [],
        "exp=15 StringOP": [],
        "exp=20 StringOP": []
}

def benchmark_void_operation(stub, num_requests):
    times = []
    for _ in range(num_requests):
        start_time = time.perf_counter()
        stub.VoidOP(service_pb2.Empty())
        end_time = time.perf_counter()
        times.append(end_time - start_time)
        if _ % 10 == 0:
            logs.get("VoidOP").append((end_time - start_time) * 100) # Better visualization
    return times

def benchmark_long_operation(stub, num_requests):
    times = []
    random.seed(42)  # For reproducibility
    for _ in range(num_requests):
        start_time = time.perf_counter()
        stub.LongOP(service_pb2.LongValue(value=random.randint(1, 100)))
        end_time = time.perf_counter()
        times.append(end_time - start_time)
        if _ % 10 == 0:
            logs.get("LongOP").append((end_time - start_time) * 100) # Better visualization
    return times

def benchmark_mult_long_operation(stub, num_requests):
    times = []
    random.seed(42)  # For reproducibility
    for _ in range(num_requests):
        values = [service_pb2.LongValue(value=random.randint(1, 100)) for _ in range(8)]
        if (len(values) != 8):
            raise ValueError("Invalid number of arguments. Expected 8.")
        start_time = time.perf_counter()
        stub.MultLongOP(service_pb2.MultLongValues(values=values))
        end_time = time.perf_counter()
        times.append(end_time - start_time)
        if _ % 10 == 0:
            logs.get("MultLongOP").append((end_time - start_time) * 100) # Better visualization
    return times

def benchmark_string_operation(stub, num_requests, exp):
    times = []
    string = ""
    random.seed(42)  # For reproducibility
    for _ in range(pow(2, exp)):
        string += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    for _ in range(num_requests):
        start_time = time.perf_counter()
        stub.StringOP(service_pb2.StringValue(value=string))
        end_time = time.perf_counter()
        times.append(end_time - start_time)
        if _ % 10 == 0:
            logs.get(f"exp={exp} StringOP").append((end_time - start_time) * 100) # Better visualization
    return times

def benchmark_class_operation(stub, num_requests):
    times = []
    random.seed(42)  # For reproducibility
    for _ in range(num_requests):
        start_time = time.perf_counter()
        start_point = service_pb2.PointValue(
            xAxis=random.randint(1, 1000), 
            yAxis=random.randint(1, 1000), 
            zAxis=random.randint(1, 1000), 
            color="Blue"
        )
        end_point = service_pb2.PointValue(
            xAxis=random.randint(1, 1000), 
            yAxis=random.randint(1, 1000), 
            zAxis=random.randint(1, 1000), 
            color="Blue"
        )
        stub.ClassOP(service_pb2.VectorValue(start=start_point, end=end_point))
        end_time = time.perf_counter()
        times.append(end_time - start_time)
        if _ % 10 == 0:
            logs.get("ClassOP").append((end_time - start_time) * 100) # Better visualization
    return times

def report(times, operation):
    mean = statistics.mean(times)
    stddev = statistics.stdev(times) if len(times) > 1 else 0
    print(f"{operation} - Mean: {mean:.6f}s, Stddev: {stddev:.6f}s")
    print(f"{operation} - Min: {min(times):.6f}s, Max: {max(times):.6f}s")
    print()

def save_logs_to_csv(logs, filename="logs.csv"):
    import csv
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'sample_number', 
            'void_operation', 
            'long_operation', 
            'mult_long_operation', 
            'class_operation',
            '00_string_operation',
            '01_string_operation',
            '02_string_operation',
            '03_string_operation',
            '04_string_operation',
            '05_string_operation',
            '06_string_operation',
            '07_string_operation',
            '08_string_operation',
            '09_string_operation',
            '10_string_operation',
            '15_string_operation',
            '20_string_operation',
        ])
        for i in range(len(logs["VoidOP"])):
            csv_writer.writerow([
                i * 10,
                logs["VoidOP"][i] if i < len(logs["VoidOP"]) else None,
                logs["LongOP"][i] if i < len(logs["LongOP"]) else None,
                logs["MultLongOP"][i] if i < len(logs["MultLongOP"]) else None,
                logs["ClassOP"][i] if i < len(logs["ClassOP"]) else None,
                logs["exp=0 StringOP"][i] if i < len(logs["exp=0 StringOP"]) else None,
                logs["exp=1 StringOP"][i] if i < len(logs["exp=1 StringOP"]) else None,
                logs["exp=2 StringOP"][i] if i < len(logs["exp=2 StringOP"]) else None,
                logs["exp=3 StringOP"][i] if i < len(logs["exp=3 StringOP"]) else None,
                logs["exp=4 StringOP"][i] if i < len(logs["exp=4 StringOP"]) else None,
                logs["exp=5 StringOP"][i] if i < len(logs["exp=5 StringOP"]) else None,
                logs["exp=6 StringOP"][i] if i < len(logs["exp=6 StringOP"]) else None,
                logs["exp=7 StringOP"][i] if i < len(logs["exp=7 StringOP"]) else None,
                logs["exp=8 StringOP"][i] if i < len(logs["exp=8 StringOP"]) else None,
                logs["exp=9 StringOP"][i] if i < len(logs["exp=9 StringOP"]) else None,
                logs["exp=10 StringOP"][i] if i < len(logs["exp=10 StringOP"]) else None,
                logs["exp=15 StringOP"][i] if i < len(logs["exp=15 StringOP"]) else None,
                logs["exp=20 StringOP"][i] if i < len(logs["exp=20 StringOP"]) else None,
            ])
    # print(f"Logs salvos em {filename}")

def run():
    server_ip = os.environ.get("SERVER_IP", "localhost")
    benchmark_flag = os.environ.get("BENCHMARKING", "True")
    if benchmark_flag == "True":
        print("Benchmarking is enabled.")
    else:
        print("Benchmarking is disabled.")
    if server_ip == "localhost":
        print("Warning: Using localhost. Ensure the server is running on the same machine.")
    else:
        print(f"Connecting to server at {server_ip}...")
    target = f'{server_ip}:50051'
    try:
        with grpc.insecure_channel(target) as channel:
            stub = service_pb2_grpc.BenchmarkServicesStub(channel)
            if not stub:
                print("Failed to create stub.")
                return
            requests = 1000
            report(benchmark_void_operation(stub, requests), "[Empty::Empty]")
            report(benchmark_long_operation(stub, requests), "[Long::Long]")
            report(benchmark_mult_long_operation(stub, requests), "[8x Long::Long]")
            report(benchmark_class_operation(stub, requests), "[Class::Class]")
            report(benchmark_string_operation(stub, requests, 0), "[exp=0 String::String]")
            report(benchmark_string_operation(stub, requests, 1), "[exp=1 String::String]")
            report(benchmark_string_operation(stub, requests, 2), "[exp=2 String::String]")
            report(benchmark_string_operation(stub, requests, 3), "[exp=3 String::String]")
            report(benchmark_string_operation(stub, requests, 4), "[exp=4 String::String]")
            report(benchmark_string_operation(stub, requests, 5), "[exp=5 String::String]")
            report(benchmark_string_operation(stub, requests, 6), "[exp=6 String::String]")
            report(benchmark_string_operation(stub, requests, 7), "[exp=7 String::String]")
            report(benchmark_string_operation(stub, requests, 8), "[exp=8 String::String]")
            report(benchmark_string_operation(stub, requests, 9), "[exp=9 String::String]")
            report(benchmark_string_operation(stub, requests, 10), "[exp=10 String::String]")
            report(benchmark_string_operation(stub, requests, 15), "[exp=15 String::String]")
            report(benchmark_string_operation(stub, requests, 20), "[exp=20 String::String]")
            if benchmark_flag == "True":
                logs_file = open("logs.txt", "w")
                for key, value in logs.items():
                    logs_file.write(f"{key}: {value}\n")
                logs_file.close()
                save_logs_to_csv(logs)
    except grpc.RpcError as e:
        print(f"RPC failed with status code {e.code()}: {e.details()}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if os.path.exists("logs.txt"):
            os.remove("logs.txt")
        print("All benchmarks completed.")

if __name__ == '__main__':
    run()
