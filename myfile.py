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

col1, col2, col3 = st.columns(3)

with col1:
    Generic_name = st.selectbox(
        'Generic_name (Category)',
        generic_name_options)

    title = st.text_input("Enter Synonym",key="gen")
    button_clicked = st.button("Add Synonym",key="genb")
    if button_clicked:
        db.genMap_collection.update_one({
            "generic_name":Generic_name
        },
        {
            "$push":{"synonyms":title}
        }
        )

    response_for_synonyms = list(db.genMap_collection.find({"generic_name":Generic_name}))
    for i in response_for_synonyms:
        for k in i["synonyms"]:
            st.write(k)

response_for_generic_name = list(db.attValueMap_collection.find({"generic_name":Generic_name}))

attribute_options = set()
for j in response_for_generic_name:
    attribute_options.add(j["attribute"])

with col2:
    Attribute = st.selectbox(
        'Attribute',
        attribute_options)

    title = st.text_input("Enter Synonym",key="att")
    button_clicked = st.button("Add Synonym",key="attb")
    if button_clicked:
        db.attMap_collection.update_one({
            "generic_name":Generic_name,
            "attribute":Attribute
        },
        {
            "$push":{"synonyms":title}
        }
        )

    response_for_synonyms = list(db.attMap_collection.find({"generic_name":Generic_name,"attribute":Attribute}))
    for i in response_for_synonyms:
        for k in i["synonyms"]:
            st.write(k)

response_for_attribute = list(db.categories_collection.find({"generic_name":Generic_name,"attribute":Attribute}))

attribute_value_options = set()
for j in response_for_attribute:
    for k in j["values"]:
        attribute_value_options.add(k)


with col3:
    Attribute_Value = st.selectbox(
        'Attribute Value',
        attribute_value_options)
    
    title = st.text_input("Enter Synonym",key="attValue")
    button_clicked = st.button("Add Synonym",key="attValb")
    if button_clicked:
        db.attValueMap_collection.update_one({
            "generic_name":Generic_name,
            "attribute":Attribute,
            "attribute_value":Attribute_Value
        },
        {
            "$push":{"synonyms":title}
        }
        )

    response_for_synonyms = list(db.attValueMap_collection.find({"generic_name":Generic_name,"attribute":Attribute,"attribute_value":Attribute_Value}))
    for i in response_for_synonyms:
        for k in i["synonyms"]:
            st.write(k)
