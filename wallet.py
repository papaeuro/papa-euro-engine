# wallet.py — Wallet ETH auto-créé

from eth_account import Account
import json, os
from config import DATA_FILE

def create_or_load_wallet():
    data = _load()
    if "wallet" in data:
        return data["wallet"]
    acc = Account.create()
    wallet = {"address": acc.address, "private_key": acc.key.hex()}
    data["wallet"] = wallet
    _save(data)
    return wallet

def get_address():
    return create_or_load_wallet()["address"]

def _load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}

def _save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
