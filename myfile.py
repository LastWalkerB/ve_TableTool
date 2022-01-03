from re import S
import streamlit as st
import pandas as pd
import numpy as np
from pymongo import MongoClient
import json
import requests


client = MongoClient("mongodb://localhost/")
db = client.ve_db

response = list(db.attValueMap_collection.find({}))

generic_name_options = set()

for i in response:
    generic_name_options.add(i["generic_name"])

st.title('VE attributes table')

col1, col2, col3, col4 = st.columns(4)

with col1:
    Generic_name = st.selectbox(
        'Generic_name (Category)',
        generic_name_options)
                

    response_for_generic_name = list(db.attValueMap_collection.find({"generic_name":Generic_name}))

    attribute_options = set()
    for j in response_for_generic_name:
        attribute_options.add(j["attribute"])

    Attribute = st.selectbox(
            'Attribute',
            attribute_options)

    title = st.text_input("Enter salesman values")
    button_clicked = st.button("Add",key="addd")
    response = list(db.salesman_collection.find({"generic_name":Generic_name,"attribute":Attribute}))
    if button_clicked:
        if len(response)<1:
            db.salesman_collection.insert_one({
                "generic_name": Generic_name,
                "attribute":Attribute,
                "values":[title],
                "salesman_values":[]
            })
        else:
            db.salesman_collection.update_one({
                "generic_name":Generic_name,
                "attribute":Attribute
            },
            {
                "$addToSet":{"values":title}
            })

response_for_attribute = list(db.categories_collection.find({"generic_name":Generic_name,"attribute":Attribute}))

attribute_value_options = set()
for j in response_for_attribute:
    for k in j["values"]:
        attribute_value_options.add(k)
    
with col2:
#    for i in attribute_value_options:
    my_values = st.multiselect(
        "Att values",
        attribute_value_options
    )

with col3:
    
    response = list(db.salesman_collection.find({"generic_name":Generic_name,"attribute":Attribute}))    
    count = 0
    salesman_values = []
    if len(response)>0:
        salesman_values = st.multiselect("Salesman values",response[0]["values"])
        count = count + 1
    else:
        salesman_values = st.multiselect("Salesman values",[])

flag1 = (len(my_values)==1) and (len(salesman_values)>0)
flag2 = (len(salesman_values)==1) and (len(my_values)>0)

button_clicked1 = st.button("Add to table",key="addtotable")
if button_clicked1:
    if flag1:
        response = db.combined_collection.find({"generic_name":Generic_name,"attribute":Attribute,"values":my_values[0]})
        if len(list(response))<1:
            db.combined_collection.insert_one({
                "generic_name":Generic_name,
                "attribute":Attribute,
                "values":my_values[0]
            })
        for val in salesman_values:
            response = db.combined_collection.update_one(
                {"generic_name":Generic_name,
                "attribute":Attribute,
                "values":my_values[0]
                },
                {
                    "$addToSet":{"salesman_values":val}
                }
                )
    elif flag2:
        for val in my_values:
            response = db.combined_collection.find({"generic_name":Generic_name,"attribute":Attribute,"values":val})
            if len(list(response))<1:
                db.combined_collection.insert_one({
                    "generic_name":Generic_name,
                    "attribute":Attribute,
                    "values":val,
                    "salesman_values":[salesman_values[0]]
                })
            else:
                response = db.combined_collection.update_one(
                    {"generic_name":Generic_name,
                    "attribute":Attribute,
                    "values":val
                    },
                    {
                        "$addToSet":{"salesman_values":salesman_values[0]}
                    }
                    )            

#with col4:


response = list(db.combined_collection.find({"generic_name":Generic_name}))
generic_name_col = []
att_col = []
att_values_col = []
salesman_values_col = []
for i in response:
    generic_name_col.append(i["generic_name"])
    att_col.append(i["attribute"])
    att_values_col.append(i["values"])
    salesman_values_col.append(",".join(i["salesman_values"]))

pd_data = {
    "generic_name": generic_name_col,
    "attribute":att_col,
    "Attribute values":att_values_col,
    "Salesman values": salesman_values_col
}
df = pd.DataFrame(pd_data)
st.write(df)