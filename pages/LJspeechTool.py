from utils.LJdataReader import read_csv_LJspeech,read_audios
import streamlit as st

def run_LJpage():
    if "a_counter" not in st.session_state:
        st.session_state["a_counter"]=0
    path_to_csv = st.text_input('MetaData CSV file path')
    metaData = None
    audioData = None
    if path_to_csv:
        metaData = read_csv_LJspeech(path_to_csv)
    path_to_audioFolder = st.text_input('Audio Data path')
    if path_to_audioFolder:
        audioData = read_audios(path_to_audioFolder)
    if metaData and audioData:
        col1,buff,col2 = st.columns([1,0.5,1])
        with col1:
            prev_press = st.button("prev")
        with col2:
            next_press = st.button("next")
        if prev_press:
            if st.session_state["a_counter"]>0:
                st.session_state["a_counter"]-=1
        if next_press:
            if st.session_state["a_counter"]<len(metaData["files"])-1:
                st.session_state["a_counter"]+=1
        audio_bytes = audioData[metaData["files"][st.session_state["a_counter"]]]
        st.audio(audio_bytes, format='audio/wav')#st.audio(data, format='audio/wav', start_time=0)
        st.text("transcripts:")
        st.write(metaData["transcripts"][st.session_state["a_counter"]])
        st.text("phoneme:")
        st.write(metaData["phonemes"][st.session_state["a_counter"]])
        st.text("file:")
        st.write(metaData["files"][st.session_state["a_counter"]])
        st.text("current counter:" + str(st.session_state["a_counter"]))

run_LJpage()