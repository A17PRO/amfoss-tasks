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
        