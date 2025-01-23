import os
import glob
def parse_kraken_report(file_path, rank):

##Kraken2 report file and return the top 3 entries for the given rank.

   top_entries = []
   with open(file_path, 'r') as file:
       for line in file:
           cols = line.strip().split('\t')
           if len(cols) < 6:
               continue
           percentage, _, _, tax_rank, _, name = cols
           if tax_rank == rank:  # Filter by rank
               top_entries.append((float(percentage), name.strip()))
   return sorted(top_entries, reverse=True)[:3]
def summarize_reports(input_folder, output_file, rank):

##Summarize the top entries from Kraken2 reports and save to a single file.
  
   report_files = glob.glob(os.path.join(input_folder, "*.report"))
   with open(output_file, 'w') as out_file:
       out_file.write("Combined Kraken2 Report Summary\n")
       out_file.write("=" * 50 + "\n\n")
       for report_file in report_files:
           file_name = os.path.basename(report_file)
           top_entries = parse_kraken_report(report_file, rank)
           out_file.write(f"Summary for {file_name}\n")
           out_file.write("Top 3 by percentage:\n")
           for percentage, name in top_entries:
               out_file.write(f"  {name}: {percentage:.2f}%\n")
           out_file.write("\n")
def print_summary(output_file):

##Print the location of the combined summary file.

   print(f"Combined summary saved in: {output_file}")

# Usage
input_folder = "/Kraken_output/"
output_file = "combined_summary.txt"
rank = "S"  # Use "S" for species or "G" for genus
summarize_reports(input_folder, output_file, rank)
print_summary(output_file)