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
    Audio: A playable audio object
    """
    subset = subset_audio_from_key(df, key, row, start_time, end_time)

    return Audio(data = subset, rate = samplerate_from_key(key))

def listen_snippet_from_df(df, row):
    """
    Extracts and returns an audio snippet from a DataFrame, provided it has been appended.

    Args:
        df (pandas.DataFrame): The DataFrame containing audio data and corresponding rates.
        row (int): The index of the row from which to extract the audio snippet.
    Returns:
        Audio: A playable audio object
    """

    return Audio(data = df["audio"][row], rate = df["rate"][row])