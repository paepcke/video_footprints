'''
Created on Jan 15, 2015

@author: paepcke

Todo:
   - add partition

Must deal with pause time less than start-play time:
"00262c4fde75f8c90f4498645fd8ff25401cf211","load_video","i4x-Medicine-MedStats-video-2db4f6a3ecac4a94816f3aef385eedb5","None","","","2014-07-05 22:01:08"
"00262c4fde75f8c90f4498645fd8ff25401cf211","load_video","i4x-Medicine-MedStats-video-2db4f6a3ecac4a94816f3aef385eedb5","None","","","2014-07-05 22:01:09"
"00262c4fde75f8c90f4498645fd8ff25401cf211","play_video","i4x-Medicine-MedStats-video-2db4f6a3ecac4a94816f3aef385eedb5","258.76334","","","2014-07-05 23:41:33"
---> "00262c4fde75f8c90f4498645fd8ff25401cf211","pause_video","i4x-Medicine-MedStats-video-2db4f6a3ecac4a94816f3aef385eedb5","238.626614","","","2014-07-05 23:45:32"
"00262c4fde75f8c90f4498645fd8ff25401cf211","play_video","i4x-Medicine-MedStats-video-2db4f6a3ecac4a94816f3aef385eedb5","238.626614","","","2014-07-05 23:45:52"
"00262c4fde75f8c90f4498645fd8ff25401cf211","pause_video","i4x-Medicine-MedStats-video-2db4f6a3ecac4a94816f3aef385eedb5","504.257887","","","2014-07-05 23:50:18"
"00262c4fde75f8c90f4498645fd8ff25401cf211","play_video","i4x-Medicine-MedStats-video-2db4f6a3ecac4a94816f3aef385eedb5","504.257887","","","2014-07-05 23:53:32"

Must deal with play start time being None sometimes:
"03ebe27e26838dac813e733ec09aee928fcec126","play_video","i4x-Medicine-MedStats-video-04cdeb59117b42c19e6e55a47265ed38","11.733333","","","2014-07-02 08:15:56"
"03ebe27e26838dac813e733ec09aee928fcec126","load_video","i4x-Medicine-MedStats-video-04cdeb59117b42c19e6e55a47265ed38","None","","","2014-07-02 08:17:02"
"03ebe27e26838dac813e733ec09aee928fcec126","load_video","i4x-Medicine-MedStats-video-04cdeb59117b42c19e6e55a47265ed38","None","","","2014-07-02 08:19:09"
--->"03ebe27e26838dac813e733ec09aee928fcec126","play_video","i4x-Medicine-MedStats-video-04cdeb59117b42c19e6e55a47265ed38","None","","","2014-07-02 09:05:50"
"03ebe27e26838dac813e733ec09aee928fcec126","seek_video","i4x-Medicine-MedStats-video-04cdeb59117b42c19e6e55a47265ed38","","19.333333","0","2014-07-02 09:05:50"
"03ebe27e26838dac813e733ec09aee928fcec126","play_video","i4x-Medicine-MedStats-video-04cdeb59117b42c19e6e55a47265ed38","19.333333","","","2014-07-02 09:05:51"
"03ebe27e26838dac813e733ec09aee928fcec126","pause_video","i4x-Medicine-MedStats-video-04cdeb59117b42c19e6e55a47265ed38","16.333333","","","2014-07-02 09:06:08"
"03ebe27e26838dac813e733ec09aee928fcec126","play_video","i4x-Medicine-MedStats-video-04cdeb59117b42c19e6e55a47265ed38","16.333333","","","2014-07-02 09:06:29"

Must deal with seek being temporarily unstable (time is None):
"0a0f64f455cb2e78300bf54336de42bce6a52a74","pause_video","i4x-Medicine-MedStats-video-af00b19971d7442886e1f79a64424f29","661.420416","","","2014-06-27 23:35:21"
"0a0f64f455cb2e78300bf54336de42bce6a52a74","load_video","i4x-Medicine-MedStats-video-af2a429134c640c7810c9f3f9cf33f76","None","","","2014-06-26 22:15:23"
"0a0f64f455cb2e78300bf54336de42bce6a52a74","load_video","i4x-Medicine-MedStats-video-af2a429134c640c7810c9f3f9cf33f76","None","","","2014-06-26 22:25:51"
"0a0f64f455cb2e78300bf54336de42bce6a52a74","play_video","i4x-Medicine-MedStats-video-af2a429134c640c7810c9f3f9cf33f76","0","","","2014-06-26 22:25:55"
--> "0a0f64f455cb2e78300bf54336de42bce6a52a74","seek_video","i4x-Medicine-MedStats-video-af2a429134c640c7810c9f3f9cf33f76","","None","748","2014-06-26 22:25:55"
--> "0a0f64f455cb2e78300bf54336de42bce6a52a74","seek_video","i4x-Medicine-MedStats-video-af2a429134c640c7810c9f3f9cf33f76","","0","705","2014-06-26 22:25:58"
"0a0f64f455cb2e78300bf54336de42bce6a52a74","seek_video","i4x-Medicine-MedStats-video-af2a429134c640c7810c9f3f9cf33f76","","0","705","2014-06-26 22:25:59"
"0a0f64f455cb2e78300bf54336de42bce6a52a74","load_video","i4x-Medicine-MedStats-video-af2a429134c640c7810c9f3f9cf33f76","None","","","2014-06-26 22:26:26"



'''
import argparse
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
                 skipEventsCSVLines = 0,
                 alignmentFile = None,
                 skipAlignmentCSVLines = 0,
                 indexSavePath = None,
                 specialLearnersList = [],
                 dbHost='localhost', 
                 mySQLUser=None, 
                 mySQLPwd=None 
                ):
        
        if type(specialLearnersList) != list:
            raise ValueError("Special learners list must be a list; was '%s'" % str(specialLearnersList))
        
        self.viewEventsCSVFile = viewEventsCSVFile
        self.alignmentFile     = alignmentFile
        self.indexSavePath = indexSavePath
        self.specialLearnersList   = specialLearnersList
        self.currAnonScreenName    = None
        self.skipEventsCSVLines    = skipEventsCSVLines
        self.skipAlignmentCSVLines = skipAlignmentCSVLines
        
        # We'll need access to the MySQL db
        # if we have to create the index or alignment
        # file, and no previously built index file
        # exists. If an index file exists, it has all
        # needed info:
        #if (viewEventsCSVFile is None or alignmentFile is None) and \
        if (indexSavePath is None or not os.path.exists(indexSavePath) or os.path.getsize(indexSavePath) < 10):
            self.dbHost = dbHost
            self.dbName = 'Edx'
            self.mySQLUser = mySQLUser
            self.mySQLPwd  = mySQLPwd
            if mySQLUser is None:
                self.mySQLUser = getpass.getuser()
            if mySQLPwd is None:
                # Try to get it from .ssh/mysql file of user
                try:
                    homeDir = os.path.expanduser('~' + self.mySQLUser)
                    pwdFile = os.path.join(homeDir,'.ssh/mysql')
                    with open(pwdFile, 'r') as fd:
                        self.mySQLPwd = fd.readline().strip()
                except Exception:
                    self.mySQLPwd = ''
                
            self.db = MySQLDB(host=self.dbHost, user=self.mySQLUser, passwd=self.mySQLPwd, db='Edx')

        self.activeFootprintDict = None
        # Dict mapping video_id to array.
        # each array element contains the 
        # view counts of a particular minute
        # in the video:
        self.videoViews = {}
        self.videoLengths = {}
        # Similar dict, but where only actions by selected
        # learners will be counted (the ones from the learnerList):
        self.videoViewsSpecialLearners = {}
        
        if indexSavePath is not None and os.path.exists(indexSavePath):
            self.log("Using existing index file '%s'" % indexSavePath)
            self.loadIndex(indexSavePath)
    
    # ----------------------------- Public Methods Other than Dict Behaviors -------------------
                
    # NOTE: after creating the instance of this class with 
    #       an existing index file given, only the usual
    #       dict methods should be needed:
    
    def loadIndex(self, indexSaveFile):
        '''
        Load an existing video footprint index into memory.
        This method is called by the constructor, but can
        be called later to load a different index.
        
        :param indexSaveFile: Path to the pickled dict
        :type indexSaveFile: string
        '''
        with open(indexSaveFile, 'r') as inFd:
            (self.videoViews, self.videoLengths) = cPickle.load(inFd)

    def setVideo(self, videoId):
        try:
            self.activeFootprintDict = self.videoViews[videoId]
        except KeyError:
            raise ValueError("Video '%s' is not part of this footprint index." % videoId)

    def videos(self):
        '''
        Return a list of videos that are covered in this index
        
        :return list of video identifiers
        :rtype [str]
        '''
        return self.videoViews.keys()
    
    def videoHeatValues(self, videoId=None):
        '''
        Return an array of two-column CSV strings: "second,numViews"
        for one video. The video is either specified in the parameter,
        or a prior call to setVideo() specified a default.
        
        :param videoId: ID of video for which to create a CSV string array.
            If None, must have set default via setVideo() ahead of time.
        :type videoId: string
        :raise ValueError if neither the parameter or the default is available.
        '''
        if videoId is not None:
            csvValues = [str(x) + ',' + str(y) + '\n' for x,y in self[videoId].items()]
            return csvValues
        if self.activeFootprintDict is None:
            raise ValueError('Must either call setVideo(<videoId>), or provide parameter videoId in call to videoHeatValues().')
        csvValues = ['%s,%s\n' % (str(x),str(y)) for x,y in self.activeFootprintDict.items()]
                    
        return csvValues
    
    def createIndex(self, courseDisplayName):
        '''
        Create a footprint index for an entire course.
         
        :param courseDisplayName: Platform name of the course as known to the databases (course_display_name)
        :type courseDisplayName: string
        '''
        self.computeFootprints(courseDisplayName)
    
    # ------------------- Main Implementation Methods (Private) ------------------------    
    
    def initPlayheadAlignments(self, alignmentFile=None):
        if alignmentFile is None:
            raise NotImplementedError("Auto-computation of playhead alignment not implemented.")
        alignmentDict = {}
        with open(alignmentFile, 'r') as alignmentFd:
            
            # Skip column header(s) if any:
            for colHeaderCount in range(self.skipAlignmentCSVLines): #@UnusedVariable
                alignmentFd.readline()
            
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

        if len(self.videoViews) != 0:
            self.logErr('A video footprint index is already loaded; to make a new index into the same file, ' +\
                        'remove the index file, and make a new VideoFootPrintIndex instance.\n' +\
                        "The existing index file used was '%s'" % self.indexSavePath)
            return
        
        event_type = None      
        currVideoId = None
        self.currVideoLength = None
        # Current playhead position of current video
        currTime    = 0
        # Some videos start at a negative number
        # of seconds. The self.alignmentFile contains
        # those offsets for each video:
        currVideoZeroTimeOffset = 0
        self.resetPlaying()

        # Dict in which each element is a counter
        # for views of one minute:
        currVideoTimeDict = None
        
        # Dict in which each element is a counter,
        # just as in currVideoTimeDict, but this
        # one is to count separately for special
        # learners. We make that dict an instance
        # var b/c it was added later, and this makes
        # it simpler to integrate into the existing code:
        self.currVideoTimeDictLearners = None
        
        if self.viewEventsCSVFile is None:
            self.viewEventsCSVFile  = tempfile.NamedTemporaryFile(prefix='%s' % courseDisplayName.replace('/','_'), 
                                                                  suffix='_video_action.csv',
                                                                  delete=False)
            self.viewEventsCSVFile.close()
            self.viewEventsCSVFile = self.viewEventsCSVFile.name
            self.log('About to start video activity query...')
