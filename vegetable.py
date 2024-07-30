import requests
import json
import pandas as pd
from datetime import datetime, timedelta 

start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 6, 30)
current_date = start_date

dates = []
while current_date <= end_date:
    dates.append(current_date.strftime("%Y-%m-%d"))
    current_date += timedelta(days=1)

def scrap_data(date):
  url = f"https://vegetablemarketprice.com/api/dataapi/market/delhi/daywisedata?date={date}"
  header = {
      "accept": "*/*",
      "accept-language": "en-US,en;q=0.9",
      "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"Windows\"",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      "cookie": "JSESSIONID=CA2C3945D16768B3EE1FB68E4312275E; _ga_2RYZG7Y4NC=GS1.1.1722273102.1.0.1722273102.0.0.0; _ga=GA1.1.1767736402.1722273102; __gads=ID=25b0eb71f470c080:T=1722273102:RT=1722273102:S=ALNI_Mbwe81AHZO7aot3nDl6p9AdVYxLiQ; __gpi=UID=00000eacc403d473:T=1722273102:RT=1722273102:S=ALNI_MZYA9RjS3mZJlZRqL5hG3IotD1NfA; __eoi=ID=d9a22223886c96bc:T=1722273102:RT=1722273102:S=AA-AfjZGM8A5ArgRJHx1wHhpVUTv",
      "Referer": "https://vegetablemarketprice.com/market/delhi/today",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36", 
      "Referrer-Policy": "strict-origin-when-cross-origin"
    }


  data = requests.get(url, headers = header)
  js_data = json.loads(data.text)

  arr_data = []
  for api in js_data["data"]:
      v_id  = api["id"]
      v_name = api["vegetablename"]
      v_wholesale_price = api["price"]
      v_ret_pri = api["retailprice"]
      v_shop_pri = api["shopingmallprice"]
      v_units = api["units"]
      v_img = api["imageProperties"]
     


      new_js_data = {
        "Date": date,
        "Vegetable_Id ": v_id,
        "Vegetable_Name ": v_name,
        "Wholesale_Price ": str(v_wholesale_price), 
        "Retail_Price ": str(v_ret_pri),
        "Shoping_Mall_Price ": str(v_shop_pri),
        "Units ": str(v_units),
        "Image": v_img
      }
      arr_data.append(new_js_data)

  return arr_data

all_data = [{"State": "delhi"}]
for date in dates:
    daily_data = scrap_data(date)
    all_data.extend(daily_data)

df = pd.DataFrame(all_data)



    # Save the data to a CSV file
df.to_csv("vegetable_data.csv", index=False)
    
print("Data successfully scraped and saved to vegetable_data.csv")
