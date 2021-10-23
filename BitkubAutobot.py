#pip install bitkub
#pip install songline

from bitkub import Bitkub
from songline import Sendline
import time

API_KEY = '' #เอาจากในเว็บมาใส่
API_SECRET = '' #เอาจากในเว็บมาใส่

# initial obj only non-secure
bitkub = Bitkub()

# initial obj non-secure and secure
bitkub = Bitkub(api_key=API_KEY, api_secret=API_SECRET)
bitkub.set_api_key(API_KEY)
bitkub.set_api_secret(API_SECRET)

token = '' #ใส่Token line
messenger = Sendline(token)

def rebalance():

  pair = 'THB_KUB' #เหรียญ
  token_name = 'KUB' #เหรียญ

  fix_value =   # ใส่จำนวนเงินที่ต้องการrebalance.
  min_rb =   # Rebalanceขั้นต่ำ

  balance_coin=bitkub.balances()
  balance_coin=balance_coin['result'][token_name]['available'] + balance_coin['result'][token_name]['reserved']
  print('จำนวนเหรียญในบัญชี' , balance_coin , 'เหรียญ')

  balance_thb=bitkub.balances()
  balance_thb=balance_thb['result']['THB']['available'] + balance_thb['result']['THB']['reserved']
  print('จำนวนเงินในบัญชี' , balance_thb , 'บาท')

  last_price = bitkub.ticker(sym = pair)
  last_price = last_price[pair]['last']
  print('ราคาเหรียญล่าสุด' , last_price , 'บาท')

  balance_value = balance_coin*last_price
  print('มูลค่าเหรียญ' ,  balance_value , 'บาท')

  portfolio = balance_thb + balance_value
  #print('มูลค่าพอร์ต' , portfolio , 'บาท')

  # Sell
  if balance_value > fix_value:
      amount = balance_value - fix_value
      if amount > min_rb:  # มูลค่าเพิ่มมากกว่าเท่าไหร่ถึงจะแจ้งเตือน
          print('Sell {:,.2f} baht @ {:,.2f} '.format(amount, last_price))
          sell = int(amount)
          sell = sell / last_price
          # print(sell)
          bitkub.place_ask(sym=pair, amt=sell, rat=last_price, typ='limit')
      else:
          print('Rebalance : Waiting')

  # Buy
  elif balance_value < fix_value:
      amount = fix_value - balance_value
      if amount > min_rb:  # มูลค่าลดมากกว่าเท่าไหร่ถึงจะแจ้งเตือน
          print('Buy {:,.2f} baht @ {:,.2f} '.format(amount, last_price))
          buy = int(amount)
          bitkub.place_bid(sym=pair, amt=buy, rat=last_price, typ='limit')
      else:
          print('Rebalance : Waiting')

  print('-----------------------------------------------')

while True:
      try:
        rebalance()
        time.sleep(10)

      except Exception as e:
        print('Error : {}'.format(str(e)))
        time.sleep(10)