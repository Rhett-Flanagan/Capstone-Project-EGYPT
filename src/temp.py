# mu = random.randint(0, 10) + 5
# sigma = random.randint(0, 5) + 5

import math


max = 0
mx = 0
mmu = 0
ms = 0
ma = 0
mb = 0
for mu in range(0, 15):
    for sigma in range(5, 10):
        for x in range (1, 30):
            alpha = (2 * sigma ** 2)
            beta = 1 / (sigma * math.sqrt(2 * math.pi))
            f = 17 * (beta * (math.exp(0 - (x - mu) ** 2 / alpha)))

            if f > max:
                max = f
                mx = x
                mmu = mu
                ms = sigma
                ma = alpha
                mb = beta

print(max)
print(mx, mmu, ms, ma, mb)