import os
import pandas as pd
import matplotlib.pyplot as plt
import itertools

# Directory containing CSV files
directory = "14-min-results/"

# Parameters of interest
params = ["ALPHA", "DELTA", "INTERVAL", "EPSILON", "NUM_PROCS"]

# Read all CSV files and combine them into a single DataFrame
df_list = []
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        df = pd.read_csv(os.path.join(directory, filename))
        df_list.append(df)
df = pd.concat(df_list, ignore_index=True)
def create_scatter_plot(x_param, fixed_params):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Filter DataFrame based on fixed parameters
    filtered_df = df
    for param, value in fixed_params.items():
        filtered_df = filtered_df[filtered_df[param] == value]
    
    # Group by the x_param and calculate mean for REPCL_SIZE and VECCL_SIZE
    grouped = filtered_df.groupby(x_param)[["REPCL_SIZE", "VECCL_SIZE"]].mean().reset_index()
    
    ax.scatter(grouped[x_param], grouped["REPCL_SIZE"], label="REPCL_SIZE", marker='o')
    ax.scatter(grouped[x_param], grouped["VECCL_SIZE"], label="VECCL_SIZE", marker='s')
    
    ax.set_xlabel(x_param)
    ax.set_ylabel("Size")
    ax.set_title(f"REPCL_SIZE and VECCL_SIZE vs {x_param}\n" + 
                 ", ".join([f"{k}={v}" for k, v in fixed_params.items()]))
    ax.legend()
    
    # Create directory for saving plots if it doesn't exist
    os.makedirs("scatter_plots_avg", exist_ok=True)
    
    # Generate filename
    filename = f"scatter_{x_param}_" + "_".join([f"{k}{v}" for k, v in fixed_params.items()]) + ".png"
    plt.savefig(os.path.join("scatter_plots_avg", filename))
    plt.close()

# # Function to create scatter plot
# def create_scatter_plot(x_param, fixed_params):
#     fig, ax = plt.subplots(figsize=(10, 6))
#     
#     # Filter DataFrame based on fixed parameters
#     filtered_df = df
#     for param, value in fixed_params.items():
#         filtered_df = filtered_df[filtered_df[param] == value]
#     
#     ax.scatter(filtered_df[x_param], filtered_df["REPCL_SIZE"], label="REPCL_SIZE", alpha=0.7)
#     ax.scatter(filtered_df[x_param], filtered_df["VECCL_SIZE"], label="VECCL_SIZE", alpha=0.7)
#     
#     ax.set_xlabel(x_param)
#     ax.set_ylabel("Size")
#     ax.set_title(f"REPCL_SIZE and VECCL_SIZE vs {x_param}\n" + 
#                  ", ".join([f"{k}={v}" for k, v in fixed_params.items()]))
#     ax.legend()
#     
#     # Create directory for saving plots if it doesn't exist
#     os.makedirs("scatter_plots", exist_ok=True)
#     
#     # Generate filename
#     filename = f"scatter_{x_param}_" + "_".join([f"{k}{v}" for k, v in fixed_params.items()]) + ".png"
#     plt.savefig(os.path.join("scatter_plots", filename))
#     plt.close()

# Generate plots for each parameter
for x_param in params:
    other_params = [p for p in params if p != x_param]
    
    # Get unique values for each parameter
    param_values = {p: df[p].unique() for p in other_params}
    
    # Generate all combinations of other parameters
    combinations = list(itertools.product(*[param_values[p] for p in other_params]))
    
    for combination in combinations:
        fixed_params = dict(zip(other_params, combination))
        create_scatter_plot(x_param, fixed_params)

print("All scatter plots have been generated and saved in the 'scatter_plots' directory.")
