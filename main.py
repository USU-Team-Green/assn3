import random
from difflib import SequenceMatcher


BLOCK_SIZE = 16 # 16 characters or bytes

def make_hash(s):
    blocks = []
    for index in range(0, len(s), BLOCK_SIZE):
        block = bytes(s[index: min(index + BLOCK_SIZE, len(s))], 'utf-8')
        block_num = 0
        for i in range(len(block)):
            block_num += block[i] * (256 ** i)
        blocks.append(block_num)

    random.seed(0)
    blocks_copy = blocks.copy()
    for i in range(30):
        temp = blocks_copy.copy()
        random.shuffle(temp)
        blocks = blocks + temp
    
    hsh = 0
    for block in blocks:
        temp = hsh
        if hsh > 0:
            hsh = (hsh * block) % (2 ** 128)
        else:
            hsh = block % (2 ** 128)
        hsh = (hsh << 10) & (2 ** 128 - 1)
        hsh = hsh ^ temp

    return hex(hsh)[2:-4]


def test():
    one = 'asdfjkalsdjfklasdjfklsdajfl'
    two = 'jeiocnkonaosjdfkaldjfklejfla'
    three = 'thebrownfoxjumpedovertheredlog'
    four = 'thebrownfaxjumpedovertheredlog'

    assert make_hash(one) == make_hash(one)
    assert make_hash(two) == make_hash(two)
    assert make_hash(three) == make_hash(three)
    assert make_hash(four) == make_hash(four)
    ratio = SequenceMatcher(None, make_hash(three), make_hash(four)).ratio()
    assert ratio < 0.7
