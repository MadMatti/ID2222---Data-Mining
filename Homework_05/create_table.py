import subprocess
import pandas as pd
from pathlib import Path
from tqdm import tqdm


# Define the parameter combinations to test

# annealing_types = ['LINEAR']
# delta_values = [0.99, 0.9, 0.8]

# annealing_types = ['EXPONENTIAL']
# delta_values = [0.99, 0.95, 0.9, 0.8]
# temperature_values = [10, 4, 2]
# restart_values = [100, 250]

annealing_types = ['EXPONENTIAL']
delta_values = [0.99, 0.95, 0.9, 0.8]
temperature_values = [10, 4, 2]
restart_values = [100, 250]



# Initialize an empty list to store results
results = []

output_dir = Path('output_exponential')
output_dir.mkdir(parents=True, exist_ok=True)


# Run the script for different parameter combinations
for annealing_type in tqdm(annealing_types, desc='Annealing Types'):
    for delta in delta_values:
        for temperature in temperature_values:
            for restarts in restart_values:
                # Run the script with subprocess
                command = [
                    './run.sh',
                    '-annealingType', annealing_type,
                    '-delta', str(delta),
                    '-temperature', str(temperature),
                    '-restart', str(restarts),
                    '-outputDir', str(output_dir),
                    '-graph', 'graphs/3elt.graph',
                    # Add other parameters as needed
                ]

                # Use subprocess to capture the output
                result = subprocess.run(command, capture_output=True, text=True)
                output_text = result.stdout.strip()  # Assuming the output is text

                # Extract the minimum edge cut, maximum migrations, and maximum swaps
                edge_cut_lines = [line for line in output_text.split('\n') if 'edge cut' in line]
                migrations_lines = [line for line in output_text.split('\n') if 'migrations' in line]
                swaps_lines = [line for line in output_text.split('\n') if 'swaps' in line]

                if edge_cut_lines:
                    min_edge_cut = min(int(line.split('edge cut:')[1].split(',')[0].strip()) for line in edge_cut_lines)
                else:
                    min_edge_cut = None

                if migrations_lines:
                    max_migrations = max(int(line.split('migrations:')[1].strip()) for line in migrations_lines)
                else:
                    max_migrations = None

                if swaps_lines:
                    max_swaps = max(int(line.split('swaps:')[1].split(',')[0].strip()) for line in swaps_lines)
                else:
                    max_swaps = None

                # Store the parameters and metrics in the results list
                results.append({
                    'annealing_type': annealing_type,
                    'delta': delta,
                    'temperature': temperature,
                    'restarts': restarts,
                    'min_edge_cut': min_edge_cut,
                    'max_migrations': max_migrations,
                    'max_swaps': max_swaps,
                })

# Create a pandas DataFrame from the results list
df = pd.DataFrame(results)

# Save the DataFrame as a CSV file
csv_file_path = output_dir / 'results.csv'
df.to_csv(csv_file_path, index=False)

# Display the DataFrame
print(df)