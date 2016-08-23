#! /usr/bin/env python
# -*- coding: utf-8 -*-

from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime

client = Client()
t1 = UTCDateTime("2004-08-26T00:00:00")
t2 = t1 + 86400
network="YS"
station = "LHSM"
date=2004
st = client.get_waveforms(network,station,"*","BHZ",t1,t2)
st.write("%s.%s.%s.BHZ.SAC"%(network,station,date),format="SAC")
