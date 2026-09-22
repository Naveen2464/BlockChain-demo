# CoinDemo Blockchain Simulation (CryptoPulse Lab)

An interactive, educational Peer-to-Peer (P2P) Cryptocurrency and Blockchain simulation engine inspired by **CoinDemo.io**. It provides both a Python command-line engine (`blockchain.py`) and a visual web demonstration interface (`index.html`).

---

## 📌 Project Overview

This project demonstrates the core cryptographic and distributed-ledger principles that power decentralized cryptocurrencies like Bitcoin:
- **Peer Accounts & Independent Node Ledgers**: Three peers (**Satoshi**, **Rita**, **George**) each maintain their own copy of the blockchain.
- **Proof of Work (PoW) & SHA-256 Mining**: Cryptographic hashing where miners increment a `nonce` to find a hash starting with difficulty target zeros (`000`).
- **Coinbase Block Reward**: 100 newly minted coins awarded to the miner of each block.
- **Mempool (Staging Area)**: Broadcasted transactions wait unconfirmed in the memory pool until packaged into a block.
- **Transaction Cancellation (Un-pending)**: Ability to revoke an unconfirmed transaction from the mempool and refund the reserved balance back to the sender.
- **P2P Nakamoto Consensus**: Nodes resolve divergent ledgers by adopting the longest valid Proof-of-Work chain.
- **Cryptographic Audit & Tamper Detection**: Instant detection of fraudulent data modifications via hash verification and cryptographic link checking (Avalanche effect).

---

## 🚀 How to Run

### 1. Python CLI Simulator
Make sure Python 3.x is installed:
```powershell
python blockchain.py
```

### 2. Web Visualizer
Open `index.html` directly in any web browser:
```powershell
start index.html
```

---

## 📋 Python Simulator Menu & Workflow

The Python engine (`blockchain.py`) features an interactive 9-option menu:

```text
=======================================================
     COINDEMO SIMULATOR (Active Peer: Satoshi)
=======================================================
  1. ⛏  Mine New Block (100 Coin Reward - Local Node)
  2. 💸 Send Payment (Amount + Fee)
  3. ✕  Un-pend / Cancel Pending Transaction (Refund)
  4. 👤 Switch Active Peer (Satoshi / Rita / George)
  5. 🔗 Connect Peers & Sync Ledgers (P2P Consensus)
  6. ⛓  View Blockchain & Balances
  7. ✓  Validate Blockchain Integrity
  8. ⚠️  Tamper with a Block (Simulate Hack)
  9. 🚪 Exit
=======================================================
```

### Option Guide & Flow

| Option | Feature | Description |
|---|---|---|
| **1** | **⛏ Mine New Block** | Solves Proof of Work, mints 100 COIN Coinbase reward to the active peer's local node ledger, and packages any pending mempool transactions (collecting their miner fees). |
| **2** | **💸 Send Payment** | Specifies a recipient, transfer amount, and miner fee. Deducts the cost from sender and places the transfer into the unconfirmed Mempool. |
| **3** | **✕ Un-pend / Cancel** | Cancels a staged transaction from the Mempool before it is mined, immediately refunding the amount and fee back to the sender. |
| **4** | **👤 Switch Active Peer** | Toggles the active node context between **Satoshi**, **Rita**, and **George**. |
| **5** | **🔗 Connect Peers & Sync** | Triggers P2P Nakamoto consensus. Desynchronized peers adopt the longest valid Proof-of-Work blockchain from the network. |
| **6** | **⛓ View Blockchain & Balances** | Displays peer wallet balances, pending mempool transactions, and the local node's blockchain blocks with timestamps, hashes, nonces, and cryptographic links. |
| **7** | **✓ Validate Blockchain** | Audits cryptographic integrity across the chain. Checks SHA-256 hash calculations and verifies `previous_hash` parent block links. |
| **8** | **⚠️ Tamper with a Block** | Simulates a cyberattack by modifying the transaction data of an existing block without recalculating the Proof of Work. |
| **9** | **🚪 Exit** | Exits the simulator application. |

---

## 🧪 Demonstration Scenario (Classroom / Lab Walkthrough)

### Step 1: Initial State & Genesis Block
1. Run `python blockchain.py`.
2. Select **Option 6** to inspect the starting state:
   - Peers start with 0 circulating coins.
   - All 3 peer nodes have **Genesis Block #0** in sync.

### Step 2: Mining the First Coins
1. Select **Option 1** (`Mine New Block`).
2. Satoshi mines **Block 1**, earning a **100 COIN** Coinbase subsidy.
3. Notice: Block 1 is added **only** to Satoshi's local node. Rita and George remain at Block 0 (desynchronized).

### Step 3: Sending a Payment & Mempool Staging
1. Select **Option 2** (`Send Payment`):
   - Recipient: `Rita`
   - Amount: `20`
   - Fee: `5`
2. Satoshi's balance updates to **75 COIN** (25 COIN reserved).
3. The payment is held in the **Mempool** as an unconfirmed transaction.

### Step 4: Testing Un-pending (Cancel & Refund)
1. Select **Option 3** (`Un-pend / Cancel Pending Transaction`).
2. Enter index `0` to cancel the transaction.
3. The transaction is removed from the Mempool, and Satoshi's **25 COIN** is instantly refunded (balance returns to 100 COIN).

### Step 5: Sealing Transactions into a Block
1. Queue the transaction again via **Option 2** (20 COIN to Rita, 5 Fee).
2. Select **Option 1** (`Mine New Block`).
3. Satoshi solves Proof of Work for **Block 2**, packaging the payment. Satoshi collects the 100 COIN reward + 5 COIN fee.

### Step 6: P2P Network Synchronization
1. Select **Option 5** (`Connect Peers & Sync Ledgers`).
2. Rita and George connect to Satoshi and adopt the longest chain (Height: 3 Blocks). All ledgers are now in consensus.

### Step 7: Simulating Data Tampering & Hash Audit
1. Select **Option 8** (`Tamper with a Block`):
   - Block index: `1`
   - Enter fraudulent transaction: `Satoshi -> Hacker : 5000 COIN`
2. Select **Option 7** (`Validate Blockchain Integrity`):
   - The audit recalculates the SHA-256 hash of Block 1.
   - Result: **`[FAIL] Data altered at BLOCK 1! Status: TAMPER DETECTED!`**
   - Cryptographic immutability catches the alteration immediately.

---

## 🧱 Technical Architecture

### Block Structure
Each block contains:
- `index`: Position in the chain (0 for Genesis Block).
- `name`: Human-readable identifier (`BLOCK 1`, `BLOCK 2`).
- `timestamp`: Formatted date and time when the block was mined.
- `transactions`: List of confirmed transaction records.
- `previous_hash`: 64-character SHA-256 hash of the preceding block.
- `nonce`: Arbitrary number adjusted during mining to meet Proof of Work.
- `hash`: SHA-256 digest of `(index + name + timestamp + transactions + previous_hash + nonce)`.

### Proof of Work Algorithm
```python
def mine_block(self, difficulty):
    target = "0" * difficulty
    while not self.hash.startswith(target):
        self.nonce += 1
        self.hash = self.calculate_hash()
```

---
