#
# Script to read in total RAC project allocations and split into 
# equal quarterly allocations
#
import numpy as np
import pandas as pd
import sys
from itertools import cycle

# Create the Quarter cycle, RAC allocations always start in Q2
quarters = ['Q2','Q3','Q4','Q1']
quarters_pool = cycle(quarters)

# Read in the total allocations
infile = sys.argv[1].strip()
total_df = pd.read_csv(infile, quotechar="'", quoting=2)

print(total_df)

# Write out the quarterly allocations

csvfile = open("rac1.csv", 'w')

csvfile.write("'ProjectID','RACID','Quarter','Year','Resource','Allocation'\n")
for index, row in total_df.iterrows():
    year = row['Start Year'] + 0.25
    for i in range(int(row['Quarters'])):
        csvfile.write("'{:}','{:}','{:}',{:d},{:},{:.3f}\n".format(row["ProjectID"], row["RACID"], next(quarters_pool), int(year), row['Resource'], float(row['Allocation'])/row['Quarters']))
        year = year + 0.25

csvfile.close()



