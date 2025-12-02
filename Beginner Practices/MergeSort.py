def mergeSort(arrOrig):
    if (len(arrOrig) <= 1):
        return arrOrig
    mid = len(arrOrig) // 2
    arrayFirst = arrOrig[:mid]
    arraySecond = arrOrig[mid:]

    arrayFirst = mergeSort(arrayFirst)
    arraySecond = mergeSort(arraySecond)

    return merge(arrayFirst, arraySecond)


def merge(arrayFirst, arraySecond):
    arrayBuffer = []
    i = j = 0

    while i < len(arrayFirst) and j < len(arraySecond):
        if arrayFirst[i] <= arraySecond[j]:
            arrayBuffer.append(arrayFirst[i])
            i += 1
        else:
            arrayBuffer.append(arraySecond[j])
            j += 1

    while i < len(arrayFirst):
        arrayBuffer.append(arrayFirst[i])
        i += 1

    while j < len(arraySecond):
        arrayBuffer.append(arraySecond[j])
        j += 1

    return arrayBuffer


def main():
    array = [9, 7, 4, 2, 0, 1, 3, 5, 6, 8]
    sorttedArray = mergeSort(array)
    print(f"Sorted: {sorttedArray}")


main()
