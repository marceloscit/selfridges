import pandas as pd
import re

with open('repauth.txt') as f:
    lines = f.readlines()

header = {}
data = {}
firstLine = True
df = pd.DataFrame
for line in lines:

    if 'Display authority record details' in line or 'command responses received.' in line or 'Copyright IBM Corp' in line or 'Starting MQSC' in line or 'command responses received' in line:

        if header != {}:
            print('----')
            print(data)
            if firstLine:
                df = pd.DataFrame(header)
                firstLine  = False
            else:
                df = df.append(data, ignore_index=True)    
        data = {}
        pass
    else:
        result = re.findall('(\w+([^()]*))', line)
        it = iter(result)

        for x, y in zip(it, it):  
            if firstLine:
                header[x[0]] = [y[0]]
            else:
                data[x[0]] = y[0]
    
df.to_excel('pandas_to_excel.xlsx', sheet_name='new_sheet_name')






        

