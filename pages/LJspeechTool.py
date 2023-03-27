from utils.dataReader import read_csv_LJspeech,read_audios
import streamlit as st
#path_to_csv = "C:\\Users\\mraka\\Downloads\\vits-rod-bettersplit-ds-20230327T111700Z-001\\vits-rod-bettersplit-ds\\metadata.csv"

def run_LJpage():
    path_to_csv = st.text_input('MetaData CSV file path')
    metaData = None
    audioData = None
    if path_to_csv:
        metaData = read_csv_LJspeech(path_to_csv)
    path_to_audioFolder = st.text_input('Audio Data path')
    if path_to_audioFolder:
        audioData = read_audios(path_to_audioFolder)
    if metaData and audioData:
        for file,transcript in zip(metaData["files"][:5],metaData["transcripts"][:5]):
            audio_bytes = audioData[file]
            st.audio(audio_bytes, format='audio/ogg')#st.audio(data, format='audio/wav', start_time=0)
            st.text(transcript)



run_LJpage()