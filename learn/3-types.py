print(10_000_000_000)
print(10000000000)
print(0xa1b2_c3d4)
print(9.01)
print(1.23e9)
print('I\'m \"OK\"!')
print("I'm \"OK\"")
print('I\'m "OK"')
print(r'I\'m "OK"')
print('''
I'm "OK
new line is new world
''')

print(ord('A'))
print(ord('中'))
print(chr(20013))
print(chr(25991))

print('ABC'.encode('ascii'))
print('ABC'.encode('utf-8'))
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))
print(b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore'))

try:
  b'\xe4\xb8\xad\xff'.decode('utf-8')
except UnicodeDecodeError as e:
  print(e)

'''
---这里是注释吗---
'''
print(len('ABC'))
print(len('中文'))

print('Hello, %s' % 'world')
print('Hi, %s, you have $%d.' % ('Michael', 1000000))

# 整数和小数位数，前面补0
print('%04d-%02d' % (3, 1))
print('%.2f' % 3.1415926)
a = 'hell,%s' % 'wld'
print(a)
print('Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125))
r = 2.5
s = 3.14 * r ** 2
print(f'The area of a circle with radius {r} is {s:.2f}')

s1 = 72
s2 = 85
percent = (s1 / s2) * 100
print('%2.1f%%' % percent)
print(f'{percent:2.1f}%')
print(float('0.2'))