import csv, re
import numpy as np

'''
get video_name video_id matching 
this is needed because video_name is what is used for profile, but it is unreadable 
video id is readable and can be sorted chronological 
'''
video_name_id_matching = {}
video_id_name_matching = {}
event_type = ['play_video','stop_video','pause_video','seek_video']
wk1 = ['2wLfFB_6SKI','LvaTokhYnDw'] 
wk2 = ['WjyuiK5taS8','UvxHOkYQl8g','VusKAosxxyk','vVj2itVNku4','jwBgGS_4RQA','jk9S3RTAl38']
wk3 = ['PsE9UqoWtS4','J6AdoiNUyWI','1hbCJyM9ccs','3T6RXmIHbJ4','IFzVxLv0TKQ','5ONFqIk3RFg']
wk4 = ['sqq21-VIa1c','31Q5FGRnxt4','MpX8rVv_u4E','GavRXXEHGqU','RfrGiG1Hm3M',
'QG0pVJXT6EU','X4VDZDp2vqw','6FiNGTYAOAA','TxvEVc8YNlU','2cl7JiPzkBY','9TVVF7CS3F4']
wk5 = ['6l9V1sINzhE','_2ij6eaaSl0','nZAM5OXrktY','S06JpVoNaA0','p4BYWX7PTBM','BzHz0J9a6k0',
'6dSXlqHAoMk','YVSmsWoBKnA']
wk6 = ['MEMGOlJxxz0','91si52nk3LA','nLpJd_iKmrE','NJhMSpI2Uj8','LkifE44myLc','3p9JNaJCOb4',
'cSKzqb0EKS0','A5I1G1MfUmA','xMKVUstjXBE','QlyROnAjnEk','eYxwWGJcOfw','3kwdDGnV8MM','mv-vdysZIb4',
'F8MMHCCoALU','1REe3qSotx8']
wk7 = ['gtXQXA7qF3c','7ZIqzTNB8lk','mxXHJa1DsWQ','N2hBXqPiegQ','uQBnDGu6TYU','DCn83aXXuHc']
wk8 = ['79tR7BvYE6w','6ENTbK3yQUQ','GfPR7Xhdokc','hPEJoITBbQ4','lq_xzBRIWm4','U3MdBNysk9w',
'0wZUXtvAtDc','IY7oWGXb77o']
wk9 = ['QpbynqiTCsY','xKsTsGE7KpI','dm32QvCW7wE','mI18GD4_ysE','qhyyufR0930','L3n2VF7yKkk']
wk10 = ['ipyxSYXgzjQ','dbuSGWCgdzw','aIybuNt9ps4','Tuuc9Y06tAc','yUJcTpWNY_o','lFHISDj_4EQ',
'YDubYJsZ9iM','4u3zvtfqb7w']
videos = wk1 + wk2 + wk3 + wk4 + wk5 + wk6 + wk7 + wk8 + wk9 + wk10
with open('[file/path/to/videoInteraction]','r') as csvfile :
    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    for line in lines :
        if line[0] in event_type and line[-1] != '' and line[9] in videos:
                if line[9] != 'html5':
                    video_name_id_matching[line[-1]] = line[9]
                    video_id_name_matching[line[9]] = line[-1]
                    
