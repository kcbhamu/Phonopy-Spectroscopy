# SpectroscoPy/IR.py


# ---------
# Docstring
# ---------

""" Core routines for calculating infrared (IR) intensities. """


# ---------
# Functions
# ---------

def CalculateIRIntensity(eigendisplacements, becTensors):
    """
    Calculate the infrared intensity of a mode with eigendisplacements X_j,b from the Born effective-charge tensor Z_j,ab.

    Arguments:
        eigendisplacements -- mode eigendisplacements (N x three-component vectors).
        becTensors -- Born effective-charge tensors (N x 3x3 matrices).
    """

    # This should in principle allow external code to supply the parameters as (correctly-dimensioned) lists.

    eigDim1, eigDim2 = len(eigendisplacements), len(eigendisplacements[0]);

    if eigDim2 != 3:
        raise Exception("Error: eigendisplacements must be a set of N three-component vectors.")

    becDim1, becDim2, becDim3 = len(becTensors), len(becTensors[0]), len(becTensors[0][0]);

    if becDim2 != 3 or becDim3 != 3:
        raise Exception("Error: becTensors must be a set of N 3x3 matrices.");

    if eigDim1 != becDim1:
        raise Exception("Error: The first dimensions of eigendisplacements and becTensors (= the number of atoms) must be the same.");

    # In principle, this could be written more efficiently using e.g. np.einsum.
    # However, this routine is unlikely to be called inside a tight loop, and having the formula laid out clearly makes it a lot more readable.

    irIntensity = 0.0;

    for a in range(0, 3):
        # Sum(a).

        sumTemp1 = 0.0;

        # eigDim1 = becDim1 is the number of atoms.

        for j in range(0, eigDim1):
            # Sum(j).

            sumTemp2 = 0.0;

            for b in range(0, 3):
                # Sum(b) Z_j,ab x X_j,b

                sumTemp2 += becTensors[j][a][b] * eigendisplacements[j][b];

            sumTemp1 += sumTemp2;

        irIntensity += sumTemp1 ** 2;

    return irIntensity;