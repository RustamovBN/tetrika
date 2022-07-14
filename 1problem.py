def task(array):
    for index in range(len(array)):
        if int(array[index]) == 0:
            return index
    return 'Не содержит 0'



