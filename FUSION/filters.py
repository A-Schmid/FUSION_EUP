def highpass(value, highpass):
    if(value > highpass):
        return value
    else:
        return highpass

def lowpass(value, lowpass):
    if(value < lowpass):
        return value
    else:
        return lowpass

def bandpass(value, bandpass_low, bandpass_high):
    if(bandpass_low > bandpass_high):
        temp = bandpass_low
        bandpass_low = bandpass_high
        bandpass_high = temp
    if(value < bandpass_low):
        return bandpass_low
    elif(value > bandpass_high):
        return bandpass_high
    else:
        return value
