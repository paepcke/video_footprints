'''
Created on Jan 18, 2015

@author: paepcke
'''

import tempfile

from video_footprint_index import VideoFootPrintIndex
videoId = 'i4x-Medicine-HRP258-videoalpha-67b77215c10243f1a20d81350909084a'

#footprintIndex = VideoFootPrintIndex(indexSavePath='/tmp/medstatsIndex1')
#VideoFootPrintIndex.computeFootprints('Medicine/HRP258/Statistics_in_Medicine')
footprintIndex = VideoFootPrintIndex(indexSavePath='/tmp/medstatsIndex')


# Print list of all videos covered in the index:
print(str(footprintIndex.videos()))

# Print number of views for video 'i4x-Medicine...' at second 10:
print(footprintIndex[(videoId, 10)])

# To avoid having to specify the video id when
# it will stay the same for a while:
footprintIndex.setVideo('i4x-Medicine-HRP258-videoalpha-67b77215c10243f1a20d81350909084a')

# Get the now 'default' video's views at second 10:
print(footprintIndex[10])

# Write a heatmap to a file: '<second>,<numViews>':
csvFd = tempfile.NamedTemporaryFile(prefix='videoHeatmap', suffix='_%s.csv' % videoId, delete=False)
csvFd.write('second,views\n')
for csvLine in footprintIndex.videoHeatValues():
    csvFd.write(csvLine)
csvFd.close()
print("Heatmap is in '%s'" % csvFd.name)    

# VideoFootPrintIndex(viewEventsCSVFile='/tmp/medstatsVideoUse.csv', 
#                         alignmentFile='/tmp/medstatsAlignment.csv',
#                         indexSavePath='/tmp/medstatsIndex')
# 
# 
# (viewEventsCSVFile='/tmp/medstatsVideoUse.csv', 
#                         alignmentFile='/tmp/medstatsAlignment.csv',
#                         indexSavePath='/tmp/medstatsIndex')

