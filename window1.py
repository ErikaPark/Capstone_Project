import streamlit as st
import pandas as pd 
import numpy as np 
from st_aggrid import AgGrid

import Helper

s = st.session_state

class Window1:
    def __init__(self):
        super().__init__()
        self.processed_df_path = '../../data/processed1/'
        self.preprocess_code_df = '../preprocess/'

    def create_window1(self):
        st.markdown("<h1 style='text-align: center; color: grey;'> 데이터 전처리 </h1>", unsafe_allow_html=True)
        Helper.space(1)
        col1, col2 = st.columns([1,1])
        s['data_option1'] = col1.selectbox(label = 'Choose Data Option:', options = ('기존 파일 사용', '파일 불러오기'))
        s['data_option2'] = col2.radio('전처리 하고싶은 행동변수 유형:',('이항형', '연속형'))
        
        if s['data_option1'] == '파일 불러오기':
            c1, c2,c3 = st.columns([1,1,1])
            file_format = c1.radio('file format:', ('csv', 'excel'), key='file_format')
            dataset = c1.file_uploader(label = 'Load ContactDB')
            file_format2 = c2.radio('file format:', ('csv', 'excel'), key='file_format2')
            dataset2 = c2.file_uploader(label = 'Load Activity_Merged')
            file_format3 = c3.radio('file format:', ('csv', 'excel'), key='file_format3')
            dataset3 = c3.file_uploader(label = 'Load EmailSent')       
            if dataset:
                contactDB = self.load_data(file_format, dataset)
                if dataset2:
                    activity_merged = self.load_data(file_format2, dataset2)    
                    if dataset3:
                        emailsent = self.load_data(file_format3, dataset3)
                        Helper.space(3)
                        self.display_raw_data(contactDB, activity_merged, emailsent)
                        self.preprocess(contactDB, activity_merged, emailsent)

        else:
            contactDB = pd.read_csv(self.processed_df_path + 'ContactDB.csv')
            activity_merged = pd.read_csv(self.processed_df_path + 'activity_merged.csv')
            emailsent = pd.read_csv(self.processed_df_path + 'EmailSent.csv')
            Helper.space(3)
            self.display_raw_data(contactDB, activity_merged, emailsent)
            self.preprocess(contactDB, activity_merged, emailsent)
        
        

    def load_data(self, file_format, dataset):
        if file_format == 'csv':
            data = pd.read_csv(dataset)
        else:
            data = pd.read_excel(dataset)
        return data 

    def display_raw_data(self,contactDB, activity_merged, emailsent):
        c1, c2,c3 = st.columns([1,1,1])
        c1.markdown("<h3 style='text-align: center; color: CornflowerBlue;'> ContactDB </h3>", unsafe_allow_html=True)
        c1.dataframe(contactDB.head())
        c2.markdown("<h3 style='text-align: center; color: CornflowerBlue;'> activity_merged </h3>", unsafe_allow_html=True)
        c2.dataframe(activity_merged.head())
        c3.markdown("<h3 style='text-align: center; color: CornflowerBlue;'> EmailSent </h3>", unsafe_allow_html=True)
        c3.dataframe(emailsent.head())
    
    def preprocess(self,contactDB, activity_merged, emailsent):
        Helper.space(3)
        st.markdown("<h2 style='text-align: center; color: IndianRed;'> 전처리 후 데이터 </h2>", unsafe_allow_html=True)
        # TODO: Preprocess 모듈화 한 후 연동시키기

    # ContactDB.head()
    # Activity_merged.head()

    