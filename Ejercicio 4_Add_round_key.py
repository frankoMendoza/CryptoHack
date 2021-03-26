state = [
	[206, 243, 61, 34],
	[171, 11, 93, 31],
	[16, 200, 91, 108],
	[150, 3, 194, 51],
]

round_key = [
	[173, 129, 68, 82],
	[223, 100, 38, 109],
	[32, 189, 53, 8],
	[253, 48, 187, 78],
]

def bytes2matrix(text):
	""" Converts a 16-byte array into a 4x4 matrix.  """
	return [list(text[i:i+4]) for i in range(0, len(text), 4)]


def add_round_key(s, k):
	S=matrix2bytes(state)
	K=matrix2bytes(round_key)
	return bytes(i^j for i, j in zip(S, K))

def matrix2bytes(matrix):
	return bytes(sum(matrix, []))


print(add_round_key(state, round_key))



