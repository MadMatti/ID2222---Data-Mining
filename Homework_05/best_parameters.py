import pandas as pd
from pathlib import Path

# Load the results from the CSV file
output_dir = Path('output_exponential')
csv_file_path = output_dir / 'results.csv'
df = pd.read_csv(csv_file_path)

# Filter rows where annealing_type is exponential

# Find the row with the minimum min_edge_cut
min_edge_cut_row = df.loc[df['min_edge_cut'].idxmin()]

# Display the parameters of the row with the minimum min_edge_cut
print("Parameters with the minimum min_edge_cut:")
print(min_edge_cut_row)
