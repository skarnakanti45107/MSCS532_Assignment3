import random

class HashTable:
    def __init__(self, initial_capacity=8):
        """Initializes the hash table with empty chains (lists) and universal hash parameters."""
        self.capacity = initial_capacity
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]
        
        # Universal Hashing Parameters
        # Formula: h(k) = ((a*k + b) mod p) mod m
        self.p = 10**9 + 7  # A large prime number (p > m)
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

    def _hash(self, key):
        """
        Computes the hash value using a universal hash function family.
        Converts strings to integers first if necessary.
        """
        k = hash(key) if isinstance(key, str) else key
        return ((self.a * k + self.b) % self.p) % self.capacity

    def insert(self, key, value):
        """Adds a key-value pair to the hash table."""
        # Check load factor and resize if necessary (threshold = 0.75)
        if self.size / self.capacity >= 0.75:
            self._resize(self.capacity * 2)

        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]

        # Check if the key already exists; if so, update the value
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # If key doesn't exist, append it to the chain (collision resolution)
        bucket.append((key, value))
        self.size += 1

    def search(self, key):
        """Retrieves a value associated with a given key."""
        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]

        for k, v in bucket:
            if k == key:
                return v  # Key found
        
        return None  # Key not found

    def delete(self, key):
        """Removes a key-value pair from the hash table."""
        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                
                # Shrink table if load factor drops below 0.25 (optional, but good practice)
                if self.size > 0 and self.size / self.capacity <= 0.25:
                    self._resize(max(8, self.capacity // 2))
                return True # Successfully deleted
                
        return False # Key not found

    def _resize(self, new_capacity):
        """Dynamically resizes the hash table and rehashes all elements."""
        old_table = self.table
        self.capacity = new_capacity
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]
        
        # Generate new universal hashing parameters for the new capacity
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

        # Rehash all existing elements into the new table
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)


# ==========================================
# TEST SCRIPT TO DEMONSTRATE FUNCTIONALITY
# ==========================================
if __name__ == "__main__":
    ht = HashTable(initial_capacity=4)
    
    print("1. Inserting values...")
    ht.insert("student_1", "Alice")
    ht.insert("student_2", "Bob")
    ht.insert("student_3", "Charlie")
    ht.insert("student_4", "David")
    ht.insert("student_5", "Eve") # This will trigger a dynamic resize
    
    print(f"Current Size: {ht.size}, Current Capacity: {ht.capacity}")
    
    print("\n2. Searching for values...")
    print(f"Search 'student_3': {ht.search('student_3')}")
    print(f"Search 'student_99': {ht.search('student_99')}")
    
    print("\n3. Deleting values...")
    ht.delete("student_2")
    print(f"Search 'student_2' after deletion: {ht.search('student_2')}")
    print(f"Current Size after deletion: {ht.size}")