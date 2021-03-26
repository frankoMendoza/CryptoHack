def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]
    
    return s

# learned from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def matrix2bytes(matrix):
    return bytes(sum(matrix, []))

def mix_single_column(a):
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)
    return a

def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])

    return s

def inv_shift_rows(s):
    s_len = len(s)
    n = [word[:] for word in s]

    for i in range(s_len):
        for j in range(4):
            #print(n[i][j])
            #print(s[(i-j) % Nb][j])
            n[i][j] = s[(i-j) % s_len][j]

    return n


def inv_mix_columns(s):
    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v
    mix_columns(s)
    return s

def sub_bytes(state, sbox):
    sub_matrix = []
    for state_row in range(len(state)):
        sub_row = []
        for state_col in range(len(state[state_row])):
            val = hex(state[state_row][state_col])
            s_row, s_col = int(val[2], 16), int(val[3], 16)
            sbox_val = sbox[16 * s_row + s_col]
            sub_row.append(sbox_val)
        sub_matrix.append(sub_row)
    return sub_matrix

state = [
    [108, 106, 71, 86],
    [96, 62, 38, 72],
    [42, 184, 92, 209],
    [94, 79, 8, 54],
]


#state_final = shift_rows(state)
state_final = inv_mix_columns(state)
state_final1 = matrix2bytes(state_final)
print(state_final1)
state_final = inv_shift_rows(state_final)
byte = matrix2bytes(state_final)

print(byte)
