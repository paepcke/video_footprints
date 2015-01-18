'''
Created on Jan 18, 2015

@author: paepcke
'''

from video_footprint_index import VideoFootPrintIndex

footprintIndex = VideoFootPrintIndex(indexSavePath='/tmp/medstatsIndex1')
VideoFootPrintIndex.computeFootprints('Medicine/HRP258/Statistics_in_Medicine')


# VideoFootPrintIndex(viewEventsCSVFile='/tmp/medstatsVideoUse.csv', 
#                         alignmentFile='/tmp/medstatsAlignment.csv',
#                         indexSavePath='/tmp/medstatsIndex')
# 
# 
# (viewEventsCSVFile='/tmp/medstatsVideoUse.csv', 
#                         alignmentFile='/tmp/medstatsAlignment.csv',
#                         indexSavePath='/tmp/medstatsIndex')

