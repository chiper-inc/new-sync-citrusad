def map_list_int_to_list_str(list_int):
    list_str = []
    for item in list_int:
        list_str.append(str(item))
    return list_str

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
 
    while low <= high:
 
        mid = (high + low) // 2
 
        if arr[mid] < x:
            low = mid + 1
 
        elif arr[mid] > x:
            high = mid - 1
 
        else:
            return mid
 
    return -1

def chunks(xs, n):
    n = max(1, n)
    return list((xs[i:i+n] for i in range(0, len(xs), n)))