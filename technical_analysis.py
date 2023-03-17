

class EMA():
    """
    Exponential Moving Average is calculated first computing the simple moving average for the first
    length entries and afterwards that sma is basis for the upcoming ema value.
    
    for a 5% trend, hence using a factor of 0.05 use a length of 39
    
    """

    def __init__(self, length: int):
        # ema length
        self._length = length
        self.__counter = 0
        self.__factor = float(2 / (1 + length))
        self._previousEMA = None
        self.__ema_reached = False
        self.__sma_sum = 0

    def add(self, value: float) -> float:
        """
        returns the current ema for the given value if a valid ema does exist, else None
        """
        if self.__ema_reached:
            self._previousEMA = (value * self.__factor) + (self._previousEMA * (1 - self.__factor))
            return self._previousEMA 
        else:
            if self.__counter < self._length:
                self.__sma_sum += value
                self.__counter += 1
            else:
                self._previousEMA = self.__sma_sum / self._length
                self.__ema_reached = True
            return None