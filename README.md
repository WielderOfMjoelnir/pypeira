# pypeira
A data reduction pipeline for space-based infrared observations.

### Description
My attempt at reducing images from the SSC into ultra high-precision time-resolved photometry.

### Dependencies
* numpy >= 1.10.4
* matplotlib >= 
* fitsio >= 0.9.7

### Usage

<pre><code>
import pypeira.pypeira as p

# Create instance of IRA (not necessary but much more convenient for now)
ira = p.IRA()
path = "/path/to/FITS/files"

# Read files. The read() function will walk from the given dir and find all files satisfying 
# the given criteria. Set 'walk' to False if this is not wanted.
data = ira.read(path, data_type='bcd', walk=True)

# get_brigthest() returns a (index, maximum_value)-pair
idx, max_val = ira.get_brightest(data)

# pixel_data() then collects all the values of that specific pixel, for all the HDUs in the "data" list.
xs, ys = ira.pixel_data(idx, data)

# Finally one simply plots using Matplotlib
# NOTE: Hot pixels have not been removed at this stage, so some use of plt.ylim() is highly recommended.
import matplotlib.pyplot as plt

plt.plot(xs, ys)
plt.show()

# OR, instead of all this code, one can simply
ira.plot_brightest()
<code></pre>