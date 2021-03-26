
N_ROUNDS = 10

key        = b'\xc3,\\\xa6\xb5\x80^\x0c\xdb\x8d\xa5z*\xb6\xfe\\'
ciphertext = b'\xd1O\x14j\xa4+O\xb6\xa1\xc4\x08B)\x8f\x12\xdd'

s_box = b'c|w{\xf2ko\xc50\x01g+\xfe\xd7\xabv\xca\x82\xc9}\xfaYG\xf0\xad\xd4\xa2\xaf\x9c\xa4r\xc0\xb7\xfd\x93&6?\xf7\xcc4\xa5\xe5\xf1q\xd81\x15\x04\xc7#\xc3\x18\x96\x05\x9a\x07\x12\x80\xe2\xeb\'\xb2u\t\x83,\x1a\x1bnZ\xa0R;\xd6\xb3)\xe3/\x84S\xd1\x00\xed \xfc\xb1[j\xcb\xbe9JLX\xcf\xd0\xef\xaa\xfbCM3\x85E\xf9\x02\x7fP<\x9f\xa8Q\xa3@\x8f\x92\x9d8\xf5\xbc\xb6\xda!\x10\xff\xf3\xd2\xcd\x0c\x13\xec_\x97D\x17\xc4\xa7~=d]\x19s`\x81O\xdc"*\x90\x88F\xee\xb8\x14\xde^\x0b\xdb\xe02:\nI\x06$\\\xc2\xd3\xacb\x91\x95\xe4y\xe7\xc87m\x8d\xd5N\xa9lV\xf4\xeaez\xae\x08\xbax%.\x1c\xa6\xb4\xc6\xe8\xddt\x1fK\xbd\x8b\x8ap>\xb5fH\x03\xf6\x0ea5W\xb9\x86\xc1\x1d\x9e\xe1\xf8\x98\x11i\xd9\x8e\x94\x9b\x1e\x87\xe9\xceU(\xdf\x8c\xa1\x89\r\xbf\xe6BhA\x99-\x0f\xb0T\xbb\x16'

inv_s_box = b'R\tj\xd506\xa58\xbf@\xa3\x9e\x81\xf3\xd7\xfb|\xe39\x82\x9b/\xff\x874\x8eCD\xc4\xde\xe9\xcbT{\x942\xa6\xc2#=\xeeL\x95\x0bB\xfa\xc3N\x08.\xa1f(\xd9$\xb2v[\xa2Im\x8b\xd1%r\xf8\xf6d\x86h\x98\x16\xd4\xa4\\\xcc]e\xb6\x92lpHP\xfd\xed\xb9\xda^\x15FW\xa7\x8d\x9d\x84\x90\xd8\xab\x00\x8c\xbc\xd3\n\xf7\xe4X\x05\xb8\xb3E\x06\xd0,\x1e\x8f\xca?\x0f\x02\xc1\xaf\xbd\x03\x01\x13\x8ak:\x91\x11AOg\xdc\xea\x97\xf2\xcf\xce\xf0\xb4\xe6s\x96\xact"\xe7\xad5\x85\xe2\xf97\xe8\x1cu\xdfnG\xf1\x1aq\x1d)\xc5\x89o\xb7b\x0e\xaa\x18\xbe\x1b\xfcV>K\xc6\xd2y \x9a\xdb\xc0\xfex\xcdZ\xf4\x1f\xdd\xa83\x88\x07\xc71\xb1\x12\x10Y\'\x80\xec_`Q\x7f\xa9\x19\xb5J\r-\xe5z\x9f\x93\xc9\x9c\xef\xa0\xe0;M\xae*\xf5\xb0\xc8\xeb\xbb<\x83S\x99a\x17+\x04~\xbaw\xd6&\xe1i\x14cU!\x0c}'

