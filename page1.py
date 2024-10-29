import streamlit as st

#Markdown
st.title("File Upload")
#initializations of session states:
if 'trigger_ready' not in st.session_state:
    st.session_state['trigger_ready'] = False
if 'file_storage' not in st.session_state:
    st.session_state['file_storage'] = []
if 'selected_dropdownbox' not in st.session_state:
    st.session_state['selected_dropdownbox'] = "No File Selected"
if 'dropdown_index' not in st.session_state:
    st.session_state['dropdown_index'] = 0
# Updating the drodown menu for selecting the file that will be used for data analysis.
def updt_file_select_dropdown():
    if st.session_state['uploaded_files']:
        st.session_state['file_storage'] = []
        for file in st.session_state['uploaded_files']:
            st.session_state['file_storage'].append(file)


def updt_dropdown_selection():    
   st.session_state['dropdown_index'] = st.session_state['dropdown']
   
#streamlit built in file uploader calling the method to update the selection box. 
file_uploader= st.file_uploader("EMG File",
                        type = ['acq'],
                        accept_multiple_files=True,
                        key = 'uploaded_files',
                        on_change= updt_file_select_dropdown)
dropdown = st.selectbox(label = "File Selection",
                        key = 'dropdown',
                        index = st.session_state['dropdown_index'] ,
                        options = range(len(st.session_state['file_storage'])),
                        format_func=lambda x: st.session_state['file_storage'][x].name,
                        on_change=updt_dropdown_selection)
if st.session_state['file_storage'] != []:
    st.session_state['trigger_ready'] = True