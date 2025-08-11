import hashlib
import time

def merkle_root(transactions):
    if not transactions:
        return hashlib.sha256("".encode()).hexdigest()
    hashes = [hashlib.sha256(str(tx).encode()).hexdigest() for tx in transactions]
    while len(hashes) > 1:
        temp = []
        for i in range(0, len(hashes), 2):
            left = hashes[i]
            right = hashes[i+1] if i+1 < len(hashes) else left
            temp.append(hashlib.sha256((left + right).encode()).hexdigest())
        hashes = temp
    return hashes[0]

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.previous_hash}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class BlockWithMerkle(Block):
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        self.merkle_root = merkle_root(transactions)
        self.nonce = 0
        super().__init__(index, transactions, previous_hash, timestamp)

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.nonce}{self.merkle_root}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class ProofOfWork:
    def __init__(self, block, difficulty):
        self.block = block
        self.difficulty = difficulty

    def mine(self):
        prefix = '0' * self.difficulty
        nonce = 0
        while True:
            block_string = f"{self.block.index}{self.block.previous_hash}{self.block.timestamp}{nonce}{self.block.merkle_root}"
            hash_result = hashlib.sha256(block_string.encode()).hexdigest()
            if hash_result.startswith(prefix):
                return nonce, hash_result
            nonce += 1

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def add_block(self):
        if not self.pending_transactions:
            print("No transactions to add.")
            return
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            transactions=self.pending_transactions.copy(),
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)
        self.pending_transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def print_chain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Transactions: {block.transactions}")
            print(f"  Hash: {block.hash}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Timestamp: {block.timestamp}")
            print("-" * 30)

class BlockchainWithPoW(Blockchain):
    def __init__(self, difficulty=2):
        super().__init__()
        self.difficulty = difficulty
        self.block_times = []

    def add_block(self):
        if not self.pending_transactions:
            print("No transactions to add.")
            return
        latest_block = self.get_latest_block()
        new_block = BlockWithMerkle(
            index=latest_block.index + 1,
            transactions=self.pending_transactions.copy(),
            previous_hash=latest_block.hash
        )
        pow = ProofOfWork(new_block, self.difficulty)
        start_time = time.time()
        nonce, hash_result = pow.mine()
        end_time = time.time()
        new_block.nonce = nonce
        new_block.hash = hash_result
        self.chain.append(new_block)
        self.pending_transactions = []
        block_time = end_time - start_time
        self.block_times.append(block_time)
        print(f"Blok muvaffaqiyatli yaratildi! Nonce: {nonce}, Hash: {hash_result}")
        print(f"Blokni topish vaqti: {block_time:.2f} soniya")

    def print_block_times(self):
        for i, t in enumerate(self.block_times, 1):
            print(f"{i}-blok: {t:.2f} soniya")
        if self.block_times:
            avg = sum(self.block_times) / len(self.block_times)
            print(f"O'rtacha blok vaqti: {avg:.2f} soniya")

if __name__ == "__main__":
    blockchain = BlockchainWithPoW(difficulty=3)  # Qiyinlikni o'zing sozla (masalan, 2-4 orasida)

    while True:
        print("\n1. Tranzaksiya qo'shish")
        print("2. Yangi blok yaratish (Proof of Work bilan)")
        print("3. Blokcheynni ko'rish")
        print("4. Blokcheyn to'g'riligini tekshirish")
        print("5. Blok yaratish vaqtlarini ko'rish")
        print("6. Chiqish")
        choice = input("Tanlang: ")

        if choice == "1":
            tx = input("Tranzaksiya matnini kiriting: ")
            blockchain.add_transaction(tx)
            print("Tranzaksiya qo'shildi.")
        elif choice == "2":
            blockchain.add_block()
        elif choice == "3":
            blockchain.print_chain()
        elif choice == "4":
            if blockchain.is_chain_valid():
                print("Blokcheyn to'g'ri.")
            else:
                print("Blokcheyn buzilgan!")
        elif choice == "5":
            blockchain.print_block_times()
        elif choice == "6":
            print("Dasturdan chiqildi.")
            break
        else:
            print("Noto'g'ri tanlov.")
