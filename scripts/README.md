# Scripts for Contract Data Benchmarking

This directory contains utilities to fetch and summarize contract award data from
Canada's open procurement portal. The primary entry point is
`fetch_and_summarize.py`, which queries the CKAN API and outputs simple
statistics.

## Requirements
- Python 3.8+
- `requests` and `pandas`

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Usage
```bash
python fetch_and_summarize.py "interpretation" --max-records 200 --output results.csv
```
This command fetches up to 200 records matching the keyword "interpretation" and
writes them to `results.csv`. A brief summary is printed to the console.

Because the CKAN API contains hundreds of thousands of rows, consider adjusting
`--max-records` depending on your bandwidth and required accuracy.

## Running the Streamlit app

After installing the requirements you can launch a tiny dashboard with:

```bash
streamlit run app.py
```

This provides a form to enter a keyword and displays the results in your
browser.

## Limitations
- Provincial data sources are not yet included; scraping those sites will require additional code.
- Network access is required to reach `open.canada.ca`.
