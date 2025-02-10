import requests
import pandas as pd

API_KEY = "AIzaSyADWhQdW-LgwsZADPpUtGXOKUu9-jClXVw"
SEARCH_ENGINE_ID = "96fda36fb2fe342a8"

def find_domain(company_name):
    print(f"\n[DEBUG] Searching domain for: {company_name}")

    # Build the query
    query = f"{company_name} official website"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query
    }

    # Make the request
    try:
        response = requests.get(url, params=params)
        data = response.json()
    except Exception as e:
        print(f"[DEBUG] Error during request: {e}")
        return None

    # Print out the entire response JSON for debugging
    print("[DEBUG] Response JSON:")
    print(data)

    # Check for 'items' in the response
    if "items" in data:
        # Go through each item, printing debug info
        for idx, item in enumerate(data["items"], start=1):
            link = item.get("link", "")
            print(f"[DEBUG] Item #{idx} link: {link}")

            # Heuristic: if company_name is in the link, assume it's the official site
            if company_name.lower() in link.lower():
                print(f"[DEBUG] Matched domain with company_name: {link}")
                return link

        # Fallback to the first link if no direct match was found
        fallback_link = data["items"][0]["link"] if data["items"] else None
        print(f"[DEBUG] Fallback link: {fallback_link}")
        return fallback_link
    else:
        print("[DEBUG] No 'items' found in the response.")
        return None

def process_csv(input_file, output_file):
    # Read the input CSV into a pandas DataFrame
    df = pd.read_csv(input_file)
    
    # Print out the dataframe for sanity check
    print("\n[DEBUG] DataFrame read from CSV:")
    print(df)

    # Apply the find_domain function to each row in the 'company_name' column
    df['domain'] = df['company_name'].apply(find_domain)

    # Print out the dataframe before saving
    print("\n[DEBUG] DataFrame after adding 'domain' column:")
    print(df)

    # Save the updated DataFrame to a new CSV
    df.to_csv(output_file, index=False)
    print(f"[DEBUG] Processed file saved to: {output_file}")

if __name__ == "__main__":
    # Example usage
    input_csv = "input_companies.csv"
    output_csv = "output_with_domains.csv"
    process_csv(input_csv, output_csv)
