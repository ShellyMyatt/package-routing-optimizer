from package import Package

class HashTable:
    def __init__(self, capacity=40):
        self.table = [[] for _ in range(capacity)]
        self.size = 0

    def _hash_function(self, key):
        return key % len(self.table)

    #Self adjusting algorithm this will dynamically resize as items are inserted into the table.
    def resize_self_adjusting(self):
        old_table_size = self.table
        new_capacity = len(self.table) * 2
        self.table = [[] for _ in range(new_capacity)]
        self.size = 0

        for bucket in old_table_size:
            for key, value in bucket:
                self.insert(key, value)

    #Inserts a key_value pair into the hashtable
    def insert(self, package_id, package):
        if not isinstance(package, Package):
            raise ValueError("Value must be a instance of the package class")

        if self.size / len(self.table) > 0.5:
            self.resize_self_adjusting()

        bucket = self._hash_function(package_id)
        for item in self.table[bucket]:
            if item[0] == package_id:
                item[1] = package
                return
        self.table[bucket].append([package_id, package])
        self.size += 1

    #Uses the key to search for a value in the hashtable
    def lookup(self, package_id):
        bucket = self._hash_function(package_id)
        for item in self.table[bucket]:
            if item[0] == package_id:
                return item[1]
        return None

    def get_all_keys(self):
        keys = []
        for bucket in self.table:
            for item in bucket:
                keys.append(item[0])
        return keys

    def __str__(self):
        result = []
        for i, bucket in enumerate(self.table):
            result.append(f"Bucket {i}: {bucket}")
        return "\n".join(result)


