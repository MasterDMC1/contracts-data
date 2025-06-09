import streamlit as st
import pandas as pd
from fetch_and_summarize import fetch_all, summarize

st.title("Contract Benchmarking MVP")

keyword = st.text_input("Keyword", "interpretation")
max_records = st.slider("Max records", min_value=100, max_value=1000, value=200, step=100)

if st.button("Search"):
    with st.spinner("Fetching data..."):
        records = fetch_all(keyword, max_records)
    summary = summarize(records)
    if summary:
        st.write(f"Fetched {summary['frequency']} records")
        st.write(f"Average contract value: {summary['average_value']:.2f}")
        st.subheader("Top vendors")
        for vendor, count in summary['top_vendors']:
            st.write(f"{vendor}: {count}")
        df = pd.DataFrame(records)
        st.dataframe(df)
    else:
        st.write("No records found")
