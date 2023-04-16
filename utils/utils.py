import streamlit as st
import os
from typing import Optional,List,Any
from pathlib import Path
import pandas as pd

def file_uploader() -> Optional[str]:
    """
    creates a upload file widget and copies the file in local and returnes the copied path
    output: returns path
    """
    file = st.file_uploader("Select a file")
    if file is not None:
        file_details = {"filename": file.name, "filetype": file.type, "filesize": file.size}
        st.write(file_details)
        file.seek(0)
        with open(file.name, "wb") as f:
            f.write(file.read())
        return file.name
    else:
        st.write("No file uploaded.")


def clickable_file_list(items: List[str]) -> Optional[str]:
    """
    creates a clickable list and returns the clicked item given a list as input
    input:a list of strings
    output: the string that is selected after clicking
    """
    options = [f"{item}" for item in items]
    item_index = st.selectbox("Select a file or folder", options)
    return item_index

def clickable_grid(items:List[Any]) -> str:
    """
    creates a grid to display files and folders and creates a dropdown to select one
    input :a list of file names and dict of folders with folder description
    returns: the selected folder or file
    """
    selected_item = st.empty()
    col1, col2, col3 = st.columns([0.3, 0.1, 0.6])
    for item in items:
        if isinstance(item, str):
            col1.write(item)
            col2.write("")
            col3.write("")
        else:
            col1.write(item["name"])
            col2.write("📁")
            col3.write(item["description"])
    selected_item.text("")
    if len(items) == 0:
        st.write("No items to display.")
    else:
        item_index = st.selectbox("Select an item", options=[i["name"] if isinstance(i, dict) else i for i in items])
        selected_item.text(f"You selected: {item_index}")
        return item_index
    
def edit_csv(filepath:str,row:int,col:int ,data:str) -> None :
    # reading the csv file
    df = pd.read_csv(filepath,sep="|")
    
    # updating the column value/data
    df.iat[row,col] = data
    
    # writing into the file
    df.to_csv(filepath,sep="|", index=False)
