# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os

# Import constants.py and necessary functions from bit and web3
from constants import *
from bit import wif_to_key, PrivateKeyTestnet
from bit.network import NetworkAPI
from web3 import Web3
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware
from eth_account import Account

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("MNEMONIC")
private_key=os.getenv("PRIVATE_KEY")
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
account_one = Account.from_key(private_key)

# Create a function called `derive_wallets`
def derive_wallets(coin):
    command ='php ./derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --format=json --coin="{coin}" --numderive="{numderive}"'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    "ETH": derive_wallets(ETH),
    "BTCTEST": derive_wallets(BTCTEST)
}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTC:
        retrun PrivateKeyTestnet(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(account, recipient, amount):
    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(account, recipient, amount):
    tx = create_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()

# send
send_tx(account_one, "0xf2Aa69925Ef5d26A02586F10f9Ea949D35740C4a",333)