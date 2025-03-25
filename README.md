## corpusparser
Toolkit for efficiently loading and manipulating our audio files.

### Context
This Python package collects all we learned from [the prototype](https://github.com/elpaco-escience/ffmpeg-test/tree/prototype).

# Tutorial

The heaviest task we want to perform on the input data frame consists on appending audio snippets.
This involves opening a `.wav` file for each row.

Some of these rows points to the same `.wav` file, so we'll make sure the file is opened only once.

## Input dataframe


```python
from pandas import read_csv
```


```python
df = read_csv("tests/test_input.csv")
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>start_time</th>
      <th>end_time</th>
      <th>participant</th>
      <th>utterance</th>
      <th>key</th>
      <th>language</th>
      <th>uid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>629.960</td>
      <td>630.510</td>
      <td>A</td>
      <td>aha</td>
      <td>/german1/5298</td>
      <td>german</td>
      <td>german-059-255-629960</td>
    </tr>
    <tr>
      <th>1</th>
      <td>398.870</td>
      <td>399.330</td>
      <td>A</td>
      <td>aha</td>
      <td>/german1/5298</td>
      <td>german</td>
      <td>german-059-151-398870</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2009.100</td>
      <td>2009.500</td>
      <td>tx@ADUSBS</td>
      <td>aoq</td>
      <td>/sambas1/SBS-20111031</td>
      <td>sambas</td>
      <td>sambas-24-0883-2009100</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1782.890</td>
      <td>1783.400</td>
      <td>tx@JEPSBS</td>
      <td>aoq</td>
      <td>/sambas1/SBS-20111031</td>
      <td>sambas</td>
      <td>sambas-24-0764-1782890</td>
    </tr>
    <tr>
      <th>4</th>
      <td>341.410</td>
      <td>341.830</td>
      <td>B</td>
      <td>mhm</td>
      <td>/german1/4123</td>
      <td>german</td>
      <td>german-008-097-341410</td>
    </tr>
    <tr>
      <th>5</th>
      <td>622.020</td>
      <td>622.370</td>
      <td>A</td>
      <td>ja</td>
      <td>/german1/4123</td>
      <td>german</td>
      <td>german-008-223-622020</td>
    </tr>
    <tr>
      <th>6</th>
      <td>220.343</td>
      <td>220.682</td>
      <td>f37ln</td>
      <td>sí</td>
      <td>/catalan1/ca_f37s_f38s_und</td>
      <td>catalan</td>
      <td>catalan-12-091-220343</td>
    </tr>
    <tr>
      <th>7</th>
      <td>266.974</td>
      <td>267.346</td>
      <td>f37ln</td>
      <td>sí</td>
      <td>/catalan1/ca_f37s_f38s_und</td>
      <td>catalan</td>
      <td>catalan-12-108-266974</td>
    </tr>
    <tr>
      <th>8</th>
      <td>145.130</td>
      <td>145.820</td>
      <td>tx@39</td>
      <td>yeah</td>
      <td>/arapaho1/25b</td>
      <td>arapaho</td>
      <td>arapaho-22-076-145130</td>
    </tr>
    <tr>
      <th>9</th>
      <td>417.900</td>
      <td>418.310</td>
      <td>tx@5</td>
      <td>yeah</td>
      <td>/arapaho1/25b</td>
      <td>arapaho</td>
      <td>arapaho-22-206-417900</td>
    </tr>
    <tr>
      <th>10</th>
      <td>318.486</td>
      <td>318.890</td>
      <td>f02lp</td>
      <td>sí</td>
      <td>/catalan1/ca_f02a_m05a_und</td>
      <td>catalan</td>
      <td>catalan-08-222-318486</td>
    </tr>
    <tr>
      <th>11</th>
      <td>84.358</td>
      <td>84.546</td>
      <td>m05lp</td>
      <td>sí</td>
      <td>/catalan1/ca_f02a_m05a_und</td>
      <td>catalan</td>
      <td>catalan-08-061-84358</td>
    </tr>
    <tr>
      <th>12</th>
      <td>445.980</td>
      <td>446.300</td>
      <td>B</td>
      <td>mhm</td>
      <td>/german1/6297</td>
      <td>german</td>
      <td>german-095-071-445980</td>
    </tr>
    <tr>
      <th>13</th>
      <td>473.030</td>
      <td>473.300</td>
      <td>B</td>
      <td>ja</td>
      <td>/german1/6297</td>
      <td>german</td>
      <td>german-095-085-473030</td>
    </tr>
    <tr>
      <th>14</th>
      <td>86.188</td>
      <td>86.442</td>
      <td>f48ln</td>
      <td>sí?</td>
      <td>/catalan1/ca_m47s_f48s_und</td>
      <td>catalan</td>
      <td>catalan-36-034-86188</td>
    </tr>
    <tr>
      <th>15</th>
      <td>111.308</td>
      <td>111.634</td>
      <td>m47ln</td>
      <td>sí?</td>
      <td>/catalan1/ca_m47s_f48s_und</td>
      <td>catalan</td>
      <td>catalan-36-042-111308</td>
    </tr>
    <tr>
      <th>16</th>
      <td>1924.458</td>
      <td>1924.758</td>
      <td>CLR2_MW_1</td>
      <td>tak</td>
      <td>/polish1/MW_002</td>
      <td>polish</td>
      <td>polish-13-0596-1924458</td>
    </tr>
    <tr>
      <th>17</th>
      <td>1666.742</td>
      <td>1667.249</td>
      <td>CLR2_MW_25</td>
      <td>tak</td>
      <td>/polish1/MW_004</td>
      <td>polish</td>
      <td>polish-15-397-1666742</td>
    </tr>
    <tr>
      <th>18</th>
      <td>515.450</td>
      <td>515.799</td>
      <td>tx@52</td>
      <td>yeah</td>
      <td>/arapaho1/24a</td>
      <td>arapaho</td>
      <td>arapaho-20-216-515450</td>
    </tr>
    <tr>
      <th>19</th>
      <td>127.100</td>
      <td>127.590</td>
      <td>tx@5</td>
      <td>yeah</td>
      <td>/arapaho1/24a</td>
      <td>arapaho</td>
      <td>arapaho-20-060-127100</td>
    </tr>
  </tbody>
</table>
</div>



Please note the times are in seconds.

## Auxiliary functions:
This adapter will help us converting our syntax (using keys) into librosa's syntax (using filenames).


```python
from corpusparser.auxs import filename_from_key
filename_from_key("/catalan1/ca_f02a_m05a_und")
```




    'data/catalan1/ca_f02a_m05a_und.wav'



## Extract audio features


```python
from corpusparser.parsers import *
```

### Example of usage

### Extract all audio


```python
audio_from_key("/catalan1/ca_f02a_m05a_und")
```




    array([-0.00175476, -0.00236511, -0.00218201, ...,  0.        ,
            0.        ,  0.        ], dtype=float32)



### Extract sample rate


```python
samplerate_from_key("/catalan1/ca_f02a_m05a_und")
```




    16000



### Extract an audio snippet


```python
key = "/catalan1/ca_f02a_m05a_und"
df[df["key"] == key].reset_index()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>start_time</th>
      <th>end_time</th>
      <th>participant</th>
      <th>utterance</th>
      <th>key</th>
      <th>language</th>
      <th>uid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10</td>
      <td>318.486</td>
      <td>318.890</td>
      <td>f02lp</td>
      <td>sí</td>
      <td>/catalan1/ca_f02a_m05a_und</td>
      <td>catalan</td>
      <td>catalan-08-222-318486</td>
    </tr>
    <tr>
      <th>1</th>
      <td>11</td>
      <td>84.358</td>
      <td>84.546</td>
      <td>m05lp</td>
      <td>sí</td>
      <td>/catalan1/ca_f02a_m05a_und</td>
      <td>catalan</td>
      <td>catalan-08-061-84358</td>
    </tr>
  </tbody>
</table>
</div>




```python
snippet = subset_audio_from_key(df, key, row=0)
snippet
```




    array([-0.00238037, -0.01153564, -0.00408936, ..., -0.01112366,
           -0.01062012, -0.01023865], dtype=float32)



### Append all audio snippets to dataframe


```python
df = extend_dataframe(df)
```


```python

df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>start_time</th>
      <th>end_time</th>
      <th>participant</th>
      <th>utterance</th>
      <th>key</th>
      <th>language</th>
      <th>uid</th>
      <th>audio</th>
      <th>rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>629.960</td>
      <td>630.510</td>
      <td>A</td>
      <td>aha</td>
      <td>/german1/5298</td>
      <td>german</td>
      <td>german-059-255-629960</td>
      <td>[-0.00012207031, -0.00061035156, -0.0008544922...</td>
      <td>8000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>398.870</td>
      <td>399.330</td>
      <td>A</td>
      <td>aha</td>
      <td>/german1/5298</td>
      <td>german</td>
      <td>german-059-151-398870</td>
      <td>[-0.0009765625, -0.0008544922, -0.0010986328, ...</td>
      <td>8000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2009.100</td>
      <td>2009.500</td>
      <td>tx@ADUSBS</td>
      <td>aoq</td>
      <td>/sambas1/SBS-20111031</td>
      <td>sambas</td>
      <td>sambas-24-0883-2009100</td>
      <td>[0.008453369, 0.008483887, 0.007232666, 0.0072...</td>
      <td>96000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1782.890</td>
      <td>1783.400</td>
      <td>tx@JEPSBS</td>
      <td>aoq</td>
      <td>/sambas1/SBS-20111031</td>
      <td>sambas</td>
      <td>sambas-24-0764-1782890</td>
      <td>[-0.012969971, -0.012939453, -0.011016846, -0....</td>
      <td>96000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>341.410</td>
      <td>341.830</td>
      <td>B</td>
      <td>mhm</td>
      <td>/german1/4123</td>
      <td>german</td>
      <td>german-008-097-341410</td>
      <td>[-0.0020141602, -0.0015869141, -0.0014648438, ...</td>
      <td>8000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>622.020</td>
      <td>622.370</td>
      <td>A</td>
      <td>ja</td>
      <td>/german1/4123</td>
      <td>german</td>
      <td>german-008-223-622020</td>
      <td>[0.00024414062, 0.0, 0.0, -0.00024414062, -0.0...</td>
      <td>8000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>220.343</td>
      <td>220.682</td>
      <td>f37ln</td>
      <td>sí</td>
      <td>/catalan1/ca_f37s_f38s_und</td>
      <td>catalan</td>
      <td>catalan-12-091-220343</td>
      <td>[-0.0016174316, -0.0015258789, -0.0014343262, ...</td>
      <td>16000</td>
    </tr>
    <tr>
      <th>7</th>
      <td>266.974</td>
      <td>267.346</td>
      <td>f37ln</td>
      <td>sí</td>
      <td>/catalan1/ca_f37s_f38s_und</td>
      <td>catalan</td>
      <td>catalan-12-108-266974</td>
      <td>[0.00019836426, -0.00044250488, -0.0014038086,...</td>
      <td>16000</td>
    </tr>
    <tr>
      <th>8</th>
      <td>145.130</td>
      <td>145.820</td>
      <td>tx@39</td>
      <td>yeah</td>
      <td>/arapaho1/25b</td>
      <td>arapaho</td>
      <td>arapaho-22-076-145130</td>
      <td>[0.006210327, 0.0040740967, 0.0043640137, 0.00...</td>
      <td>44100</td>
    </tr>
    <tr>
      <th>9</th>
      <td>417.900</td>
      <td>418.310</td>
      <td>tx@5</td>
      <td>yeah</td>
      <td>/arapaho1/25b</td>
      <td>arapaho</td>
      <td>arapaho-22-206-417900</td>
      <td>[0.023712158, 0.022613525, 0.025222778, 0.0259...</td>
      <td>44100</td>
    </tr>
    <tr>
      <th>10</th>
      <td>318.486</td>
      <td>318.890</td>
      <td>f02lp</td>
      <td>sí</td>
      <td>/catalan1/ca_f02a_m05a_und</td>
      <td>catalan</td>
      <td>catalan-08-222-318486</td>
      <td>[-0.002380371, -0.0115356445, -0.0040893555, 0...</td>
      <td>16000</td>
    </tr>
    <tr>
      <th>11</th>
      <td>84.358</td>
      <td>84.546</td>
      <td>m05lp</td>
      <td>sí</td>
      <td>/catalan1/ca_f02a_m05a_und</td>
      <td>catalan</td>
      <td>catalan-08-061-84358</td>
      <td>[-0.008148193, -0.005874634, 0.009735107, -0.0...</td>
      <td>16000</td>
    </tr>
    <tr>
      <th>12</th>
      <td>445.980</td>
      <td>446.300</td>
      <td>B</td>
      <td>mhm</td>
      <td>/german1/6297</td>
      <td>german</td>
      <td>german-095-071-445980</td>
      <td>[0.0029907227, 0.0010986328, -0.00048828125, -...</td>
      <td>8000</td>
    </tr>
    <tr>
      <th>13</th>
      <td>473.030</td>
      <td>473.300</td>
      <td>B</td>
      <td>ja</td>
      <td>/german1/6297</td>
      <td>german</td>
      <td>german-095-085-473030</td>
      <td>[-0.0079956055, -0.0056762695, 0.0009765625, 0...</td>
      <td>8000</td>
    </tr>
    <tr>
      <th>14</th>
      <td>86.188</td>
      <td>86.442</td>
      <td>f48ln</td>
      <td>sí?</td>
      <td>/catalan1/ca_m47s_f48s_und</td>
      <td>catalan</td>
      <td>catalan-36-034-86188</td>
      <td>[0.0001373291, 0.0004119873, 0.0005493164, 0.0...</td>
      <td>16000</td>
    </tr>
    <tr>
      <th>15</th>
      <td>111.308</td>
      <td>111.634</td>
      <td>m47ln</td>
      <td>sí?</td>
      <td>/catalan1/ca_m47s_f48s_und</td>
      <td>catalan</td>
      <td>catalan-36-042-111308</td>
      <td>[-0.00061035156, -0.00050354004, -0.0004577636...</td>
      <td>16000</td>
    </tr>
    <tr>
      <th>16</th>
      <td>1924.458</td>
      <td>1924.758</td>
      <td>CLR2_MW_1</td>
      <td>tak</td>
      <td>/polish1/MW_002</td>
      <td>polish</td>
      <td>polish-13-0596-1924458</td>
      <td>[-0.00021362305, 0.00018310547, 0.00047302246,...</td>
      <td>48000</td>
    </tr>
    <tr>
      <th>17</th>
      <td>1666.742</td>
      <td>1667.249</td>
      <td>CLR2_MW_25</td>
      <td>tak</td>
      <td>/polish1/MW_004</td>
      <td>polish</td>
      <td>polish-15-397-1666742</td>
      <td>[-0.0043792725, -0.004470825, -0.0042877197, -...</td>
      <td>48000</td>
    </tr>
    <tr>
      <th>18</th>
      <td>515.450</td>
      <td>515.799</td>
      <td>tx@52</td>
      <td>yeah</td>
      <td>/arapaho1/24a</td>
      <td>arapaho</td>
      <td>arapaho-20-216-515450</td>
      <td>[0.015365601, 0.013687134, 0.017715454, 0.0172...</td>
      <td>44100</td>
    </tr>
    <tr>
      <th>19</th>
      <td>127.100</td>
      <td>127.590</td>
      <td>tx@5</td>
      <td>yeah</td>
      <td>/arapaho1/24a</td>
      <td>arapaho</td>
      <td>arapaho-20-060-127100</td>
      <td>[-0.045440674, -0.050338745, -0.045944214, -0....</td>
      <td>44100</td>
    </tr>
  </tbody>
</table>
</div>



## (Optional) Listen to the snippets

### From key


```python
from corpusparser.listeners import *

key = "/catalan1/ca_f02a_m05a_und"
#listen_audio_from_key(df, key = key, row = 0)
```

### From data frame index


```python
#listen_snippet_from_df(df, row = 0)
```
