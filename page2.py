import streamlit as st
import page1
import bioread
import matplotlib.pyplot as plt
import pandas as pd

import Streamlitapp

st.title("Trigger Events")
col1,col2 = st.columns([.3,.7])
graph_container = col2.container()


def initialize_states():  
    if st.session_state['trigger_ready'] == True:
        if 'acq_data' not in st.session_state:
            st.session_state['acq_data'] = load_data()
        if 'current_df' not in st.session_state:
            st.session_state['current_df'] = acq_to_pandas_df()
        if 'list_of_triggers' not in st.session_state:
            st.session_state['list_of_triggers'] = find_triggers()     
        if 'windows_to_plot' not in st.session_state:
            st.session_state['windows_to_plot'] = extract_windows()

def load_data():
    acq_data = None
    file_selected= st.session_state['file_storage'][st.session_state['dropdown_index']]
    acq_data = bioread.read_file(file_selected)
    return acq_data


def acq_to_pandas_df():
    df = pd.DataFrame()
    acq_file = st.session_state['acq_data']
    for channel in acq_file.channels:
        df[channel.name] = channel.data
    timecol = []
    timestep = 1.0 / acq_file.channels[0].samples_per_second
    numsamples = len(acq_file.channels[0].data)
    for n in range(numsamples):
        timecol.append(n * timestep)
    df['Time'] = timecol
    return df


def find_triggers():
    current_trigger_sample = 0
    threshold = 3
    indexes_of_triggers = []
    df = st.session_state['current_df']
    filtered_df = df[df['Trigger'] > threshold]
    for index,row in filtered_df.iterrows():
        if index > current_trigger_sample + 200:
            indexes_of_triggers.append(index)
            current_trigger_sample = index
    return indexes_of_triggers


def extract_windows():
    # We want to extract a window, about 10 ms before the trigger point as well as 300ms after. 
    list_of_windows = []
    list_of_triggers = st.session_state['list_of_triggers']
    for i in list_of_triggers:
        window = [i - 10]
        window.append(i + 300)
        list_of_windows.append(window)
    return list_of_windows   


def plot_triggers():
    if st.session_state['trigger_ready'] == True:
        fig, ax = plt.subplots()
        count = 1
        windows = st.session_state['windows_to_plot']
        df = st.session_state['current_df']
        for start,end in windows:    
            ax.plot(df['Time'][start : end], df['EMG RF'][start : end])
            ax.plot(df['Time'][start+10], df['EMG RF'][start+10], marker='x', markerfacecolor='blue', markersize=7)
            ax.set_title(f"Cortical Silent Period Number: {count}")
            ax.set_xlabel('Time (ms)')
            ax.set_ylabel('EMG Signal (mV)')
            graph_container.pyplot(fig)
            ax.clear()
            count = count + 1


def add_checkboxes():
    if st.session_state['trigger_ready'] == True:
        col1.write("Cortical Silent periods Extracted:")
        count = 1
        for i in range(len(st.session_state['list_of_triggers'])):
            col1.checkbox(f"Cortical Silent Period {count}", key = f"csp_number_{count}")
            if f'csp_number_{count}' not in st.session_state:
                st.session_state[f'csp_number_{count}'] = False
            count = count + 1
        col1.button("Remove Periods", on_click = remove_csp_from_trigger)   

def remove_csp_from_trigger():
    count = 1
    for i in range(len(st.session_state['list_of_triggers'])):
        if st.session_state[f'csp_number_{count}'] == True:
            st.session_state['list_of_triggers'].pop(count-1)
            st.session_state['windows_to_plot'].pop(count-1)
            st.session_state[f'csp_number_{count}'] = False
            count = count - 1
        count = count + 1


initialize_states()
plot_triggers()
add_checkboxes()

st.button('refresh',key = 234567890)




