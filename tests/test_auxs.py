from corpusparser.auxs import filename_from_key

def test_filename_from_key():
    assert(filename_from_key("/01") == "data/01.wav")
    assert(filename_from_key("/02", data_folder="audio", ext = ".mp3") == "audio/02.mp3")