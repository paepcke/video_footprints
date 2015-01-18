'''
Created on Jan 15, 2015

@author: paepcke
'''
import cPickle
import collections
import datetime
import getpass
import os
import sys
import tempfile

from pymysql_utils.pymysql_utils import MySQLDB


class VideoFootPrintIndex(collections.Mapping):
    
    timeResolution = 1 # second
    
    def __init__(self,
                 viewEventsCSVFile = None,
                 alignmentFile = None,
                 indexSavePath = None,
                 dbHost='localhost', 
                 mySQLUser=None, 
                 mySQLPwd=None 
                ):
        self.viewEventsCSVFile = viewEventsCSVFile
        self.alignmentFile     = alignmentFile
        self.indexSavePath = indexSavePath
        if viewEventsCSVFile is None or alignmentFile is None:
            self.dbHost = dbHost
            self.dbName = 'Edx'
            self.mySQLUser = mySQLUser
            self.mySQLPwd  = mySQLPwd
            if mySQLUser is None:
                self.mySQLUser = getpass.getuser()
            if mySQLPwd is None:
                # Try to get it from .ssh/mysql file of user
                try:
                    homeDir = os.path.expanduser('~' + mySQLUser)
                    pwdFile = os.path.join(homeDir,'.ssh/mysql')
                    with open(pwdFile, 'r') as fd:
                        self.mySQLPwd = fd.readline().strip()
                except Exception:
                    self.mySQLPwd = ''
                
            self.db = MySQLDB(host=self.dbHost, user=self.mySQLUser, passwd=self.mySQLPwd, db='Edx')

        self.activeFootprintDict = None
    
    def initPlayheadAlignments(self, alignmentFile=None):
        if alignmentFile is None:
            raise NotImplementedError("Auto-computation of playhead alignment not implemented.")
        alignmentDict = {}
        with open(alignmentFile, 'r') as alignmentFd:
            for line in alignmentFd:
                (videoId, startTime) = line.split(',')
                alignmentDict[videoId.strip('"')] = int(startTime.strip('"\n'))
        return alignmentDict;
    
    def computeFootprints(self, courseDisplayName=None):
        '''
        Create dict mapping each video id of a course to 
        a dict that maps floating point time codes to the
        number of views of that section of video. If courseDisplayName
        is None, it is assumed that self.viewEventsCSVFile is the
        path to a file with rows (anon_screen_name, event_type, video_id, video_current_time, video_old_time, video_new_time)

        :param courseDisplayName: course whose videos are to be profiled
        :type courseDisplayName: string
        '''
        
        currVideoId = None
        # Current playhead position of current video
        currTime    = 0
        # Some videos start at a negative number
        # of seconds. The self.alignmentFile contains
        # those offsets for each video:
        currVideoZeroTimeOffset = 0
        playing     = False
        # Array in which each element is a counter
        # for views of one minute:
        currVideoTimeDict = None
        # Dict mapping video_id to array.
        # each array element contains the 
        # view counts of a particular minute
        # in the video:
        self.videoViews = {}
        
        if self.viewEventsCSVFile is None:
            self.viewEventsCSVFile  = tempfile.NamedTemporaryFile(prefix='%s' % courseDisplayName, 
                                                                  suffix='_video_action.csv',
                                                                  delete=False)
            self.log('About to start video activity query; will take about 2 minutes...')
            mysqlCmd = "SELECT time, event_type, video_id \
                          INTO OUTFILE '%s' \
                        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' \
                          FROM EdxTrackEvent \
                         WHERE event_type = 'play_video' \
                            OR event_type = 'pause_video' \
                            OR event_type = 'stop_video' \
                            OR event_type = 'seek_video' \
                           AND course_display_name = 'Medicine/HRP258/Statistics_in_Medicine' \
                         ORDER BY video_id, time;" % self.viewEventsCSVFile
            
            self.db.query(mysqlCmd)
            self.log('Done video activity query...')

        # If no alignment file was provided, create it now:
        if self.alignmentFile is None:
            self.alignmentFile = tempfile.NamedTemporaryFile(prefix='%s' % courseDisplayName, 
                                                                  suffix='_alignment.csv',
                                                                  delete=False)
            self.log('About to find start time offset for all videos...')
            mysqlCmd = "SELECT video_id, MIN(CAST(video_current_time AS SIGNED INTEGER)) \
                          INTO OUTFILE '%s' \
                          FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' \
                          FROM EdxTrackEvent PARTITION (pAY2013_Summer) \
                          WHERE course_display_name = 'Medicine/HRP258/Statistics_in_Medicine' \
                            AND video_id != '' \
                          GROUP BY video_id;" % self.alignmentFile
        
        # Create a dict: video_id --> start-time offset
        alignmentDict = self.initPlayheadAlignments(self.alignmentFile)
        
        # From the footprint file get one line after another:
        #    anon_screen_name, event_type, video_id
           
        with open(self.viewEventsCSVFile, 'r') as fd:
            for line in fd:
                (time,  #@UnusedVariable 
                 event_type, 
                 video_id,
                 video_current_time,
                 video_old_time,
                 video_new_time) = line.split(',')
                 
                event_type         = event_type.strip('"')
                video_id           = video_id.strip('"')
                try:
                    video_current_time = 0 if video_current_time.startswith('""') else int(round(float(video_current_time.strip('"\n'))))
                except ValueError:
                    if video_current_time.startswith('"None'):
                        video_current_time = None 
                try:
                    video_old_time     = 0 if video_old_time.startswith('""') else int(round(float(video_old_time.strip('"\n'))))
                except ValueError:
                    if video_old_time.startswith('"None'):
                        video_old_time = None 
                        
                try:
                    video_new_time     = 0 if video_new_time.startswith('""') else int(round(float(video_new_time.strip('"\n'))))
                except ValueError:
                    if video_new_time.startswith('"None'):
                        video_new_time = None 
                
                if video_id != currVideoId:
                    # All done with one video of one learner
                    self.videoViews[currVideoId] = currVideoTimeDict
                    currVideo = video_id
                    currTime   = 0
                    try:
                        currVideoZeroTimeOffset = -1 * alignmentDict[video_id]
                    except KeyError:
                        currVideoZeroTimeOffset = 0
                    try:
                        currVideoTimeDict = self.videoViews[currVideo]
                    except KeyError:
                        # Never encountered this video. Put
                        # empty minutes dict for this video into dict:
                        self.videoViews[currVideo] = currVideoTimeDict = {}

                # Add time alignment offset to the playhead times;
                # the type error occurs when one of the times is
                # None. That value is OK if the respective time is
                # not needed further down. We check that need 
                # in the next block:
                try:
                    video_current_time += currVideoZeroTimeOffset
                except TypeError:
                    pass
                try:
                    video_old_time     += currVideoZeroTimeOffset
                except TypeError:
                    pass
                try:
                    video_new_time     += currVideoZeroTimeOffset
                except TypeError:
                    pass
                
                # All set: got a learner and a video minutes array
                # What's the event?
                if event_type == 'play_video':
                    if not type(video_current_time) == int:
                        self.log("Play event without, or with bad current time: '%s'" % line)
                        continue
                    playing = True
                    currTime = video_current_time
                    
                elif event_type == 'pause_video':
                    if not type(video_current_time) == int:
                        self.log("Pause event without, or with bad current time: '%s'" % line)
                        continue
                    currVideoTimeDict = self.handlePauseVideo(currTime, video_current_time, currVideoTimeDict)
                    continue
                
                elif event_type == 'seek_video':
                    if not type(video_new_time) == int:
                        self.log("Seek event without, or with bad new time: '%s'" % line)
                        continue
                    currVideoTimeDict = self.handleSeekVideo(currTime, playing, video_old_time, currVideoTimeDict)
                    currTime = video_new_time
                    
                elif event_type == 'stop_video':
                    if not type(video_current_time) == int:
                        self.log("Stop event without, or with bad current time: '%s'" % line)
                        continue
                    self.handleStopVideo(currTime, playing, video_current_time, currVideoTimeDict)
                    playing = False
            # All done, wrap up:
            self.finish(self.videoViews)
        
                    
    def handlePauseVideo(self, currTime, pauseTime, videoTimeDict):
        '''
        Handle a video pause event. Retrieves viewing counters from
        every key in videoTimeDict between currTime and pauseTime.
        Does this in VideoFootPrintIndex.timeResolution increments.
        
        :param currTime: last known playhead time
        :type currTime: int
        :param pauseTime: playhead time when pause event occurred
        :type pauseTime: float
        :param videoTimeDict: time dict for the current video 
        :type videoTimeDict: {float --> int}
        :return: the updated videoTimeDict
        :rtype {float --> int}
        :raise ValueError if new time is less than old time.
        '''
        # Credit the minutes to the current video:
        if pauseTime < currTime:
            raise ValueError('New time (%s) less than old time (%s) in pause' % (pauseTime, currTime))
        return self.creditTime(videoTimeDict, currTime, pauseTime)
        
    def handleSeekVideo(self, currTime, playing, srcTime, videoTimeDict):
        '''
        Handle seeking video from one spot to another. If currently playing,
        credit time from last known time to start of the seek.
        
        :param currTime: last known playhead time
        :type currTime: int
        :param playing: is player currently playing?
        :type playing: boolean
        :param srcTime: time from which to move playhead
        :type srcTime: float
        :param videoTimeDict: time dict for the current video
        :type videoTimeDict: {float --> int}
        :return the updated videoTimeDict
        :rtype {float --> int}
        '''
        # First credit the minutes between
        # currTime and srcTime, the from-time of the seek:
        if playing:
            videoTimeDict = self.creditTime(videoTimeDict, currTime, srcTime)
        return videoTimeDict 

    def handleStopVideo(self, currTime, playing, stopTime, videoTimeDict):
        '''
        If currently playing, credit time from last known
        playhead time to current time.
        
        :param currTime: last known playhead time
        :type currTime: int
        :param playing: is player currently playing?
        :type playing: boolean
        :param stopTime: playhead time when stop occurred
        :type srcTime: float
        :param videoTimeDict: time dict for the current video
        :type videoTimeDict: {float --> int}
        :return the updated videoTimeDict
        :rtype {float --> int}
        '''
        if playing:
            videoTimeDict = self.creditTime(videoTimeDict, currTime, stopTime)
        return videoTimeDict
        
    def creditTime(self, videoTimeDict, startTime, stopTime):
        '''
        Given a dict of floatTime --> viewCounters, a start time,
        and a stop time, credit the time between start and stop. 
        The resolution is controlled by VideoFootPrintIndex.timeResolution.

        :param videoTimeDict: videoTimeDict: time dict for the current video
        :type videoTimeDict: {int --> int}
        :param startTime: start of time from which on view counters are to be bumped
        :type startTime: int
        :param stopTime: final time whose view counter is to be bumped
        :type stopTime: int
        :return updated videoTimeDict
        :rtype: {int --> int}
        '''
        theTime = startTime
        while (theTime < stopTime):
            try:
                viewCount = videoTimeDict[theTime]
            except KeyError:
                viewCount = 0
            videoTimeDict[theTime] = viewCount + 1
            theTime += VideoFootPrintIndex.timeResolution
        return videoTimeDict

    # --------------------------------- Persistence ------------------
    
    def finish(self, videoViews):
        if self.indexSavePath is not None:
            with open(self.indexSavePath, 'w') as outFd:
                cPickle.dump(videoViews, outFd)
                
    def load(self, indexSaveFile):
        with open(indexSaveFile, 'r') as inFd:
            self.videoViews = cPickle.load(inFd)

    def setVideo(self, videoId):
        try:
            self.activeFootprintDict = self.videoViews[videoId]
        except KeyError:
            raise ValueError("Video '%s' is not part of this footprint index." % videoId)
    


    # --------------------------------- Dict Method Implementations ------------------
    
    def __getitem__(self,key):
        try:
            (videoId,second) = key
        except ValueError:
            # Key is not a tuple; is activeFootprintDict
            # set to provide context? If so, interpret
            # the non-tuple key as a seconds-into-video specifier:
            if self.activeFootprintDict is not None:
                return self.activeFootprintDict[key]
            else:
                raise ValueError("Key into index must be a tuple (videoId, theSecond), or must first call setVideo(videoId); was '%s'" % str(key))
        return self.videoViews[videoId][second]
    
    def __setitem__(self,key, value):
        raise NotImplementedError("Video footprint index does not allow updates.")
    
    def __len__(self):
        if self.activeFootprintDict is not None:
            return len(self.activeFootprintDict)
        return len(self.videoViews)
    
    def __iter__(self):
        if self.activeFootprintDict is not None:
            return self.activeFootprintDict.__iter__()
        return self.videoViews.__iter__()
    
    def __delitem__(self, key):
        raise NotImplementedError("Video footprint index does not allow deletion.")
    
    def videos(self):
        '''
        Return a list of videos that are covered in this index
        
        :return list of video identifiers
        :rtype [str]
        '''
        return self.videoViews.keys()

    # --------------------------------- Logging ------------------
    
    def log(self, msg):
        print('%s: %s' %  (str(datetime.datetime.now()), msg))
        sys.stdout.flush()
        
    def logErr(self, msg):
        sys.stderr.write('     %s: %s\n' %  (str(datetime.datetime.now()), msg))
        sys.stderr.flush()

if __name__ == '__main__':
    
    
    footprintIndex = VideoFootPrintIndex(viewEventsCSVFile='/tmp/medstatsVideoUse.csv', 
                                             alignmentFile='/tmp/medstatsAlignment.csv',
                                             indexSavePath='/tmp/medstatsIndex')
    footprintIndex.computeFootprints()
    pass
