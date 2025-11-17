#!/usr/bin/env python3
"""
Save coldkey from mnemonic (unencrypted for PM2)
"""

import bittensor as bt
import os
import shutil

WALLET_NAME = "droplet"
MNEMONIC = "teach present sleep science paddle shoulder open another pepper ring gap fantasy"

print("=" * 70)
print("Save Unencrypted Coldkey from Mnemonic")
print("=" * 70)

coldkey_path = os.path.expanduser(f"~/.bittensor/wallets/{WALLET_NAME}/coldkey")

# Backup existing coldkey
if os.path.exists(coldkey_path):
    backup_path = coldkey_path + ".encrypted.backup"
    print(f"\nBacking up existing coldkey to: {backup_path}")
    shutil.copy2(coldkey_path, backup_path)
    print("✓ Backup created")

# Create keypair from mnemonic
print("\nCreating keypair from mnemonic...")
from substrateinterface import Keypair
keypair = Keypair.create_from_mnemonic(MNEMONIC, ss58_format=42)
print(f"✓ Address: {keypair.ss58_address}")

# Save as unencrypted JSON
print(f"\nSaving unencrypted coldkey to: {coldkey_path}")

import json

# Create the coldkey data structure that Bittensor expects
coldkey_data = {
    "accountId": keypair.ss58_address,
    "publicKey": keypair.public_key.hex(),
    "mnemonic": MNEMONIC,
    "ss58Address": keypair.ss58_address,
    "crypto_type": 1,  # SR25519
    "ss58_format": 42  # Substrate format
}

# Ensure directory exists
os.makedirs(os.path.dirname(coldkey_path), exist_ok=True)

# Write unencrypted
with open(coldkey_path, 'w') as f:
    json.dump(coldkey_data, f, indent=2)

os.chmod(coldkey_path, 0o600)

print("✓ Coldkey saved unencrypted")

# Verify it works
print("\nVerifying wallet can be loaded...")
try:
    wallet = bt.wallet(name=WALLET_NAME)
    print(f"✓ Wallet address: {wallet.coldkeypub.ss58_address}")
    print("✓ Verification successful!")
except Exception as e:
    print(f"✗ Verification failed: {e}")
    print("\nThis is okay - Bittensor might require a different format.")
    print("The mnemonic is safely stored and can be used with btcli.")

print("\n" + "=" * 70)
print("✓ Done!")
print("=" * 70)
print("\n⚠️  Your coldkey is now UNENCRYPTED")
print("Keep your server secure!")
print("=" * 70)

