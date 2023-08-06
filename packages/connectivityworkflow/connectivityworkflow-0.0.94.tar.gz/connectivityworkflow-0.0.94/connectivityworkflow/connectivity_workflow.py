#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 15:56:02 2018

@author: ghiles.reguig
"""
import argparse
from nipype import config
from os.path import join as opj
import json
from connectivityworkflow.workflow_builder import BuildConnectivityWorkflow, BuildConnectivityWorkflowSurface

def RunConnectivityWorkflow(path, outDir,workdir, conf_file=None, type_analysis="volume", space=None, atlas=None, lh=None, rh=None):

    if conf_file is not None :
        res=open(conf_file,'r').read()
        conf=json.loads(res)
        config.update_config(conf)

    plugin = config.get("execution","plugin")
    plugin_args = config.get("execution","plugin_args")
    if plugin_args is not None :
        plugin_args = eval(plugin_args)
    print("Conducting {} analysis".format(type_analysis))
    if type_analysis=="surface":
        if lh is None or rh is None : 
            raise ValueError("For a surface analysis, annotation files must be specified for both hemispheres")
        wf = BuildConnectivityWorkflowSurface(path, outDir, lh_annot=lh, 
                                              rh_annot=rh, space=space)
    else:
        wf = BuildConnectivityWorkflow(path,outDir, atlas=atlas, space=space)
        
    wf.base_dir = workdir
    wf.run(plugin=plugin, plugin_args=plugin_args)
   #wf.run(plugin='MultiProc', plugin_args={'n_procs' : 28})




if __name__ == "__main__" :
    #Argument parser
    parser = argparse.ArgumentParser(description="Path to BIDS Dataset")
    #Add the filepath argument to the BIDS dataset
    parser.add_argument("-p","--path", dest="path",help="Path to BIDS Dataset", required=True)
    parser.add_argument("-w", "--workdir", dest="workdir", help="Path to working directory", required=False)
    parser.add_argument("-c", "--config", dest="conf", help="Nipype JSON configuration file ", required=False)
    parser.add_argument("-t","--type", dest="type",help="Type of analysis to make", required=False)
    parser.add_argument("-s","--space", dest="space",help="Space of the fMRI input", required=False)
    parser.add_argument("-a","--atlas", dest="atlas",help="Path to the file to use as an atlas for a volume analysis", required=False)
    parser.add_argument("-lh",dest="lh",help="Left hemisphere annot file for surface analysis", required=False)
    parser.add_argument("-rh",dest="rh",help="Right hemisphere annot file for surface analysis", required=False)
    
    #Parse the commandline
    args = parser.parse_args()
    #Get the filepath argument specified by the user
    path = args.path
    workdir = args.workdir
    conf = args.conf
    outDir = opj(path,"derivatives","connectivityWorkflowVolume")
    type_analysis = args.type
    space = args.space
    atlas = args.atlas
    lh = args.lh
    rh = args.rh
    print("Results will be written in {}".format(outDir))
    #Build and run the workflow
    RunConnectivityWorkflow(path, outDir, workdir, conf, type_analysis, space, atlas, lh, rh)
    print("ConnectivityWorkflow Done")
