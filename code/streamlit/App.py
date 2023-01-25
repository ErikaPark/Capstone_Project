import streamlit as st
from streamlit_option_menu import option_menu

from window1 import Window1
from window2 import Window2
from window3 import Window3
from window4 import Window4
#from window5 import Window5

def initialize():
    st.set_page_config(page_title='LG CNS & KU - Capstone Project', layout="wide")
    with st.sidebar: #사이드바 메뉴 생성
        st.session_state['choose'] = option_menu("Options", ['Preprocess', '데이터 탐색', '분류분석 & Profiling', '오퍼링 연관분석'],
                         icons=['journal', 'bar-chart', 'bar-chart', 'bar-chart'])
   
    if 'EDA_df' not in st.session_state:
        st.session_state['EDA_df'] = None
    if 'model_df' not in st.session_state:
        st.session_state['model_df'] = None
    # if 'account_book' not in st.session_state:
    #     st.session_state['account_book'] = AccountBook()
    # if 'uploaded' not in st.session_state:
    #     st.session_state['uploaded'] = False

    if 'data_option1' not in st.session_state: # existing file / upload file? 
        st.session_state['data_option1'] = None
    if 'data_option2' not in st.session_state:  # 행동변수 연속/이항? 
        st.session_state['data_option2'] = None

if __name__ == "__main__":
    initialize()
    window1 = Window1()
    window2 = Window2()
    window3 = Window3()
    window4 = Window4()
    
    if st.session_state['choose'] == 'Preprocess': # 1페이지 이동
        window1.create_window1()
    elif st.session_state['choose'] == '데이터 탐색': # 2페이지 이동
        window2.create_window2()
    elif st.session_state['choose'] == '분류분석 & Profiling': # 3페이지 이동
        window3.create_window3()
    elif st.session_state['choose'] == '오퍼링': # 4페이지 이동
        window4.create_window4()
 







