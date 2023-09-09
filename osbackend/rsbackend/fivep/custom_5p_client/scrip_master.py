import csv
import requests
import pandas as pd
import datetime as dt
url = 'https://images.5paisa.com/website/scripmaster-csv-format.csv'

csv_path= "scripmaster-csv-format.csv"
# Load CSV file into a Pandas DataFrame
# content = response.content.decode('utf-8')
# lines = content.splitlines()

# data = []
# for line in csv.reader(lines):
#     data.append(line)

# print(data[0])
# print(data[1][0])
import logging
logger = logging.getLogger(__name__)


class ScripMaster():

    def __init__(self, ):
        self.csv_url= url
        self.csv_path="scripmaster-csv-format.csv"
        # response = requests.get(url)
        
    # download the scrip master
    def download_scrip_master(self):
        try:
            response = requests.get(url)
            print("response", response)
            open('scripmaster-csv-format.csv', 'wb').write(response.content)
        except Exception:
            logger.error("Error downloading the scripmaster")

    # For Nifty.banknifty it will be montly fut
    def get_next_week_or_monthly_future_scrip_details(self,exch, exch_type, root, option_type, current_fut_price, range_size ):
        df = pd.read_csv(self.csv_path, encoding='utf-8')
        # Filter the data based on conditions
        exch_type = exch_type
        root = root
        # if option_type is not None:
        df['Expiry'] = pd.to_datetime(df['Expiry'], format='%Y-%m-%d %H:%M:%S')
        range_start = current_fut_price - range_size
        range_end = current_fut_price + range_size

        # data = df[(df['ExchType'] == exch_type) &  (df['Root'] == root) &(df['CpType'] == option_type)]
        df = df[(df['ExchType'] == exch_type) & (df['Root'] == root) & (df['CpType'] == option_type) & (df['StrikeRate'] >= range_start) & (df['StrikeRate'] <= range_end)]
        # else:
        #     data = df[(df['ExchType'] == exch_type) & (df['CpType'] == 'XX') & (df['Root'] == root)]
        
        # Sort the DataFrame based on the 'Name' column
       
       
        sorted_df = df.sort_values(by='Expiry')

        # Access the sorted data
        # print(sorted_df.head())  # print the first 5 rows

        # Get today's date
        today = dt.datetime.now().date()

        # Filter the sorted_df DataFrame to select rows where Expiry is greater than today's date
        filtered_df = sorted_df[sorted_df['Expiry'].dt.date > today]

        print(filtered_df.head())


        # Extract the first column from the filtered DataFrame
        first_row = filtered_df.iloc[0]
        # expiry = first_row["Expiry"].strftime('%Y-%m-%d %H:%M:%S')

        # filtered_rows = data[(data['ExchType'] == 'U') & (data['Expiry'] == expiry) & (data['CpType'] == option_type) & (data['StrikeRate'] >= range_start) & (data['StrikeRate'] <= range_end) & (data['Root'] == root)]

        return first_row
    
    def get_next_exp_fut_scrip_details(self,exch, exch_type, root, cp_type):
        df = pd.read_csv(self.csv_path, encoding='utf-8')
        exch_type = exch_type
        root = root
        cp_type = "XX"
        # if option_type is not None:
        df['Expiry'] = pd.to_datetime(df['Expiry'], format='%Y-%m-%d %H:%M:%S')
        
        # data = df[(df['ExchType'] == exch_type) &  (df['Root'] == root) &(df['CpType'] == option_type)]
        df = df[(df['Exch'] == exch) & (df['ExchType'] == exch_type) & (df['Root'] == root) & (df['CpType'] == cp_type)]
        # else:
        #     data = df[(df['ExchType'] == exch_type) & (df['CpType'] == 'XX') & (df['Root'] == root)]
        
        # Sort the DataFrame based on the 'Name' column
       
       
        sorted_df = df.sort_values(by='Expiry')

        # Access the sorted data
        # print(sorted_df.head())  # print the first 5 rows

        # Get today's date
        today = dt.datetime.now().date()

        # Filter the sorted_df DataFrame to select rows where Expiry is greater than today's date
        filtered_df = sorted_df[sorted_df['Expiry'].dt.date > today]

        # print(filtered_df.head())


        # Extract the first column from the filtered DataFrame
        first_row = filtered_df.iloc[0]
        # expiry = first_row["Expiry"].strftime('%Y-%m-%d %H:%M:%S')

        # filtered_rows = data[(data['ExchType'] == 'U') & (data['Expiry'] == expiry) & (data['CpType'] == option_type) & (data['StrikeRate'] >= range_start) & (data['StrikeRate'] <= range_end) & (data['Root'] == root)]

        return first_row
    

    def get_next_week_atm_option(self, expiry, current_fut_price, option_type, range_size, root):
        # expiry= "2023-05-04 14:30:00"
        # current_usdinr_fut_price = 81.8225
        # option_type = "CE"

        # range_size = 0.25
        range_start = current_fut_price - range_size
        range_end = current_fut_price + range_size
        data = pd.read_csv(csv_path, encoding='utf-8')
        filtered_rows = data[(data['ExchType'] == 'U') & (data['Expiry'] == expiry) & (data['CpType'] == option_type) & (data['StrikeRate'] >= range_start) & (data['StrikeRate'] <= range_end) & (data['Root'] == root)]

        # Sort the filtered rows based on the absolute difference between StrikeRate and current_usdinr_fut_price
        filtered_rows = filtered_rows.assign(difference=abs(filtered_rows['StrikeRate'] - current_fut_price)).sort_values('difference')

        # Select the first row
        return filtered_rows.iloc[0]

    def get_nifty_atm_option(self, current_fut_price):

        current_fut_price= self.next_expiry_fut_scrip_nifty
        atm_op= self.get_next_week_atm_option(expiry = self.next_expiry_fut_scrip_nifty["Expiry"].strftime('%Y-%m-%d %H:%M:%S'),current_fut_price=current_fut_price,option_type="CE", range_size=50, root="NIFTY" )
        pass

