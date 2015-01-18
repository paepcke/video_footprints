'''
Created on Jan 18, 2015

@author: paepcke
'''

import tempfile

from video_footprint_index import VideoFootPrintIndex


videoId = 'i4x-Medicine-HRP258-videoalpha-67b77215c10243f1a20d81350909084a'

# ------------------- Simplest Case -----------------------

# Simplest case: the index file was built earlier
# Create an index instance, passing location of 
# the index file:
footprintIndex = VideoFootPrintIndex(indexSavePath='/tmp/medstatsIndex')

# Print list of all videos covered in the index:
print(str(footprintIndex.videos()))

# Print number of views for video 'i4x-Medicine...' at second 10.
# Note the dictionary syntax, but keys may be
# 2-tuples, passing a video ID and a playhead
# position in seconds:
print(footprintIndex[(videoId, 10)])

# To avoid having to specify the video id when
# it will stay the same for a while:
footprintIndex.setVideo('i4x-Medicine-HRP258-videoalpha-67b77215c10243f1a20d81350909084a')

# Get the now 'default' video's views at second 10
# (same result as above)
print(footprintIndex[10])

# ------------------- Get heatmap for one video -----------------------

# Write a heatmap to a file: '<second>,<numViews>':

# Get a destination file name:
csvFd = tempfile.NamedTemporaryFile(prefix='videoHeatmap', suffix='_%s.csv' % videoId, delete=False)
# Write the column header: 
csvFd.write('second,views\n')
# Get list of strings like '10,325\n',
# and write them to your file:
for csvLine in footprintIndex.videoHeatValues():
    csvFd.write(csvLine)
csvFd.close()
print("Heatmap is in '%s'" % csvFd.name)    

# --------------------- When index file does not exist yet -------

# Task: build the index file via MySQL queries.
# Let's assume you have mysql pwd of current user
# in ~/.ssh/mysql. We'll ask to have the index file
# dumped into /tmp/medstatsIndex:

footprintIndex = VideoFootPrintIndex(indexSavePath='/tmp/medstatsIndex')
footprintIndex.computeFootprints('Medicine/HRP258/Statistics_in_Medicine')

# And use it:
print(footprintIndex[('i4x-Medicine-HRP258-videoalpha-67b77215c10243f1a20d81350909084a', 10)])

