import camelot
import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader
import tempfile
import os

def extract_tables(pdf_path, pages_to_extract):
    tables = camelot.read_pdf(pdf_path, pages=pages_to_extract)

    dfs = []
    for table in tables:
        df = table.df
        df = df.applymap(lambda x: x.replace("\n", " ") if isinstance(x, str) else x)
        df = df.applymap(lambda x: x.replace("  ", " ") if isinstance(x, str) else x)
        df = df.applymap(lambda x: x.replace("✓", "Sim") if isinstance(x, str) else x)
        df = df.applymap(lambda x: x.replace("", "Não") if isinstance(x, str) else x)

        df.replace({"": pd.NA}, inplace=True)
        cleaned_dfs_filled = df.fillna(method='ffill')

        dfs.append(cleaned_dfs_filled)

    return dfs
  

def main():
    st.header("Extract table from pdf")

    # upload a pdf file
    pdf = st.file_uploader("Upload your PDF", type='pdf')
    
    #st.write(pdf)
    if pdf is not None:
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, "temp.pdf")
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(pdf.read())

        pdf_reader = PdfReader(pdf)
        
        for i, page in enumerate(pdf_reader.pages):
            print(i)
            print(page.annotations)
            text = page.extract_text()
            
            tables = extract_tables(temp_file_path, pages_to_extract=str(i+1))
            for table in tables:
                st.dataframe(table)


if __name__ == '__main__':
    main()
