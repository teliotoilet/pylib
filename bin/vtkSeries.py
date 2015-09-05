#!/usr/local/bin/python
import os

dirlist = []
timesteps = []

#dirs=*.*
#curdir=`pwd`
dirs = os.walk('.').next()[1]
for d in dirs:
    try: 
        step = float(d) # need this to verify this is a time-step dir!
        dirlist.append(d)
        timesteps.append(step)
    except ValueError: pass

extMapping = dict()
extMapping['xy'] = 'xyz'

def tname(tval):
    return '%d' % (tval*10)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

sampleNames = []
varNames = []
extNames = []
for timestep_dir in dirlist:
    print 'Processing', timestep_dir
    for f in [ f for f in os.listdir(timestep_dir) if os.path.isfile(os.path.join(timestep_dir,f)) ]:
        # fname = f.split('.')[0]
        # var = fname.split('_')[0]
        # #name = fname.split('_')[1]
        # name = '_'.join(fname.split('_')[1:])
        fname = f.split('.')
        ext = fname[1]
        fbasename = fname[0].split('_')
        var = fbasename[-1]
        name = '_'.join(fbasename[0:-1])
        print ' ',f,'( name=',name,' var=',var,' ext=',ext,')'
        if not name in sampleNames:
            sampleNames.append(name)
            if not os.path.exists(name): os.makedirs(name)
        if not var in varNames:
            varNames.append(var)
        if not ext in extNames:
            extNames.append(ext)

if not len(extNames)==1:
    print 'Don''t know how to handle different extensions',extNames
if ext in extMapping:
    extNew = extMapping[ext]
else: extNew = ext

indices = sorted(range(len(timesteps)), key=lambda k: timesteps[k])
for sample in sampleNames:
    for var in varNames:
        for i in range(len(timesteps)):
            dname = dirlist[indices[i]]#.split()
            src = os.getcwd() + os.sep + dname + os.sep + sample+'_'+var+'.'+ext
            #dest = sample + os.sep + '%s_%d.vtk'%(var,i+1)
            #dest = sample + os.sep + '%s_%g.%s'%(var,timesteps[i],extNew)
            dest = sample + os.sep + '%s_%s.%s'%(var,tname(timesteps[i]),extNew)
            print dest,'-->',src
            os.symlink(src,dest)

