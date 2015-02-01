'''
Created on Jan 31, 2015

@author: paepcke
'''
import unittest
from video_footprint_index import VideoFootPrintIndex


TEST_ALL = True

class VideoFootprintTest(unittest.TestCase):

    def setUp(self):
        with open('Test/vid1Len.csv', 'r') as fd:
            # Swallow the col header:
            (col1Header, col2Header) = fd.readline().strip('\n').split(',') #@UnusedVariable
            (vidName, vidLen) = fd.readline().strip('\n').split(',')
            
        self.vidDict = {vidName : vidLen}    

    def tearDown(self):
        pass

# ----------------------  10 Learners, All Play All Of 10 Videos ------------------------------


    @unittest.skipIf(not TEST_ALL, "Temporarily disabled")    
    def test10PlaysAllToEnd(self):
        footprintIndex = VideoFootPrintIndex(indexSavePath='Test/Results/vidSynth10PlaysToEnd.csv',
                                             viewEventsCSVFile='Test/videoTest10PlaysToEnd.csv',
                                             alignmentFile=    'Test/vid1AlignmentFile.csv',
                                             skipEventsCSVLines=1,
                                             skipAlignmentCSVLines=1
                                             )
    
        footprintIndex.videoLengths = self.vidDict    
        footprintIndex.computeFootprints('Medicine/HRP258/Statistics_in_Medicine')
        heatMap = footprintIndex.videoHeatValues(videoId='vid1')
        #print(str(heatMap))
        self.assertItemsEqual(['0,10\n', '1,10\n', '2,10\n', '3,10\n', '4,10\n', '5,10\n', '6,10\n', '7,10\n', '8,10\n', '9,10\n', '10,10\n', '11,10\n', '12,10\n', '13,10\n', '14,10\n', '15,10\n', '16,10\n', '17,10\n', '18,10\n', '19,10\n', '20,10\n', '21,10\n', '22,10\n', '23,10\n', '24,10\n', '25,10\n', '26,10\n', '27,10\n', '28,10\n', '29,10\n', '30,10\n', '31,10\n', '32,10\n', '33,10\n', '34,10\n', '35,10\n', '36,10\n', '37,10\n', '38,10\n', '39,10\n', '40,10\n', '41,10\n', '42,10\n', '43,10\n', '44,10\n', '45,10\n', '46,10\n', '47,10\n', '48,10\n', '49,10\n', '50,10\n', '51,10\n', '52,10\n', '53,10\n', '54,10\n', '55,10\n', '56,10\n', '57,10\n', '58,10\n', '59,10\n', '60,10\n', '61,10\n', '62,10\n', '63,10\n', '64,10\n', '65,10\n', '66,10\n', '67,10\n', '68,10\n', '69,10\n', '70,10\n', '71,10\n', '72,10\n', '73,10\n', '74,10\n', '75,10\n', '76,10\n', '77,10\n', '78,10\n', '79,10\n', '80,10\n', '81,10\n', '82,10\n', '83,10\n', '84,10\n', '85,10\n', '86,10\n', '87,10\n', '88,10\n', '89,10\n', '90,10\n', '91,10\n', '92,10\n', '93,10\n', '94,10\n', '95,10\n', '96,10\n', '97,10\n', '98,10\n', '99,10\n', '100,10\n'], 
                              heatMap)

        # write the heat map for visualization:
        with open('Test/Results/heatMapSynth10PlaysToEnd.csv', 'w') as fd:
            for secNumViewsCR in heatMap:
                (second,numViews) = secNumViewsCR.split(',')
                numViews = numViews.strip('\n')
                fd.write('%s,%s\n' % (str(second),str(numViews)))
    

