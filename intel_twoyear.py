from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import os
import pandas as pds
from matplotlib import pyplot as plt

# sample directory: /Users/stephaniezha/Desktop/Coding/Python/WebScrapping
options = webdriver.ChromeOptions()
prefs = {'download.default_directory': '/Users/stephaniezha/Desktop/Coding/Python/WebScrapping'}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)

link = 'https://www.nasdaq.com/market-activity/stocks/intc/historical'

# try:
driver.get(link)
time.sleep(5)
driver.execute_script('window.scrollBy(0,400)')
path1 = '/html/body/div[3]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/div/div/div/button[4]'
path2 = '/html/body/div[3]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/button'
button1 = driver.find_element(By.XPATH, path1)
button2 = driver.find_element(By.XPATH, path2)
button1.click()
time.sleep(5)
button2.click()
time.sleep(5)
driver.close()

file_name = ""

for filename in os.listdir('/Users/stephaniezha/Desktop/Coding/Python/WebScrapping'):
    if filename.startswith("HistoricalData"):
        file_name = filename
        print(file_name)
        
plt.rcParams["figure.figsize"] = [15.00, 3.50]
plt.rcParams["figure.autolayout"] = True
columns = ["Date", "Close/Last", "Open", "High", "Low"]
df = pds.read_csv(file_name, usecols=columns)

for i in range(0, len(df.Date)):
    close = df['Close/Last'][i]
    new_close = close[1:]
    df.loc[i, 'Close/Last'] = new_close

    open1 = df.Open[i]
    new_open = open1[1:]
    df.loc[i, 'Open'] = new_open

    high = df.High[i]
    new_high = high[1:]
    df.loc[i, 'High'] = new_high

    low = df.Low[i]
    new_low = low[1:]
    df.loc[i, 'Low'] = new_low

df.to_csv(file_name, index=False)
df['Close/Last'] = df['Close/Last'].astype('float')
df.Open = df.Open.astype('float')
df.High = df.High.astype('float')
df.Low = df.Low.astype('float')


# print("Contents in csv file: ", df)

color_up = 'red'
color_down = 'green'
width1 = 0.4
width2 = 0.05

for i in range(len(df.Date)-1, -1, -1):
    if df['Close/Last'][i] >= df.Open[i]:
        plt.bar(df.Date[i], abs(df['Close/Last'][i]-df.Open[i]), width1, bottom=min(df.Open[i], df['Close/Last'][i]),
                color=color_up)
        plt.bar(df.Date[i], df.High[i] - df.Low[i], width2, bottom=df.Low[i], color=color_up)

    else:
        plt.bar(df.Date[i], abs(df['Close/Last'][i]-df.Open[i]), width1, bottom=min(df.Open[i], df['Close/Last'][i]),
                color=color_down)
        plt.bar(df.Date[i], df.High[i] - df.Low[i], width2, bottom=df.Low[i], color=color_down)


plt.xlabel("Date")
plt.ylabel("Stock value ($)")
plt.title("Intel NASDAQ Stock - 1 Year")
# plt.legend(['open', 'highest', 'lowest', 'close'])
plt.savefig("intel_stock_year1.jpg", dpi=300)
plt.show()


