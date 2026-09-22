# CryptoPulse Network Lab - Presentation & Viva Guide

> **Activity:** Implementation and Demonstration of Cryptocurrency & Blockchain Operations.  
> **Interface:** **CryptoPulse Network Lab** (Original FinTech UI with Network Wallets, Send Payment Hub, Interactive Mempool with Un-pending, Mining Workbench, and Tamper-Proof Blockchain Ledger).

---

## 1. System Overview: Core Architecture

**CryptoPulse Network Lab** demonstrates how peer-to-peer cryptocurrency systems process and protect transactions:
1. **Network Wallets & Peers:** Accounts (**Satoshi, Rita, George**) with balances. Clicking any wallet activates it and switches to that peer's node ledger.
2. **Independent Peer Node Ledgers (No Automated Sync):**
   - In a true decentralized P2P network, peers maintain **independent copies** of the blockchain ledger.
   - When a peer mines a block, it is added **only to their local node**. Other peers do **not** automatically receive it.
3. **P2P Connection & Consensus Button (`🔗 Connect Peers & Sync Ledgers`):**
   - Manually connects peer nodes over the network.
   - Applies the **Nakamoto Consensus Rule** (nodes adopt the longest valid Proof-of-Work chain).
   - Synchronizes blocks and settles balances across all peers.
4. **Send Payment Hub:** Broadcasts peer-to-peer transfers with custom amounts and miner fees.
5. **Mempool (Pending Pool) & Un-pending:**
   - Broadcasted transactions wait here before confirmation.
   - **How to Un-pend (Cancel):** Click the **`✕ Un-pend`** button on any staged transaction to revoke it and **immediately refund the coins back to the sender**.
   - **How to Mine:** Click **`⛏ Mine`** or **`Mine All Pending Tx`** to package the transactions into the miner's local block.
6. **Mining Workbench:** Miners earn a **100 COIN Coinbase Subsidy** + all transaction fees for solving Proof of Work.
7. **Blockchain Ledger:** Permanent chain of blocks linking via SHA-256 hashes. Allows real-time tamper simulation.

---

## 2. Step-by-Step Classroom Demonstration

### Step 1: Show Network Wallets
- Open `index.html` (or run `python blockchain.py`).
- Show the 3 starting peers: **Satoshi (100 COIN)**, **Rita (50 COIN)**, **George (25 COIN)**.
- Satoshi is the active wallet by default.

### Step 2: Broadcast a Payment to the Mempool
- In the **Send Payment** hub on the left:
  - Recipient: **Rita**
  - Amount: **20**, Miner Fee: **5** (Total: 25 COIN).
  - Click **`📤 Broadcast to Mempool`**.
- Notice: Satoshi's balance updates to **75 COIN** (funds placed into escrow).
- The payment appears in the center **Mempool** as an unconfirmed transaction.

### Step 3: Demonstrate "How to Un-pend a Transaction" (Cancel & Refund)
- Click the **`✕ Un-pend`** button next to the pending transaction in the Mempool.
- **The transaction is instantly removed from the Mempool, and Satoshi's balance is refunded back to 100 COIN!**
- *Explanation to Class:* "In a blockchain mempool, if a transaction has not yet been mined into a block, a user can cancel or replace it, preventing their coins from being locked or spent."

### Step 4: Mine and Confirm into Block #1
- Broadcast the transaction again (20 COIN to Rita).
- Click **`⛏ Mine All Pending Tx (+100 Reward)`**.
- The computer solves Proof of Work (hash starting with `000`).
- **Block #1 is sealed into the Blockchain Ledger** with accurate local timestamp!
- Satoshi collects the 100 COIN reward + 5 fee (balance becomes **180 COIN**), and Rita receives **20 COIN** (balance becomes **70 COIN**).

### Step 5: Real-Time Tamper Simulation
- Scroll down to **Block #1** in the Blockchain Ledger.
- Edit the transaction text box to: `Satoshi -> Hacker : 1000 COIN`.
- **Block #1 turns RED (`✖ CORRUPTED / TAMPERED`)**, and the link arrow turns **`BROKEN (Hash Mismatch)`**!
- This demonstrates the **Avalanche Effect** and mathematical immutability.

---

## 3. Top Viva & Examination Questions

1. **Q: What is the Mempool, and what does "Un-pending" mean?**  
   *A:* The Mempool (Memory Pool) is the temporary staging area where broadcasted transactions wait before miners package them into blocks. "Un-pending" is the ability to cancel or drop an unconfirmed transaction before it gets mined, returning the reserved funds to the sender.

2. **Q: Who receives the transaction fee?**  
   *A:* The miner who successfully solves Proof of Work and includes the transaction in their block receives the fee as an incentive.

3. **Q: What is a Coinbase Subsidy?**  
   *A:* The block reward (here, 100 COIN) minted out of thin air to reward the miner for expending computational power to secure the network.

4. **Q: Why are timestamps important in blocks?**  
   *A:* Timestamps establish chronological order, prevent double spending, and verify that blocks were created sequentially.

5. **Q: Why does changing Block 1 break Block 2?**  
   *A:* Because Block 2 contains Block 1's hash in its `previous_hash` field. Any change in Block 1 changes its hash, breaking the cryptographic link.
