from utils.LJdataReader import read_csv_LJspeech,read_audios
from utils.utils import edit_csv,write_to_json_save,create_intial_save,read_save
import uuid
import streamlit as st


def run_LJpage():
    def change_norm_transcripts():
        st.session_state["editednormtranscripts"] = st.session_state["editedtranscript"]
    if "a_counter" not in st.session_state:
        st.session_state["a_counter"]=0
    if "fixed_session" not in st.session_state:
        st.session_state["fixed_session"]=False
    if "enable_edit" not in st.session_state:
        st.session_state["enable_edit"]=False
    if "session_id" not in st.session_state:
        st.session_state["session_id"]="Not assigned"
        
    sessionid_continue = st.text_input('enter session id to continue a saved session')
    if not st.session_state["fixed_session"]:
        if sessionid_continue:
            st.session_state["session_id"]=sessionid_continue  
            st.session_state["fixed_session"] =True
        if st.button("or begin new session"):
            st.session_state["session_id"]=str(uuid.uuid4())
            st.session_state["fixed_session"] =True
            create_intial_save(st.session_state["session_id"],"edited_files")
    st.text("session id:"+ st.session_state["session_id"])
    path_to_csv = st.text_input('MetaData CSV file path')
    metaData = None
    audioData = None
    
    if path_to_csv:
        metaData = read_csv_LJspeech(path_to_csv)
    path_to_audioFolder = st.text_input('Audio Data path')
    if path_to_audioFolder:
        audioData = read_audios(path_to_audioFolder)
    if metaData and audioData and st.session_state["fixed_session"] :
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
        with buff:
            if metaData["files"][st.session_state["a_counter"]] in set(read_save(st.session_state["session_id"],"edited_files")):
                st.text("Edited ")
            else :
                st.text("Not edited ")
        audio_bytes = audioData[metaData["files"][st.session_state["a_counter"]]]
        st.audio(audio_bytes, format='audio/wav')#st.audio(data, format='audio/wav', start_time=0)
        st.text("transcripts:")
        st.write(metaData["transcripts"][st.session_state["a_counter"]])
        edit = st.button("edit")
        if edit:
            st.session_state["enable_edit"]= not  st.session_state["enable_edit"]
        if st.session_state["enable_edit"]:
            new_transcript = st.text_area("enter new transcript:",metaData["transcripts"][st.session_state["a_counter"]],key="editedtranscript",
                                          on_change=change_norm_transcripts)
           

        st.text("normalised transcripts:")
        st.write(metaData["norm_transcripts"][st.session_state["a_counter"]])
        if st.session_state["enable_edit"]:
            norm_transcript = st.text_area("new normalised transcript is same as transcription by default:",metaData["norm_transcripts"][st.session_state["a_counter"]],key="editednormtranscripts")
            #call function to save new norm_transcripts when apply is clicked and reload data
        if st.session_state["enable_edit"]:
            save = st.button("save", type="primary")
            if save:
                #call function to edit it in csv when apply button is pressed and reload data and add to save
                edit_csv(path_to_csv,st.session_state["a_counter"],1,new_transcript)
                edit_csv(path_to_csv,st.session_state["a_counter"],2,norm_transcript)
                metaData = read_csv_LJspeech(path_to_csv)
                write_to_json_save(st.session_state["session_id"],"edited_files",metaData["files"][st.session_state["a_counter"]])


        st.text("file:")
        st.write(metaData["files"][st.session_state["a_counter"]])
        st.text("current counter:" + str(st.session_state["a_counter"]+1) + '/' + str(len(metaData["files"])))
        st.text("total edited files :" +str(len(set(read_save(st.session_state["session_id"],"edited_files")))) )

run_LJpage()