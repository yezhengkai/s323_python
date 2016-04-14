#!/usr/bin/env python
#
# by kmo, s323 2016/04/12
# use obspy to do routine seismic data processing
#
# environment 
# os:linuxmint17.3 64
# pyenv-> anaconda3-2.5.0-> obspy 1.0.1
#
# folder inside should be miniseed file name like VNAS.HHZ.2016.047
# !! Notice you need to remove old folder (001,001_2 ...)
#    ex: rm `ls -d ???/ && ls -d ???_*/`
#==========================================
# Monkey 2013 master thesis page 24 
# about 801H stations in philippine
#==========================================
#表 3.1 本研究架設之 801H 地震測站
#測站名稱 經度(°E) 緯度(°N) 海拔(m) 架設時間
#ABRA 120.7516 13.4440 45 2010/4
#CALA 120.6529 13.7799 45 2010/9
#CALP 121.1868 13.4146 35 2010/9
#GALE 120.9453 13.5018 60 2010/9
#ILIJ 121.0705 13.6319 10 2010/9
#LIMA 120.5887 14.5563 40 2010/9
#MABI 120.9420 13.7481 44 2010/4
#MAMB 120.6071 13.2228 47 2010/4
#PALU 120.4300 13.4436 128 2010/4
#SANT 120.8344 12.9964 20 2010/4
#==========================================
# Broadband in #ABRA #MAMB #PALU #SANT 
# same location
# And PGPB from IES ( PGPB unkown evalatin )
# VNAS from BATS
#==========================================

# need to modify for your data
# filename like VNAS.HHZ.2016.047, staid is "VNAS"
staid='VNAS'

# this script just to processing one component, but you can modify
compp='HHZ'

# pole-zero file for removing instrument respones 
sacpz='SAC_PZs_TW_VNAS_HHZ__2014.150'

####### station #######
# python list of dictionaries search 
# reference : http://stackoverflow.com/q/8653516
###########################
sta_dict = [
    { "namesta": "VNAS", "lon": 114.3650, "lat": 10.3774},
    { "namesta": "PGPB", "lon": 120.9524, "lat": 13.5009},
    { "namesta": "ABRA", "lon": 120.7516, "lat": 13.4440},
    { "namesta": "PALU", "lon": 120.4300, "lat": 13.4436},
    { "namesta": "SANT", "lon": 120.8344, "lat": 12.9964},
    { "namesta": "MAMB", "lon": 120.6071, "lat": 13.2228},
]

# so you can use blew to call station lon and lat
# -----------------
# staname=next((item for item in stations if item["namesta"] == "VNAS"))
# print(staname['lon'])
# -----------------
####### station #######

import os
import glob # for read multi-data 
import subprocess # for linux command inside
from datetime import datetime # for calculate script processing time 
import obspy
from obspy.core.event import read_events # for read catalog/event 
from obspy.core import UTCDateTime # for time format and read
from obspy.core import read # read seismic data to obspy stream
import shutil # for move file to folder


startTime = datetime.now() # script start time  



######### catalogue #########
#
# obspy refernce : read, write and filter catalog example 
# https://docs.obspy.org/tutorial/code_snippets/quakeml_custom_tags.html
# https://docs.obspy.org/packages/autogen/obspy.core.event.catalog.Catalog.write.html
# https://docs.obspy.org/packages/autogen/obspy.core.event.catalog.Catalog.filter.html
#
# And we use gcmt ndk file for read
# 1976-2013 gcmt ndk 
# http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/jan76_dec13.ndk
# 2014-now gcmt quick ndk
# http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/NEW_QUICK/qcmt.ndk
#
# you can use wget command to download them
# ----------
# wget url_link .
# ---------- 
#
# And I use cat command to combine them new file
# and rename jan76_apr16_kmo.ndk
# ---------- 
# cat qcmt.ndk >> jan76_dec13.ndk && mv jan76_dec13.ndk jan76_apr16_kmo.ndk
# ---------- 
#
# Read all event (jan76_apr16_kmo.ndk) and output what you need time range 
# (I am not sure which output format is better for you,
#  what I tested result is that the output file more small and reading catalog more fast !) 
# ---------- 
# catalog_ndk = obspy.read_events("jan76_apr16_kmo.ndk")
# catalog_ndk_filter = catalog_ndk.filter("time > 2015-12-31T23:59") # I want 2016 year
# catalog_ndk_filter.write("gcmt_2016.xml", format="QUAKEML")
# ---------- 
#
# And you can print catalog (notice catalog variable name)
# ---------- 
# print(catalog_ndk.__str__(print_all=True))
# ---------- 
#
######### catalogue #########

