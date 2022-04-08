class LFSR:

    def __init__(self, nbits, taps, seed):
        """
        Initialize an instance of a linear feedback shift register that generates a
        pseudorandom sequence.

        Arguments
        ---------
        int : nbits
            The number of bits that the LFSR outputs.

        list : taps
            A list containing the taps of the feedback on the LFSR. The least significant
            bit should correspond.

        int : seed
            The seed of the LFSR that starts the random sequence. Should be non-zero, otherwise
            the sequence will always be zero.
        """

        self.__nbits = nbits
        self.__taps = taps

        self.__bits = nbits * [0]
        val = seed

        # Seed the LFSR output
        for i in range(nbits):
            self.__bits[i] = (val & 1)
            val = val >> 1

    def curr(self):
        """
        Returns the current value output by the LFSR.
        """
        out = 0
        for i in range(self.__nbits):
            out |= (self.__bits[i] << i)
        
        return out

    def next(self):
        """
        Gets the next value in the pseudorandom sequence and returns the current
        value.
        """
        self.__update()
        return self.curr()

    def __update(self):
        """
        Updates the current value to the next value in the pseudorandom sequence.
        """
        updated_output = self.__nbits * [0]
        for i in range(self.__nbits):
            if i < self.__nbits - 1:
                updated_output[i] = self.__bits[i + 1]
            else:
                val = 0
                for tap in self.__taps:
                    val ^= (self.__bits[tap])
                updated_output[-1] = val
        
        self.__bits = updated_output