#            mysqlCmd = "SELECT anon_screen_name, event_type, video_id \
#                          INTO OUTFILE '%s' \
#                        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' \
#                          FROM EdxTrackEvent \
#                         WHERE event_type = 'play_video' \
#                            OR event_type = 'pause_video' \
#                            OR event_type = 'stop_video' \
#                            OR event_type = 'seek_video' \
#                           AND course_display_name = '%s' \
#                         ORDER BY video_id, anon_screen_name;" % (self.viewEventsCSVFile, courseDisplayName)

            # The event_time below is not strictly needed,
            # and is included for debugging: 
            mysqlCmd = "SELECT anon_screen_name, \
                               event_type, video_id, \
                               video_current_time, \
                               video_old_time, \
                               video_new_time, \
                               time AS event_time \
                          INTO OUTFILE '%s' \
                        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' \
                          FROM EdxTrackEvent \
                         WHERE course_display_name = '%s' \
                         ORDER BY anon_screen_name, video_id, time;" % (self.viewEventsCSVFile, courseDisplayName)
            
            self.db.query(mysqlCmd)
            self.log('Done video activity query...')

        # If no alignment file was provided, create it now:
        if self.alignmentFile is None:
            self.alignmentFile = tempfile.NamedTemporaryFile(prefix='%s' % courseDisplayName.replace('/','_'), 
                                                                  suffix='_alignment.csv',
                                                                  delete=False)
            self.alignmentFile.close()
            self.alignmentFile = self.alignmentFile.name
            self.log('About to find start time offset for all videos (calibration)...')
            mysqlCmd = "SELECT video_id, MIN(CAST(video_current_time AS SIGNED INTEGER)) \
                          INTO OUTFILE '%s' \
                          FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' \
                          FROM EdxTrackEvent PARTITION (pAY2013_Summer) \
                          WHERE course_display_name = '%s' \
                            AND video_id != '' \
                          GROUP BY video_id;" % (self.alignmentFile, courseDisplayName)
            self.db.query(mysqlCmd)
            self.log("Done creating playhead time calibration")
        
        # Create a dict: video_id --> start-time offset
        alignmentDict = self.initPlayheadAlignments(self.alignmentFile)
        
        # From the footprint file get one line after another:
        #    anon_screen_name, event_type, video_id
           
        with open(self.viewEventsCSVFile, 'r') as fd:
            # Skip column header(s) if any:
            for colHeaderCount in range(self.skipEventsCSVLines): #@UnusedVariable
                fd.readline()
                
            for line in fd:
                (anon_screen_name,
                 event_type, 
                 video_id,
                 video_current_time,
                 video_old_time,
                 video_new_time,
                 event_time) = line.split(',')  #@UnusedVariable
                 
                event_type          	  = event_type.strip('"')
                # If event type isn't a video event, assume viewing
                # has stopped:
                if event_type not in ['play_video', 'pause_video', 'stop_video', 'seek_video']:
                    self.resetPlaying()
                    continue
                
                video_id            	  = video_id.strip('"')
                anon_screen_name          = anon_screen_name.strip('"')
                
                # If we transitioned to a different learner,
                # reset 'self.playing.' Without a pause/stop from 
                # the old learner we ignore his final play:
                if anon_screen_name != self.currAnonScreenName:
                    # If previous learner was playing the video, we
                    # assume the video ran to the end. Remember: unclear
                    # whether an automatic stop_video event truly occurs at the 
                    # end of each video:
                    self.resetPlaying(currVideoTimeDict)
                    self.currAnonScreenName = anon_screen_name

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
                
                # Take care of time-slider-equipped video players;
                # they spew many play events in a short time:
                if self.playing and \
                    event_type == 'play_video' and \
                    video_id   == currVideoId and \
                    anon_screen_name == self.currAnonScreenName:
                    currTime = video_new_time
                    continue
                    
                # Take care of None in current time when event
                # is play_video (see file header):
                if event_type == 'play_video' and video_current_time is None:
                    self.resetPlaying()
                    continue
                
                if video_id != currVideoId:
                    # All done with one video watched by one learner
                    self.videoViews[currVideoId] = currVideoTimeDict
                    currVideoId = video_id
                    currTime   = 0
                    self.getVideoLen(video_id)
                    try:
                        currVideoZeroTimeOffset = -1 * alignmentDict[video_id]
                    except KeyError:
                        currVideoZeroTimeOffset = 0
                    try:
                        currVideoTimeDict = self.videoViews[currVideoId]
                    except KeyError:
                        # Never encountered this video. Put
                        # empty minutes dict for this video into dict:
                        self.videoViews[currVideoId] = currVideoTimeDict = {}
                    # Same for special-learners dict:
                    try:
                        self.currVideoTimeDictLearners = self.videoViewsSpecialLearners[currVideoId]
                    except KeyError:
                        # Never encountered this video. Put
                        # empty minutes dict for this video into dict:
                        self.videoViewsSpecialLearners[currVideoId] = self.currVideoTimeDictLearners = {}

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
                    self.setPlaying(video_current_time)
                    currTime = video_current_time
                    
                elif event_type == 'pause_video':
                    if not type(video_current_time) == int:
                        self.log("Pause event without, or with bad current time: '%s'" % line)
                        continue
                    # The conditional takes care of pause appearing to occur
                    # earlier than the start-play time (see file header):
                    pauseRes = self.handlePauseVideo(currTime, video_current_time, currVideoTimeDict)
                    if pauseRes is None:
                        self.resetPlaying()
                        continue
                    currVideoTimeDict = pauseRes
                    currTime = video_current_time
                    continue
                
                elif event_type == 'seek_video':
                    if type(video_new_time) != int:
                        self.log("Seek event without, or with bad new time: '%s'" % line)
                        self.resetPlaying()
                        continue
                    if type(video_old_time) != int:
                        self.log("Seek event without, or with bad old time: '%s'" % line)
                        self.resetPlaying()
                        continue
                        
                    currVideoTimeDict = self.handleSeekVideo(currTime, self.playing, video_old_time, currVideoTimeDict)
                    currTime = video_new_time
                    
                elif event_type == 'stop_video':
                    if not type(video_current_time) == int:
                        self.log("Stop event without, or with bad current time: '%s'" % line)
                        continue
                    self.handleStopVideo(currTime, self.playing, video_current_time, currVideoTimeDict)
                    self.resetPlaying()
                    currTime = video_new_time  # not really relevant, but to be sure...                    
                    
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
        :return: the updated videoTimeDict. If an anomaly was encountered where the
                 current time is larger than the pause time (i.e. the video seems
                 to have run backward), we return None.
        :rtype {float --> int  |  None}
        '''
        # Credit the minutes to the current video:
        if pauseTime < currTime:
            # raise ValueError('New time (%s) less than old time (%s) in pause' % (pauseTime, currTime))
            return None
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
    # ------------------------------------------ Utilities ---------------------------
    
    def getVideoLen(self, videoId):
        
        try:
            return self.videoLengths[videoId]
        except KeyError:
            pass
        self.log('Query video length for %s' % videoId)
        mysqlQuery = "SELECT MAX(CAST(video_current_time AS DECIMAL(7,3))) \
                     FROM EdxTrackEvent \
                     WHERE course_display_name = 'Medicine/MedStats/Summer2014' \
                     AND video_code = '%s' \
                     AND video_current_time != 'None';" % videoId
        vidLen = self.db.query(mysqlQuery).next()[0]
        self.log('Video length for %s is %s' % (videoId, str(vidLen)))
        self.currVideoLength = vidLen
        # For saving in method finish()
        self.videoLengths[videoId] = vidLen
        
    
    def resetPlaying(self, currVideoTimeDict=None):
        '''
        Remember that playback just stopped.
        '''
    
        if currVideoTimeDict is not None:
            self.creditEstimatedPlaytime(currVideoTimeDict)    
        self.playing = False
        
    def setPlaying(self, startTimeVideoContext):
        '''
        Flag to remember that video just started playing.
        
        :param startTimeVideoContext: time in fractions of second into the video where start occurred
        :type startTimeVideoContext: float
        '''
        self.playStartTimeVideo = startTimeVideoContext
        self.playing = True
        
    def creditEstimatedPlaytime(self, currVideoTimeDict):
        if not self.playing or self.currVideoLength is None or self.playStartTimeVideo is None:
            return
        self.creditTime(currVideoTimeDict, self.playStartTimeVideo, self.currVideoLength)
        
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
        currLearnerIsSpecial = self.currAnonScreenName in self.specialLearnersList
        while (theTime <= stopTime):
            # Add time to all appropriate slots in 
            # the overall videoViews dict:
            try:
                viewCount = videoTimeDict[theTime]
            except KeyError:
                viewCount = 0
            videoTimeDict[theTime] = viewCount + 1
            theTime += VideoFootPrintIndex.timeResolution
            
            # If the current learner is one of the special
            # learners for which we are to keep track separately:
            if currLearnerIsSpecial:
                try:
                    # The '-1' is to compensate for the already above incremented
                    # 'theTime' value:
                    viewCount = self.currVideoTimeDictLearners[theTime-1]
                except KeyError:
                    viewCount = 0
                self.currVideoTimeDictLearners[theTime] = viewCount + 1

        return videoTimeDict

    # --------------------------------- Persistence ------------------
    
    def finish(self, videoViews):
        if self.indexSavePath is not None:
            with open(self.indexSavePath, 'w') as outFd:
                cPickle.dump((videoViews, self.videoLengths), outFd)

    # --------------------------------- Dict Method Implementations ------------------
    
    def __getitem__(self,key):
        try:
            (videoId,second) = key
        except (ValueError,TypeError):
            # Key is not a tuple; is activeFootprintDict
            # set to provide context? If so, interpret
            # the non-tuple key as a seconds-into-video specifier:
            if self.activeFootprintDict is not None:
                return self.activeFootprintDict[key]
            else:
                # Key is not a seconds number,
                # assume the key is a video id.
                # Return the view frequency dict of that id:
                return self.videoViews[key]
                #raise ValueError("Key into index must be a tuple (videoId, theSecond), or must first call setVideo(videoId); was '%s'" % str(key))
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
    
    # --------------------------------- Logging ------------------
    
    def log(self, msg):
        print('%s: %s' %  (str(datetime.datetime.now()), msg))
        sys.stdout.flush()
        
    def logErr(self, msg):
        sys.stderr.write('     %s: %s\n' %  (str(datetime.datetime.now()), msg))
        sys.stderr.flush()

if __name__ == '__main__':
    
        # -------------- Manage Input Parameters ---------------
    
    usage = 'Usage: video_footprint_index \n'

    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-u', '--user',
                        action='store',
                        help='User ID that is to log into MySQL. Default: the user who is invoking this script.')
    parser.add_argument('-p', '--pwd',
                        action='store_true',
                        help='Request to be asked for pwd for operating MySQL;\n' +\
                             '    default: content of scriptInvokingUser$Home/.ssh/mysql if --user is unspecified,\n' +\
                             '    or, if specified user is root, then the content of scriptInvokingUser$Home/.ssh/mysql_root.'
                        )
    parser.add_argument('-w', '--password',
                        action='store',
                        help='User explicitly provided password to log into MySQL.\n' +\
                             '    default: content of scriptInvokingUser$Home/.ssh/mysql if --user is unspecified,\n' +\
                             '    or, if specified user is root, then the content of scriptInvokingUser$Home/.ssh/mysql_root.'
                        )
    parser.add_argument('-v', '--videoOnly', 
                        help='Only consider video events as engagement (default: consider all types).', 
                        dest='videoOnly',
                        default=False,
                        action='store_true');
    parser.add_argument('course',
                        action='store',
                        help='The course for which engagement is to be computed. Else: engagement for all courses.\n' +\
                             "To have engagement computed for all courses, use All"
                        ) 
    
    # Optionally: any number of years as ints:
    parser.add_argument('years',
                        nargs='*',
                        type=int,
                        help='A list of start years (YYYY) to limit the courses that are computed. Leave out if all start years are acceptable'
                        ) 
    
    
    args = parser.parse_args();
    if args.user is None:
        user = getpass.getuser()
    else:
        user = args.user
        
    if args.password and args.pwd:
        raise ValueError('Use either -p, or -w, but not both.')
        
    if args.pwd:
        pwd = getpass.getpass("Enter %s's MySQL password on localhost: " % user)
    elif args.password:
        pwd = args.password
    else:
        # Try to find pwd in specified user's $HOME/.ssh/mysql
        currUserHomeDir = os.getenv('HOME')
        if currUserHomeDir is None:
            pwd = None
        else:
            # Don't really want the *current* user's homedir,
            # but the one specified in the -u cli arg:
            userHomeDir = os.path.join(os.path.dirname(currUserHomeDir), user)
            try:
                if user == 'root':
                    with open(os.path.join(currUserHomeDir, '.ssh/mysql_root')) as fd:
                        pwd = fd.readline().strip()
                else:
                    with open(os.path.join(userHomeDir, '.ssh/mysql')) as fd:
                        pwd = fd.readline().strip()
            except IOError:
                # No .ssh subdir of user's home, or no mysql inside .ssh:
                pwd = ''
    
    if args.course.lower() == 'all':
        courseName = None
    else:
        courseName = args.course
    
    if len(args.years) == 0 or args.years[0] == 0:
        years = None
    else:
        years = args.years

# ==============    
#     footprintIndex = VideoFootPrintIndex(viewEventsCSVFile='/tmp/medstatsVideoFootprintUseAnonSortedChopped.csv', 
#                                              alignmentFile='/tmp/medstatsVideoFootprintAlignment.csv',
#                                              indexSavePath='/tmp/medstatsVideoFootprintIndex')

#     footprintIndex.computeFootprints()
#     pass
