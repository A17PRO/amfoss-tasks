## Integer to Roman conversion

- **Question**: Seven different symbols represent Roman numerals with the following values:
```text

Symbol	Value
I	1

V	5

X	10

L	50

C	100

D	500

M	1000

```
Roman numerals are formed by appending the conversions of decimal place values from highest to lowest. Converting a decimal place value into a Roman numeral has the following rules:

If the value does not start with 4 or 9, select the symbol of the maximal value that can be subtracted from the input, append that symbol to the result, subtract its value, and convert the remainder to a Roman numeral.
If the value starts with 4 or 9 use the subtractive form representing one symbol subtracted from the following symbol, for example, 4 is 1 (I) less than 5 (V): IV and 9 is 1 (I) less than 10 (X): IX. Only the following subtractive forms are used: 4 (IV), 9 (IX), 40 (XL), 90 (XC), 400 (CD) and 900 (CM).
Only powers of 10 (I, X, C, M) can be appended consecutively at most 3 times to represent multiples of 10. You cannot append 5 (V), 50 (L), or 500 (D) multiple times. If you need to append a symbol 4 times use the subtractive form.
Given an integer, convert it to a Roman numeral.

- **Language Used**: Python

- **Code**
```text
class Solution(object):
    def intToRoman(self, num):
        thousands = ["", "M", "MM", "MMM"]
        hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
        tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
        ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

        thou_digit = num // 1000
        hund_digit = (num%1000) // 100
        ten_digit = (num%100) // 10
        one_digit = num%10

        result = thousands[thou_digit] + hundreds[hund_digit] + tens[ten_digit] + ones[one_digit]

        return result

```

- **Method of Approach**: Since I didn't know how to loop the code to manually find one and decipher them, I thought if everything were predefined and then we just pull and append the values based on the index, that would work. So I made them into many arrays that I used to pull the value out through the indices of the array since I could get the digits for each place.

<img width="1920" height="1200" alt="Screenshot_20260805_000753" src="https://github.com/user-attachments/assets/605af9e6-097d-4904-82e9-066b1bfd95bc" />
