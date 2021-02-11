set frequency tx 6G
set samplerate tx 2M
set bandwidth tx 1M
set biastee tx on
tx config file=samples.sc16q11 format=bin repeat=1
set gain tx 56
tx start
