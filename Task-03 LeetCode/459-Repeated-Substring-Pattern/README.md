## Find repeated substring pattern

- **Question**: Given a string s, check if it can be constructed by taking a substring of it and appending multiple copies of the substring together.

- **Language Used**: Python

- **Code**
```text
class Solution(object):
    def repeatedSubstringPattern(self, s):
        repeat = s + s
        repeat_without_ends = repeat[1:-1]
        if s in repeat_without_ends:
            return True
        else:
            return False
        
```

- **Method of Approach**: The method we did in school always showed us a correct answer if we would add the string with itself again and then take away both the first letter and the last and then check if the original string could be found inside the new string.