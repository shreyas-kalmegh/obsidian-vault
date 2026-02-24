class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        # insert open braces inside the stack
        # if its a close brace we check stack for complementry and pop

        map = {
            "[": "]",
            "{": "}",
            "(": ")"
        }

        for c in s:
            if c in map:
                stack.append(c)
            else:
                if stack and map[stack[-1]] == c:
                    stack.pop()
                else: return False
        
        return False if stack else True

