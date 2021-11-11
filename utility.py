def convertToMinutes(input):
    arr = input.split(' ')
    arr = list(filter(None, arr))

    if (len(arr) == 2):
        return int(arr[0])
    else:
        return int(arr[0]) * 60 + int(arr[3])