#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:36:38 2018

@author: ghiles.reguig
"""
from bids.grabbids import BIDSLayout
from nipype import Function, Node
from os.path import join as opj

def get_BidsData(pathBids, subject, session, outputDir):
    """
    Function  to get the aparcaseg and the pre-processed BOLD fmri filepaths from BIDS dataset
    """
    from bids.grabbids import BIDSLayout
    from os.path import join as opj
    import os

    layout = BIDSLayout(pathBids)
    try :
        prep = layout.get(type="preproc", space="MNI152NLin2009cAsym", subject=subject, session=session)[0]
        aparcaseg = layout.get(type="roi", label="aparcaseg", space="T1w", subject=subject, session=session)[0].filename
        preproc = prep.filename
        confounds = layout.get(type="confounds", subject=subject, session=session)[0].filename
        prefix = "sub-"+prep.subject+"_ses-"+prep.session+"_task-"+prep.task+"-"+prep.type+"_"
    except IndexError :
        raise Exception("Data missing for subject : {}, session : {}".format(subject, session))
        
    outDir = opj(outputDir, "sub-"+subject, "ses-"+session, "func")
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    return aparcaseg, preproc, confounds, outDir, prefix

def GetBidsDataGrabberNode(pathBids):
    layout = BIDSLayout(pathBids)
    subjects = layout.get_subjects()
    sessions = layout.get_sessions()
    print("Found {} subjects and {} sessions in the dataset".format(len(subjects), len(sessions)))
    #Initialize the dataGrabber node
    BIDSDataGrabber = Node(Function(function=get_BidsData, input_names=["pathBids","subject","session", "outputDir"], output_names=["aparcaseg", "preproc", "confounds", "outputDir", "prefix"]), name="FunctionalDataGrabber")
    #Specify path to dataset
    BIDSDataGrabber.inputs.pathBids = pathBids    
    BIDSDataGrabber.inputs.outputDir = opj(pathBids, "derivatives", "connectivityWorkflow")
    #Specify subjects and sessions to iterate over them
    #Stored in iterables for multiprocessing purpose
    BIDSDataGrabber.iterables = [("subject", subjects), ("session", sessions)]
    #Return the node 
    return BIDSDataGrabber


def get_bids_surf_data(path_bids, subject, session, output_dir):
    """
    Function  to get the aparcaseg and the pre-processed BOLD fmri filepaths from BIDS dataset
    """
    from bids.grabbids import BIDSLayout
    from os.path import join as opj
    import os

    layout = BIDSLayout(path_bids)
    try :
        layout_surfs = layout.get(space="fsaverage", subject=subject, session=session)
        surfaces = [hemisphere.filename for hemisphere in layout_surfs]
        if surfaces[0].find(".R.") != -1 :
            rh_surf, lh_surf = surfaces[0], surfaces[1]
        else : 
            rh_surf, lh_surf = surfaces[1], surfaces[0]
        confounds = layout.get(type="confounds", subject=subject, session=session)[0].filename
        prefix = "sub-"+subject+"_ses-"+session+"_task-"+layout_surfs[0].task+"-fsaverage_"
    except IndexError :
        raise Exception("Data missing for subject : {}, session : {}".format(subject, session))
        
    outDir = opj(output_dir, "sub-"+subject, "ses-"+session, "func")
    if not os.path.exists(outDir):
        print("\n\n{} created\n\n".format(outDir))
        os.makedirs(outDir)
    return lh_surf, rh_surf, confounds, outDir, prefix

def get_bids_surf_data_node(path_bids):
    layout = BIDSLayout(path_bids)
    subjects = layout.get_subjects()
    sessions = layout.get_sessions()
    print("Found {} subjects and {} sessions in the dataset".format(len(subjects), len(sessions)))
    bids_data_grabber = Node(Function(function = get_bids_surf_data, 
                                      input_names=["path_bids", "subject", "session", "output_dir"],
                                      output_names=["lh_surf","rh_surf","confounds","outputDir","prefix"]),
                                      name="SurfaceDataGrabber")    
    bids_data_grabber.inputs.path_bids = path_bids
    bids_data_grabber.inputs.output_dir = opj(path_bids,"derivatives","connectivityWorkflowSurface")
    bids_data_grabber.iterables = [("subject",subjects), ("session",sessions)]
    return bids_data_grabber

################### T E S T 
"""
pathBids = "/export/dataCENIR/users/ghiles.reguig/testBIDSB0/"

l = BIDSLayout(pathBids)

BIDSDataGrabber = Node(Function(function=get_BidsData, input_names=["pathBids", "subject", "session"], 
                                output_names=["aparcaseg", "preproc"]), name="getRoi")

#BIDSDataGrabber.inputs.type="roi"
#BIDSDataGrabber.inputs.label="aparcaseg"
BIDSDataGrabber.inputs.pathBids = pathBids
BIDSDataGrabber.iterables =  [("subject", l.get_subjects()), ("session", l.get_sessions())]
#r = BIDSDataGrabber.run()

#Test on workflow




def printMe(aseg, preproc):
    print("\n\nanalyzing " + str(aseg)  + "\n\n"+str(preproc))
    
analyze = Node(Function(function=printMe, input_names=["aseg","preproc"], output_names=[]), name="analyzeBOLD")

wf = Workflow(name="bids_test")
wf.connect(inputNode, "aparcaseg", analyze, "aseg")
wf.connect(inputNode, "preproc", analyze, "preproc")
res = wf.run()

"""
"""
#Confounds Selector
confNode = getConfoundsReaderNode()
confNode.inputs.regex = None, "all"

#Input node
pathBids = "/export/dataCENIR/users/ghiles.reguig/testBIDSB0/"

inputNode = GetBidsDataGrabberNode(pathBids)

#Signal Extraction
signalExtraction = Node(SignalExtractionFreeSurfer(), name="SignalExtraction")

signalExtraction.inputs.lutFile = "/export/data/opt/CENIR/freesurfer6.0_cento06/FreeSurferColorLUT.txt"

#Connectivity Calculation

connectivityCalculation = Node(ConnectivityCalculation())

wf = Workflow(name="bids_test")

wf.connect([(inputNode, signalExtraction, 
             [("aparcaseg", "roi_file"), ("preproc", "fmri_file"),("outputDir", "output_dir")]),
    (inputNode, confNode, [("confounds","filepath")]), (confNode, signalExtraction, [("values", "confounds")])]
    )
    
wf.run()
"""