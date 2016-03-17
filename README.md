# pypeira

## Description
My attempt at reducing images from the SSC into ultra high-precision time-resolved photometry.
**NOTE:** I had to change it quite a bit recently, so some documentation (almost everything about FITS objects)
might not be correct. Will change this as soon as I have time.

## Installation

First clone the project

<pre><code>git https://github.com/WielderOfMjoelnir/pypeira.git</code></pre>

Then <code>cd</code> into the project folder and run the command

<pre><code>python setup.py install</code></pre>

You *should* then be able to import <code>pypeira</code> as you normal.

## Usage

<pre><code>
import pypeira.pypeira as pype

# Create instance of IRA (not necessary but much more convenient for now)
ira = pype.IRA()
path = "/path/to/FITS/files"

# Read files. The read() function will walk from the given dir and find all files satisfying 
# the given criteria. Set 'walk' to False if this is not wanted.
data = ira.read(path, dtype='bcd', walk=True)

# Uncomment plot_brightest(data) below, and comment out EVERYTHING after this line for the easiest way.
# ira.plot_brightest(data)

# get_brigthest() returns a (index, maximum_value)-pair
idx, max_val = ira.get_brightest(data)

# pixel_data() then collects all the values of that specific pixel, for all the HDUs in the "data" list.
xs, ys = ira.pixel_data(idx, data)

# Finally one simply plots using Matplotlib
# NOTE: Hot pixels have not been removed at this stage, so some use of plt.ylim() is highly recommended.
import matplotlib.pyplot as plt

plt.plot(xs, ys)
plt.show()
</code></pre>

## TODO
1. Fix documentation for current version and clean up code.
2. Complete the "config"-object <code>IRA</code> and determine whether to let the subclasses to-be of
<code>HDU</code> depend on source or file type. This is something that should be discussed with mentor.
3. Implement centroid algorithms.
4. Removal of hot pixels, bad frames, etc.
5. Background subtraction
6. Implementation of aperture photometry
7. Visualizing data

## Dependencies
* numpy >= 1.10.4
* matplotlib >= 1.5.1
* fitsio >= 0.9.7

## License
MIT