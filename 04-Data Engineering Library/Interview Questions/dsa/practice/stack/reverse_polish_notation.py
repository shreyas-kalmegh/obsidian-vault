from typing import List
# You are given an array of strings tokens that represents a valid arithmetic expression in Reverse Polish Notation.

# Return the integer that represents the evaluation of the expression.

#     The operands may be integers or the results of other operations.
#     The operators include '+', '-', '*', and '/'.
#     Assume that division between integers always truncates toward zero.

# Example 1:

# Input: tokens = ["1","2","+","3","*","4","-"]

# Output: 5

# Explanation: ((1 + 2) * 3) - 4 = 5

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        s = ("+", "*", "/", "-")
        stack = []

        for c in tokens:
            if c in s:
                v2 = stack.pop()
                v1 = stack.pop()
                match c:
                    case "+": 
                        stack.append(v1 + v2)
                    case "*": 
                        stack.append(v1 * v2)
                    case "-": 
                        stack.append(v1 - v2)
                    case "/": 
                        stack.append(int(v1 / v2))
            else:
                stack.append(int(c))
        return stack[-1]