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
