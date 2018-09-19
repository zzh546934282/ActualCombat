def g1(x):
    yield range(x)


def g2(x):
    yield from range(x)


it1 = g1(5)
it2 = g2(5)

print(next(it1))


print(next(it2))
print(next(it2))
print(next(it2))
print(next(it2))
print(next(it2))