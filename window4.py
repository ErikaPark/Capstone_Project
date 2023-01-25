import streamlit as st
import pandas as pd 
import numpy as np 

import Helper

class Window4:
    def __init__(self):
        super().__init__()

    def create_window4(self):
        st.markdown("<h1 style='text-align: center; color: grey;'> 연관분석: Offering </h1>", unsafe_allow_html=True)
        Helper.space(1)
