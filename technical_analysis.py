from typing import Optional
from collections import deque
from statistics import mean, stdev

class MovingAverage:

    def __init__(self, length: int):
        # ma length
        self._length = length

        self._value = 0.0
        self._queue: deque = deque(maxlen=length)

    def queue(self) -> deque:
        return self._queue


class EMA(MovingAverage):
    """
    Exponential Moving Average is calculated first computing the simple moving average for the first
    length entries and afterwards that sma is basis for the upcoming ema value.
    
    for a 5% trend, hence using a factor of 0.05 use a length of 39
    
    """

    def __init__(self, length: int):
        super().__init__(length)

        self.__factor = float(2 / (1 + length))
        self.__ema = 0.0
        self.__ema_reached = False


    def add(self, value: float) -> Optional[float]:
        """
        returns the current ema for the given value if a valid ema does exist, else None
        """
        
        self.__value = value

        # if the threshold for the ema is reached, we can use the factor calculation
        # in addition we use this value now for the queue
        if self.__ema_reached:
            self.__ema = (value * self.__factor) + (self.__ema * (1 - self.__factor))
            self._queue.appendleft(self.__ema)
            return self.__ema 
        # for the first ema value, we have to calculate the sma as a first basis
        else:
            self._queue.appendleft(value)
            if len(self._queue) == self._length:
                self.__ema_reached = True
                self.__ema = mean(self._queue)
            return None
    
    def sigma_delta(self) -> Optional[float]:

        if self.__ema_reached:
            return (self.__value - self.__ema) / stdev(self._queue)
        return None
    
    
class SMA(MovingAverage):
    def __init__(self, length: int):
        super().__init__(length)

        self.__sma = 0.0

    def add(self, value: float) -> float:
        """
        returns the current ema for the given value if a valid ema does exist, else None
        """

        self.__value = value
        self._queue.appendleft(self.__value)
        self.__sma = mean(self._queue)
        
        return self.__sma
    
    def sigma_delta(self) -> Optional[float]:

        if len(self._queue) == self._length:
            return (self.__value - self.__sma) / stdev(self._queue)
        else:
            return None
        