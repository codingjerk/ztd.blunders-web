def getK(Ra, Rb):
    Ka = 32
    Kb = 32

    return Ka, Kb

def calculate(Ra, Rb, success):
    scaling = 400
    Ka, Kb = getK(Ra, Rb)

    Sa = 1 if success else 0
    Sb = 0 if success else 1

    Qa = 10 ** (Ra / 400)
    Qb = 10 ** (Rb / 400)

    Qab = Qa + Qb

    Ea = Qa / Qab
    Eb = Qb / Qab

    Na = Ra + Ka * (Sa - Ea)
    Nb = Rb + Kb * (Sb - Eb)

    print(Na - Ra, Nb - Rb)

    return round(Na), round(Nb)