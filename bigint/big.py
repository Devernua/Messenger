import base64

def pack_bigint(i):
    b = bytearray()
    while i:
        b.append(i & 0xFF)
        i >>= 8
    return b


def unpack_bigint(b):
    b = bytearray(b) # in case you're passing in a bytes/str
    return sum((1 << (bi*8)) * bb for (bi, bb) in enumerate(b))


def base_str_to_int(s):
    return int(s)
    #return unpack_bigint(base64.b64decode(s))



def int_to_base_str(i):
    return str(i)
    #return base64.standard_b64encode(bytes(pack_bigint(i))).decode()
