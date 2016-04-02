import pypeira.pypeira as pype

if __name__ == "__main__":
    # Create instance of IRA (not necessary but much more convenient for now)
    ira = pype.IRA()
    path = "./data"

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
    
    plt.ylabel('Flux (MJy/sr)')
    plt.title('Flux vs. Time')
    plt.xlabel('Time (BJD)')

    plt.show()
