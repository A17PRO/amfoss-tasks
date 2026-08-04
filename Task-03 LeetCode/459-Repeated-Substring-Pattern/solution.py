class Solution(object):
    def repeatedSubstringPattern(self, s):
        repeat = s + s
        repeat_without_ends = repeat[1:-1]
        if s in repeat_without_ends:
            return True
        else:
            return False
        