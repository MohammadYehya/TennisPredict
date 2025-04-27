"""
Just some common methods used in utils
"""
def mean(arr):
    if len(arr) == 0:
        return 0.5
    else:
        total = 0
        for val in arr:
            total += val
        return total/(len(arr))

def getWinnerLoserIDS(p1_id, p2_id, result):
    if result == 1 or result == "1":
        return p1_id, p2_id
    return p2_id, p1_id

if __name__ == '__main__':
    pass