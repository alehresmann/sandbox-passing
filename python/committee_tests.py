from committee import committee


def test_committee_get():
    # Test 1: with 402 -> binary: 000110010010
    c2 = committee('000000000011', '10')
    #c2.shift(1)
    print(c2.get())
    print(c2.equals(1))
    print(c2.equals(12))
    print(c2.equals(3))

def main():
    test_committee_get()

main()
