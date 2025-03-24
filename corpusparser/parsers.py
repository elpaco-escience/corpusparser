import librosa
from math import floor, ceil
from corpusparser.auxs import filename_from_key

def audio_from_key(key, sr = None, **kwargs):
    """ Equivalent to librosa.core.load, but works with keys instead of with filenames """
    audio, rate = librosa.core.load(filename_from_key(key), sr=sr, **kwargs) # sr=None uses the native sampling rate
    audio = audio.astype('float32')
    return audio # We'll ignore the rate in this function output

def samplerate_from_key(key, **kwargs):
    """ Equivalent to librosa.get_samplerate, but works with keys instead of with filenames """
    return librosa.get_samplerate(filename_from_key(key), **kwargs)

def subset_audio(audio, start_time, end_time, rate):
    """
    Extracts a subset of the audio signal between the specified start and end times.
    Args:
        audio (list or numpy array): The audio signal to subset.
        start_time (float): The start time in seconds for the subset.
        end_time (float): The end time in seconds for the subset.
        rate (int): The sampling rate of the audio signal.
    Returns:
        list or numpy array: The subset of the audio signal between start_time and end_time.
    Raises:
        Exception: If the start or end indices are out of the bounds of the audio signal.
    """
    start_i = floor(start_time * rate)
    end_i = ceil(end_time * rate)

    if start_i < 0 or end_i > len(audio):
        raise Exception("Subset out of bounds!")
        
    return audio[start_i : end_i]

def subset_audio_from_key(df, key, row=0, start_time = None, end_time = None):
    """
    Extracts a subset of audio from a given key in the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe containing audio metadata.
    key (str): The key to identify a file in the dataframe.
    row (int, optional): The row index to use if multiple rows match the key. Defaults to 0.
    start_time (float, optional): The start time for the audio subset. If None, it is taken from the dataframe. Defaults to None.
    end_time (float, optional): The end time for the audio subset. If None, it is taken from the dataframe. Defaults to None.

    Returns:
    np.ndarray: The subset of the audio.
    """

    # Get the audio
    sr = samplerate_from_key(key)
    audio = audio_from_key(key, sr)

    # Cut it
    ## First, we filter by key
    subdf = df[df.key == key].reset_index() # So the rows start at 0

    ## Because some keys contain multiple rows, we need the logic below
    if(len(subdf) == 1):
        if start_time == None: # If no time is manually provided, it gets it from the dataframe...
            start_time = subdf['start_time']
        if end_time == None: # ... this is useful for testing and prototyping
            end_time = subdf['end_time']
    else:
        if start_time == None: # If no time is manually provided, it gets it from the dataframe...
            start_time = subdf['start_time'][row]
        if end_time == None: # ... this is useful for testing and prototyping
            end_time = subdf['end_time'][row]

    return subset_audio(audio, start_time, end_time, sr)

# Some handy list comprehensions
def audio_from_keys(keys, **kwargs):
    return [audio_from_key(key, **kwargs) for key in keys]

def samplerate_from_keys(keys, **kwargs):
    return [samplerate_from_key(key, **kwargs) for key in keys]