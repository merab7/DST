"""
A generic dynamic array implementation

@author William Fiset, william.alexandre.fiset@gmail.com
Python translation
"""

from typing import TypeVar, Generic, Optional, Iterator

T = TypeVar("T")


class DynamicArray(Generic[T]):
    """A generic dynamic array implementation that automatically resizes."""

    def __init__(self, capacity: int = 16):
        """
        Initialize a dynamic array with the given capacity.

        Args:
            capacity: Initial capacity of the array (default: 16)

        Raises:
            ValueError: If capacity is negative
        """
        if capacity < 0:
            raise ValueError(f"Illegal Capacity: {capacity}")

        self._capacity = capacity
        self._len = 0  # length user thinks array is
        self._arr = [None] * capacity  # Actual array

    def size(self) -> int:
        """Return the number of elements in the array."""
        return self._len

    def is_empty(self) -> bool:
        """Check if the array is empty."""
        return self.size() == 0

    def get(self, index: int) -> T:
        """
        Get element at the specified index.

        Args:
            index: Index of the element

        Returns:
            Element at the specified index
        """
        return self._arr[index]

    def set(self, index: int, elem: T) -> None:
        """
        Set element at the specified index.

        Args:
            index: Index where to set the element
            elem: Element to set
        """
        self._arr[index] = elem

    def clear(self) -> None:
        """Clear all elements from the array."""
        for i in range(self._len):
            self._arr[i] = None
        self._len = 0

    def add(self, elem: T) -> None:
        """
        Add an element to the end of the array.

        Args:
            elem: Element to add
        """
        # Time to resize!
        if self._len + 1 >= self._capacity:
            if self._capacity == 0:
                self._capacity = 1
            else:
                self._capacity *= 2  # double the size

            new_arr = [None] * self._capacity
            for i in range(self._len):
                new_arr[i] = self._arr[i]
            self._arr = new_arr  # arr has extra nulls padded

        self._arr[self._len] = elem
        self._len += 1

    def remove_at(self, rm_index: int) -> T:
        """
        Remove an element at the specified index.

        Args:
            rm_index: Index of element to remove

        Returns:
            The removed element

        Raises:
            IndexError: If index is out of bounds
        """
        if rm_index >= self._len or rm_index < 0:
            raise IndexError("Index out of bounds")

        data = self._arr[rm_index]
        new_arr = [None] * (self._len - 1)

        j = 0
        for i in range(self._len):
            if i == rm_index:
                continue  # Skip over rm_index
            new_arr[j] = self._arr[i]
            j += 1

        self._arr = new_arr
        self._len -= 1
        self._capacity = self._len
        return data

    def remove(self, obj: object) -> bool:
        """
        Remove the first occurrence of the specified element.

        Args:
            obj: Element to remove

        Returns:
            True if element was found and removed, False otherwise
        """
        index = self.index_of(obj)
        if index == -1:
            return False
        self.remove_at(index)
        return True

    def index_of(self, obj: object) -> int:
        """
        Find the index of the first occurrence of the specified element.

        Args:
            obj: Element to find

        Returns:
            Index of the element, or -1 if not found
        """
        for i in range(self._len):
            if obj is None:
                if self._arr[i] is None:
                    return i
            else:
                if obj == self._arr[i]:
                    return i
        return -1

    def contains(self, obj: object) -> bool:
        """
        Check if the array contains the specified element.

        Args:
            obj: Element to check

        Returns:
            True if element is in the array, False otherwise
        """
        return self.index_of(obj) != -1

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements in the array."""
        for i in range(self._len):
            yield self._arr[i]

    def __str__(self) -> str:
        """Return a string representation of the array."""
        if self._len == 0:
            return "[]"
        else:
            result = "["
            for i in range(self._len - 1):
                result += str(self._arr[i]) + ", "
            result += str(self._arr[self._len - 1]) + "]"
            return result

    def __repr__(self) -> str:
        """Return a detailed string representation of the array."""
        return f"DynamicArray({self.__str__()})"

    def __len__(self) -> int:
        """Return the number of elements (enables len() function)."""
        return self._len

    def __getitem__(self, index: int) -> T:
        """Enable indexing with [] operator."""
        if index < 0 or index >= self._len:
            raise IndexError("Index out of bounds")
        return self.get(index)

    def __setitem__(self, index: int, value: T) -> None:
        """Enable assignment with [] operator."""
        if index < 0 or index >= self._len:
            raise IndexError("Index out of bounds")
        self.set(index, value)


# Example usage
if __name__ == "__main__":
    # Create a dynamic array
    arr = DynamicArray[int]()

    # Add elements
    for i in range(10):
        arr.add(i)

    print(f"Array: {arr}")
    print(f"Size: {arr.size()}")
    print(f"Element at index 5: {arr.get(5)}")

    # Remove element
    removed = arr.remove_at(3)
    print(f"Removed element: {removed}")
    print(f"Array after removal: {arr}")

    # Check contains
    print(f"Contains 5: {arr.contains(5)}")
    print(f"Contains 100: {arr.contains(100)}")

    # Iterate
    print("Iterating:")
    for elem in arr:
        print(elem, end=" ")
    print()
