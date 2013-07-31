import re

## vdmShowRAIDVolList
vol_list_count = re.compile('\s*Total\sRAIDVolumes:\s(\d+)', re.MULTILINE)
vol_list_entry = re.compile('\s0x\w{8}\s(\d{6})\s(RV_\w+)\s+(\d+)\s(\w{3,4})\s+(\w{3,4})\s+(\d+)', re.MULTILINE)

## vdmShowVGInfo
# Seq:1 / RAID 6 / VGCompleteState / TLP:F / DLP:F / SSM:T / ActDrv:8 / InActDrv:0 / VolCnt:2 / Secure:No
# PI Capable:F - 0 / Label:0 / VGWwn:600a0b800050d676000002354c5ae04a
vg_details = re.compile('Seq:\d+\s\/\sRAID\s(\d+)\s\/\s(\w+)\s\/\sTLP:(T|F)\s\/\sDLP:(T|F)\s\/\sSSM:\w\s\/\sActDrv:(\d+)\s\/\sInActDrv:(\d+)\s\/\sVolCnt:(\d+)\s\/\sSecure:(Yes|No)\nPI\sCapable:(T|F)\s-\s(\d+)\s\/\sLabel:(\w+)', re.MULTILINE)

# (Active) Drive:0x02c38260 devnum:0x00010001 seqNum:1 Tray/Slot:85/02  State:Acc/GrA/Opt
vg_drive_entry = re.compile('\((Active|Inactive)\)\sDrive:0x\w{8}\sdev[n,N]um:0x(\w{8})\sseqNum:(\d+)\sTray\/Slot:(\d+)\/(\d+)\s+State:(\w+)\/GrA\/(\w+)', re.MULTILINE)

## evfShowVol
# 1 - Vol Details
vol_num_children = re.compile('\s+(\d+)\sChildren', re.MULTILINE)
vol_user_label = re.compile('\s+User\sLabel:\s+(\w+)', re.MULTILINE)
vol_capacity = re.compile('\s+Capacity:\s+(\d+)\sblocks', re.MULTILINE)
vol_blocksize = re.compile('\s+BlockSize:\s+(\d+)', re.MULTILINE)
vol_segment_size = re.compile('^\s+Segment\sSize:\s+(\d+)\sblocks', re.MULTILINE)
vol_stripe_size = re.compile('^\s+Stripe\sSize:\s+(\d+)\sblocks', re.MULTILINE)
vol_pre_read = re.compile('^\s+Pre-Read\sRedundancy\sCheck:\s(Enabled|Disabled)', re.MULTILINE)

# 2 - IO Statistics:
#                        Small      Small      Large      Large                 Cache
#                        Reads     Writes      Reads     Writes      Total       Hits
#          Requests      36362        422          0          0      36784      29235
#            Blocks    4574801       4870          0          0    4579671    3666758
#        Avg Blocks        125         11          0          0        124        125
#            IO Pct     98.85%      1.14%      0.00%      0.00%    100.00%     79.47%
vol_io_requests = re.compile('^\s+Requests\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', re.MULTILINE)
vol_io_blocks = re.compile('^\s+Blocks\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', re.MULTILINE)
vol_io_avg_blocks = re.compile('^\s+Avg\sBlocks\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', re.MULTILINE)

#                         IOs    Stripes        /IO   Clusters        /IO
#            Reads      36362      36362       1.00      36362       1.00
#           Writes        422        422       1.00        422       1.00
#
#            Write       Full    Partial        RMW  No Parity       RMW2       FSWT
#       Algorithms          0          3          3          0        287          0
vol_io_reads = re.compile('^\s+Reads\s+(\d+)\s+(\d+)\s+\S+\s+(\d+)\s+\S+', re.MULTILINE)
vol_io_writes = re.compile('^\s+Writes\s+(\d+)\s+(\d+)\s+\S+\s+(\d+)\s+\S+', re.MULTILINE)
vol_io_write_alg = re.compile('^\s+Algorithms\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', re.MULTILINE)

# 3 - Cache
vol_cache_read_ahead = re.compile('^\s*Read\sAhead:\s+(\d+)', re.MULTILINE)
vol_cache_fast_write = re.compile('^\s*Fast\sWrite:\s+(\d+)', re.MULTILINE)
vol_cache_flush_mod = re.compile('^\s+Cache\sFlush\sModifier:\s+(\d+)', re.MULTILINE)
vol_cache_min_warn_flush = re.compile('^\s*Min\sWarn\sFlush\sModifier:\s+(\d+)', re.MULTILINE)
vol_cache_granularity = re.compile('^\s*Cache\sGranularity:\s+(\d+)', re.MULTILINE)

# 4 - VG Info
vol_vg_label = re.compile('^\s*VG\sLabel\s+:\s+(\w+)', re.MULTILINE)
vol_vg_drive_count = re.compile('^\s*Drive\sCount:\s+(\d+)', re.MULTILINE)
vol_vg_boundary = re.compile('^\s*Boundary\s+:\s+(\d+)', re.MULTILINE)
vol_vg_media_type = re.compile('^\s*Media\sType\s+:\s+(\w+)', re.MULTILINE)
