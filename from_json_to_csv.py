
import json
import csv
import pandas as pd
import pprint



with open("data_query_birthplaces_a.json", "r") as json_file:
    data = json.load(json_file)
    #pprint.pprint(data)
    

df = pd.DataFrame(data)

#df = pd.read_json(data)
df.to_csv(index=False)
pprint.pprint(df)

#ho trovato il modo per trasformare un dataframe json in un csv, peccato che proprio graficamente non sia il massimo il risultato... bisognerebbe spacchettare bene le colonne del json
#servirebbe un for loop per sistemare le colonne del json
#                                                      head  \
#vars      [historian, historian_name, birthplace, birthp...   
#bindings                                                NaN   

                                                    #results  
#vars                                                    NaN  
#bindings  [{'historian': {'type': 'uri', 'value': 'http:...  
