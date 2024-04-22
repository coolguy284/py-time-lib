from enum import Enum

class TimeInstMonotonic():
  # static stuff
  
  TIME_SCALES = Enum('TIME_SCALES', [
    'TT',
    'TAI',
    #'TCG',
    #'TCB',
    #'UT1',
    #'TIME_CENTER_GALAXY',
    #'TIME_COMOVING_FRAME',
  ])
  
  # https://en.wikipedia.org/wiki/Terrestrial_Time
  #TT_OFFSET_FROM_TAI: FixedPrec = FixedPrec('32.184')
  
  # instance stuff
  
  __slots__ = ()
