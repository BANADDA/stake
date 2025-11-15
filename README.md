# Bittensor Stake Bot

Simple script to automatically stake and unstake TAO on Bittensor subnets, block-by-block.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script
python3 stake_bot.py
```

The script will prompt you for:
- Wallet name
- Hotkey name
- Validator hotkey address
- Stake amount
- Subnet ID
- Network (test/finney)
- Continuous mode (y/n)
- Wallet password (secure prompt)

## 📋 Requirements

- Python 3.8+
- Bittensor SDK
- Configured Bittensor wallet with TAO balance

## ⚙️ How It Works

The bot automatically:

1. **Connects** to Bittensor network
2. **Unlocks** your wallet (prompts for password)
3. **Stakes** TAO to validator on specified subnet
4. **Waits** for next block (~12 seconds)
5. **Unstakes** TAO from validator
6. **Repeats** if continuous mode is enabled

### Block-by-Block Operation

```
Block N:     Stake 0.001 TAO
  ↓
~12 seconds (wait for next block)
  ↓
Block N+1:   Unstake 0.001 TAO
  ↓
60 seconds (if continuous)
  ↓
Repeat...
```

## 💡 Example Usage

### Single Cycle (Test)

```bash
python3 stake_bot.py

# Prompts:
Enter wallet name: my-wallet
Enter hotkey name: my-hotkey
Enter validator hotkey: 5E2LP6EnZ54m3wS8s1yPvD5c3xo71kQroBw7aUVK32TKeZ5u
Enter stake amount in TAO: 0.001
Enter subnet ID: 1
Enter network: test
Run continuously? (y/n): n
Enter your password: ********
```

### Continuous Mode (Production)

```bash
python3 stake_bot.py

# When prompted, enter 'y' for continuous mode
# The bot will run forever until you press Ctrl+C
```

## 🔍 Finding Validators

Find active validators at:
- **TaoStats:** https://taostats.io/
- **Bittensor Explorer:** https://x.taostats.io/

Make sure the validator is active on your chosen subnet!

## ⚠️ Important Notes

### Minimum Stake Amounts

- **Test network:** 0.001 TAO minimum
- **Finney (mainnet):** Usually 1 TAO minimum (varies by subnet)

If you get `AmountTooLow` error, increase the stake amount.

### Network Selection

- **test:** For testing (recommended first)
- **finney:** Mainnet (real TAO)

### Balance Requirements

Make sure you have enough TAO:
- For staking amount
- Plus transaction fees

Check balance:
```bash
btcli wallet balance --wallet.name [YOUR_WALLET]
```

## 🛑 Stopping the Bot

Press `Ctrl+C` to stop the bot gracefully.

## 🔒 Security

- ✅ Password entered interactively (not stored)
- ✅ Runs in foreground (you see everything)
- ✅ Easy to stop with Ctrl+C

**Best Practices:**
- Always test on test network first
- Use small amounts for testing
- Verify validator addresses
- Never share your password

## 🛠️ Troubleshooting

### "Wrong password"
Make sure you're entering the correct wallet password. Test it first:
```bash
btcli wallet overview --wallet.name [YOUR_WALLET]
```

### "Insufficient balance"
Check your balance:
```bash
btcli wallet balance --wallet.name [YOUR_WALLET]
```

### "AmountTooLow"
Increase the stake amount. Finney mainnet typically requires 1 TAO minimum.

### "Failed to stake/unstake"
- Check validator is active on the subnet
- Verify you have enough balance
- Make sure network is accessible

## 📚 What is Block Time?

Bittensor produces a new block approximately every **12 seconds**. The script:
- Stakes in block N
- Waits ~12 seconds for block N+1
- Unstakes in block N+1

This ensures transactions are confirmed in separate blocks.

## 📄 License

MIT License

## ⚠️ Disclaimer

This software is provided "as is" without warranty. Staking involves financial risk. Always test on test network first. Use at your own risk.

---

**Simple, straightforward, and it works!** 🎯
