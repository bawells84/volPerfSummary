import StringIO
from regexes import *
from types import DictType

# Metaclass impl for iterator


class IterInstancesVG(type):
    def __iter__(cls):
        return iter(cls._instances)


class RAIDVolume(DictType):
    
    __metaclass__ = IterInstancesVG
    global INFO, CACHE, IOSTAT, VGINFO
        
    _instances = []
        
    INFO = int(0)
    CACHE = int(1)
    IOSTAT = int(2)
    VGINFO = int(3)
    
    def __init__(self, buf):

        self.vol = dict() 
        self.vol[INFO] = {
                            'ssid': "",
                            'user_label': "",
                            'capacity': "",
                            'blocksize': "",
                            'segment_size': "",
                            'stripe_size': "",
                            'pre_read': "",
                            'owner': "",
                            'preferred_owner': ""
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
        
        voltype = vol_ssid_type.search(buf)
        
        if voltype:
            
            if voltype.group(2) == "RAIDVolume":
                ssid = voltype.group(1)
                self.populate_with_buffer(buffer, ssid)
                RAIDVolume._instances.append(self)
            else:
                del self

    def populate_with_buffer(self, buf, ssid):
        
        user_label = vol_user_label.search(buf)
        capacity = vol_capacity.search(buf)
        blksize = vol_blocksize.search(buf)
        seg_size = vol_segment_size.search(buf)
        stripe_sz = vol_stripe_size.search(buf)
        pre_rd = vol_pre_read.search(buf)
        owner = vol_ownership.search(buf)
        pref_own = vol_pref_ownership.search(buf)
        
        self.vol[INFO]['ssid'] = ssid
        self.vol[INFO]['user_label'] = user_label.group(1)
        self.vol[INFO]['capacity'] = capacity.group(1)
        self.vol[INFO]['blocksize'] = blksize.group(1)
        self.vol[INFO]['segment_size'] = seg_size.group(1)
        self.vol[INFO]['stripe_size'] = stripe_sz.group(1)
        self.vol[INFO]['pre_read'] = pre_rd.group(1)
        self.vol[INFO]['owner'] = owner.group(1)
        self.vol[INFO]['preferred_owner'] = pref_own.group(1)
        
        rd_ahead = vol_cache_read_ahead.search(buf)
        fast_wr = vol_cache_fast_write.search(buf)
        flush_mod = vol_cache_flush_mod.search(buf)
        warn_flush = vol_cache_min_warn_flush.search(buf)
        cache_blk = vol_cache_granularity.search(buf)
        
        self.vol[CACHE]['read_ahead'] = rd_ahead.group(1)
        self.vol[CACHE]['fast_write'] = fast_wr.group(1)
        self.vol[CACHE]['flush_mod'] = flush_mod.group(1)
        self.vol[CACHE]['warn_mod'] = warn_flush.group(1)
        self.vol[CACHE]['cache_block'] = cache_blk.group(1)
        
        requests = vol_io_requests.search(buf)
        blocks = vol_io_blocks.search(buf)
        avg_blocks = vol_io_avg_blocks.search(buf)
        reads = vol_io_reads.search(buf)
        writes = vol_io_writes.search(buf)
        write_alg = vol_io_write_alg.search(buf)
        
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
                                        'sm_writesame': blocks.group(3)
                                        ,
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
                                        'clusters': reads.group(3)}
        
        self.vol[IOSTAT]['writes'] = {
                                        'io': writes.group(1),
                                        'stripes': writes.group(2),
                                        'clusters': writes.group(3)}
        
        self.vol[IOSTAT]['write_algorithm'] = {
                                        'full': write_alg.group(1),
                                        'partial': write_alg.group(2),
                                        'RMW': write_alg.group(3),
                                        'no_parity': write_alg.group(4),
                                        'RMW2': write_alg.group(5),
                                        'FSWT': write_alg.group(6)}
        
        vg_label = vol_vg_label.search(buf)
        drive_cnt = vol_vg_drive_count.search(buf)
        boundary = vol_vg_boundary.search(buf)
        media_type = vol_vg_media_type.search(buf)
        
        self.vol[VGINFO]['vg_label'] = vg_label.group(1)
        self.vol[VGINFO]['drive_count'] = drive_cnt.group(1)
        self.vol[VGINFO]['boundary'] = boundary.group(1)
        self.vol[VGINFO]['media_type'] = media_type.group(1)
        
    def get_ssid(self, dec):
        # Dec is a 'bool' to return a base 10 version of the SSID
        if dec:
            s = str(int(self.vol[INFO]['ssid'], 16))
            return s
        else:
            return self.vol[INFO]['ssid']
    
    def print_vol_info(self):
        
        ssid_hex = self.get_ssid(False)
        ssid_dec = self.get_ssid(True)
        
        print "SSID       : " + ssid_dec + " (" + ssid_hex + ")"
        print "User Label : " + self.vol[INFO]['user_label']
        print "Capacity   : " + self.vol[INFO]['capacity']
        print "BlockSize  : " + self.vol[INFO]['blocksize']
        print "Stripe Size: " + self.vol[INFO]['stripe_size']
        print "Pre-Read   : " + self.vol[INFO]['pre_read']
        print "Cur. Owner : " + self.vol[INFO]['owner']
        print "Pref Owner : " + self.vol[INFO]['preferred_owner']
   
    def print_vol_cache(self):
        
        print "Read Ahead      : " + self.vol[CACHE]['read_ahead']
        print "Fast Write      : " + self.vol[CACHE]['fast_write']
        print "Cache Flush Mod.: " + self.vol[CACHE]['flush_mod']
        print "Min. Warn Mod.  : " + self.vol[CACHE]['warn_mod']
        k = int(self.vol[CACHE]['cache_block']) * 512 / 1024
        print "Cache Block Size: " + str(k) + "K"
    
    def print_vol_vginfo(self):
        
        print "VG Label    : " + self.vol[VGINFO]['vg_label']
        print "Drive Count : " + self.vol[VGINFO]['drive_count']
        print "Boundary    : " + self.vol[VGINFO]['boundary']
        print "Media Type  : " + self.vol[VGINFO]['media_type']
        
    def print_vol_iostats(self):
        pass
    
    def get_value_with_keys(self, cat, key):
        
        return self.vol[cat][key]
    
    def get_iostats_with_keys(self, cat, key):
        
        return self.vol[IOSTAT][cat][key]
    
