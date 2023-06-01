import pandas as pd
import streamlit as st
import numpy as np


def main():
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

if __name__=='__main__':
    main()