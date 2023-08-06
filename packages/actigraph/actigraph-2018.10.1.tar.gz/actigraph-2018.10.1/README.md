# ActiGraph "count" computer #

A library to convert raw accelerometer data to ActiGraph-like "counts".

I created this using https://doi.org/10.1249/MSS.0000000000001344 as a guide.

### Prerequisites ###

`numpy` and `scipy`

### Installation ###

    pip3 install actigraph

### Example ###

    from actigraph import raw_to_counts
    my_sr = <some value in Hz>
    my_data = <array of accelerometer samples>
    counts = raw_to_counts(my_data, my_sr)

### Who do I talk to? ###

* Alex Page, alex.page@rochester.edu