# sm = ScripMaster()
# # exch_type, root, option_type, current_fut_price, range_size

# next_expiry_fut_scrip_nifty = sm.get_next_week_or_monthly_future_scrip_details(exch_type = "D", root = "NIFTY", option_type="CE", current_fut_price= 17026, range_size= 50)
         
# print("next_expiry_fut_scrip_nifty ", next_expiry_fut_scrip_nifty)


# next_expiry_fut_scrip_banknifty = sm.get_next_week_or_monthly_future_scrip_details(exch_type = "D", root = "BANKNIFTY", option_type="CE", current_fut_price= 43200, range_size= 100)
         
# print("next_expiry_fut_scrip_banknifty ", next_expiry_fut_scrip_banknifty)


    def get_nifty_scrip(self):
        df = pd.read_csv(self.csv_path, encoding='utf-8')
        df['Expiry'] = pd.to_datetime(df['Expiry'], format='%Y-%m-%d %H:%M:%S')
        nifty= df[(df['Name']=='NIFTY')]
        nifty_scrip_code = nifty.iloc[0].Scripcode
        return nifty_scrip_code
    
    def get_banknifty_scrip(self):
        df = pd.read_csv(self.csv_path, encoding='utf-8')
        df['Expiry'] = pd.to_datetime(df['Expiry'], format='%Y-%m-%d %H:%M:%S')
        nifty= df[(df['Name']=='BANKNIFTY')]
        banknifty_scrip_code = nifty.iloc[0].Scripcode
        return banknifty_scrip_code
    
    def get_vix_scrip_code(self):
        df = pd.read_csv(self.csv_path, encoding='utf-8')
        # df['Expiry'] = pd.to_datetime(df['Expiry'], format='%Y-%m-%d %H:%M:%S')
        vix_row= df[(df['Name']=='India VIX')]
        india_vix_scrip_code = vix_row.iloc[0].Scripcode
        
        return india_vix_scrip_code
        
        
    
    def get_option_scripcode(self, underlying,option_type, expriy_formated_string, strike_price, ):
                
        formatted_date = expriy_formated_string
        strike_price = strike_price
        underlying = underlying
        option_type = option_type
        formatted_strike_price = "{:.2f}".format(strike_price)

        # Extract year, month, and day from the formatted_date
        year = formatted_date[0:4]
        month = formatted_date[4:6]
        day = formatted_date[6:8]

        # Convert the month number to a corresponding abbreviation
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month_abbrev = months[int(month) - 1]

        # Create the desired string
        output_string = f"{underlying} {day} {month_abbrev} {year} {option_type} {formatted_strike_price}"
        print(output_string)
        df = pd.read_csv(self.csv_path, encoding='utf-8')
        nifty= df[(df['Name']==output_string)]
        option_scrip_code = nifty.iloc[0].Scripcode
        print("option_scrip_code is", option_scrip_code)
        return option_scrip_code