# Constants
## FS = 70.0 
    - Frequency sampling : how many packets arrive per second.
    - why 70? 70 packets per second
    - to convert every packets ber second into times per second : 740 / 70 = 10.04 sec (so 700 packets arrived in 10 sec)
    - This creates the Nyquist limit (70 / 2 = 35) : 70 samples only detect 35Hz. A wave need two sample (up and down)
    - So 35Hz is the highest Hz u can see or recieve.
## BREATH = (0.15, 0.6)
    - Constants(low_val, upper_val)
    - Avg human breathes 9 - 36. so (9 / 60 = 0.15), (36 / 60 = 0.6)
## BODY = (0.6, 5.0)
    - so the body movements ends exactly where the brething ends. so waves touch each other but dosen't overlap
    - And 0.6 Hz to 5.0 Hz is the level body moments form waving and walking
## NOISE = (15.0, 33.0)
    - Nothing in human's body does a thing that release 15hz to 33.0 Hz per second. between these values are nothing but sound or noise from electric devices, outdoor noise etc.

0 Hz      0.15    0.6           5.0            15.0         33.0  35 (Nyquist)
|---------|=======|=============|--------------|============|-----|
           BREATH     BODY         (unused)        NOISE
           still      moving                       reference
           person     person
    
    - The gap from 5–15 Hz is unused, a buffer between "human" and "noise."

## Function init (amplitude, timestamps)

-> Goal : to kill the null values.

### good_thershold = amplitude.std(axis=0) > 1e-9
- .std() - standard deviation root(sum(x1....xn))**2 / n, used to check the null values occured in the packets.
- If null values occured we gonna do that for every line increases time complexity
- .std(axis=0):  where axis=0 calculates std in column wise where (axis=1) calculates in column wise.
- by this we caught the null values by boolean
  
### amp = amplitude[:, good_thershold]
- amplitude[:-> everything, good_thershold -> keep only true values]

## The AGC problem (ESP32 has the (agc) automatic gain control thing)
    - which constantly up's , down's or double's the packets issues is thing not happens for all it happen ina random manner. 
    - This increases the lodness of the sample
## GOAL : Break this lowdness make all the bits same.

### Normalization : Adjusting the signal's amplitude or strength in order to place it in a standard scale

### normalization = amp / amp.mean(axis=1, keepdims=True) : We got the standard values
    - .mean(axis=1) calculate the mean by via row
    - keepdims=True : keep the dimention Standared if its 2*2 then op = 2*2
    - divide every single amp values in the row by mean value.

### t = (timestamp - timestamps[0]) / 1e6 
    - the idea is to calculate this millisecond timestamps in sec time stamps
    - timestamp[0] is where our live started
    - so timestamp - timestamp[0] = we get our updated seconds 5678908 - 5676000 = 8908
    - / 1e6 = 8908 / 1000000 = 0.008

### if len(t) < 100 or t[-1] < 20:
    - to check wheather the len of the timestamp is lesser than 20s.
### raise ValueError(f"capture too short : {len(t)} and {t[-1]}sec")
    - if yes then it raises the ValueError with a statment

## Now what happens if CSI repeated or a jump backwards happen?
simply we can - the next value with past value to check the timestamp increase...

### advance = np.diff(t, prepend[0]]=-1) > 0
    - np.diff(...): check the diff between past and present value
    - prepend[0]-1 : 0th index dosen't have past value its where the time-stamps are getting started, so prepend adds a -1 to 0th
    - t           = [ 0.00,  0.01,  0.02,  0.02,  0.015,  0.03 ]
    - np.diff(t)  = [        0.01,  0.01,  0.00, -0.005,  0.015 ]
    - > 0 : makes boolean if the value greter than 0 true else it return the same timestamp or return past timestamp so false.

### normalization = normalization[advance]
    - now the normalized amplitude values are stored based on the correct timestamps.

## Resampling 
    - packets dont arrive at even timeline so we need even that
  
### grid = np.arange(t[0], t[-1], 1 / FS)
    - np.arange(start, stop, step) : gives a list of values that occures from the range of given i/p.
    - 1/FS : 1 / 70 = 0.0142s between every values

now we go the correct time-line now we need resampled data

### even = np.empty(len(grid), normalization.shape[1])
    - np.empty(rows:, cols:) : created a empty list

adding the values with respected time-frame
### for 
