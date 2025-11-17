#!/usr/bin/env python3
"""
Decrypt and save wallet coldkey unencrypted for PM2 usage
⚠️ WARNING: This removes encryption from your coldkey!
Only use this on secure servers where you trust the environment.
"""

import bittensor as bt
import os
import shutil

WALLET_NAME = "droplet"

print("=" * 70)
print("Wallet Decryption Tool")
print("=" * 70)
print(f"\nWallet: {WALLET_NAME}")
print("\n⚠️  WARNING: This will save your coldkey UNENCRYPTED")
print("Only proceed if you understand the security implications!")
proceed = input("\nProceed? (yes/no): ").strip().lower()

if proceed != 'yes':
    print("Aborted.")
    exit(0)

# Initialize wallet
print("\nInitializing wallet...")
wallet = bt.wallet(name=WALLET_NAME)

# Check if coldkey exists
coldkey_path = os.path.expanduser(f"~/.bittensor/wallets/{WALLET_NAME}/coldkey")
if not os.path.exists(coldkey_path):
    print(f"✗ Coldkey not found at {coldkey_path}")
    exit(1)

# Backup the encrypted coldkey
backup_path = coldkey_path + ".encrypted.backup"
print(f"\nBacking up encrypted coldkey to: {backup_path}")
shutil.copy2(coldkey_path, backup_path)
print("✓ Backup created")

# Unlock the coldkey (will prompt for password)
print("\nUnlocking coldkey...")
try:
    wallet.unlock_coldkey()
    print("✓ Coldkey unlocked successfully")
except Exception as e:
    print(f"✗ Failed to unlock: {e}")
    exit(1)

# The coldkey is now loaded in memory
# Get the keypair
coldkeypair = wallet.coldkey

# Save it unencrypted
print(f"\nSaving unencrypted coldkey to: {coldkey_path}")
try:
    # Get the mnemonic from the wallet
    print("\nAttempting to extract mnemonic...")
    
    # Check what attributes are available
    print(f"Keypair type: {type(coldkeypair)}")
    print(f"Available methods: {[m for m in dir(coldkeypair) if not m.startswith('_')][:20]}")
    
    # Try to get private key data
    private_key_hex = None
    mnemonic = None
    
    if hasattr(coldkeypair, 'private_key'):
        private_key_hex = coldkeypair.private_key.hex()
        print(f"✓ Found private_key")
    
    if hasattr(coldkeypair, 'mnemonic'):
        mnemonic = coldkeypair.mnemonic
        print(f"✓ Found mnemonic")
        
    if hasattr(coldkeypair, 'seed_hex'):
        print(f"✓ Found seed_hex")
    
    # Create a simple unencrypted format
    # Just store the hex-encoded private key or mnemonic
    import json
    
    unencrypted_data = {
        "ss58Address": coldkeypair.ss58_address,
        "publicKey": coldkeypair.public_key.hex() if hasattr(coldkeypair, 'public_key') else None,
    }
    
    if mnemonic:
        unencrypted_data["mnemonic"] = mnemonic
    elif private_key_hex:
        unencrypted_data["privateKey"] = private_key_hex
    else:
        raise Exception("Could not extract mnemonic or private key")
    
    # Write as plain JSON
    with open(coldkey_path, 'w') as f:
        json.dump(unencrypted_data, f, indent=2)
    
    os.chmod(coldkey_path, 0o600)
    print("✓ Coldkey saved unencrypted")
    
except Exception as e:
    print(f"✗ Failed to save: {e}")
    import traceback
    traceback.print_exc()
    # Restore backup
    print("\nRestoring backup...")
    shutil.copy2(backup_path, coldkey_path)
    exit(1)

print("\n" + "=" * 70)
print("✓ Wallet decrypted successfully!")
print("=" * 70)
print(f"\nOriginal encrypted coldkey backed up to:")
print(f"  {backup_path}")
print(f"\nYour coldkey is now stored UNENCRYPTED at:")
print(f"  {coldkey_path}")
print("\n⚠️  Keep your server secure!")
print("=" * 70)

