#!/usr/local/bin/python
import numpy as np

DEBUG       = False
DUMP_PEAKS  = True
TIMING      = True

if DEBUG: import matplotlib.pyplot as plt
if TIMING: import time

def find_peaks(data,x=[],Nsmoo=1):

    N = len(data)
    i = np.arange(N)
    if len(x)==0: 
        x = i # assume evenly spaced data
    else:
        assert(len(x)==N)
    dx = np.diff(x)

    if TIMING: t0 = time.time()
    ist = i   - Nsmoo
    ind = i+1 + Nsmoo
    ist = np.maximum(0,ist)
    ind = np.minimum(N,ind)
    width = ind - ist
    if TIMING: print ' - walltime [s] to calculate indices:',time.time()-t0

    if TIMING: t0 = time.time()
    ysmoo = np.zeros((N))
    #ysmoo2= np.zeros((N))

# SLOW, and moving avg for last two indices are wrong (doesn't affect overall results)
#    ysum = data[0]
#    for i in range(N):
#        #ysmoo[i] = np.mean( data[ist[i]:ind[i]] )
#
#        # faster:
#        #ysmoo[i] = np.sum( data[ist[i]:ind[i]] ) / width[i]
#
#        # even faster:
#        if ist[i] > 0: ysum -= data[ist[i]-1]
#        if ind[i] < N: ysum += data[ind[i]-1]
#        #ysmoo2[i] = ysum / width[i]
#        ysmoo[i] = ysum / width[i]

    #ysmoo2 = data.copy()
    ysmoo = data.copy()
    buff = np.zeros((N))
    for ismoo in range(1,Nsmoo+1):
        # add LHS
        buff[:ismoo] = 0.
        buff[ismoo:] = data[:N-ismoo]
        print -ismoo,buff
        #ysmoo2 += buff
        ysmoo += buff
        # add RHS
        buff[:N-ismoo] = data[ismoo:]
        buff[N-ismoo:] = 0.
        #ysmoo2 += buff
        ysmoo += buff
        print ismoo,buff
    #ysmoo2 /= width
    ysmoo /= width

    # DEBUG
#    for i in range(N):
#        print ist[i],ind[i],width[i],ysmoo[i],ysmoo2[i]
#    print 'SHOULD BE ~ZERO:',np.max(ysmoo2-ysmoo)

    if TIMING: print ' - walltime [s] to smooth data:',time.time()-t0

    if TIMING: t0 = time.time()
    twodx = dx[1:] + dx[:-1]
    dydx = np.zeros((N))
    for i in range(1,N-1):
        dydx[i] = ysmoo[i+1] - ysmoo[i-1]
    dydx[1:-1] /= twodx
    if TIMING: print ' - walltime [s] to calculate slope:',time.time()-t0

    if TIMING: t0 = time.time()
    indices = []
    for i in range(1,N-1):
        if not np.sign(dydx[i]) == np.sign(dydx[i+1]):
            if np.abs(dydx[i]) < np.abs(dydx[i+1]):
                indices.append(i)
            else: indices.append(i+1)
    if TIMING: print ' - walltime [s] to find peak indices:',time.time()-t0

    peaks = data[indices]

    if DUMP_PEAKS:
        with open('peaks.tmp','w') as f:
            for xi,yi in zip(x[indices],peaks):
                f.write('%f %f\n'%(xi,yi))
        print 'wrote peaks.tmp'

    if DEBUG:
        print len(indices),'min/maxima found',indices
        plt.plot(x,data,label='input data')
        plt.plot(x,ysmoo,'k--',label='smoothed input')
        plt.plot(x[indices],peaks,'o',label='detected peaks')
        #plt.xlim((72,77))
        #plt.ylim((200,700))
        plt.legend(loc='best')
        plt.show()

    return peaks, indices
