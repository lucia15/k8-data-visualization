import pandas as pd
import yaml
import csv
import os
import re


# Include this path if working in Google Colab    
#d = '/content/gdrive/My Drive/p2-p-data-visualization-Pappaterra-Lucia/'
# If not 
d = ''


def xlsx_to_csv(xlsxfile, sheetname):

    data = pd.read_excel(xlsxfile, sheetname, index_col=None)   
    
    if sheetname == 'Upwork People List' or sheetname == 'Offboarded People':
        # drop unnamed columns
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        
    elif sheetname == 'Projects Team Structure':
    
        data = data.rename(columns={'Business Owner\nStakeholders': 'Stakeholders'})
        
        data['Slack Channel'] = data['Slack Channel'].apply(lambda s: s.replace('#', '') if isinstance(s, str) else s)
        data['Slack Channel'] = data['Slack Channel'].apply(lambda s: '#'+s if isinstance(s, str) else s)
        
        data.dropna(subset = ['Project Name'], inplace=True)
        
        data['Project Name'] = data['Project Name'].apply(lambda s: s.rstrip('\n') if isinstance(s, str) else s)
        
        # consider only the projects that have some priority            
        df = data[data['Priority']!='']
        data = df[df['Priority']!=' ']
        
        # sort by priority
        data['Priority'] = pd.Categorical(data['Priority'], categories=['One (1)','Two (2)','Three (3)'], ordered=True)            
        data = data.sort_values('Priority')
        
        data = data.reset_index(drop=True)
        
        ############# Save Resource and Responsability separately ##############
        data2 = data.copy()
        data2.drop(data2.columns.difference(['Project Name', 'Slack Channel', 'Delivery Manager', 'Resource Name']), 1, inplace=True)        
        data2.replace(float("NaN"), '', inplace=True) 
                
        project_name = []
        slack_channel = []
        delivery_manager = []
        resource_name = []
        responsability = []
        
        for index, row in data2.iterrows():   
        
            ll = row['Resource Name'].split('\n')
  
            for elem in ll:
                project_name.append(row['Project Name'])
                slack_channel.append(row['Slack Channel'])
                delivery_manager.append(row['Delivery Manager'])
        
                name = remove_parenthesis(elem).rstrip()
                resource_name.append(name)
        
                respo = get_between_parenthesis(elem)
                if len(respo)>0:
                    respo = get_between_parenthesis(elem)[0]
                else:
                    respo=''
                responsability.append(respo)
        
        data3 = pd.DataFrame()
        
        data3['Project Name'] = project_name
        data3['Slack Channel'] = slack_channel
        data3['Delivery Manager'] = delivery_manager
        data3['Resource Name'] = resource_name
        data3['Resource Responsability'] = responsability
        
        data3.replace('', float("NaN"), inplace=True)
        data3.dropna(axis=0, how='all', inplace=True)
        data3.dropna(subset = ['Resource Name'], inplace=True)
        data3.replace(float("NaN"), '', inplace=True)
        
        # save to csv file
        data3.to_csv(d+'csv_files/Resource and responsability.csv', index=False, encoding='utf-8')
        ########################################################################
        
        data['Delivery Manager'] = data['Delivery Manager'].apply(lambda s: s.rstrip('\n').strip().replace('\n', ', ') if isinstance(s, str) else s)            
        
        data = data.loc[:, ~data.columns.str.contains('Resource Name')]
        
        # drop empty rows
        data.replace('', float("NaN"), inplace=True)
        data.dropna(how='all', inplace=True) 
        
        for col in data.columns:
            if col not in ['Stakeholders', 'Delivery Manager', 'Security Champ'] :
                data[col] = data[col].apply(lambda s: s.replace('\n', '') if isinstance(s, str) else s)
    
    elif sheetname == 'Skills Matrix':
        h1 = data.iloc[5]
        h1 = h1.tolist()
        h1 = h1[:2]

        h2 = data.iloc[6]
        h2 = h2.tolist()
        h2 = h2[2:]

        data.columns = h1 + h2    
        data = data.iloc[7:]
              
    data.to_csv(os.path.join(d+'csv_files', sheetname+'.csv'), index=False, encoding='utf-8')


def csv_to_yaml(filename):

    csvfile = open(os.path.join(d+'csv_files', filename+'.csv'), 'r')
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

    with open(os.path.join(d+'yaml_files',filename+'.yml'), 'w') as f:
        doc = yaml.dump(result, f) 
        

def get_between_parenthesis(mystring):
    """
    Get text between parenthesis from string
    Return a list with all string  between parenthesis
    """ 
    regex = re.compile(".*?\((.*?)\)")
    text = re.findall(regex, mystring) 
    return text
  
        
def remove_parenthesis(mystring):
    """
    Delete substring between parenthesis from string
    """
    text = get_between_parenthesis(mystring)
    
    for i in range(len(text)):
        substring = '('+text[i]+')'
        mystring = mystring.replace(substring, '')

    return mystring
        