#### begin ####


# read catalog first
cata_xml = obspy.read_events("gcmt_2016.xml")

#
# if you need to filter or print
# ---------- 
# cata = cata_xml.filter("magnitude >= 5") 
# print(cata.__str__(print_all=True))
# ---------- 
#

######## event ########
# obspy reference : 
# https://docs.obspy.org/packages/obspy.core.event.html
# https://docs.obspy.org/packages/autogen/obspy.core.event.origin.Origin.html
#
# Spend time to understand obspy class of event metadata
######## event ########


# Iteration read catalog become event
# maybe for loop faster than while you can test

for eventss in cata_xml:
  orig =  eventss.origins[0]
  event_lat = orig.latitude
  event_lon = orig.longitude
  event_dep = orig.depth
  event_time = orig.time
#  print(eventss.orig)

######## utcdatetime ########
# obspy reference :
# https://docs.obspy.org/packages/autogen/obspy.core.utcdatetime.UTCDateTime.html
# utcdatetime is a powerful obspy tool format time and catalog
######## utcdatetime ########

  dt=UTCDateTime(event_time)

# our seismic data is miniseed format, 
# and name format is like as "VNAS.HHZ.2016.047"

  # filename is like VNAS.HHZ.2016.047
  mseeds =str(staid)+"."+str(compp)+"."+str(dt.year)+"."+str(dt.julday).zfill(3)
#  print(mseeds)

  
  if os.path.isfile(mseeds):      #if miniseed file exist, then do below
    st = read(mseeds)             # read miniseed data use obspy stream
    st.trim(dt-60*5, dt+60*20)    # cut data before 5 min catalog time and after 20 min
    # one stream may have manay trace, merge them and gap fill 0
    st.merge(fill_value=0)
    # after cut, new file name     
    fnc = mseeds+".sac.new."+str(dt.month).zfill(2)+str(dt.day).zfill(2)+str(dt.hour).zfill(2)+str(dt.minute).zfill(2)+".cut"
    st.write(fnc, format="SAC")  # output waveform for sac format
#    subprocess.call('echo "r "%s";trans from polezero s "%s" freq 0.02 0.03 9 10;w append .gg ;q" | sac'%(fnc, sacpz), shell=True)
#    sac transfer usage https://ds.iris.edu/files/sac-manual/commands/transfer.html
#    example https://seiscode.iris.washington.edu/projects/sac/wiki/Instrument_response_removal_using_Polezero_files
#    a suggestr rule-of-thumb is f1 ,= f2/2 and f4 >= 2*f3.
#    
    dirr = str(dt.julday).zfill(3)   # folder for cut data
   
    # do below you have to clear old folder for cut file first!
    if not os.path.isdir(dirr):      # if folder not exist
      os.mkdir(dirr)                 # create folder
      shutil.move(fnc, dirr)         # move cut file to julia folder
      print("Move "+fnc+" to "+dirr)
      cnt=1                          # initial count = 1
    else:
    # else mean folder exist, and auto plus 1 to like as 001_2
      cnt =cnt+ 1                    
      ndirr=str(dirr)+"_"+str(cnt)
      os.mkdir(ndirr)
      shutil.move(fnc, ndirr)
      print("Move "+fnc+" to "+ndirr)
  else:
    print("No such file " + mseeds+" to cut event "+str(dt.month).zfill(2)+str(dt.day).zfill(2)+str(dt.hour).zfill(2)+str(dt.minute).zfill(2) )





print ('this python script cost '+str(datetime.now() - startTime))

