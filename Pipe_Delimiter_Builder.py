
# This script is used to convert CSV files to Pipe Delimiter Text file format, as requested by stakeholders

import csv
import time 

timestr = time.strftime("%Y%m%d")   # Use time string for output file

with open("C:/Users/robert.enright/PEMS_Marco/MoH CSV Template.csv", "rU") as f:    # Open existing CSV file that is to be converted
    with open("C:/Users/robert.enright/PEMS_Marco/MoH Output File " + timestr +".txt", 'w', newline='') as f1:  # Open new blank output file

        reader = csv.reader(f, delimiter=',')       # Use CSV reader on input file, with comma delimiter
        next(reader, None)                          # Skip the header

        writer = csv.writer(f1, delimiter='|')      # Likewise, use CSV writer on output file, with pipe delimiter
        writer.writerow(['Report 1'])               # Title line of file as header, format requested by stakeholder
        writer.writerow('')
        writer.writerow(['DATA_FIELD'])

        for row in reader:                      
            writer.writerow(row)                    # Add input rows to output file