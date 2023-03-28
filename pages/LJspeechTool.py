from utils.LJdataReader import read_csv_LJspeech,read_audios
import streamlit as st


def run_LJpage():
    def change_phonemes():
        st.session_state["editedPhoneme"] = st.session_state["editedtranscript"]
    if "a_counter" not in st.session_state:
        st.session_state["a_counter"]=0
    if "enable_edit" not in st.session_state:
        st.session_state["enable_edit"]=False
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
                st.session_state["enable_edit"]=False
        if next_press:
            if st.session_state["a_counter"]<len(metaData["files"])-1:
                st.session_state["a_counter"]+=1
                st.session_state["enable_edit"]=False
        audio_bytes = audioData[metaData["files"][st.session_state["a_counter"]]]
        st.audio(audio_bytes, format='audio/wav')#st.audio(data, format='audio/wav', start_time=0)
        st.text("transcripts:")
        st.write(metaData["transcripts"][st.session_state["a_counter"]])
        edit = st.button("edit")
        if edit:
            st.session_state["enable_edit"]= not  st.session_state["enable_edit"]
        if st.session_state["enable_edit"]:
            new_transcript = st.text_area("enter new transcript:",metaData["transcripts"][st.session_state["a_counter"]],key="editedtranscript",
                                          on_change=change_phonemes)
            #call function to edit it in csv when apply button is pressed


        st.text("phoneme:")
        st.write(metaData["phonemes"][st.session_state["a_counter"]])
        if st.session_state["enable_edit"]:
            new_phoneme = st.text_area("new phoneme is same as transcription by default:",metaData["phonemes"][st.session_state["a_counter"]],key="editedPhoneme")
            #call function to save new phoneme when apply is clicked

        st.text("file:")
        st.write(metaData["files"][st.session_state["a_counter"]])
        st.text("current counter:" + str(st.session_state["a_counter"]))

run_LJpage()