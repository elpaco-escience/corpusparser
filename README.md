## Prototype
Here we tried to simplify and optimize the process of loading and interpreting data.

### Conclusions
1. The bottleneck regarding code speed is loading the `.wav` files.
2. Parallelization, although seemd like [an idea worth trying](https://github.com/elpaco-escience/ffmpeg-test/blob/fdbb6c44c49f10c76237a05579fd6c2e9e265e07/approaches.ipynb) will not help us here (we tried it [here](https://github.com/elpaco-escience/ffmpeg-test/blob/4c30c46af2cf8da82fb205b2c037d3d0d4fa5046/clean.ipynb)).
3. The same `.wav` can appear in multiple rows of the dataframe. Loading it only once is the only way we see to improve the execution time.
