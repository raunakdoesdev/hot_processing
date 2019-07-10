import pandas as pd
import subprocess

#Find the cruise number from the file name string
def cruiseNum(file_name):
  return int(''.join(filter(str.isdigit, file_name)))

# REMOVE duplicates from list of files (after sorting call)
def removeDups(x):
  return list(dict.fromkeys(x))

# TEST: print('the cruise number for this thing is: ', cruiseNum('hot112.sea'))
# Load the list of files
with open('col.csv', 'r') as file:
    col_files = file.read().split()    
    # SORTING THE FILES BY CRUISE NUM/ALPHA
    col_files = sorted(col_files, key=cruiseNum)
      
full_data = None

print(col_files)

for col_file in col_files:
  if(not col_file.endswith('.sea')):
    continue
#   if(not col_file in list_permitted):
#     break
  # download each file
  print(col_file)
  process = subprocess.Popen(['wget', 'ftp://ftp.soest.hawaii.edu/hot/water/' + col_file, '-O', col_file], stdout=subprocess.PIPE)
  output, error = process.communicate()
  
  print(error)
  print(output)
  # First remove the column information which is stored between the ****'s
  lines = open(col_file).readlines()
  with open(col_file, 'w') as f:
      f.writelines(lines[5:])
      
  
  # Then load the txt file into pandas
  data = pd.read_csv(col_file, delim_whitespace=True, header=None)
  data.columns = lines[1].split()
  
  if(full_data is None):
    full_data = data
    print(data.shape)
  else:
    print(data.shape)
    full_data = pd.concat([full_data,data], axis=1)

print(full_data.shape)
full_data.to_pickle('./df.pkl')
  
