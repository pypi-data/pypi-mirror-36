#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 11:33:52 2018

@author: ghiles.reguig
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from nipype.interfaces.base.core import LibraryBaseInterface,SimpleInterface
from nipype.interfaces.base import BaseInterfaceInputSpec, TraitedSpec
import nipype.interfaces.base.traits_extension as trait
from nilearn.connectome import ConnectivityMeasure
from nilearn import plotting
from sklearn.covariance import OAS, EmpiricalCovariance

plt.switch_backend("agg")

"""
Class for Nilearn Interface
"""

class NilearnBaseInterface(LibraryBaseInterface):
    _pkg = 'nilearn'
    
    
class ConnectivityCalculationInputSpec(BaseInterfaceInputSpec):
    time_series = trait.traits.Array(mandatory=True, 
                             desc="A 2-D array of time series : (timesteps x RoI)")
    kind = trait.traits.Enum('correlation', 'partial correlation', 'tangent', 'covariance', 'precision', usedefault="correlation",mandatory=False,  
                     desc="Measure of connectivity to compute, must be one of {'correlation', 'partial_correlation', 'tangent', 'covariance', 'precision'}. By default, correlation is used.")
    output_dir = trait.Directory(exists=False, mandatory=True, usedefault=".",
                                 desc="Directory to store generated file")
    absolute = trait.traits.Bool(mandatory=False, usedefault=False, 
                                 desc="Whether to use the absolute value of the connectivity measure. By default, False.")
    labels = trait.traits.List(mandatory=False, usedefault=None,
                               desc="List of labels associated with each time_serie")
    plotName = trait.traits.Str(mandatory=False, usedefault=None,
                                desc="Title of the connectivity matrix")
    prefix = trait.traits.Str(mandatory=False, usedefault="", desc="Prefix of the bids files")
    mask = trait.traits.Array(mandatory=False, 
                              desc="A 2-D array corresponding to a threshold mask : (nb of RoI x nb of RoI)", usedefault=None)

    
class ConnectivityCalculationOutputSpec(TraitedSpec):
    connectivityMatrix = trait.traits.Array(desc="Matrix of connectivity computed")
    dfPath = trait.traits.Str(desc="DataFrame containing the connectivity matrix")
    kind = trait.traits.Str(desc="Kind of connectivity calculated")
    
class ConnectivityCalculation(NilearnBaseInterface, SimpleInterface):
    
    input_spec = ConnectivityCalculationInputSpec
    output_spec = ConnectivityCalculationOutputSpec
    
    def _run_interface(self, runtime):
        self._check_kind()
        connKind = self.inputs.kind.replace(" ","")
        title = self.inputs.plotName+"_connectivity-"+connKind if self.inputs.plotName else connKind
        time_series = self.inputs.time_series
        directory = os.path.join(self.inputs.output_dir,"connectivityMeasures", title)
        if not os.path.exists(directory):
            os.makedirs(directory)
        plotpath = os.path.join(directory, self.inputs.prefix+title)
        connMatrixPath = os.path.join(directory, self.inputs.prefix+title)
        labels = list(self.inputs.labels) if self.inputs.labels else None
        print("Starting connectivity calculation...\nOAS Estimator")
        conn_measure = ConnectivityMeasure(OAS(), kind=self.inputs.kind)
        #Compute connectivity matrix
        conn_matrix = conn_measure.fit_transform([time_series])[0]
        if self.inputs.absolute : 
            conn_matrix = np.absolute(conn_matrix)
            
        if isinstance(self.inputs.mask, np.ndarray):
            try:
                conn_matrix = conn_matrix * self.inputs.mask
            except Exception as e:
                print("Could not apply mask :\n {}".format(e))
            
        print("Connectivity matrix computed.\nPlotting...")
        plt.figure()
        plotting.plot_matrix(conn_matrix, colorbar=True, labels=labels, title=title, figure=(10,8))
        plt.savefig(plotpath+".png")
        connDataFrame = pd.DataFrame(conn_matrix, columns = labels, index=labels)
        connDataFrame.to_csv(connMatrixPath+".tsv", sep="\t")
        self._results["connectivityMatrix"] = conn_matrix
        self._results["dfPath"] = connMatrixPath+".tsv"
        self._results["kind"] = connKind
            
        print("Connectivity calculation successfully finished")
        plt.close("all")
        return runtime
                    
    def _check_kind(self):
        self.inputs.kind = self.inputs.kind.lower()
        kind = self.inputs.kind            
        print("{} connectivity matrix will be computed".format(kind))
                
    
    
    
########################## T E S T ################
"""
pathTimeSeries = time_series
output_dir = "/home/ghiles.reguig/ConnectivityWorkflow/tests/"
connCalc = ConnectivityCalculation()
#connCalc.inputs.kind="covaFFDGDnce"
connCalc.inputs.time_series = pathTimeSeries
#connCalcti.inputs.labels = labels
connCalc.inputs.absolute = True
c = connCalc.run()
"""
