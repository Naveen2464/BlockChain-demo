"""
================================================================================
COINDEMO BLOCKCHAIN SIMULATION (Python Engine)
Modeled after CoinDemo.io
Topic: Peer-to-Peer Cryptocurrency & Blockchain Demonstration
================================================================================
Features:
  - Peers: Satoshi, Rita, George
  - Mining Reward: 100 Coins per mined block
  - Payments: Recipient, Amount, and Transaction Fee
  - Cryptographic Hashing (SHA-256) & Proof of Work
  - Chain Integrity Validation & Tamper Detection
================================================================================
"""

import hashlib
import time
import datetime


# ==============================================================================
# CLASS 1: BLOCK
# ==============================================================================
class Block:
    def __init__(self, index, name, transactions, previous_hash):
        self.index = index
        self.name = name
        self.timestamp = datetime.datetime.now().strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.transactions = transactions if isinstance(transactions, list) else [transactions]
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def serialize_data(self):
        return " | ".join(str(tx) for tx in self.transactions)

    def calculate_hash(self):
        block_text = (
            str(self.index)
            + str(self.name)
            + str(self.timestamp)
            + self.serialize_data()
            + str(self.previous_hash)
            + str(self.nonce)
        )
        return hashlib.sha256(block_text.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        print(f"\n[Mining {self.name}] Finding hash starting with '{target}'...")

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"[Success] {self.name} mined! Nonce: {self.nonce} | Hash: {self.hash}")