'''
These script-generated command sets the maximum timestamp for each video, pulled with Youtube API 
'''
video_length = {}
video_length[video_id_name_matching['2wLfFB_6SKI']] = 1099  #1.1 Opening Remarks
video_length[video_id_name_matching['LvaTokhYnDw']] = 733  #1.2 Examples and Framework
video_length[video_id_name_matching['WjyuiK5taS8']] = 702  #2.1 Introduction to Regression Model
video_length[video_id_name_matching['UvxHOkYQl8g']] = 701  #2.2 Dimensionality and Structured Models
video_length[video_id_name_matching['VusKAosxxyk']] = 605  #2.3 Model Selection and Bias-Variance Tradeoff
video_length[video_id_name_matching['vVj2itVNku4']] = 938  #2.4 Classification
video_length[video_id_name_matching['jwBgGS_4RQA']] = 853  #2.R Introduction to R
video_length[video_id_name_matching['PsE9UqoWtS4']] = 782  #3.1 Simple Linear Regression
video_length[video_id_name_matching['J6AdoiNUyWI']] = 505  #3.2 Hypothesis Testing and Interval Confidence
video_length[video_id_name_matching['1hbCJyM9ccs']] = 938  #3.3 Multiple Linear Regression
video_length[video_id_name_matching['3T6RXmIHbJ4']] = 892  #3.4 Some Important Questions
video_length[video_id_name_matching['IFzVxLv0TKQ']] = 857  #3.5 Extensions of the linear models
video_length[video_id_name_matching['5ONFqIk3RFg']] = 1331  #3.R Linear Regression in R
video_length[video_id_name_matching['sqq21-VIa1c']] = 626  #4.1 Introduction to Classification Problems
video_length[video_id_name_matching['31Q5FGRnxt4']] = 548  #4.2 Logistic Regression
video_length[video_id_name_matching['MpX8rVv_u4E']] = 594  #4.3 Multivariate Logistic Regression
video_length[video_id_name_matching['GavRXXEHGqU']] = 449  #4.4 Logistic Regression - Case Control Sampling and Multiclass
video_length[video_id_name_matching['RfrGiG1Hm3M']] = 433  #4.5 Discriminant Analysis
video_length[video_id_name_matching['QG0pVJXT6EU']] = 458  #4.6 Gaussian Discriminant Analysis - One Variable
video_length[video_id_name_matching['X4VDZDp2vqw']] = 1063  #4.7 Gaussian Discriminant Analysis - Many Variable
video_length[video_id_name_matching['6FiNGTYAOAA']] = 608  #4.8 Quadratic Discriminant Analysis and Naive Bayes
video_length[video_id_name_matching['TxvEVc8YNlU']] = 615  #4.R Classification in R.A
video_length[video_id_name_matching['2cl7JiPzkBY']] = 503  #4.R Classification in R.B
video_length[video_id_name_matching['9TVVF7CS3F4']] = 302  #4.R Classification in R.C
video_length[video_id_name_matching['_2ij6eaaSl0']] = 842  #5.1 Cross-Validation
video_length[video_id_name_matching['nZAM5OXrktY']] = 814  #5.2 K-fold Cross-Validation
video_length[video_id_name_matching['S06JpVoNaA0']] = 608  #5.3 Cross-Validation: the wong and right way
video_length[video_id_name_matching['p4BYWX7PTBM']] = 690  #5.4 The Bootstrap
video_length[video_id_name_matching['BzHz0J9a6k0']] = 876  #5.5 More on the Bootstrap
video_length[video_id_name_matching['6dSXlqHAoMk']] = 682  #5.R Resampling in R.A
video_length[video_id_name_matching['YVSmsWoBKnA']] = 461  #5.R Resampling in R.B
video_length[video_id_name_matching['91si52nk3LA']] = 825  #6.1 Introduction and Best-Subset Selection
video_length[video_id_name_matching['nLpJd_iKmrE']] = 747  #6.2 Stepwise selection
video_length[video_id_name_matching['NJhMSpI2Uj8']] = 327  #6.3 Backward stepwise selection
video_length[video_id_name_matching['LkifE44myLc']] = 847  #6.4 Estimating test error
video_length[video_id_name_matching['3p9JNaJCOb4']] = 524  #6.5 Validation and cross-validation
video_length[video_id_name_matching['cSKzqb0EKS0']] = 758  #6.6 Shrinkage methods and ridge regression
video_length[video_id_name_matching['A5I1G1MfUmA']] = 922  #6.7 The Lasso
video_length[video_id_name_matching['xMKVUstjXBE']] = 328  #6.8 Tuning parameter selection
video_length[video_id_name_matching['QlyROnAjnEk']] = 286  #6.9 Dimension Reduction Methods
video_length[video_id_name_matching['eYxwWGJcOfw']] = 949  #6.10 Principal Components Regression and Partial Least Squares
video_length[video_id_name_matching['3kwdDGnV8MM']] = 637  #6.R Model Selection in R.A
video_length[video_id_name_matching['mv-vdysZIb4']] = 633  #6.R Model Selection in R.B
video_length[video_id_name_matching['F8MMHCCoALU']] = 333  #6.R Model Selection in R.C
video_length[video_id_name_matching['1REe3qSotx8']] = 995  #6.R Model Selection in R.D
video_length[video_id_name_matching['gtXQXA7qF3c']] = 915  #7.1 Polynomials and Step Functions
video_length[video_id_name_matching['7ZIqzTNB8lk']] = 794  #7.2 Piecewise-Polynomials and Splines
video_length[video_id_name_matching['mxXHJa1DsWQ']] = 611  #7.3 Smoothing Splines
video_length[video_id_name_matching['N2hBXqPiegQ']] = 646  #7.4 Generalized Additive Models and Local Regression
video_length[video_id_name_matching['uQBnDGu6TYU']] = 1272  #7.R Nonlinear Functions in R.A
video_length[video_id_name_matching['DCn83aXXuHc']] = 736  #7.R Nonlinear Functions in R.B
video_length[video_id_name_matching['6ENTbK3yQUQ']] = 878  #8.1 Tree-based methods
video_length[video_id_name_matching['GfPR7Xhdokc']] = 706  #8.2 More details on Trees
video_length[video_id_name_matching['hPEJoITBbQ4']] = 661  #8.3 Classification trees
video_length[video_id_name_matching['lq_xzBRIWm4']] = 826  #8.4 Bagging and Random Forest
video_length[video_id_name_matching['U3MdBNysk9w']] = 724  #8.5 Boosting
video_length[video_id_name_matching['0wZUXtvAtDc']] = 614  #8.R Tree-based Methods in R.A
video_length[video_id_name_matching['IY7oWGXb77o']] = 936  #8.R Tree-based Methods in R.B
video_length[video_id_name_matching['QpbynqiTCsY']] = 696  #9.1 Optimal Separating Hyperplanes
video_length[video_id_name_matching['xKsTsGE7KpI']] = 485  #9.2 Support Vector Classifier
video_length[video_id_name_matching['dm32QvCW7wE']] = 905  #9.3 Feature Expansion and the SVM
video_length[video_id_name_matching['mI18GD4_ysE']] = 888  #9.4 Example and Comparison with Logistic Regression
video_length[video_id_name_matching['qhyyufR0930']] = 614  #9.R SVMs in R.A
video_length[video_id_name_matching['L3n2VF7yKkk']] = 475  #9.R SVMs in R.B
video_length[video_id_name_matching['ipyxSYXgzjQ']] = 758  #10.1 Principal Components
video_length[video_id_name_matching['dbuSGWCgdzw']] = 1060  #10.2 Higher Order Principal Components
video_length[video_id_name_matching['aIybuNt9ps4']] = 1038  #10.3 k-means Clustering
video_length[video_id_name_matching['Tuuc9Y06tAc']] = 886  #10.4 Hierarhical Clustering
video_length[video_id_name_matching['yUJcTpWNY_o']] = 565  #10.5 Breast Cancer Example
video_length[video_id_name_matching['lFHISDj_4EQ']] = 389  #10.R Unsupervised in R.A
video_length[video_id_name_matching['YDubYJsZ9iM']] = 392  #10.R Unsupervised in R.B
video_length[video_id_name_matching['4u3zvtfqb7w']] = 394  #10.R Unsupervised in R.C



'''
read individual profile into memories, filtered by max timestamp
'''
video_user = {}
with open('[/file/path/to/individual profile]','r') as csvfile :
    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    count = 0
    for line in lines :
        count+= 1
        if count % 5000000 == 0:
            print count
        if line == ['videoId', 'second', 'numViews']:
            continue
        else:
            try:
                videoID,userID,second,numViews = line
            except:
                print line
            if videoID not in video_user:
                video_user[videoID] = {}
                
            if userID not in video_user[videoID]:
                video_user[videoID][userID] = {}
            if int(second) <= video_length[videoID]:
            	video_user[videoID][userID][int(second)] = int(numViews)

'''
These are the quizzes that I looked at, which have 0.45 - 0.55 success rate
'''
quiz = ['1.2.R1','5.5.R1','2.3 R1','7.1.R1','5.1.R2','3.2.R2','1.2.R1']
