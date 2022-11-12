from web3 import Web3
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import json
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.8.7")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.7",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#now we will get our ABI and bytecode from json file by walking down all the brackets in the given manner:-

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# Connecting with ganache using the details given below. In metamask, the httpprovider and address were of our metamask, in this case, we will use virtual environment of ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chainId = 1337
my_virt_address = w3.eth.accounts[0]
private_key = os.getenv("pvt_key")  #Add 0x at start of private key while copy-pasting since python takes these values in hexadecimals
nonce = w3.eth.getTransactionCount(my_virt_address)

#creating a contract in python
simpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

transaction = simpleStorage.constructor().build_transaction(
    {
        "chainId" : chainId,
        "nonce" : nonce,
        "from" : my_virt_address,
        "gasPrice" : w3.eth.gas_price,
    }
)

sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)
w3.eth.default_address = my_virt_address
newStorage = w3.eth.contract(
    address = tx_reciept.contractAddress,
    abi=abi
)
print(newStorage.functions.store(15))
print(newStorage.functions.retrieve().call())