from IPython.display import Audio
from corpusparser.parsers import subset_audio_from_key, samplerate_from_key

def listen_audio_from_key(df, key, row=0, start_time = None, end_time = None):
    """
    Plays a subset of audio from a given key in the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe containing audio metadata.
    key (str): The key to identify a file in the dataframe.
    row (int, optional): The row index to use if multiple rows match the key. Defaults to 0.
    start_time (float, optional): The start time for the audio subset. If None, it is taken from the dataframe. Defaults to None.
    end_time (float, optional): The end time for the audio subset. If None, it is taken from the dataframe. Defaults to None.

    Returns:
    np.ndarray: The subset of the audio.
    """
    subset = subset_audio_from_key(df, key, row, start_time, end_time)

    return Audio(data = subset, rate = samplerate_from_key(key))