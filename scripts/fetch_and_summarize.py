import argparse
import requests
import pandas as pd
from collections import Counter

CKAN_API_ENDPOINT = "https://open.canada.ca/data/api/3/action/datastore_search"
RESOURCE_ID = "fac950c0-00d5-4ec1-a4d3-9cbebf98a305"  # Proactive Disclosure of Contracts


def fetch_page(keyword: str, offset: int = 0, limit: int = 100) -> dict:
    """Fetch a single page of CKAN results."""
    params = {
        "resource_id": RESOURCE_ID,
        "q": keyword,
        "offset": offset,
        "limit": limit,
    }
    resp = requests.get(CKAN_API_ENDPOINT, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_all(keyword: str, max_records: int = 500) -> list:
    """Fetch up to max_records from the CKAN API."""
    results = []
    offset = 0
    while offset < max_records:
        page = fetch_page(keyword, offset=offset, limit=min(100, max_records - offset))
        records = page.get("result", {}).get("records", [])
        if not records:
            break
        results.extend(records)
        offset += len(records)
        if len(records) < 100:
            break
    return results


def summarize(records: list) -> dict:
    if not records:
        return {}
    df = pd.DataFrame(records)
    df["contract_value"] = pd.to_numeric(df.get("contract_value", 0), errors="coerce")
    avg_value = df["contract_value"].mean()
    frequency = len(df)
    top_vendors = Counter(df.get("vendor_name", []))
    top_vendors = top_vendors.most_common(5)
    return {
        "average_value": avg_value,
        "frequency": frequency,
        "top_vendors": top_vendors,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch and summarize contract data from CKAN")
    parser.add_argument("keyword", help="Keyword to search for, e.g. 'interpretation'")
    parser.add_argument("--max-records", type=int, default=500, help="Maximum number of records to fetch")
    parser.add_argument("--output", help="Optional CSV output file")
    args = parser.parse_args()

    records = fetch_all(args.keyword, args.max_records)
    if args.output:
        pd.DataFrame(records).to_csv(args.output, index=False)
    summary = summarize(records)
    if summary:
        print(f"Fetched {summary['frequency']} records")
        print(f"Average contract value: {summary['average_value']:.2f}")
        print("Top vendors:")
        for vendor, count in summary['top_vendors']:
            print(f"  {vendor}: {count}")
    else:
        print("No records found")


if __name__ == "__main__":
    main()