# ----------------------  10 Learners, Half Play All, Half Play Only Half of 10 Videos ----------

    @unittest.skipIf(not TEST_ALL, "Temporarily disabled")    
    def test10PlaysHalfToEnd (self):
        footprintIndex = VideoFootPrintIndex(indexSavePath='Test/Results/vidSynth10PlaysHalfPlayToEnd.csv',
                                             viewEventsCSVFile='Test/videoTest10PlaysHalfPlayToEnd.csv',
                                             alignmentFile=    'Test/vid1AlignmentFile.csv',
                                             skipEventsCSVLines=1,
                                             skipAlignmentCSVLines=1
                                             )
        footprintIndex.videoLengths = self.vidDict    
        footprintIndex.computeFootprints('Medicine/HRP258/Statistics_in_Medicine')
        heatMap = footprintIndex.videoHeatValues(videoId='vid1')
        #print(str(heatMap))
        self.assertItemsEqual(['0,10\n', '1,10\n', '2,10\n', '3,10\n', '4,10\n', '5,10\n', '6,10\n', '7,10\n', '8,10\n', '9,10\n', '10,10\n', '11,10\n', '12,10\n', '13,10\n', '14,10\n', '15,10\n', '16,10\n', '17,10\n', '18,10\n', '19,10\n', '20,10\n', '21,10\n', '22,10\n', '23,10\n', '24,10\n', '25,10\n', '26,10\n', '27,10\n', '28,10\n', '29,10\n', '30,10\n', '31,10\n', '32,10\n', '33,10\n', '34,10\n', '35,10\n', '36,10\n', '37,10\n', '38,10\n', '39,10\n', '40,10\n', '41,10\n', '42,10\n', '43,10\n', '44,10\n', '45,10\n', '46,10\n', '47,10\n', '48,10\n', '49,10\n', '50,10\n', '51,5\n', '52,5\n', '53,5\n', '54,5\n', '55,5\n', '56,5\n', '57,5\n', '58,5\n', '59,5\n', '60,5\n', '61,5\n', '62,5\n', '63,5\n', '64,5\n', '65,5\n', '66,5\n', '67,5\n', '68,5\n', '69,5\n', '70,5\n', '71,5\n', '72,5\n', '73,5\n', '74,5\n', '75,5\n', '76,5\n', '77,5\n', '78,5\n', '79,5\n', '80,5\n', '81,5\n', '82,5\n', '83,5\n', '84,5\n', '85,5\n', '86,5\n', '87,5\n', '88,5\n', '89,5\n', '90,5\n', '91,5\n', '92,5\n', '93,5\n', '94,5\n', '95,5\n', '96,5\n', '97,5\n', '98,5\n', '99,5\n', '100,5\n'],
                              heatMap)

        with open('Test/Results/heatMapSynth10PlaysHalfPlayToEnd.csv', 'w') as fd:
            for secNumViewsCR in heatMap:
                (second,numViews) = secNumViewsCR.split(',')
                numViews = numViews.strip('\n')
                fd.write('%s,%s\n' % (str(second),str(numViews)))

# ----------------------  10 Learners, Play All, Half Play Also Re-View from 75 to 100 ----------

    @unittest.skipIf(not TEST_ALL, "Temporarily disabled")    
    def test10PlaysHalfReViewFrom75ToEnd(self):
        footprintIndex = VideoFootPrintIndex(indexSavePath='Test/Results/vidSynth10Plays5ReViewFrom75.csv',
                                             viewEventsCSVFile='Test/videoTest10PlaysToEnd5ReViewFrom75.csv',
                                             alignmentFile=    'Test/vid1AlignmentFile.csv',
                                             skipEventsCSVLines=1,
                                             skipAlignmentCSVLines=1
                                             )
        footprintIndex.videoLengths = self.vidDict
        footprintIndex.computeFootprints('Medicine/HRP258/Statistics_in_Medicine')
        heatMap = footprintIndex.videoHeatValues(videoId='vid1')
        #print(str(heatMap))
        self.assertItemsEqual(['0,10\n', '1,10\n', '2,10\n', '3,10\n', '4,10\n', '5,10\n', '6,10\n', '7,10\n', '8,10\n', '9,10\n', '10,10\n', '11,10\n', '12,10\n', '13,10\n', '14,10\n', '15,10\n', '16,10\n', '17,10\n', '18,10\n', '19,10\n', '20,10\n', '21,10\n', '22,10\n', '23,10\n', '24,10\n', '25,10\n', '26,10\n', '27,10\n', '28,10\n', '29,10\n', '30,10\n', '31,10\n', '32,10\n', '33,10\n', '34,10\n', '35,10\n', '36,10\n', '37,10\n', '38,10\n', '39,10\n', '40,10\n', '41,10\n', '42,10\n', '43,10\n', '44,10\n', '45,10\n', '46,10\n', '47,10\n', '48,10\n', '49,10\n', '50,10\n', '51,10\n', '52,10\n', '53,10\n', '54,10\n', '55,10\n', '56,10\n', '57,10\n', '58,10\n', '59,10\n', '60,10\n', '61,10\n', '62,10\n', '63,10\n', '64,10\n', '65,10\n', '66,10\n', '67,10\n', '68,10\n', '69,10\n', '70,10\n', '71,10\n', '72,10\n', '73,10\n', '74,10\n', '75,14\n', '76,14\n', '77,14\n', '78,14\n', '79,14\n', '80,14\n', '81,14\n', '82,14\n', '83,14\n', '84,14\n', '85,14\n', '86,14\n', '87,14\n', '88,14\n', '89,14\n', '90,14\n', '91,14\n', '92,14\n', '93,14\n', '94,14\n', '95,14\n', '96,14\n', '97,14\n', '98,14\n', '99,14\n', '100,14\n'], 
                              heatMap)
        with open('Test/Results/heatMapSynth10PlaysToEnd5ReViewFrom75.csv', 'w') as fd:
            for secNumViewsCR in heatMap:
                (second,numViews) = secNumViewsCR.split(',')
                numViews = numViews.strip('\n')
                fd.write('%s,%s\n' % (str(second),str(numViews)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    