from collections import defaultdict

# Implement a time-based key-value data structure that supports:

#     Storing multiple values for the same key at specified time stamps
#     Retrieving the key's value at a specified timestamp

# Implement the TimeMap class:

#     TimeMap() Initializes the object.
#     void set(String key, String value, int timestamp) Stores the key key with the value value at the given time timestamp.
#     String get(String key, int timestamp) Returns the most recent value of key if set was previously called on it and the most recent timestamp for that key prev_timestamp is less than or equal to the given timestamp (prev_timestamp <= timestamp). If there are no values, it returns "".

# Note: For all calls to set, the timestamps are in strictly increasing order.

# Example 1:

# Input:
# ["TimeMap", "set", ["alice", "happy", 1], "get", ["alice", 1], "get", ["alice", 2], "set", ["alice", "sad", 3], "get", ["alice", 3]]

# Output:
# [null, null, "happy", "happy", null, "sad"]

# Explanation:
# TimeMap timeMap = new TimeMap();
# timeMap.set("alice", "happy", 1);  // store the key "alice" and value "happy" along with timestamp = 1.
# timeMap.get("alice", 1);           // return "happy"
# timeMap.get("alice", 2);           // return "happy", there is no value stored for timestamp 2, thus we return the value at timestamp 1.
# timeMap.set("alice", "sad", 3);    // store the key "alice" and value "sad" along with timestamp = 3.
# timeMap.get("alice", 3);           // return "sad"

# Constraints:

#     1 <= key.length, value.length <= 100
#     key and value only include lowercase English letters and digits.
#     1 <= timestamp <= 1000


class TimeMap:
    def __init__(self):
        self.map = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.map[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        # Notes:
        # 1) For each key, timestamps are already sorted (strictly increasing set calls).
        # 2) We binary-search for first timestamp > query timestamp (upper bound).
        # 3) Answer is then previous index (left - 1), if it exists.
        values = self.map.get(key, [])
        if not values:
            return ""

        left, right = 0, len(values)

        while left < right:
            mid = left + (right - left) // 2

            if values[mid][0] <= timestamp:
                left = mid + 1
            else:
                right = mid

        idx = left - 1
        if idx < 0:
            return ""
        return values[idx][1]


def run_ops(ops, args):
    obj = None
    out = []

    for op, arg in zip(ops, args):
        if op == "TimeMap":
            obj = TimeMap()
            out.append(None)
        elif op == "set":
            obj.set(*arg)
            out.append(None)
        elif op == "get":
            out.append(obj.get(*arg))
        else:
            raise ValueError(f"Unsupported op: {op}")

    return out


if __name__ == "__main__":
    test_cases = [
        (
            "example_case",
            ["TimeMap", "set", "get", "get", "set", "get"],
            [[], ["alice", "happy", 1], ["alice", 1], ["alice", 2], ["alice", "sad", 3], ["alice", 3]],
            [None, None, "happy", "happy", None, "sad"],
        ),
        (
            "before_first_timestamp",
            ["TimeMap", "set", "get"],
            [[], ["alice", "happy", 5], ["alice", 4]],
            [None, None, ""],
        ),
        (
            "missing_key",
            ["TimeMap", "get"],
            [[], ["bob", 10]],
            [None, ""],
        ),
        (
            "multiple_updates_same_key",
            ["TimeMap", "set", "set", "set", "get", "get", "get", "get"],
            [[], ["a", "x", 1], ["a", "y", 4], ["a", "z", 10], ["a", 1], ["a", 6], ["a", 10], ["a", 100]],
            [None, None, None, None, "x", "y", "z", "z"],
        ),
    ]

    all_passed = True
    for name, ops, args, expected in test_cases:
        got = run_ops(ops, args)
        passed = got == expected
        all_passed = all_passed and passed
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {name}")
        if not passed:
            print(f"  expected={expected}")
            print(f"  got={got}")

    if all_passed:
        print("All test cases passed.")
