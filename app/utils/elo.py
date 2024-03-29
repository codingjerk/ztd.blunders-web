def getK(Ra, Rb): #pylint: disable=unused-argument
    Ka = 32
    Kb = 32

    return Ka, Kb

def calculate(Ra, Rb, success):
    scaling = 400
    Ka, Kb = getK(Ra, Rb)

    Sa = 1 if success else 0
    Sb = 0 if success else 1

    Qa = 10 ** (Ra / scaling)
    Qb = 10 ** (Rb / scaling)

    Qab = Qa + Qb

    Ea = Qa / Qab
    Eb = Qb / Qab

    Na = Ra + Ka * (Sa - Ea)
    Nb = Rb + Kb * (Sb - Eb)

    return round(Na), round(Nb)
