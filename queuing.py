import math


def eval_queue(which_queue: str, *, lmda: float, mu: float, sigma2: float, c: int, N: int, K: int):
    if which_queue == 'MG1':
        if lmda >= mu:
            raise ValueError('The arrival rate must be less than the service rate')
        elif lmda <= 0 or mu <= 0:
            raise ValueError('Arrival rate and service rate must be positive')
        elif sigma2 < 0:
            raise ValueError('Variance must be nonnegative')
        else:
            rho = lmda / mu
            l = rho + (rho ** 2 * (1 + sigma2 * mu ** 2)) / 2 / (1 - rho)
            w = l / lmda
            wq = w - 1 / mu
            lq = wq * lmda
            p0 = 1 - rho
            return rho, l, w, wq, lq, p0
    elif which_queue == 'MMc':
        if lmda >= c * mu:
            raise ValueError('The arrival rate must be less than c times the service rate')
        elif lmda <= 0 or mu <= 0:
            raise ValueError('Arrival rate and service rate must be positive')
        elif c < 1:
            raise ValueError('Number of servers must be positive')
        else:
            rho = lmda / mu / c
            offered_load = lmda / mu
            factor = 1
            p0 = 1
            for i in range(1, c):
                factor = factor * offered_load / i
                p0 = p0 + factor
            cfactorial = math.factorial(c)
            p0 = p0 + factor * offered_load / c / (1 - rho)
            p0 = 1 / p0

            rho = rho
            l = offered_load * (offered_load ** (c + 1) * p0) / c / cfactorial / (1 - rho) ** 2
            w = l / lmda
            wq = w - 1 / mu
            lq = wq * lmda
            p0 = p0
    elif which_queue == 'MGc':
        if lmda >= c * mu:
            raise ValueError('The arrival rate must be less than c times the service rate')
        elif lmda <= 0 or mu <= 0:
            raise ValueError('Arrival rate and service rate must be positive')
        elif c < 1:
            raise ValueError('Number of servers must be positive')
        elif sigma2 < 0:
            raise ValueError('Variance must be nonnegative')
        else:
            cv2 = sigma2 * mu ** 2
            rho = lmda / mu / c
            offered_load = lmda / mu
            factor = 1
            p0 = 1
            for i in range(1, c):
                factor = factor * offered_load / i
                p0 = p0 + factor
            cfactorial = math.factorial(c)
            p0 = p0 + factor * offered_load / c / (1 - rho)
            p0 = 1 / p0

            rho = rho
            l = offered_load * (offered_load ** (c + 1) * p0) / c / cfactorial / (1 - rho) ** 2 * (1 + cv2) / 2
            w = l / lmda
            wq = w + 1 / mu
            lq = wq * lmda
    elif which_queue == 'MMcN':
        if lmda == c * mu:
            raise ValueError('This spreadsheet does not handle the case Lambda equal c*Mu')
        elif lmda <= 0 or mu <= 0:
            raise ValueError('Arrival rate and service rate must be positive')
        elif c < 1:
            raise ValueError('Number of servers must be positive')
        elif N < c:
            raise ValueError('Capacity must be at least as large as the number of servers')
        else:
            rho = lmda / mu / c
            offered_load = lmda / mu
            factor = 1
            p0 = 1
            for i in range(1, c):
                factor = factor * offered_load / i
                p0 = p0 + factor
            if c < N:
                rhosum = rho
                if c < N + 1:
                    for i in range(c + 2, N):
                        rhosum += rho ** (i - c)
            cfactorial = math.factorial(c)
            p0 = 1 / p0
            pN = (offered_load ** N / cfactorial / c ** (N - c)) * p0
            lq = p0 * offered_load ** c * rho / cfactorial / (1 - rho) ** 2 * (
                    1 - rho ** (N - c) - (N - c) * rho ** (N - c) * (1 - rho)
            )
            lambda_effective = lmda * (1 - pN)
            wq = lq / lambda_effective
            w = wq + 1 / mu
            l = lambda_effective * w

            rho = lambda_effective / c / mu
            l = l
            w = w
            wq = wq
            lq = lq
            p0 = p0
            pN = pN
            lambda_effective = lambda_effective
    elif which_queue == 'MMcKK':
        if lmda < 0 or mu < 0:
            raise ValueError('Arrival rate and service rate must be positive')
        elif c < 1:
            raise ValueError('Number of servers must be positive')
        elif K < c:
            raise ValueError('Size of calling population must be at least as large as the number of servers')
        else:
            p = [0] * K
            offered_load = lmda / mu
            kfac = math.factorial(K)
            p0 = 1
            if c > 1:
                for i in range(1, c):
                    p[i] = (kfac / math.factorial(i) / math.factorial(K - i)) * offered_load ** i
                    p0 += p[i]
            p0 = 1 / p0
            l = 0
            lq = 0
            lambda_effective = K * lmda * p0
            for i in range(c, K):
                p[i] *= p0
                l += i * p[i]
                lq += max(0, i - c) * p[i]
            w = l / lambda_effective
            wq = lq / lambda_effective
            rho = lambda_effective / c / mu

            rho = rho
            l = l
            w = w
            wq = wq
            lq = lq
            p0 = p0
            lambda_effective = lambda_effective