def expand_key(master_key):
    """
    Expands and returns a list of key matrices for the given master_key.
    """
    #s_box = bytes2matrix(s_box1)
    # Round constants https://en.wikipedia.org/wiki/AES_key_schedule#Round_constants
    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )

    # Initialize round keys with raw key material.
    key_columns = bytes2matrix(master_key, 4)
    #print(key_columns)
    iteration_size = len(master_key) // 4


    # Each iteration has exactly as many columns as the key material.
    columns_per_iteration = len(key_columns)
    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 4:
        # Copy previous word.
        word = list(key_columns[-1])

        # Perform schedule_core once every "row".
        if len(key_columns) % iteration_size == 0:
            # Circular shift.
            word.append(word.pop(0))
            # Map to S-BOX.
            word = [s_box[b-1] for b in word]

            # XOR with first byte of R-CON, since the others bytes of R-CON are 0.
            word[0] ^= r_con[i]
            i += 1
        elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
            # Run word through S-box in the fourth iteration when using a
            # 256-bit key.
            word = [s_box[b] for b in word]

        # XOR with equivalent word from previous iteration.
        word = bytes(i^j for i, j in zip(word, key_columns[-iteration_size]))
        key_columns.append(word)

    # Group key words in 4x4 byte matrices.
    return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

def bytes2matrix(text, x):
    return [list(text[i:i+x]) for i in range(0, len(text), x)]

def matrix2bytes(matrix):
    return bytes(sum(matrix, []))


def inv_shift_rows(s):
    Nb = len(s)
    n = [word[:] for word in s]

    for i in range(Nb):
        for j in range(4):
            n[i][j] = s[(i-j) % Nb][j]

    return n

xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

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

def add_round_key(s, k):
    S=matrix2bytes(s)
    K=matrix2bytes(k)
    return bytes(i^j for i, j in zip(S, K))

'''def AddRoundKey(state, key):
    new_state = []
    for i, word in enumerate(state):
        for j, byte in enumerate(word):
            print('state: ',state[i][j])
            print('key: ',key[i][j])
            new_state[-1].append(state[i][j] ^ key[i][j])
    return new_state'''

def inv_sub_bytes(state):

    return [[s_box[byte] for byte in word] for word in state]

def decrypt(key, ciphertext):

    master_key = expand_key(key) # Remember to start from the last round key and work backwards through them when decrypting
    print('Master key: ', master_key)
    index=10

    # Convert ciphertext to state matrix
    state_matrix = bytes2matrix(ciphertext, 4)
    round_keys = Rounds_key_get(master_key ,index)
    state_matrix = add_round_key(state_matrix, round_keys)
    state_matrix = bytes2matrix(state_matrix, 4)

    
    for i in range(N_ROUNDS - 1, 0, -1):
        round_keys = Rounds_key_get(master_key ,index)
        state_matrix=inv_shift_rows(state_matrix)
        state_matrix=inv_sub_bytes(state_matrix)

        state_matrix=add_round_key(state_matrix, round_keys)
        print('AAAA: ', state_matrix)
        state_matrix = bytes2matrix(state_matrix, 4)
        print('ZZZZ: ', state_matrix)
        state_matrix=inv_mix_columns(state_matrix)
        index = index-1
        pass # Do round

    # Run final round (skips the InvMixColumns step)
    print(state_matrix)
    state_matrix=inv_shift_rows(state_matrix)
    state_matrix=inv_sub_bytes(state_matrix)
    state_matrix=add_round_key(state_matrix, round_keys)
    print('STATE: ', state_matrix)
    # Convert state matrix to plaintext
    sub_plaintext = bytes2matrix(state_matrix, 4)
    print('MATRIX: ', sub_plaintext)
    plaintext = matrix2bytes(sub_plaintext)
    #print(plaintext)
    return plaintext


def Rounds_key_get (master_key, point):
    round_key= [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
    key = master_key[point]
    for i in range(4):
        rows = bytes2matrix(key[i], 4)
        print('ROWS: ', rows)
        for j in range(4):
            #print('COLUMNS:  ', rows[0][j])
            round_key[j][i] = rows[0][j]
        #round_key.append(rows[0])
    print(round_key)
    return round_key
print(decrypt(key, ciphertext))
