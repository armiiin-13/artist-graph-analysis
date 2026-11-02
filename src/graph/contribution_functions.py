def jaccard_index(set1, set2):
    shared = len(set1 & set2)
    union = len(set1 | set2)
    return round(shared / union, 1)

def quantitative_contribution(n, m):
    return abs(n-m)
    
def qualitative_contribution(string1, string2):
    if string1 == string2:
        return 1
    else:
        return 0
    
def set_contribution(set1, set2):
    return len(set1.intersection(set2))
    
def interval_contribution(a,b,c,d): # [a,b] intersects [c,d]
    if a == 0 or b == 0 or c == 0 or d == 0:
        return 0
    else:
        intersect = max(0, min(b, d) - max(a, c) + 1)
        union = max(b,d) - min(a,c) + 1
        return intersect/union