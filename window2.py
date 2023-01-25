import streamlit as st
import pandas as pd 
import numpy as np 

from st_aggrid import AgGrid
from st_aggrid import grid_options_builder
import plotly.express as px
import io

import Helper

s = st.session_state

class Window2:
    def __init__(self):
        super().__init__()
        self.eda_df_path = '../../data/processed2/'

    def create_window2(self):
        st.markdown("<h1 style='text-align: center; color: grey;'> Exploratory Data Analysis </h1>", unsafe_allow_html=True)
        col1, col2 = st.columns([1,1])
        s['data_option1'] = col1.selectbox(label = 'Choose Data', options = ('기존 파일 사용', '파일 불러오기'))
        s['data_option2'] = col1.radio('행동변수 유형을 선택하세요:',('이항형', '연속형'))
        
        if s['data_option1'] == '파일 불러오기':
            file_format = col1.radio('Select file format:', ('csv', 'excel'), key='file_format')
            dataset = col1.file_uploader(label = '')
            if dataset:
                if file_format == 'csv':
                    s['EDA_df'] = pd.read_csv(dataset)
                else:
                    s['EDA_df'] = pd.read_excel(dataset)
  
        else:
            if s['data_option2'] == '연속형':
                s['EDA_df'] = pd.read_csv(self.eda_df_path + 'data_연속형행동.csv')
                
            else: #이항형 
                 s['EDA_df'] = pd.read_csv(self.eda_df_path + 'data_이항형행동.csv')
        
        st.subheader('Show dataframe')
        self.display_df()
        st.subheader('Choose Visualization Option')
        self.draw_inputs()

    
    def display_df(self):
        n = len(s['EDA_df']); m =len(s['EDA_df'].columns)
        st.write(f'<p style="font-size:130%">rows: {n}, columns: {m}</p>', unsafe_allow_html=True)
        gb = grid_options_builder.GridOptionsBuilder.from_dataframe(s['EDA_df']) 
        gb.configure_pagination(enabled=True)
        gb.configure_default_column(groupable = True) #변수 별로 그룹핑 가능하게 하기

        gridoptions = gb.build()
        col1, col2, col3 = st.columns([1,3,1])
        AgGrid(s['EDA_df'], gridOptions = gridoptions)

    def draw_inputs(self):
        df = s['EDA_df']
        #option1
        options = ['Data Type Info', 'NA값 개수/비율', 'Count Plots / Histogram']
        c1, c2, c3 = st.columns([0.5, 2, 0.5])
        option_input = c2.multiselect("", options)
        Helper.space(3)
        
        if 'Data Type Info' in option_input: 
            self.data_type_info(df)
            Helper.space(2)

        if 'NA값 개수/비율' in option_input: 
            self.count_NA(df)
            Helper.space(2)

        if 'Count Plots / Histogram' in option_input:
            cat_columns = df.select_dtypes(include = 'object').columns
            st.subheader('Count/Distribution Plots of Selected Columns')
            if len(cat_columns) == 0:
                st.write('There is no categorical columns in the data.')
            else:
                #container = st.container(2)
                c1, c2, c3 = st.columns([0.5, 2, 0.5])
               
                select_all_button = c2.checkbox("Select all for plots")

                if select_all_button:
                    selected_num_cols = c2.multiselect('Choose columns for plots:',  cat_columns, default = list(cat_columns))
                else:
                    selected_num_cols = c2.multiselect('Choose columns for plots:',cat_columns, default = cat_columns[0])
                
                selected_cat_cols = selected_num_cols

                
                self.draw_plots(selected_cat_cols, df)
            Helper.space(2)
                

    def data_type_info(self, data):
        st.subheader("변수 별 Data Type 정보:")
        c1, c2, c3 = st.columns([1, 2, 1])
        c2.dataframe(self.df_info(data))

    def df_info(self,df):
        df.columns = df.columns.str.replace(' ', '_')
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()

        df_info = s.split('\n')

        counts = []
        names = []
        nn_count = []
        dtype = []
        for i in range(5, len(df_info)-3):
            line = df_info[i].split()
            counts.append(line[0])
            names.append(line[1])
            nn_count.append(line[2])
            dtype.append(line[4])

        df_info_dataframe = pd.DataFrame(data = {'#':counts, 'Column':names, 'Non-Null Count':nn_count, 'Data Type':dtype})
        return df_info_dataframe.drop('#', axis = 1)
    
    def count_NA(self, data):
        st.subheader('변수 별 NA 개수와 비율(%):')
        if data.isnull().sum().sum() == 0:
            st.write('There is not any NA value in your dataset.')
        else:
            c1, c2, c3 = st.columns([0.5, 2, 0.5])
            c2.dataframe(Helper.df_isnull(data), width=1500)
            Helper.space(2)

    def draw_plots(self, columns, df):
        i = 0
        while (i < len(columns)):
            c1, c2 = st.columns(2)
            for j in [c1, c2]:
                if (i >= len(columns)):
                    break
                fig = px.histogram(df, x = columns[i], color_discrete_sequence=['indianred'])
                j.plotly_chart(fig)
                i += 1