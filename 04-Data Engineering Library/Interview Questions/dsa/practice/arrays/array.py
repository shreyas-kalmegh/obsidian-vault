class Array:
    # Dynamic array with explicit capacity and logical length.
    def __init__(self):
        self.capacity = 1
        self.length = 0
        self.array = [None] * self.capacity

    def find(self, value):
        for i in range(self.length):
            if self.array[i] == value:
                return i
        raise ValueError("Value not found")

    def get(self, index):
        if not 0 <= index < self.length:
            raise IndexError("Out of bounds")
        return self.array[index]

    def append(self, value):
        if self.length == self.capacity:
            self._resize()
        self.array[self.length] = value
        self.length += 1

    def pop(self):
        if self.length == 0:
            raise IndexError("Array empty")
        last_index = self.length - 1
        value = self.array[last_index]
        self.array[last_index] = None
        self.length -= 1
        return value

    def insert_at(self, index, value):
        if not 0 <= index <= self.length:
            raise IndexError("Out of bounds")
        if self.length == self.capacity:
            self._resize()

        for i in range(self.length, index, -1):
            self.array[i] = self.array[i - 1]
        self.array[index] = value
        self.length += 1

    def remove_at(self, index):
        if not 0 <= index < self.length:
            raise IndexError("Out of bounds")

        removed = self.array[index]
        for i in range(index, self.length - 1):
            self.array[i] = self.array[i + 1]
        self.array[self.length - 1] = None
        self.length -= 1
        return removed

    def _resize(self):
        new_capacity = self.capacity * 2
        new_array = [None] * new_capacity
        for i in range(self.length):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def __len__(self):
        return self.length
