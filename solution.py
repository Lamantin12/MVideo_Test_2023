import pandas as pd
import streamlit as st
import numpy as np

def preprocess_data(dataframe):
    return dataframe

def main():
    # Начальные настройки
    st.set_page_config(layout="wide")
    
    # Загрузка файла и все что с ним связано 
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None: # Если пользователь ввел файл
        # Читаем
        df_raw = pd.read_csv(uploaded_file, encoding="Windows-1251")
    else:
        # Если нет - кидаем ошибку
        st.warning("you need to upload a csv or excel file.")
    
    # Если прочитали
    if df_raw is not None:
        df_column_raw, df_column_processed = st.columns(2)
        data = preprocess_data(df_raw)

        df_column_raw.dataframe(df_raw)
        df_column_processed.dataframe(data)






if __name__=='__main__':
    main()