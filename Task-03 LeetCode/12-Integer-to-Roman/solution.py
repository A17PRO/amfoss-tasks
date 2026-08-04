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