def build_raid_volumes(statecapture):
    # Generate all RAIDVolume objects with a passed in buffer
    # buffer should be open file object
    statecapture.seek(0)
    buf = statecapture.readlines()
    # Be Kind, Rewind!
    statecapture.seek(0)
    
    temp = StringIO.StringIO()
    start = False
    
    for line in buf:
        
        start_evfshow = executing.search(line)
        
        if start_evfshow:

            if start:
                if start_evfshow.group(1) == "evfShowVol":
                    
                    evfshow = temp.getvalue()
                    match = vol_ownership.search(evfshow)
                    
                    if match.group(1) == "This controller":
                        RAIDVolume(evfshow)
                        temp = StringIO.StringIO()
                    else:
                        temp = StringIO.StringIO()
                        
                else:
                    evfshow = temp.getvalue()
                    match = vol_ownership.search(evfshow)
                    
                    if match.group(1) == "This controller":
                        start = False
                        RAIDVolume(evfshow)
                        temp = StringIO.StringIO()
                    else:
                        start = False
                        temp = StringIO.StringIO()
        
            elif not start:
                if start_evfshow.group(1) == "evfShowVol":
                    start = True
                
        elif start:
            temp.write(line)
            
    del buf

def getRAIDVolumeInstances():
    # Length returned is entries + 1
    c = len(RAIDVolume.instances)
    return c


    
    
