import string
from bs4 import BeautifulSoup
import requests
import sys
import time
import chime


def live_price(stock):
    url = f'https://finance.yahoo.com/quote/{stock}?p={stock}&.tsrc=fin-srch'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    price = soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)').text
    return float(price.replace(',',''))


def _invalid(str):
    print("You have entered an invalid {str}" + "\n" +
              "Press 1 to restart or 0 to quit")
    num = int(input())

    while num != 1 and num != 0:
        print("You have entered an invalid {str}" + "\n" +
              "Press 1 to restart or 0 to quit")
        num = input()

    if num == 1:
        main()
    elif num == 0:
        sys.exit(0)

def checker(bool: bool, curr_price: float, target: float, stock: string):
    p = curr_price
    if bool:
        while p < target:
            time.sleep(5)
            p = live_price(stock)
            
    else:
        while p > target:
            time.sleep(5)
            p = live_price(stock)
    
    chime.success(True)
    chime.success(True)
    print(f"The target price of {target}USD has been reached. Go now!!")
    sys.exit(0)

def main():

    print("\n" + "Welcome, this is a Stock Alarm" + "\n" + "\n" + 
    "Which stock would you like to set an alarm for?")

    stock = str(input("Enter the Stock Ticker here: ")).upper()
    
    try:
        price = live_price(stock)

    except Exception:
        _invalid("Stock Ticker")

    
    print(f"The stock price of {stock} is currently {price}")
    print("\n" +"At what specific price would you like be alerted?")
    target_p = input("Enter the target price here: ")
    try:
        target_p = float(target_p)
    except Exception:
        _invalid("Price")
    
    print("\n" + "\n" + "Got it. You will be alerted with a chime when the target price is reached...")
    if target_p > price:
        checker(True, price, target_p, stock)
    elif target_p < price:
        checker(False, price, target_p, stock)
    else:
        chime.success(True)
        chime.success(True)
        print("The price you targetted is now happening live.")
        sys.exit(0)




if __name__ == "__main__":
    main()