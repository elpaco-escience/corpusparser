from pandas import read_csv
from corpusparser.parsers import *


def test_samplerate_from_key():
    rate = samplerate_from_key("/public-dutch/dutch-01")
    assert(rate == 24000)

    rate = samplerate_from_key("/public-spanish/spanish-01")
    assert(rate == 16000)

    rate = samplerate_from_key("/public-spanish/spanish-02")
    assert(rate == 16000)

def test_all():
    df = read_csv("tests/test_public.csv")
    df = extend_dataframe(df)

