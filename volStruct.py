from regexes import *
from types import DictType

class RAIDVolume(DictType):
    
    global INFO, CACHE, IOSTAT, VGINFO
    
    INFO = int(0)
    CACHE = int(1)
    IOSTAT = int(2)
    IOSTAT_REQ = int(3)
    VGINFO = int(4)
    
    def __init__(self, SSID):
        
        self.vol = dict() 
        self.vol[INFO] = {
                            'ssid': SSID,
                            'user_label': "",
                            'capacity': "",
                            'blocksize': "",
                            'segment_size': "",
                            'stripe_size': "",
                            'pre_read': "",
        }
        
        self.vol[CACHE] = {
                            'read_ahead': "",
                            'fast_write': "",
                            'flush_mod': "",
                            'warn_mod': "",
                            'cache_block': "",
        }
        
        self.vol[IOSTAT] = {
                            'requests': "",
                            'blocks': "",
                            'avg_blocks': "",
                            'reads': "",
                            'writes': "",
                            'write_algorithm': ""
        }
        
        self.vol[VGINFO] = {
                            'vg_label': "",
                            'drive_count': "",
                            'boundary': "",
                            'media_type': ""
        }
        
    def populateWithBuffer(self, buffer):
        
        user_label = vol_user_label.search(buffer)
        capacity = vol_capacity.search(buffer)
        blksize = vol_blocksize.search(buffer)
        seg_size = vol_segment_size.search(buffer)
        stripe_sz = vol_stripe_size.search(buffer)
        pre_rd = vol_pre_read.search(buffer)
        
        self.vol[INFO]['user_label'] = user_label.group(1)
        self.vol[INFO]['capacity'] = capacity.group(1)
        self.vol[INFO]['blocksize'] = blksize.group(1)
        self.vol[INFO]['segment_size'] = seg_size.group(1)
        self.vol[INFO]['stripe_size'] = stripe_sz.group(1)
        self.vol[INFO]['pre_read'] = pre_rd.group(1)
        
        rd_ahead = vol_cache_read_ahead.search(buffer)
        fast_wr = vol_cache_fast_write.search(buffer)
        flush_mod = vol_cache_flush_mod.search(buffer)
        warn_flush = vol_cache_min_warn_flush.search(buffer)
        cache_blk = vol_cache_granularity.search(buffer)
        
        self.vol[CACHE]['read_ahead'] = rd_ahead.group(1)
        self.vol[CACHE]['fast_write'] = fast_wr.group(1)
        self.vol[CACHE]['flush_mod'] = flush_mod.group(1)
        self.vol[CACHE]['warn_mod'] = warn_flush.group(1)
        self.vol[CACHE]['cache_block'] = cache_blk.group(1)
        
        requests = vol_io_requests.search(buffer)
        blocks = vol_io_blocks.search(buffer)
        avg_blocks = vol_io_avg_blocks.search(buffer)
        reads = vol_io_reads.search(buffer)
        writes = vol_io_writes.search(buffer)
        write_alg = vol_io_write_alg.search(buffer)
        
        self.vol[IOSTAT]['requests'] = {
                                        'sm_reads': requests.group(1),
                                        'sm_writes': requests.group(2),
                                        'sm_writesame': requests.group(3),
                                        'lg_reads': requests.group(4),
                                        'lg_writes': requests.group(5),
                                        'lg_writesame': requests.group(6),
                                        'comp_write': requests.group(7),
                                        'total': requests.group(8),
                                        'cache_hits': requests.group(9)}
        
        self.vol[IOSTAT]['blocks'] = {
                                        'sm_reads': blocks.group(1),
                                        'sm_writes': blocks.group(2),
                                        'sm_writesame': blocks.group(3),
                                        'lg_reads': blocks.group(4), 
                                        'lg_writes': blocks.group(5),
                                        'lg_writesame': blocks.group(6),
                                        'comp_write': blocks.group(7),
                                        'total': blocks.group(8),
                                        'cache_hits': blocks.group(9)}
        
        self.vol[IOSTAT]['avg_blocks'] = {
                                        'sm_reads': avg_blocks.group(1),
                                        'sm_writes': avg_blocks.group(2),
                                        'sm_writesame': avg_blocks.group(3),
                                        'lg_reads': avg_blocks.group(4),
                                        'lg_writes': avg_blocks.group(5),
                                        'lg_writesame': avg_blocks.group(6),
                                        'comp_write': avg_blocks.group(7),
                                        'total': avg_blocks.group(8),
                                        'cache_hits': avg_blocks.group(9)}
        
        self.vol[IOSTAT]['reads'] = {
                                        'io': reads.group(1),
                                        'stripes': reads.group(2),
                                        'clusters': reads.group(3)
        }
        
        self.vol[IOSTAT]['writes'] = {
                                        'io': writes.group(1),
                                        'stripes': writes.group(2),
                                        'clusters': writes.group(3)
        }
        
        self.vol[IOSTAT]['write_algorithm'] = {
                                        'full': write_alg.group(1),
                                        'partial': write_alg.group(2),
                                        'RMW': write_alg.group(3),
                                        'no_parity': write_alg.group(4),
                                        'RMW2': write_alg.group(5),
                                        'FSWT': write_alg.group(6)
        }
        
        vg_label = vol_vg_label.search(buffer)
        drive_cnt = vol_vg_drive_count.search(buffer)
        boundary = vol_vg_boundary.search(buffer)
        media_type = vol_vg_media_type.search(buffer)
        
        self.vol[VGINFO]['vg_label'] = vg_label.group(1)
        self.vol[VGINFO]['drive_count'] = drive_cnt.group(1)
        self.vol[VGINFO]['boundary'] = boundary.group(1)
        self.vol[VGINFO]['media_type'] = media_type.group(1)
    
    def getVolInfo(self):
        
        print "User Label : " + self.vol[INFO]['user_label']
        print "Capacity   : " + self.vol[INFO]['capacity']
        print "BlockSize  : " + self.vol[INFO]['blocksize']
        print "Stripe Size: " + self.vol[INFO]['stripe_size']
        print "Pre-Read   : " + self.vol[INFO]['pre_read']
   
    def getVolCache(self):    
        
        print "Read Ahead      : " + self.vol[CACHE]['read_ahead']
        print "Fast Write      : " + self.vol[CACHE]['fast_write']
        print "Cache Flush Mod.: " + self.vol[CACHE]['flush_mod']
        print "Min. Warn Mod.  : " + self.vol[CACHE]['warn_mod']
        k = int(self.vol[CACHE]['cache_block']) * 512 / 1024
        print "Cache Block Size: " + str(k), "K"
    
    def getVolVGInfo(self):
        
        print "VG Label    : " + self.vol[VGINFO]['vg_label']
        print "Drive Count : " + self.vol[VGINFO]['drive_count']
        print "Boundary    : " + self.vol[VGINFO]['boundary']
        print "Media Type  : " + self.vol[VGINFO]['media_type']
        
    def getValueWithKeys(self, cat, key):
        
        return self.vol[cat][key]
    
    def getIOStatWithKeys(self, cat, key):
        
        return self.vol[IOSTAT][cat][key] 
        
    
    
