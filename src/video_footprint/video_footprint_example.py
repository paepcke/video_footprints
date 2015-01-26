'''
Created on Jan 18, 2015

@author: paepcke
'''

import os
import shutil
import sys
import tempfile

from video_footprint_index import VideoFootPrintIndex


videoId = 'i4x-Medicine-MedStats-video-35f3582a6444423197e50006288a7885'
# ------------------- Simplest Case -----------------------

# Simplest case: the index file was built earlier:
# Create an index instance, passing location of 
# the index file:
footprintIndex = VideoFootPrintIndex(indexSavePath='/tmp/medstatsVideoFootprintIndex')

# Print list of all videos covered in the index:
print(str(footprintIndex.videos()))

# Print number of views for video 'i4x-Medicine...' at second 10.
# Note the dictionary syntax, but keys may be
# 2-tuples, passing a video ID and a playhead
# position in seconds:
print(footprintIndex[(videoId, 10)])

# To avoid having to specify the video id when
# it will stay the same for a while:
footprintIndex.setVideo('i4x-Medicine-MedStats-video-35f3582a6444423197e50006288a7885')

# Get the new 'default' video's views at second 10
# (same result as above)
print(footprintIndex[10])

sys.exit()
# ------------------- Get data for all learners AND (in aggregate) a list of special learners -----------------------

# Simplest case: the index file was built earlier
# Create an index instance, passing location of 
# the index file:
footprintIndex = VideoFootPrintIndex(viewEventsCSVFile='/tmp/medstatsVideoUse1.csv',
                                     alignmentFile='/tmp/medstatsAlignment1.csv',
                                     specialLearnersList=[
										   'b27fef2d1c5ad0c9ace45305ce6bd3c89db43110',
										   '275a1a0fdae6071a40f907791c2ecfe17f60cb92',
										   '0dfab79268250b022f9d4449eadd21d51bdf2796',
										   '36c7903c7a98a1b6503e3040aad512509c789818',
										   '283b8e838324166b1f90ef90336f29dda1c93e4f',
										   'e60f0a3890a5e1ffc11410029e0b7bea30ecfe4e',
										   'b867a22cf2286e0cf9def73b16cb587b1d810661',
										   '5daa8f08e9ef7bf2969c67e15156a70d364cd4ff',
										   'c984107bc7ea4588784f916cd24e3d3379d18f8e',
										   '30f0517a8b98e920e853c36eec9ab21964ca7996'
                                           ])

footprintIndex.computeFootprints('Medicine/HRP258/Statistics_in_Medicine')

# Print number of views for video 'i4x-Medicine...' at second 10.
# Note the dictionary syntax, but keys may be
# 2-tuples, passing a video ID and a playhead
# position in seconds:
print(footprintIndex[(videoId, 10)])

# Same number but for the aggregate over the special learners only:
footprintIndex.videoViewsSpecialLearners[videoId, 10]
sys.exit()

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

sys.exit()

# ---------------- When you have the use, and alignment query result files, but not the index file  -------

footprintIndex = VideoFootPrintIndex(viewEventsCSVFile='/tmp/medstatsVideoUse.csv',
                                     alignmentFile='/tmp/Medicine_HRP258_Statistics_in_MedicinehZJsok_alignment.csv',
                                     indexSavePath='/tmp/medstatsIndex')
footprintIndex.computeFootprints('Medicine/HRP258/Statistics_in_Medicine')
sys.exit()




# --------------------- When index file does not exist yet -------

# Task: build the index file via MySQL queries.
# Let's assume you have mysql pwd of current user
# in ~/.ssh/mysql. We'll ask to have the index file
# dumped into /tmp/medstatsIndex:


shutil.copyfile('/tmp/medstatsIndex', '/tmp/medstatsIndex.SAVED')
os.remove('/tmp/medstatsIndex')

footprintIndex = VideoFootPrintIndex(indexSavePath='/tmp/medstatsIndex')
footprintIndex.computeFootprints('Medicine/HRP258/Statistics_in_Medicine')

# And use it:
print(footprintIndex[('i4x-Medicine-HRP258-videoalpha-67b77215c10243f1a20d81350909084a', 10)])

shutil.copyfile('/tmp/medstatsIndex.SAVED', '/tmp/medstatsIndex')

