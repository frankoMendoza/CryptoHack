def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return bytes(sum(matrix, []))

matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

#MATRIX=[[201, 192, 129, 248], [39, 154, 88, 57], [38, 13, 48, 24], [39, 60, 54, 24]]
#matrix1=[[222, 188, 97, 44], [218, 107, 83, 65], [215, 51, 31, 187], [46, 235, 225, 137]]
print(matrix2bytes(matrix))