# ==============================================================================
# CLASS 2: COINDEMO BLOCKCHAIN
# ==============================================================================
class CoinDemoBlockchain:
    def __init__(self, difficulty=3):
        self.difficulty = difficulty
        self.peers = {"Satoshi": 0, "Rita": 0, "George": 0}
        self.active_peer = "Satoshi"
        self.unconfirmed_txs = []
        self.peer_chains = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_txs = ["Genesis Root: Initial Distributed Ledger Initialized (Circulating Coins: 0)"]
        genesis = Block(0, "GENESIS BLOCK", genesis_txs, "0" * 64)
        genesis.mine_block(self.difficulty)
        # Each peer maintains their OWN independent node blockchain ledger
        for peer in self.peers:
            b_copy = Block(genesis.index, genesis.name, list(genesis.transactions), genesis.previous_hash)
            b_copy.timestamp = genesis.timestamp
            b_copy.nonce = genesis.nonce
            b_copy.hash = genesis.hash
            self.peer_chains[peer] = [b_copy]

    def get_latest_block(self):
        return self.peer_chains[self.active_peer][-1]

    # 1. Mine New Block (ONLY to active peer's local node chain!)
    def mine_new_block(self):
        # 100 Coinbase Reward to active miner
        self.peers[self.active_peer] += 100
        block_txs = [f"Coinbase Subsidy: 100 COIN -> {self.active_peer}"]

        # Include unconfirmed transactions
        if self.unconfirmed_txs:
            for tx in self.unconfirmed_txs:
                block_txs.append(tx['desc'])
                self.peers[self.active_peer] += tx['fee']  # Miner collects fee
            self.unconfirmed_txs.clear()

        prev_block = self.get_latest_block()
        active_chain = self.peer_chains[self.active_peer]
        new_block = Block(
            len(active_chain),
            f"BLOCK {len(active_chain)}",
            block_txs,
            prev_block.hash
        )
        new_block.mine_block(self.difficulty)
        active_chain.append(new_block)

        print(f"\n>>> Block successfully added to {self.active_peer}'s LOCAL node ledger! <<<")
        print(f"Notice: Peers do NOT connect automatically. Other peers (Rita, George) are desynced until you connect peers!\n")

    # 2. Connect Peers & Sync Ledgers (Manual P2P Consensus)
    def connect_and_sync_peers(self):
        # Find peer with longest valid chain (Nakamoto Consensus)
        longest_peer = max(self.peer_chains, key=lambda p: len(self.peer_chains[p]))
        longest_chain = self.peer_chains[longest_peer]
        max_height = len(longest_chain)

        all_synced = all(len(c) == max_height for c in self.peer_chains.values())
        if all_synced and max_height == 1:
            print("\n[Notice] All peers already in sync at Genesis Block #0! Mine a block first.")
            return
        if all_synced:
            print(f"\n[Notice] All peer nodes are already fully connected and synchronized at Height {max_height}!")
            return

        # Propagate longest chain to all peers
        desynced = [p for p in self.peers if len(self.peer_chains[p]) < max_height]
        for peer in self.peers:
            if peer != longest_peer:
                self.peer_chains[peer] = []
                for b in longest_chain:
                    b_copy = Block(b.index, b.name, list(b.transactions), b.previous_hash)
                    b_copy.timestamp = b.timestamp
                    b_copy.nonce = b.nonce
                    b_copy.hash = b.hash
                    self.peer_chains[peer].append(b_copy)

        print("\n" + "=" * 75)
        print("  [P2P CONSENSUS] NETWORK CONNECTED & SYNCHRONIZED!")
        print("=" * 75)
        print(f"  - Connected Peers : {', '.join(desynced)} connected to {longest_peer}")
        print(f"  - Consensus Rule  : Adopted longest valid Proof-of-Work chain ({max_height} Blocks)")
        print("  - All node ledgers are now synchronized!")
        print("=" * 75 + "\n")

    # 2. Send Payment (Amount + Fee)
    def send_payment(self, recipient, amount, fee):
        total_cost = amount + fee
        if self.peers[self.active_peer] < total_cost:
            print(f"[Error] Insufficient funds! {self.active_peer} only has {self.peers[self.active_peer]} coins.")
            return False

        self.peers[self.active_peer] -= total_cost
        desc = f"{self.active_peer} -> {recipient} : {amount} coins (Fee: {fee})"
        self.unconfirmed_txs.append({
            'sender': self.active_peer,
            'recipient': recipient,
            'amount': amount,
            'fee': fee,
            'desc': desc
        })

        print(f"\n[Payment Queued] {desc}")
        print("Payment is in UNCONFIRMED TRANSACTIONS. Choose Option 1 (Mine New Block) to seal it into the blockchain!\n")
        return True

    # 3. Un-pend / Cancel a Pending Transaction (Refund Sender)
    def unpend_transaction(self, tx_index):
        if not self.unconfirmed_txs:
            print("\n[Notice] No pending transactions to un-pend.")
            return False

        if tx_index < 0 or tx_index >= len(self.unconfirmed_txs):
            print("\n[Error] Invalid transaction index.")
            return False

        tx = self.unconfirmed_txs.pop(tx_index)
        # Refund sender
        refund_amount = tx['amount'] + tx['fee']
        self.peers[tx['sender']] += refund_amount

        print(f"\n[Un-pended] Transaction cancelled: {tx['desc']}")
        print(f"Refunded {refund_amount} COIN back to {tx['sender']}'s balance (Now: {self.peers[tx['sender']]} COIN).\n")
        return True

    # 4. Display Balances & Ledger for Active Peer Node
    def display_all(self):
        max_height = max(len(c) for c in self.peer_chains.values())
        print("\n" + "=" * 75)
        print("                   PEER NODES & INDEPENDENT LEDGERS")
        print("=" * 75)
        for name, bal in self.peers.items():
            mark = " (ACTIVE NODE)" if name == self.active_peer else ""
            chain_len = len(self.peer_chains[name])
            sync_status = "In Sync" if chain_len == max_height else f"DESYNCED ({max_height - chain_len} behind)"
            print(f"  * {name:<10}: {bal} COIN | Ledger: {chain_len} Blocks [{sync_status}]{mark}")

        print(f"\nUnconfirmed Mempool Transactions: {len(self.unconfirmed_txs)} pending")
        for tx in self.unconfirmed_txs:
            print(f"    * {tx['desc']}")

        print("\n" + "=" * 75)
        print(f"       BLOCKCHAIN LEDGER (Local Node: {self.active_peer})")
        print("=" * 75)

        active_chain = self.peer_chains[self.active_peer]
        for i, block in enumerate(active_chain):
            print(f"""
  [ {block.name} ]
  -------------------------------------------------------------------------
  Timestamp     : {block.timestamp}
  Transactions  : {block.serialize_data()}
  Previous Hash : {block.previous_hash}
  Nonce         : {block.nonce}
  Hash (SHA-256): {block.hash}
  -------------------------------------------------------------------------""")
            if i < len(active_chain) - 1:
                print("                                     |")
                print("                           [Cryptographic Link]")
                print("                                     V")

        print("=" * 75 + "\n")

    # 5. Validate Blockchain Integrity on Active Node
    def validate_chain(self):
        print(f"\n[Audit] Verifying cryptographic integrity on {self.active_peer}'s node...\n")
        active_chain = self.peer_chains[self.active_peer]

        for i in range(1, len(active_chain)):
            current = active_chain[i]
            previous = active_chain[i - 1]

            recalculated = current.calculate_hash()
            if current.hash != recalculated:
                print(f"[FAIL] Data altered at {current.name}!")
                print(f"       Stored Hash : {current.hash}")
                print(f"       Actual Hash : {recalculated}")
                print("       Status: TAMPER DETECTED!\n")
                return False

            if current.previous_hash != previous.hash:
                print(f"[FAIL] Broken link at {current.name}!")
                print(f"       Expected Prev Hash : {previous.hash}")
                print(f"       Found Prev Hash    : {current.previous_hash}")
                print("       Status: CHAIN BROKEN!\n")
                return False

            print(f"  -> {current.name}: Hash & Cryptographic Link Verified [OK]")

        print(f"\n[SUCCESS] {self.active_peer}'s Blockchain is 100% VALID and CRYPTOGRAPHICALLY SECURE!\n")
        return True

    # 6. Tamper with Block on Active Node
    def tamper_block(self):
        active_chain = self.peer_chains[self.active_peer]
        if len(active_chain) <= 1:
            print(f"\nPlease mine at least one block on {self.active_peer}'s node before tampering.")
            return

        try:
            print(f"\nAvailable Blocks on {self.active_peer}'s node:")
            for i in range(1, len(active_chain)):
                print(f"  {i}. {active_chain[i].name} ({active_chain[i].serialize_data()})")

            idx = int(input("\nEnter block index to modify: "))
            if idx <= 0 or idx >= len(active_chain):
                print("Invalid block index.")
                return

            print(f"Current Transactions: {active_chain[idx].serialize_data()}")
            fake_tx = input("Enter fraudulent transaction (e.g. Satoshi -> Hacker : 1000 coins): ").strip()
            if not fake_tx:
                fake_tx = "Satoshi -> Hacker : 1000 coins (THEFT)"

            active_chain[idx].transactions = [fake_tx]
            print(f"\n[Tamper Complete] Data in {active_chain[idx].name} altered on {self.active_peer}'s node!")
            print("Run Option 7 (Validate Blockchain) to see the system catch this attack!\n")

        except ValueError:
            print("Please enter a valid number.")


