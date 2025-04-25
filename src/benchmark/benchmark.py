import math
import pandas as pd
import argparse
import matplotlib.pyplot as plt

def moving_average(data, window_size=10):
    return data.rolling(window=window_size, min_periods=1).mean()

grpcExists = True
jsonrpcExists = True

try:
    df_grpc = pd.read_csv("../rpc-grpc/logs.csv")
except FileNotFoundError:
    grpcExists = False
    print("gRPC logs not found. Please run the gRPC server first.")
try:
    df_jsonrpc = pd.read_csv("../rpc-jsonrpc/logs.csv")
except FileNotFoundError:
    jsonrpcExists = False
    print("JSON-RPC logs not found. Please run the JSON-RPC server first.")
    
operations = [
    ('void_operation', 'VoidOP', 'blue'),
    ('long_operation', 'LongOP', 'orange'),
    ('mult_long_operation', 'MultLongOP', 'green'),
    ('class_operation', 'ClassOP', 'purple'),
]

string_operations = [
        ('00_string_operation', 'StringOP (2^0)', 'red'),
        ('01_string_operation', 'StringOP (2^1)', 'red'),
        ('02_string_operation', 'StringOP (2^2)', 'red'),
        ('03_string_operation', 'StringOP (2^3)', 'red'),
        ('04_string_operation', 'StringOP (2^4)', 'red'),
        ('05_string_operation', 'StringOP (2^5)', 'red'),
        ('06_string_operation', 'StringOP (2^6)', 'red'),
        ('07_string_operation', 'StringOP (2^7)', 'red'),
        ('08_string_operation', 'StringOP (2^8)', 'red'),
        ('09_string_operation', 'StringOP (2^9)', 'red'),
        ('10_string_operation', 'StringOP (2^10)', 'red'),
        ('15_string_operation', 'StringOP (2^15)', 'red'),
        ('20_string_operation', 'StringOP (2^20)', 'red'),
]


def plot_grid_benchmark(df, operations, output_file="png.png", suptitle=""):
    n = len(operations)

    # Mais colunas garante uma figura mais larga (modo paisagem)
    if n > 8:
        cols = 4
    elif n > 4:
        cols = 3
    else:
        cols = 2
    rows = math.ceil(n / cols)

    fig_width = 6 * cols
    fig_height = 4 * rows
    fig, axs = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
    axs = axs.flatten()

    for i, (col, label, color) in enumerate(operations):
        axs[i].plot(df['sample_number'], moving_average(df[col]), label=label, color=color)
        axs[i].set_xlabel('Sample Number')
        axs[i].set_ylabel('Tempo (x100)')
        axs[i].grid(True)
        axs[i].legend()

    for j in range(n, len(axs)):
        fig.delaxes(axs[j])

    plt.suptitle(suptitle, fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_path = "../../assets/" + output_file
    plt.savefig(output_path, dpi=300)

parse = argparse.ArgumentParser(description="Benchmark JSON-RPC and gRPC")
parse.add_argument(
    "--grpc",
    default="local",
    help="Name to save the gRPC benchmark",
)
parse.add_argument(
    "--jsonrpc",
    default="local",
    help="Name to save the JSON-RPC benchmark",
)

args = parse.parse_args()

if args.grpc == "local":
    print("No gRPC benchmark name provided. Using default: local")
if args.jsonrpc == "local":
    print("No JSON-RPC benchmark name provided. Using default: local")


jsonRPC_first_image_filename = args.jsonrpc + "_jsonrpc_operations_benchmark.png"
jsonRPC_second_image_filename = args.jsonrpc + "_jsonrpc_strings_benchmark.png"

gRPC_first_image_filename = args.grpc + "_grpc_operations_benchmark.png"
gRPC_second_image_filename = args.grpc + "_grpc_strings_benchmark.png"

if jsonrpcExists:
    plot_grid_benchmark(df_jsonrpc, operations, output_file=jsonRPC_first_image_filename, suptitle="JSON-RPC Benchmark Results")
    plot_grid_benchmark(df_jsonrpc, string_operations, output_file=jsonRPC_second_image_filename, suptitle="JSON-RPC String Operations Benchmark Results")

if grpcExists:
    plot_grid_benchmark(df_grpc, operations, output_file=gRPC_first_image_filename, suptitle="gRPC Benchmark Results")
    plot_grid_benchmark(df_grpc, string_operations, output_file=gRPC_second_image_filename, suptitle="gRPC String Operations Benchmark Results")