import streamlit as st
import pandas as pd 
import numpy as np 

import Helper

s = st.session_state

class Window3:
    def __init__(self):
        super().__init__()
        self.eda_df_path = '../../data/processed2/'
        self.model_df_path = '../../data/modelling_data/'

    def create_window3(self):
        st.markdown("<h1 style='text-align: center; color: grey;'> 분류분석 & Profiling </h1>", unsafe_allow_html=True)
        Helper.space(1)
        col1, col2 = st.columns([1,1])
        s['data_option1'] = col1.selectbox(label = 'Choose Data', options = ('기존 파일 사용', '파일 불러오기'))
        s['data_option2'] = col1.radio('행동변수 유형을 선택하세요:',('이항형', '연속형'))
        
        if s['data_option1'] == '파일 불러오기':
            file_format = col1.radio('Select file format:', ('csv', 'excel'), key='file_format')
            dataset = col1.file_uploader(label = '')
            if dataset:
                if file_format == 'csv':
                    s['model_df'] = pd.read_csv(dataset)
                else:
                    s['model_df'] = pd.read_excel(dataset)
  
        else:
            if s['data_option2'] == '연속형':
                s['EDA_df'] = pd.read_csv(self.eda_df_path + 'data_연속형행동.csv')
                s['model_df'] = pd.read_csv(self.model_df_path + 'model_data_연속형행동.csv')
            else: #이항형 
                 s['EDA_df'] = pd.read_csv(self.eda_df_path + 'data_이항형행동.csv')
                 s['model_df'] = pd.read_csv(self.model_df_path + 'model_data_이항형행동.csv')


        s['version'] = col2.selectbox(label = 'Select Modelling Option', options = ('학습된 모형 사용하기', '새로운 모형 학습시키기'))

        if s['version'] == '학습된 모형 사용하기':
            self.display_result()

        elif s['version'] == '새로운 모형 학습시키기':
            self.tuning_new_models()
            self.display_result()
        
        Helper.space(4)
    
    def display_result(self):
        st.markdown("<h2 style='text-align: left; color: grey;'> 모형 성능 비교: </h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])
        col1.markdown("<h3 style='text-align: left; color: DarkSeaGreen;'>Benchmark: Logistic Regression</h3>", unsafe_allow_html=True)
        col2.markdown("<h3 style='text-align: left; color: DarkSalmon;'>ML: Random Forests</h3>", unsafe_allow_html=True)
        col3.markdown("<h3 style='text-align: left; color: DarkSalmon;'>ML: XGBoost</h3>", unsafe_allow_html=True)
    # Logistic Regression, XGBoost, Random Forests 모델 성능 결과 보여주기 
    # 그리고 추천 모형 명시 
    # 세 모형 중 한 모형 선택하는 option

    # 전체 데이터에 대해 Fit & Predict 한 후 df 보여주기 
    # Filtering option
    # 데이터프레임 저장 기능
    # ContactID 추출 기능 


    def tuning_new_models(self):pass
    # Logistic Regression 결과는 바로 보여주기 
    # 새로 튜닝하기 
    # 10-CV로 알고리즘 별 가장 좋은 모형 보여주기
    # 두 모형에 대한 5-CV score 결과 보여주기 
    # 다 끝나면 message: 학습이 다 끝났으니 모형을 선택하라는 메시지 
    # 세 모형 중 한 모형 선택하는 option

    # 전체 데이터에 대해 Fit & Predict 한 후 df 보여주기 
    # Filtering option 
    # 데이터프레임 저장 기능 
    # ContactID 추출 기능 


