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

        