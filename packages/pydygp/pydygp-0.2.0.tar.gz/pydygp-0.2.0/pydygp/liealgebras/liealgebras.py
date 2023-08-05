import numpy as np

class so:

    def __new__(cls, n):
        if isinstance(n, int) and n > 1:

            if n == 2:
                return (np.array([[0.,-1.],
                                  [1., 0.]]),)

            elif n == 3:
                Lx = np.array([[0., 0., 0.],
                               [0., 0.,-1.],
                               [0., 1., 0.]])
                Ly = np.array([[0., 0., 1.],
                               [0., 0., 0.],
                               [-1., 0., 0.]])
                Lz = np.array([[0., -1., 0.],
                               [1., 0., 0.],
                               [0., 0., 0.]])
                return (Lx, Ly, Lz)

            else:
                msg = "Lie algebra so({}) not yet implemented".format(n) 
                raise ValueError(msg)

        else:
            msg = "n must be an integer > 1"
            raise ValueError(msg)

