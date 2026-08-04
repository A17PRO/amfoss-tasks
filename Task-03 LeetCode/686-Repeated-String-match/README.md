## Find repeated string match

- **Question**: Given two strings a and b, return the minimum number of times you should repeat string a so that string b is a substring of it. If it is impossible for b​​​​​​ to be a substring of a after repeating it, return -1.

Notice: string "abc" repeated 0 times is "", repeated 1 time is "abc" and repeated 2 times is "abcabc".



- **Language Used**: Python

- **Code**
```text
class Solution(object):
    def repeatedStringMatch(self, a, b):
        string = a
        count = 1

        while True:
            if b in string:
                return count
            
            if len(string) > len(a) + len(b):
                return -1

            string += a
            count += 1
            
```

- **Method of Approach**: It was quite easy to solve this question cause i just took the string a and replicated it until it was bigger than b and after that i searched for whether b was in a, cause if the repetion crosses the sum of both strings a and b then there was no chance b was in a. So after that I took the count of the times I had repeated to get length of a greater than b and that was the amount of times b was in a.

<img width="1920" height="1200" alt="Screenshot_20260804_233328" src="https://github.com/user-attachments/assets/838a559b-8501-4faa-b4d1-2d613a72da30" />
