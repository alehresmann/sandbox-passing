from bitarray import bitarray
from robot import robot

a = robot(bitarray('000111'), bitarray('100000'), bitarray('111110'))
print(a)
print('swapping')
a.swap()
print(a)
print('rearranging window')
a.rearrange_window()
print(a)
print('taking from sandbox')
a.rearrange_from_sandbox()
print(a)
