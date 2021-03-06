# [move this code out to a module]

# First derive a very smooth artificial signal by generating 
# motions from a captured accelerometer sequence and processing
# it to a 0.1milisecond capture rate
import numpy, pandas, scipy.signal

ax = [1, 0, -1, 2, 0, 2, 2, 0, 0, 1, 0, 1, 5, 0, 2, 0, 1, 2, 0, 0, 0, 0, -1, 1, 0, -4, 2, 0, 3, 0, 1, 0, 0, 2, 2, 2, 2, 2, 0, -1, 0, 0, 1, 2, 0, -53, 10, -6, 7, -10, -191, -153, -92, -118, -145, -125, -111, -100, -85, -65, -86, -95, -134, -207, -178, -174, -177, -179, -186, -167, -131, -96, -63, -35, -53, -51, -61, -112, -91, -64, -144, -199, -212, -285, -276, -208, -82, -138, -90, 3, 96, 209, 149, 218, 387, 379, 456, 616, 45, 755, 813, 585, 657, 228, 96, 243, 404, 566, 610, 571, 547, 466, 380, 275, 159, 196, 123, 136, 160, 228, 152, 93, -1012, -109, 701, 228, -225, -212, -266, -297, -296, -280, -244, -200, -178, -160, -203, -169, -152, -111, -146, -126, -121, -117, -80, -102, -147, -161, -122, -170, -95, -103, -42, 18, 21, 23, 23, 20, 24, 19, 18, 19, 19, 17, 19, 17, 18, 20, 20, 18, 19, 21, 22, 19, 20, 16, 15, 17, 19, 21, 19, 19, 19, 17, 18, 18, 17, 17, 15, 15, 15, 14, 13, 15, 16, 16, 15, 17, 17, 19]
#ax = [12, 12, 9, 8, 8, 10, 7, 6, 5, 6, 5, 7, 6, 3, 5, 2, 2, 0, 1, 2, 2, 3, 3, 2, 3, 1, 5, 0, 1, 1, 0, 0, 0, 0, 0, -1, 0, -1, -1, 0, 0, -1, 0, 2, 2, 0, 1, 0, 3, 1, 2, 0, 0, -98, 70, -81, -235, -311, -310, -296, -310, -293, -330, -300, -280, -262, -211, -181, -170, -160, -211, -185, -217, -192, -206, -137, -146, -44, -41, -24, -27, 7, 75, -16, 3, 28, 141, 207, 198, 177, 280, 267, 277, 392, 344, 400, 501, 586, 661, 630, 559, 438, 294, 126, 84, 365, 647, 698, 698, 483, 422, 465, 432, 308, 316, 254, 321, 221, 193, 154, 121, -8, -95, -199, -112, 129, -78, 68, 73, -87, -30, -110, -253, -171, -322, -293, -316, -296, -283, -241, -239, -282, -243, -287, -331, -324, -264, -291, -210, -244, -204, -164, -125, -42, -30, -14, -8, -74, -37, -45, -57, -28, -55, -28, -88, -44, -86, -83, -94, -85, -159, -144, -126, -116, -79, -78, -47, -63, -10, 9, 37, 66, 99, 103, 94, 81, 118, 112, 154, 200, 172, 168, 191, 152, 119, 88, 84, 13, 11, 12]
#ax = [3, 4, 7, 10, 12, 12, 4, 9, 11, 9, 8, 8, 9, 6, 2, 0, -4, -4, -2, 1, 0, -1, -1, 3, 0, -1, -2, 0, -1, -1, -4, 0, 5, 7, 9, 13, 13, 8, 2, 7, 13, 10, 11, 12, 15, 9, 6, 10, 10, 4, 6, 9, 5, 1, -1, 0, 5, 8, 7, 5, 7, 6, 0, 0, 4, 1, 1, 0, -2, -2, -2, 0, 6, 8, 5, 1, 2, -1, 0, -1, -5, -11, -17, -35, -49, -67, -112, -257, -324, -374, -410, -490, -535, -601, -646, -715, -756, -786, -777, -699, -684, -657, -589, -438, -282, -192, -103, -35, 35, 111, 252, 303, 378, 432, 488, 530, 529, 525, 522, 477, 467, 465, 460, 521, 560, 598, 596, 604, 595, 599, 610, 627, 639, 625, 617, 592, 582, 566, 548, 529, 525, 526, 512, 498, 468, 427, 374, 366, 359, 346, 328, 264, 226, 198, 170, 108, 68, 38, 25, -33, -64, -111, -165, -278, -323, -354, -361, -341, -339, -332, -334, -421, -461, -489, -497, -463, -440, -418, -371, -353, -336, -315, -306, -308, -312, -294, -281, -256, -257, -242, -205, -148, -99, -50, -22, -44, -36, -14, 3, 10]
for i0 in range(len(ax)):
    if abs(ax[i0]) < 20:     ax[i0] = 0
    else:  break
for i1 in range(len(ax)):
    if abs(ax[-1-i1]) < 25:  ax[-1-i1] = 0
    else:  break
pos = pandas.DataFrame({"ax":ax}, index=numpy.linspace(0, 2.09, len(ax)))
pos.ax = -pos.ax*0.01

t = pos.index.to_series()
dt = (t.diff().fillna(0) - t.diff(-1).fillna(0))/2
pos["dt"] = dt
pos["vx"] = (pos.ax*pos.dt).cumsum()
pos.vx = pos.vx - pos["vx"].iloc[-1]*t/t.iloc[-1]
pos["px"] = (pos.vx*pos.dt).cumsum()
#pos["px"].plot()
pos.px = pos.px - pos["px"].iloc[-1]*t/t.iloc[-1]
#pos["px"].plot()
winfunc = numpy.concatenate((numpy.zeros(i0), scipy.signal.tukey(len(pos)-i0-i1, alpha=0.5), numpy.zeros(i1)))
wpx = numpy.array(pos.px)*winfunc
#plt.plot(wpx)

wpx = numpy.array(pos.px)*winfunc
win = scipy.signal.windows.gaussian(50, 16)
wpx = scipy.signal.convolve(wpx, win, mode='same') / sum(win)

xs = numpy.interp(numpy.arange(len(wpx)*100)/10000, numpy.arange(len(wpx))/100, wpx)
win = scipy.signal.windows.gaussian(250, 64)  # leaves sawteeth on it
win = scipy.signal.hann(500)  # smooths it somehow
fxs = scipy.signal.convolve(xs, win, mode='same') / sum(win)

xs = fxs
ts = numpy.arange(len(fxs))/10000
px = pandas.DataFrame({"t":ts, "x":fxs})

