import pandas as pd
import yaml
import csv
import os


def xlsx_to_csv(xlsxfile, sheetname):

    data = pd.read_excel(xlsxfile, sheetname, index_col=None)
       
    if sheetname == 'Upwork People List' or sheetname == 'Offboarded People':
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        
    elif sheetname == 'Projects Team Structure':
        data.columns = data.iloc[2].tolist()
        data = data.iloc[3:]
        
        # Save Resource and responsability separately
        data2 = data.copy()
        data2.drop(data2.columns.difference(['Project name','Resource and responsibility']), 1, inplace=True)
        drop_empty_rows(data2)
        data2['Project name'] = data2['Project name'].ffill()
        data2['Project name'] = data2['Project name'].apply(lambda s: s.rstrip('\n'))
               
        # dropping null value columns to avoid errors 
        data2.dropna(inplace = True)
        # replace '–' by '-'
        data2['Resource and responsibility'] = data2['Resource and responsibility'].apply(lambda s: s.replace('–', '-'))
        # new data frame with split value columns 
        new = data2['Resource and responsibility'].str.split('-', n = 1, expand = True) 
        # making separate first Resource column from new data frame 
        data2['Resource'] = new[0] 
        # making separate Responsability column from new data frame 
        data2['Responsability'] = new[1] 
        # dropping old Resource and responsibility columns 
        data2.drop(columns = ['Resource and responsibility'], inplace = True) 
        
        data2['Resource'] = data2['Resource'].apply(lambda s: s.rstrip('\n').strip() if isinstance(s, str) else s)    
        data2['Responsability'] = data2['Responsability'].apply(lambda s: s.rstrip('\n').strip() if isinstance(s, str) else s)
        
        data2.to_csv('csv_files/Resource and responsability.csv', index=False, encoding='utf-8')
        #############
        
        data['Delivery Manager'] = data['Delivery Manager'].apply(lambda s: s.rstrip('\n').strip().replace('\n', ', ') if isinstance(s, str) else s)            
        data = data.loc[:, ~data.columns.str.contains('Resource and responsibility')]
        drop_empty_rows(data)
        
    elif sheetname == 'Team Structure':
        h = data.iloc[0]
        h = h.tolist()
        
        data.columns = h
        data = data.iloc[1:]
        
        data['Project name'] = data['Project name'].apply(split)
        data['Delivery Manager'] = data['Delivery Manager'].apply(delete_points)
        data['Delivery Manager'] = data['Delivery Manager'].apply(create_string)  
        data['Business Owner/Stakeholders'] = data['Business Owner/Stakeholders'].apply(create_string)
        data['Resource and responsibility'] = data['Resource and responsibility'].apply(delete_points)
        data['Resource and responsibility'] = data['Resource and responsibility'].apply(create_string)
    
    elif sheetname == 'Skills Matrix':
        h1 = data.iloc[5]
        h1 = h1.tolist()
        h1 = h1[:2]

        h2 = data.iloc[6]
        h2 = h2.tolist()
        h2 = h2[2:]

        data.columns = h1 + h2    
        data = data.iloc[7:]
              
    data.to_csv(os.path.join('csv_files', sheetname+'.csv'), index=False, encoding='utf-8')


def csv_to_yaml(filename):

    csvfile = open(os.path.join('csv_files', filename+'.csv'), 'r')
    datareader = csv.reader(csvfile, delimiter=",", quotechar='"')
    
    result = list()
    type_index = -1
    child_fields_index = -1

    for row_index, row in enumerate(datareader):
        if row_index == 0:
            data_headings = list()
            for heading_index, heading in enumerate(row):
                fixed_heading = heading.lower().replace(" ", "_").replace("-", "")
                data_headings.append(fixed_heading)
                if fixed_heading == "type":
                    type_index = heading_index
                elif fixed_heading == "childfields":
                    child_fields_index = heading_index
        else:
            content = dict()
            is_array = False
            for cell_index, cell in enumerate(row):
                if cell_index == child_fields_index and is_array:
                    content[data_headings[cell_index]] = [{
                    "source" : "fra:" + value.capitalize(),
                    "destination" : value,
                    "type" : "string",
                    "childfields" : "null"
                    } for value in cell.split(",")]
                else:
                    content[data_headings[cell_index]] = cell
                    is_array = (cell_index == type_index) and (cell == "array")
            result.append(content)

    with open(os.path.join('yaml_files',filename+'.yml'), 'w') as f:
        doc = yaml.dump(result, f) 


def drop_empty_rows(df):
    df.replace('', float("NaN"), inplace=True)
    df.dropna(how='all', inplace=True) 
    

def split(line, sep='\n'):
    if isinstance(line, str):
        return line.split(sep, 1)[0]
    else:
        pass   

    
def delete_points(line, special=['\u25CF', '\u2013']):
    if isinstance(line, str):
        for elem in special:
            line = str.replace(line, elem, '')
        return line
    else:
        pass


def remove_spaces(l):
    if isinstance(l, list):
        for elem, i in zip(l, range(len(l))):
            l[i] = elem.strip().replace('-', '/').replace('\xE1', 'a')
        return list(filter(lambda a: a != '', l))
    else:
        pass 

        
def create_string(line):
    if isinstance(line, str):   
        l = remove_spaces(line.split('\n'))
        return ', '.join(l)
    else:
        pass           