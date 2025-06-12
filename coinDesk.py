import sys
import requests
import time
import csv

Url = "https://data-api.cryptocompare.com/index/cc/v1/historical/minutes?market=cadli&instrument="

def print_first_instance(symbol):
    timestamp = str(int(time.time()))
    final_url = (
        Url + symbol +
        "-USD&limit=289&aggregate=5&fill=true&apply_mapping=true&response_format=JSON"
        "&cache_bust_ts=" + timestamp + "&to_ts=" + timestamp
    )
    response = requests.get(final_url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {symbol}: {response.status_code}")
        return

    data = response.json()
    if 'Data' in data and data['Data']:
        coin_data = data['Data'][0]
        print(f"\nFirst data point for '{symbol}':")
        for key, value in coin_data.items():
            print(f"'{key}': {value}")

        # Write to CSV
        fieldnames = list(coin_data.keys())
        with open('tester.csv', 'a', newline='') as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write header only if file is empty
            if csvfile.tell() == 0:
                thewriter.writeheader()
            thewriter.writerow(coin_data)
    else:
        print(f"No data found for {symbol}.")

if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 0 else ["BTC"]
    for symbol in args:
        print_first_instance(symbol)