#
# Script to read in quarterly RAC project allocations and combine  
# into actual allocations to be implemented in SAFE and on the 
# systems
#
import numpy as np
import pandas as pd
import sys
import os.path
from glob import glob
from itertools import cycle

wdir = sys.argv[1].strip()

files = []
if os.path.exists(wdir):
    files = glob(os.path.join(wdir, '*.csv'))
    files.sort()
else:
    sys.stderr.write("Directory does not exist: {0}".format(wdir))
    sys.exit(1)


types = {'ProjectID': str, 'RACID': str, 'PI': str, 'Quarter': str, 'Year': np.int32, 'Resource': str, 'Allocation': np.float64}
li = []
for infile in files:
    df = pd.read_csv(infile, quotechar="'", quoting=2, dtype=types)
    li.append(df)

allocation_df = pd.concat(li, axis=0, ignore_index=True)

print(allocation_df)

# Common definitions
group_func = {'RACID': '/'.join, 'Allocation':'sum'}

# Combine based on DiRAC project ID
group_col = ['ProjectID','Resource','Year','Quarter']
group_df = allocation_df.groupby(group_col).agg(group_func)
print(group_df)
# group_df.to_csv('project_alloc.csv', quoting=2, quotechar="'")

# Combine based on resource
group_col = ['Resource','Year','Quarter']
group_df = allocation_df.groupby(group_col).agg(group_func)
print(group_df)

# Produce quarterly allocation tables
years = allocation_df['Year'].unique()
quarters = allocation_df['Quarter'].unique()
resources = allocation_df['Resource'].unique()
group_col = ['ProjectID','Resource','Year','Quarter']
for year in years:
    for quarter in quarters:
        for resource in resources:
            filter_df = allocation_df.loc[(allocation_df['Year'] == year) & (allocation_df['Quarter'] == quarter) & (allocation_df['Resource'] == resource)]
            group_df = filter_df.groupby(group_col).agg(group_func)
            if not group_df.empty:
                print(group_df)