# ==============================================================================
# MAIN MENU
# ==============================================================================
def main():
    demo = CoinDemoBlockchain(difficulty=3)

    while True:
        print("\n" + "=" * 55)
        print(f"     COINDEMO SIMULATOR (Active Peer: {demo.active_peer})")
        print("=" * 55)
        print("  1. ⛏  Mine New Block (100 Coin Reward - Local Node)")
        print("  2. 💸 Send Payment (Amount + Fee)")
        print("  3. ✕  Un-pend / Cancel Pending Transaction (Refund)")
        print("  4. 👤 Switch Active Peer (Satoshi / Rita / George)")
        print("  5. 🔗 Connect Peers & Sync Ledgers (P2P Consensus)")
        print("  6. ⛓  View Blockchain & Balances")
        print("  7. ✓  Validate Blockchain Integrity")
        print("  8. ⚠️  Tamper with a Block (Simulate Hack)")
        print("  9. 🚪 Exit")
        print("=" * 55)

        choice = input("Enter choice (1-9): ").strip()

        # OPTION 1: Mine Block
        if choice == "1":
            demo.mine_new_block()

        # OPTION 2: Send Payment
        elif choice == "2":
            print(f"\n--- SEND PAYMENT FROM {demo.active_peer} (Balance: {demo.peers[demo.active_peer]} COIN) ---")
            recipients = [p for p in demo.peers.keys() if p != demo.active_peer]
            print("Available Recipients:", ", ".join(recipients))
            recipient = input("Enter recipient name: ").strip()

            if recipient not in recipients:
                print("Invalid recipient.")
                continue

            try:
                amt = float(input("Enter amount to send: ").strip() or "0")
                if amt <= 0:
                    print("Amount must be greater than 0.")
                    continue
                fee = float(input("Enter transaction fee (miner reward): ").strip() or "0")
                demo.send_payment(recipient, amt, fee)
            except ValueError:
                print("Invalid numerical amount.")

        # OPTION 3: Un-pend / Cancel Transaction
        elif choice == "3":
            if not demo.unconfirmed_txs:
                print("\n[Notice] No pending transactions in the mempool.")
                continue

            print("\nPending Transactions in Mempool:")
            for idx, tx in enumerate(demo.unconfirmed_txs):
                print(f"  [{idx}] {tx['desc']}")

            try:
                tx_i = int(input("\nEnter transaction number to un-pend (cancel & refund): "))
                demo.unpend_transaction(tx_i)
            except ValueError:
                print("Invalid numerical index.")

        # OPTION 4: Switch Peer
        elif choice == "4":
            print("\nAvailable Peers:", ", ".join(demo.peers.keys()))
            new_peer = input("Switch to peer: ").strip()
            if new_peer in demo.peers:
                demo.active_peer = new_peer
                print(f"[Switched] Active peer is now: {demo.active_peer}")
            else:
                print("Unknown peer.")

        # OPTION 5: Connect Peers & Sync Ledgers
        elif choice == "5":
            demo.connect_and_sync_peers()

        # OPTION 6: View Ledger
        elif choice == "6":
            demo.display_all()

        # OPTION 7: Validate
        elif choice == "7":
            demo.validate_chain()

        # OPTION 8: Tamper
        elif choice == "8":
            demo.tamper_block()

        # OPTION 9: Exit
        elif choice == "9":
            print("\nExiting CryptoPulse Simulator. Thank you!")
            break

        else:
            print("\nInvalid choice. Please enter 1 to 9.")


if __name__ == "__main__":
    main()