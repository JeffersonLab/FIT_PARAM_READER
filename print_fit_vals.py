#!/usr/bin/python


from numpy import *
import numpy as np
 
import Gnuplot, Gnuplot.funcutils
import math
import sys
import re
import os
from os import system
            
import subprocess

import xml.etree.ElementTree as ET




if len(sys.argv)!=5:
    print "usage: <out.xml> <values_name.dat> <correlations_name.dat> <info.txt>"
    exit(1)

xml = sys.argv[1]
valsdat = sys.argv[2]
corrsdat = sys.argv[3]
infotxt = sys.argv[4]

def printvals(xml,out):
# reads out names, values, and errors from the output xml
    tree = ET.parse(xml)

    root = tree.getroot()

    
    for child in root.find('Minimum/MinimumParams/GlobalParams/VALUES'):

        out[0].append( child.find('Key').text)
        out[1].append( child.find('Val/value').text)
        out[2].append( child.find('Val/error').text)

def printcorrs(xml,out):
#reads correlations from xml

    tree = ET.parse(xml)

    root = tree.getroot()

    key = []
    c=0
    
    for child in root.find('Minimum/MinimumParams/GlobalParams/CORR'):

        key.append(child.find('Key/First').text)
        if len(key) > 1:
            
            if key[len(key)-1] != key[len(key)-2]:
                
                c+=1
        
        out[c].append( child.find('Val').text)
def print_info(xml,out):

    tree = ET.parse(xml)

    root = tree.getroot()

    model = root.find('Amplitudes/PartialWaves/elem/model').text
    

    if model.find('kmatrix_poles')>=0:
        

        numpoles = root.find('Amplitudes/PartialWaves/elem/fixed_params/n_poles').text

        polyorder = root.find('Amplitudes/PartialWaves/elem/fixed_params/poly_order').text
        
        chewman = root.find('Amplitudes/PartialWaves/elem/fixed_params/chew_man').text

        chewsub = ""
        adler=""

        if chewman=="true":
            chewsub+=root.find('Amplitudes/PartialWaves/elem/fixed_params/chew_man_sub_point').text
        else:
            chewman+="\n"
        if root.find('Amplitudes/PartialWaves/elem/fixed_params/adler_zero_s') != None:    
            adler += root.find('Amplitudes/PartialWaves/elem/fixed_params/adler_zero_s').text
        else:
            adler+="None\n"

        string = ""

        string+="model = "
        string+=model+"\n"
        string+="number of poles = "
        string+=numpoles+"\n"
        string+="polynomial order = "
        string+=polyorder+"\n"
        string+="Chew Mandelstam phase space = "
        string+= chewman
        if chewman=="true":
            string+="\n   subtraction point = "
            string+=chewsub+"\n"
        if adler!="None":
            string+="adler zero = "
            string+=adler+"\n"

        else:
            string+="no adler zero\n"
        #print string

    if model.find('kmatrix_inv')>=0:
        polyorder=""
        for child in root.find('Amplitudes/PartialWaves/elem/fixed_params/poly_order'):

                polyorder += child.find('channel_pair').text
                polyorder += " POLYORDER= "+child.find('order').text+"\n"
        
        chewman = root.find('Amplitudes/PartialWaves/elem/fixed_params/chew_man').text

        chewsub = ""
        adler=""

        if chewman=="true":
            if root.find('Amplitudes/PartialWaves/elem/fixed_params/chew_man_sub_point')!= None:
                chewsub+=root.find('Amplitudes/PartialWaves/elem/fixed_params/chew_man_sub_point').text
            else:
                chewsub+="threshold\n"
        else:
            chewman+="\n"
        if root.find('Amplitudes/PartialWaves/elem/fixed_params/adler_zero_s') != None:    
            adler += root.find('Amplitudes/PartialWaves/elem/fixed_params/adler_zero_s').text
        else:
            adler+="None\n"

        string = ""

        string+="model = "
        string+=model+"\n"
        #string+="number of poles = "
        #string+=numpoles+"\n"
        string+="polynomial info = "
        string+=polyorder+"\n"
        string+="Chew Mandelstam phase space = "
        string+= chewman
        if chewman=="true":
            string+="\n   subtraction point = "
            string+=chewsub+"\n"
        if adler!="None":
            string+="adler zero = "
            string+=adler+"\n"

        else:
            string+="no adler zero\n"

        
    f=open(out,"w")
    f.write(string)
    f.close()
    

def print_table(valsin,corrsin,valsout,corrsout):
#makes the actual output tables
    f=open(valsout,"w+")
    for i in range(len(valsin[0])):
        f.write(valsin[0][i]+" "+valsin[1][i]+" "+valsin[2][i]+"\n")
    f.close()
    f=open(corrsout,"w+")
    string=""
    for i in range(len(corrsin[0])):
        
        for j in range(len(corrsin[0])):
            string+=corrsin[i][j]
            string+=" "
        string+="\n"
    f.write(string)
    f.close()


            
            
    


out = [[]for i in range(0,3)]        
printvals(xml,out)

corrs = [[] for i in range(len(out[0]))]

printcorrs(xml,corrs)



print_table(out,corrs,valsdat,corrsdat)

print_info(xml,infotxt)
