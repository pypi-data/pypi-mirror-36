# averager
[![GitHub license](https://img.shields.io/github/license/bsoyka/averager.svg)](https://github.com/bsoyka/averager/blob/master/LICENSE)

A simple way to average numbers in Python.
## Averager
`Averager` is the base class of the `averager` module.  To use the `Averager` class, create an instance (no parameters are needed), then use the `average` method to average your numbers.
```python
import averager
instance = averager.Averager
instance.average(1, 5)
# returns 3
```
## WeightedAverager
`WeightedAverager` allows you to set different weights for the numbers you average.  Initalize an instance of the `WeightedAverager` class using keyword arguments to set weights to labels which will be used later on.  A weight with a value of 1 is normal.  Then, once you define an instance, call its `average` method, passing keyword arguments with your labels and values.
```python
import averager
instance = averager.WeightedAverager(a=1, b=2, c=3) # This sets a to be 1x, b to be 2x, and c to be 3x.
instance.average(a=1, c=2) # This passes 1 as a and 2 as c, so 2 has 3x the weight of 1.
# returns 1.75
```
