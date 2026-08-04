## Roman to Integer

- **Question**: Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

I can be placed before V (5) and X (10) to make 4 and 9. 
X can be placed before L (50) and C (100) to make 40 and 90. 
C can be placed before D (500) and M (1000) to make 400 and 900.
Given a roman numeral, convert it to an integer.

- **Language Used**: Python

- **Code**
```text
class Solution(object):
    def romanToInt(self, s):
        roman = {
            'I':1,
            'V':5,
            'X':10,
            'L':50,
            'C':100,
            'D':500,
            'M':1000
        }

        total = 0

        for i in range(len(s)):
            curr_value = roman[s[i]]

            if (i + 1 < len(s)):
                next_value = roman[s[i + 1]]
                if curr_value < next_value:
                    total -= curr_value
                else:
                    total += curr_value
            
            else:
                total += curr_value
            
        return total
            
```

- **Method of Approach**: As soon as I understood what to do I knew I could access the string of roman numerals through an easy for loop and through that i made two if statements to find out if the roman numeral before the next one was smaller and if so we subtract the current numeral and the next numeral and if the current roman numeral was greater than the next we do the normal operation and add both to get the total. The second if was for the default case where we add both to get the total.

<img width="1920" height="1200" alt="Screenshot_20260804_235223" src="https://github.com/user-attachments/assets/d3ae8449-8a89-49d4-a6ba-b0db0a263bab" />
