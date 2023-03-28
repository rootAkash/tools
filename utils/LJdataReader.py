from typing import List,Dict,Any
import pandas as pd
import numpy as np
import os
from pathlib import Path
def read_csv_LJspeech(path_to_csv: str) -> Dict[str,List[Any]] :
    """ 
    input:path to csv file of JLspeech metadata
    output: a dict of list of indexes , filename of the audio, transcripts and normalised transcripts
    """
    path_to_csv = Path(path_to_csv)
    file = pd.read_csv(path_to_csv,sep="|")
    arr = file.to_numpy()
    indexes = file.index.to_numpy()
    data = {"indxs":list(indexes),"files":list(arr[:,0]),"transcripts":list(arr[:,1]),"norm_transcripts":list(arr[:,1])}
    return data

def check_LJ_data():
    """
    checks for missing audio or metadata 
    """
    return NotImplementedError

def read_audios(path_to_audiofolder : str) -> Dict[str,Any]:
    """
    input: path to the audio folder 
    outputs: a dict of lists of audio file names and audio_bytes object
    """
    path_to_audiofolder = Path(path_to_audiofolder)
    data ={}
    try:
        for file  in os.listdir(path_to_audiofolder):
            audio_file = open(Path(path_to_audiofolder,file), 'rb')
            audio_bytes = audio_file.read()
            data[Path(file).stem] = audio_bytes
        return data
    except :
        print("error occured , something is wrong with data")