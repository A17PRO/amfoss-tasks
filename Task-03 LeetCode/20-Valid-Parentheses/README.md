## Find Valid Parenthesis

- **Question**: Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.




- **Language Used**: Python

- **Code**
```text
class Solution(object):
    def isValid(self, s):
        brackets = {
            ")":"(",
            "]":"[",
            "}":"{"
        }

        temp = []

        for i in s:
            if i in brackets:
                first = temp.pop() if temp else '@'
                if first != brackets[i]:
                    return False
            else:
                temp.append(i)
        return not temp
            
```

- **Method of Approach**: So basically I used a dictionary to store the brackets I was using in this code and then started a loop to read 's'. After reading s I check it for a opening or closing bracket in the beginning and if there is an opening bracket the loop repeats to check if it has closed without it being closed by another type of bracket, If so the temp list I made stores a variable '@' and doesn't show empty when I try to return it.
