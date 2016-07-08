'''
Created on Jan 15, 2015

@author: paepcke

Sijun He created this modified version of video_footprint_index.py
to create an index for every learner into every video, second by
second. As opposed to the slighly aggregated index of the original.

Here Sijun's summary of his changes:

  In your script, you have self.videoViews as a dictionary, with the
  keys being the video ID and the values being currVideoTimeDict for
  the specific video. The key change I made was to change the keys of
  self.videoViews to be a tuple of the video ID and the AnonScreenName
  (videoId, AnonScreenName). The rest follows your logic and I save
  the current currVideoTimeDict and create a new empty
  currVideoTimeDict whenever videoId or AnonScreenName is
  different. Some other minor changes was made but I can't exactly
  recall.

  I also verified the correctness of my script this afternoon by
  comparing the sum of all individual profiles for the first video
  against the video profile formed by your script. The difference is
  negligible.

------
Class that builds heatmaps for all videos in a course. 
Used it stand-alone from the command line, or import 
into another application. In this case, the application
instantiates class VideoFootPrintIndex. The resulting
instance behaves like a dictionary that holds results.
The dict mapps a video_id to an array. Each array element 
contains the view counts of a particular second
in the respective video.

Takes a course triplet, and writes the heatmaps as a csv
file to /tmp. Prints name of that file in the end.

Normally, he program needs access to the MySQL database with the
Edx tracking events. This access is accomplished in one
of three ways:
   - If used from an application, pass keywords mySQLUser,
     and mySQLPwd.
   - If used from the command line, you can pass 
     the -u and -p options, similar to the mysql command:
     -u <MySQL user name>; the -p will prompt for a pwd.
   - If $HOME/.ssh/mysql exists and contains a pwd, that
     pwd is used for MySQL. The user who invokes this script
     will be used as the MySQL user.

It is possible to cause the script to save the dictionary
it creates in a file, and to reuse it later. Accomplish this
by using CLI option -i, passing a file name, including directory.
If instantiating the class, pass the file name in the keyword 
parameter indexSavePath.

When such a saved index file is available, the script does
not need access to MySQL, and processing is very fast.


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
import copy
import datetime
import getpass
import os
import sys
import tempfile
import csv




from pymysql_utils.pymysql_utils  import MySQLDB


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
        # Each array element contains the 
        # view counts of a particular second
        # in the video:
        self.videoViews = {}
        self.videoLengths = {}
        
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
    
    def videoHeatAll(self, outfileName):
        '''
        :param outfileName:
        :type outfileName:
        '''
        
        with open(outfileName, 'w') as outFd:
            outFd.write('videoId,anon_screen_name,second,numViews\n')
            for videoId in self.videoViews.keys():
                # Get ["1,10\n",'2,30\n",...]:
                secondNumViewsStrArr = self.videoHeatValues(videoId)
                for secondNumViewsStr in secondNumViewsStrArr:
                    (second,numViews) = secondNumViewsStr.strip().split(',')
                    outFd.write('%s,%s,%s,%s\n' % (videoId[0],videoId[1],second,numViews))
                 
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
    
    def createIndex(self, courseDisplayName, partition=None):
        '''
        Create a footprint index for an entire course.
         
        :param courseDisplayName: Platform name of the course as known to the databases (course_display_name)
        :type courseDisplayName: string
        :param partition: if known, the table partition where the course resides. Example: 'pAY2013_Summer'
        :type partition: string 
        '''
        self.computeFootprints(courseDisplayName, partition)
    
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
    
    def computeFootprints(self, courseDisplayName=None, partition=None):
        '''
        Create dict mapping each video id of a course to 
        a dict that maps floating point time codes to the
        number of views of that section of video. If courseDisplayName
        is None, it is assumed that self.viewEventsCSVFile is the
        path to a file with rows (anon_screen_name, event_type, video_id, video_current_time, video_old_time, video_new_time)

        :param courseDisplayName: course whose videos are to be profiled
        :type courseDisplayName: string
        :param partition: if known, the table partition where the course resides. Example: 'pAY2013_Summer'
        :type partition: string 
        '''

        if len(self.videoViews) != 0:
            self.log('The existing video footprint index file  (%s) has been loaded; to instead make a new ' % self.indexSavePath +\
                     'index with the same file, remove the index file, and make a new VideoFootPrintIndex instance.\n')
            return
        
        event_type = None      
        currVideoId = None
        self.currVideoLength = None
        self.courseDisplayName = courseDisplayName
        # Current playhead position of current video
        currTime    = 0
        # Some videos start at a negative number
        # of seconds. The self.alignmentFile contains
        # those offsets for each video:
        currVideoZeroTimeOffset = 0
        self.resetPlaying()

        # Dict in which each element is a counter
        # for views of one minute:
        currVideoTimeDict = {}
        
        if self.viewEventsCSVFile is None:
            self.viewEventsCSVFile  = tempfile.NamedTemporaryFile(prefix='%s_' % courseDisplayName.replace('/','_'), 
                                                                  suffix='_video_action.csv',
                                                                  delete=False)
            self.viewEventsCSVFile.close()
            self.viewEventsCSVFile = self.viewEventsCSVFile.name
            os.remove(self.viewEventsCSVFile)

            self.log('About to start video activity query...')

            # The event_time below is not strictly needed,
            # and is included for debugging: 
            mysqlCmd = "SELECT anon_screen_name, \
                               event_type, \
                               video_id, \
                               video_current_time, \
                               video_old_time, \
                               video_new_time, \
                               time AS event_time \
                          INTO OUTFILE '%s' \
                        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' \
                          FROM EdxTrackEvent %s \
                         WHERE course_display_name = '%s' \
                         ORDER BY anon_screen_name, video_id, time;" % (self.viewEventsCSVFile, 'PARTITION ('+partition+')' if partition is not None else '', courseDisplayName)
            #*************                         
            #print('Query: %s' % mysqlCmd)
            #*************
            
            try:
                self.db.query(mysqlCmd).next()
            except StopIteration:
                pass
            self.log('Done video activity query...')

        # If no alignment file was provided, create it now:
        if self.alignmentFile is None:
            self.alignmentFile = tempfile.NamedTemporaryFile(prefix='%s_' % courseDisplayName.replace('/','_'), 
                                                                  suffix='_alignment.csv',
                                                                  delete=False)
            self.alignmentFile.close()
            self.alignmentFile = self.alignmentFile.name
            os.remove(self.alignmentFile)

            self.log('About to find start time offset for all videos (calibration)...')

            mysqlCmd = "SELECT video_id, MIN(CAST(video_current_time AS SIGNED INTEGER)) \
                           INTO OUTFILE '%s' \
                           FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' \
                           FROM EdxTrackEvent %s \
                           WHERE course_display_name = '%s' \
                             AND video_id != '' \
                           GROUP BY video_id;" % (self.alignmentFile, 'PARTITION ('+partition+')' if partition is not None else '',courseDisplayName)
            try:
                self.db.query(mysqlCmd).next()
            except StopIteration:
                pass
            self.log("Done creating playhead time calibration")
        
        # Create a dict: video_id --> start-time offset
        alignmentDict = self.initPlayheadAlignments(self.alignmentFile)
        
        # From the footprint file get one line after another:
        #    anon_screen_name, event_type, video_id
           
        with open(self.viewEventsCSVFile, 'r') as fd:
            # Skip column header(s) if any:
            for colHeaderCount in range(self.skipEventsCSVLines): #@UnusedVariable
                fd.readline()
            csv_reader = csv.reader(fd)
            for line in csv_reader:
                try:
                    (anon_screen_name,
                     event_type, 
                     video_id,
                     video_current_time,
                     video_old_time,
                     video_new_time,
                     event_time) = line  #@UnusedVariable
                except ValueError as e:
                    self.logErr("While reading line after '%s': %s" % (line, `e`))
                    continue
                event_type                = event_type.strip('"')
                # If event type isn't a video event, assume viewing
                # has stopped:
                if event_type not in ['play_video', 'pause_video', 'stop_video', 'seek_video']:
                    self.resetPlaying()
                    continue
                
                video_id                  = video_id.strip('"')
                if video_id is None:
                    continue
                anon_screen_name          = anon_screen_name.strip('"')
                # If we transitioned to a different learner,
                # reset 'self.playing.' Without a pause/stop from 
                # the old learner we ignore his final play:

                try:
                    video_current_time = 0 if video_current_time.startswith('""') else int(round(float(video_current_time.strip('"\n'))))
                except ValueError:
                    if video_current_time.startswith('"None'):
                        video_current_time = None
                except OverflowError:
                    video_current_time = None
                try:
                    video_old_time     = 0 if video_old_time.startswith('""') else int(round(float(video_old_time.strip('"\n'))))
                except ValueError:
                    if video_old_time.startswith('"None'):
                        video_old_time = None 
                except OverflowError:
                    video_old_time = None
                        
                try:
                    video_new_time     = 0 if video_new_time.startswith('""') else int(round(float(video_new_time.strip('"\n'))))
                except ValueError:
                    if video_new_time.startswith('"None'):
                        video_new_time = None 
                except OverflowError:
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
                
                if video_id != currVideoId or anon_screen_name != self.currAnonScreenName:
                    # All done with one video watched by one learner
                    self.resetPlaying(currVideoTimeDict)
                    if currVideoId is not None:
                        self.videoViews[(currVideoId,self.currAnonScreenName)] = copy.copy(currVideoTimeDict)

                    currVideoId = video_id
                    self.currAnonScreenName = anon_screen_name
                    currTime   = 0
                    
                    
                    tmpVideoLen = self.getVideoLen(video_id, partition)
                    if tmpVideoLen is None:
                        self.logErr('Video %s in course %s seems to have no length; skipping event.' % (self.courseDisplayName, video_id))
                        continue
                    else:
                        self.currVideoLength = tmpVideoLen
                    try:
                        currVideoZeroTimeOffset = -1 * alignmentDict[video_id]
                    except KeyError:
                        currVideoZeroTimeOffset = 0
                    try:
                        currVideoTimeDict = copy.copy(self.videoViews[(currVideoId,self.currAnonScreenName)])
                    except KeyError:
                        # Never encountered this video. Put
                        # empty minutes dict for this video into dict:
                        self.videoViews[(currVideoId,self.currAnonScreenName)] = currVideoTimeDict = {}
                        

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
            # Account for final event of final learner, if needed:
            self.resetPlaying(currVideoTimeDict)
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
    
    def getVideoLen(self, videoId, partition=None):
        
        try:
            return self.videoLengths[videoId]
        except KeyError:
            pass
        self.log('Query video length for %s' % videoId)
        mysqlQuery = "SELECT MAX(CAST(video_current_time AS DECIMAL(7,3))) \
                     FROM EdxTrackEvent %s \
                    WHERE video_id = '%s' \
                     AND video_current_time != 'None';" % ('PARTITION ('+partition+')' if partition is not None else '', videoId)
        vidLen = self.db.query(mysqlQuery).next()[0]
        self.log('Video length for %s is %s' % (videoId, str(vidLen)))
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
        while (theTime <= stopTime):
            # Add time to all appropriate slots in 
            # the overall videoViews dict:
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
        return self.videoViews[key]
    
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
        
    #*********************
#     def excerptVideoViews(self, comment):
#         print("Excerpting from videoViews during collection: %s" % comment)
#         for videoId in self.videoViews:
#             print("%s (1): %s" % (videoId, self.videoViews[videoId][0]))
#             print("%s (2): %s" % (videoId, self.videoViews[videoId][1]))
#             print("%s (3): %s" % (videoId, self.videoViews[videoId][2]))
    #*********************    

if __name__ == '__main__':
    
        # -------------- Manage Input Parameters ---------------
    
    #usage = 'Usage: video_footprint_index \n'

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
    parser.add_argument('-i', '--indexfile',
                        action='store',
                        default=None,
                        help="File where index is to be stored for later use, or existing index file to use."
                        )
    parser.add_argument('-r', '--partition',
                        action='store',
                        default=None,
                        help="Disk partition where course resides; e.g. 'pAY2013_Summer'.\n"
                        )
    parser.add_argument('course',
                        action='store',
                        help='The course for which engagement is to be computed. Else: engagement for all courses.\n' +\
                             "To have engagement computed for all courses, use All"
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
                
    indexFile = args.indexfile
    courseDisplayName = args.course
    resultFilePrefix = '/tmp/heatMaps_Individual_%s' % courseDisplayName.replace('/','_')
    indexFileDest    = '%s_VideoFootprintIndex.pkl' % resultFilePrefix
    footprintIndex = VideoFootPrintIndex(indexSavePath=indexFileDest)
    footprintIndex.createIndex(courseDisplayName, partition=args.partition)
    heatMapResultFile = '%s.csv' % resultFilePrefix
    footprintIndex.videoHeatAll(heatMapResultFile)
    #*****************
#     print("Excerpting:")
#     for videoId in footprintIndex.videoViews:
#         print("%s (1): %s" % (videoId, footprintIndex.videoViews[videoId][0]))
#         print("%s (2): %s" % (videoId, footprintIndex.videoViews[videoId][1]))
#         print("%s (3): %s" % (videoId, footprintIndex.videoViews[videoId][2]))
    #*****************
            
    print("Heatmaps are in %s" % heatMapResultFile)
    # If user entered a file name where to save the 
    # resulting index file, print where it went:
    if indexFile is not None:
        print("Saved index file is in %s" % indexFileDest)

# ==============    
#     footprintIndex = VideoFootPrintIndex(viewEventsCSVFile='/tmp/medstatsVideoFootprintUseAnonSortedChopped.csv', 
#                                              alignmentFile='/tmp/medstatsVideoFootprintAlignment.csv',
#                                              indexSavePath='/tmp/medstatsVideoFootprintIndex')

#     footprintIndex.computeFootprints()
#     pass
