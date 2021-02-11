set frequency rx 1G
set samplerate rx 2M
set bandwidth rx 1M
rx config file=my_samples_rx.sc16q11 format=bin n=10M
rx start;

set frequency tx 1G
set samplerate tx 2M
set bandwidth tx 1M
set gain tx 30
tx config file=samples.sc16q11 format=bin
tx start

