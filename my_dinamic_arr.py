from typing import TypeVar, Generic, Optional, Iterator, List, Any

T = TypeVar("T")


class MerabsDinamicArr(Generic[T]):  # Use square brackets, not parentheses
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.len = 0
        self.arr: List[Optional[T]] = [
            None
        ] * capacity  # Create list, not multiply None

    def size(self) -> int:
        return self.len

    def is_empty(self) -> bool:
        return self.len == 0

    def get(self, index: int) -> Optional[T]:
        if index < 0 or index >= self.len:  # Check bounds properly
            raise IndexError(f"Index: {index} is out of range")
        return self.arr[index]

    def set_at(self, index: int, value: T):  # Fixed typo: sett_at -> set_at
        if index < 0 or index >= self.len:
            raise IndexError(f"index: {index} out of range")
        self.arr[index] = value
        # Don't increment len or resize - we're replacing, not adding

    def add(self, value: T):
        self._resize()
        self.arr[self.len] = value
        self.len += 1

    def remove(self, value: T) -> bool:
        index = self.index_of(value)
        if index != -1:
            self.remove_at(index)
            return True
        return False

    def remove_at(self, index: int):
        if index < 0 or index >= self.len:
            raise IndexError(f"index: {index} is out of range")

        # Shift elements left to fill the gap
        for i in range(index, self.len - 1):
            self.arr[i] = self.arr[i + 1]

        self.arr[self.len - 1] = None  # Clear last element
        self.len -= 1

    def index_of(self, value: T) -> int:
        for i in range(self.len):  # Only search up to len, not capacity
            if self.arr[i] == value:
                return i
        return -1

    def contains(self, value: T) -> bool:
        return self.index_of(value) != -1

    def _resize(self):
        if self.len >= self.capacity:  # Resize when full
            self.capacity *= 2
            new_arr: List[Optional[T]] = [None] * self.capacity
            for i in range(self.len):
                new_arr[i] = self.arr[i]
            self.arr = new_arr

    def __iter__(self) -> Iterator[T]:
        for i in range(self.len):  # Fixed: self._len -> self.len
            if self.arr[i] is not None:
                yield self.arr[i]  # Fixed: self._arr -> self.arr

    def __str__(self) -> str:
        if self.len == 0:  # Fixed: self._len -> self.len
            return "[]"
        result = "["
        for i in range(self.len - 1):
            result += str(self.arr[i]) + ", "  # Fixed: self._arr -> self.arr
        result += str(self.arr[self.len - 1]) + "]"
        return result


# Test suite for MerabsDinamicArr
if __name__ == "__main__":
    print("=== Testing MerabsDinamicArr ===\n")

    # Create a dynamic array
    arr = MerabsDinamicArr[int]()

    print("1. Testing add() method:")
    for i in range(10):
        arr.add(i)
    print(f"   Array: {arr}")
    print(f"   Size: {arr.size()}")
    print(f"   Is empty: {arr.is_empty()}")
    print(f"   Capacity: {arr.capacity}\n")

    print("2. Testing get() method:")
    print(f"   Element at index 5: {arr.get(5)}")
    print(f"   Element at index 0: {arr.get(0)}")
    print(f"   Element at index 9: {arr.get(9)}")
    try:
        arr.get(15)
    except IndexError as e:
        print(f"   Out of bounds access: {e}\n")

    print("3. Testing set_at() method:")
    arr.set_at(5, 999)
    print(f"   Set index 5 to 999: {arr}")
    print(f"   Element at index 5: {arr.get(5)}\n")

    print("4. Testing remove_at() method:")
    print(f"   Before removal: {arr}")
    arr.remove_at(3)
    print(f"   After removing index 3: {arr}")
    print(f"   Size after removal: {arr.size()}\n")

    print("5. Testing contains() method:")
    print(f"   Contains 999: {arr.contains(999)}")
    print(f"   Contains 5: {arr.contains(5)}")
    print(f"   Contains 100: {arr.contains(100)}")
    print(f"   Contains 3 (removed): {arr.contains(3)}\n")

    print("6. Testing index_of() method:")
    print(f"   Index of 999: {arr.index_of(999)}")
    print(f"   Index of 0: {arr.index_of(0)}")
    print(f"   Index of 100 (not present): {arr.index_of(100)}\n")

    print("7. Testing remove() method:")
    print(f"   Before removing value 7: {arr}")
    result = arr.remove(7)
    print(f"   After removing value 7: {arr}")
    print(f"   Remove result: {result}")
    result = arr.remove(999)
    print(f"   After removing value 999: {arr}")
    print(f"   Size: {arr.size()}\n")

    print("8. Testing iteration:")
    print("   Iterating through array:")
    for elem in arr:
        print(f"   {elem}", end=" ")
    print("\n")

    print("9. Testing with strings:")
    str_arr = MerabsDinamicArr[str]()
    words = ["hello", "world", "dynamic", "array", "test"]
    for word in words:
        str_arr.add(word)
    print(f"   String array: {str_arr}")
    print(f"   Contains 'world': {str_arr.contains('world')}")
    str_arr.remove("dynamic")
    print(f"   After removing 'dynamic': {str_arr}\n")

    print("10. Testing edge cases:")
    empty_arr = MerabsDinamicArr[int]()
    print(f"   Empty array: {empty_arr}")
    print(f"   Is empty: {empty_arr.is_empty()}")
    print(f"   Size: {empty_arr.size()}")

    # Add one element
    empty_arr.add(42)
    print(f"   After adding 42: {empty_arr}")
    print(f"   Is empty: {empty_arr.is_empty()}")

    # Remove it
    empty_arr.remove_at(0)
    print(f"   After removing: {empty_arr}")
    print(f"   Is empty: {empty_arr.is_empty()}\n")

    print("11. Testing capacity growth:")
    growth_arr = MerabsDinamicArr[int](capacity=2)
    print(f"   Initial capacity: {growth_arr.capacity}")
    for i in range(10):
        growth_arr.add(i)
        if i in [1, 3, 7]:  # Check capacity at certain points
            print(f"   After adding {i+1} elements, capacity: {growth_arr.capacity}")
    print(f"   Final array: {growth_arr}")
    print(f"   Final capacity: {growth_arr.capacity}")
    print(f"   Final size: {growth_arr.size()}\n")

    print("=== All tests completed! ===")
