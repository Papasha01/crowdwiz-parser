import requests
import json

def write_to_file(string, filename):
    with open(f'{filename}.txt', 'a+', encoding="utf-8") as f:
        f.write(str(string))

def get_data_coin(list_coin):
    l = '", "'.join(list_coin)
    s = requests.Session()
    data = '{"jsonrpc": "2.0", "method": "get_assets" "params": [["'+l+'"]], "id": 1}'
    response = s.get('https://cwd.global/ws', data=data)
    jsMessage = json.loads(json.dumps(response.json()))

    return jsMessage

def get_data_acc():
    print('Input Account Name: ')
    name = input()

    s = requests.Session()
    data = '{"jsonrpc": "2.0", "method": "get_full_accounts" "params": [["'+name+'"]false], "id": 1}'
    response = s.get('https://cwd.global/ws', data=data)
    jsMessage = json.loads(json.dumps(response.json()))
    print()

    # calculate cashback
    try:
        jscashback = get_data_coin(['1.3.0', f'{jsMessage["result"][0][1]["cashback_balance"]["balance"]["asset_id"]}'])["result"][1]
        amount = float(jsMessage['result'][0][1]['cashback_balance']['balance']['amount'])
        real_amount_cashback = amount / (10** float(jscashback['precision']))
    except:
        real_amount_cashback = 0

    list_asset_type = []
    dict_balance = {}
    if not 'error' in jsMessage:
        for js in jsMessage['result'][0][1]['balances']:
            list_asset_type.append(js['asset_type'])
        jsDataCoin = get_data_coin(list_asset_type)

        i=0
        for js in jsMessage['result'][0][1]['balances']:
            if float(jsDataCoin['result'][i]['precision']) != 0:
                real_balance = (float(js['balance']) / (10**float(jsDataCoin['result'][i]['precision'])))
            else: real_balance = (float(js['balance']))

            dict_balance[jsDataCoin['result'][i]['symbol']] = real_balance
            i+=1
        print('Information:')
        print(f"name account: {jsMessage['result'][0][1]['account']['name']}")
        print(f"referrer name: {jsMessage['result'][0][1]['referrer_name']}")
        print(f'cashback balance: CWD {real_amount_cashback}')
        print(f"had staking: {jsMessage['result'][0][1]['statistics']['had_staking']}")

        if len(dict_balance) == 0:
            print(f'balance: empty wallet')
        else:
            print(f'balance:')
            for key, value in dict_balance.items():
                print("{0}: {1}".format(key,value))
        print()
    else:
        print('input error, try again')

if __name__ == '__main__':
    while True:
        get_data_acc()