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
types = {'ProjectID': str, 'RACID': str, 'RACID': str, 'Start Year': np.int32, 'Start Quarter': str, 'Quarters': np.int32, 'Resource': str, 'Allocation': np.float64}
total_df = pd.read_csv(infile, quotechar="'", quoting=2, dtype=types)

print(total_df)

# Write out the quarterly allocations
stem = sys.argv[1].strip().split('.')[0]
outfile = stem + '_split.csv'
csvfile = open(outfile, 'w')

csvfile.write("'ProjectID','RACID','PI','Quarter','Year','Resource','Allocation'\n")
for index, row in total_df.iterrows():
    year = row['Start Year'] + 0.25
    for i in range(int(row['Quarters'])):
        csvfile.write("'{:}','{:}','{:}','{:}',{:d},'{:}',{:.3f}\n".format(row["ProjectID"], row["RACID"], row["PI"], next(quarters_pool), int(year), row['Resource'], float(row['Allocation'])/row['Quarters']))
        year = year + 0.25

csvfile.close()



