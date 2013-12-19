import StringIO
from regexes import *
from types import DictType

# Metaclass impl for iterator


class IterInstancesVol(type):
    def __iter__(cls):
        return iter(cls._instances)


class RAIDVolume(DictType):
    
    __metaclass__ = IterInstancesVol
    global INFO, CACHE, IOSTAT, VGINFO
        
    _instances = []
        
    INFO = int(0)
    CACHE = int(1)
    IOSTAT = int(2)
    VGINFO = int(3)
    
    def __init__(self, buf):

        self[INFO] = {
                            'ssid': "",
                            'raid_level': "",
                            'user_label': "",
                            'capacity': "",
                            'blocksize': "",
                            'segment_size': "",
                            'stripe_size': "",
                            'pre_read': "",
                            'owning_ctrl': "",
                            'owner': "",
                            'preferred_owner': ""
        }
        
        self[CACHE] = {
                            'read_ahead': "",
                            'fast_write': "",
                            'flush_mod': "",
                            'warn_mod': "",
                            'cache_block': "",
        }
        
        self[IOSTAT] = {
                            'requests': "",
                            'blocks': "",
                            'avg_blocks': "",
                            'reads': "",
                            'writes': "",
                            'write_algorithm': ""
        }
        
        self[VGINFO] = {
                            'vg_label': "",
                            'drive_count': "",
                            'boundary': "",
                            'media_type': ""
        }
        
        voltype = vol_ssid_type.search(buf)
        
        if voltype:
            
            if voltype.group(2) == "RAIDVolume":
                ssid = voltype.group(1)
                self.populate_with_buffer(buf, ssid)
                RAIDVolume._instances.append(self)
            else:
                del self

    @classmethod
    def build_raid_volumes(cls, statecapture):
        """
        Generate all RAIDVolume objects with a passed in buffer
        buffer should be open file object
        @param statecapture: A state-capture-data.txt
        """
        statecapture.seek(0)
        buf = statecapture.readlines()
        # Be Kind, Rewind!
        statecapture.seek(0)

        temp = StringIO.StringIO()
        start = False

        for line in buf:

            start_evfshow = find_executing.search(line)

            if start_evfshow:

                if start:
                    if start_evfshow.group(1) == "evfShowVol":

                        evfshow = temp.getvalue()
                        match = vol_ownership.search(evfshow)

                        if match.group(1) == "This controller":
                            RAIDVolume(evfshow)
                            temp = StringIO.StringIO()
                            temp.write(line)
                        else:
                            temp = StringIO.StringIO()
                            temp.write(line)

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
                        temp.write(line)
                        start = True

            elif start:
                temp.write(line)

        del buf

    def populate_with_buffer(self, buf, ssid):
        """
        Populate the RAIDVolume instance's dict
        @param buf: A buffer of one volume's evfShowVol output
        @param ssid: The SSID of the RAIDVolume instance to populate
        """
        owning_ctrl = vol_evfshowvol.search(buf)
        user_label = vol_user_label.search(buf)
        raid_level = vol_raid_level.search(buf)
        capacity = vol_capacity.search(buf)
        blksize = vol_blocksize.search(buf)
        seg_size = vol_segment_size.search(buf)
        stripe_sz = vol_stripe_size.search(buf)
        pre_rd = vol_pre_read.search(buf)
        owner = vol_ownership.search(buf)
        pref_own = vol_pref_ownership.search(buf)
        
        self[INFO]['ssid'] = ssid
        self[INFO]['raid_level'] = raid_level.group(1)
        self[INFO]['user_label'] = user_label.group(1)
        self[INFO]['capacity'] = capacity.group(1)
        self[INFO]['blocksize'] = blksize.group(1)
        self[INFO]['segment_size'] = seg_size.group(1)
        self[INFO]['stripe_size'] = stripe_sz.group(1)
        self[INFO]['pre_read'] = pre_rd.group(1)
        self[INFO]['owning_ctrl'] = owning_ctrl.group(3)
        self[INFO]['owner'] = owner.group(1)
        self[INFO]['preferred_owner'] = pref_own.group(1)
        
        rd_ahead = vol_cache_read_ahead.search(buf)
        fast_wr = vol_cache_fast_write.search(buf)
        flush_mod = vol_cache_flush_mod.search(buf)
        warn_flush = vol_cache_min_warn_flush.search(buf)
        cache_blk = vol_cache_granularity.search(buf)
        
        self[CACHE]['read_ahead'] = rd_ahead.group(1)
        self[CACHE]['fast_write'] = fast_wr.group(1)
        self[CACHE]['flush_mod'] = flush_mod.group(1)
        self[CACHE]['warn_mod'] = warn_flush.group(1)
        self[CACHE]['cache_block'] = cache_blk.group(1)
        
        requests = vol_io_requests.search(buf)
        blocks = vol_io_blocks.search(buf)
        avg_blocks = vol_io_avg_blocks.search(buf)
        reads = vol_io_reads.search(buf)
        writes = vol_io_writes.search(buf)
        
        self[IOSTAT]['requests'] = {
                                        'sm_reads': requests.group(1),
                                        'sm_writes': requests.group(2),
                                        'sm_writesame': requests.group(3),
                                        'lg_reads': requests.group(4),
                                        'lg_writes': requests.group(5),
                                        'lg_writesame': requests.group(6),
                                        'comp_write': requests.group(7),
                                        'total': requests.group(8),
                                        'cache_hits': requests.group(9)}
        
        self[IOSTAT]['blocks'] = {
                                        'sm_reads': blocks.group(1),
                                        'sm_writes': blocks.group(2),
                                        'sm_writesame': blocks.group(3),
                                        'lg_reads': blocks.group(4), 
                                        'lg_writes': blocks.group(5),
                                        'lg_writesame': blocks.group(6),
                                        'comp_write': blocks.group(7),
                                        'total': blocks.group(8),
                                        'cache_hits': blocks.group(9)}
        
        self[IOSTAT]['avg_blocks'] = {
                                        'sm_reads': avg_blocks.group(1),
                                        'sm_writes': avg_blocks.group(2),
                                        'sm_writesame': avg_blocks.group(3),
                                        'lg_reads': avg_blocks.group(4),
                                        'lg_writes': avg_blocks.group(5),
                                        'lg_writesame': avg_blocks.group(6),
                                        'comp_write': avg_blocks.group(7),
                                        'total': avg_blocks.group(8),
                                        'cache_hits': avg_blocks.group(9)}
        
        self[IOSTAT]['reads'] = {
                                        'io': reads.group(1),
                                        'stripes': reads.group(2),
                                        'clusters': reads.group(3)}
        
        self[IOSTAT]['writes'] = {
                                        'io': writes.group(1),
                                        'stripes': writes.group(2),
                                        'clusters': writes.group(3)}
        
        if int(raid_level.group(1)) in {5, 6}:

            write_alg = vol_io_write_alg.search(buf)
            self[IOSTAT]['write_algorithm'] = {
                                            'full': write_alg.group(1),
                                            'partial': write_alg.group(2),
                                            'RMW': write_alg.group(3),
                                            'no_parity': write_alg.group(4),
                                            'RMW2': write_alg.group(5),
                                            'FSWT': write_alg.group(6)}

        vol_trad = vol_is_trad.search(buf)
        vol_crush = vol_is_crush.search(buf)

        if vol_trad:

            vg_label = vol_vg_label.search(buf)
            drive_cnt = vol_vg_drive_count.search(buf)
            boundary = vol_vg_boundary.search(buf)
            media_type = vol_vg_media_type.search(buf)
            self[VGINFO]['vg_label'] = vg_label.group(1)
            self[VGINFO]['drive_count'] = drive_cnt.group(1)
            self[VGINFO]['boundary'] = boundary.group(1)
            self[VGINFO]['media_type'] = media_type.group(1)

        elif vol_crush:

            vg_label_crush = vol_vg_label_crush.search(buf)
            drive_cnt_crush = vol_vg_drive_count_crush.search(buf)

            self[VGINFO]['vg_label'] = vg_label_crush.group(1)
            self[VGINFO]['drive_count'] = drive_cnt_crush.group(1)
            self[VGINFO]['boundary'] = 'CRUSH'
            self[VGINFO]['media_type'] = 'CRUSH'



    def get_ssid(self, dec):
        """
        Get a RAIDVolume instance's SSID in hex or decimal
        @param dec: BOOL to return a decimal version of the SSID
        @return: Volume SSID
        """
        if dec:
            s = str(int(self[INFO]['ssid'], 16))
            return s
        else:
            return self[INFO]['ssid']

    def print_vol_info(self):
        """
        Print a RAIDVolume instance's INFO
        """
        ssid_hex = self.get_ssid(False)
        ssid_dec = self.get_ssid(True)
        
        print " SSID             : " + ssid_dec + " (" + ssid_hex + ")"
        print " RAID Level       : " + self[INFO]['raid_level']
        print " User Label       : " + self[INFO]['user_label']
        print " Capacity         : " + self[INFO]['capacity'] + " blocks"
        print " BlockSize        : " + self[INFO]['blocksize'] + " bytes"
        print " Segment Size     : " + self[INFO]['segment_size'] + " blocks"
        print " Stripe Size      : " + self[INFO]['stripe_size'] + " blocks"
        print " Pre-Read         : " + self[INFO]['pre_read']
        print " Cur. Owner       : " + self[INFO]['owner'] + " (" + self[INFO]['owning_ctrl'] + ")"
        print " Pref Owner       : " + self[INFO]['preferred_owner']
        print " "

    def print_vol_cache(self):
        """
        Print a RAIDVolume instance's CACHE info
        """
        print " Read Ahead       : " + self[CACHE]['read_ahead']
        print " Fast Write       : " + self[CACHE]['fast_write']
        print " Cache Flush Mod. : " + self[CACHE]['flush_mod']
        print " Min. Warn Mod.   : " + self[CACHE]['warn_mod']
        k = int(self[CACHE]['cache_block']) * 512 / 1024
        print " Cache Block Size : %dK (%s blocks)" % (k, self[CACHE]['cache_block'])
        print " "

    def print_vol_vginfo(self):
        """
        Print a RAIDVolume instance's VGINFO
        """
        print " VG Label         : " + self[VGINFO]['vg_label']
        print " Drive Count      : " + self[VGINFO]['drive_count']
        print " Boundary         : " + self[VGINFO]['boundary']
        print " Media Type       : " + self[VGINFO]['media_type']
        
    def print_vol_iostats(self):
        pass

    def get_value_with_keys(self, cat, key):
        """
        Get the value off a RAIDVolume instance's dict
        @param cat: INFO, CACHE, VGINFO
        @param key: String of the key being requested
        @return: Returns value requested if value of cat meets criteria, otherwise returns False
        """
        if cat in [INFO, CACHE, VGINFO]:
            return self[cat][key]
        else:
            return False

    # Direct access to a RAIDVolume instrance's IOSTAT dict
    # by passing an IOSTAT category and relative key.

    def get_iostats_with_keys(self, cat, key):
        return self[IOSTAT][cat][key]


def get_raid_volume_instances():
    # Length returned is entries + 1
    c = len(RAIDVolume.instances)
    return c

def print_all_volumes():

    for v in RAIDVolume._instances:
        v.print_vol_info()
        v.print_vol_cache()
        v.print_vol_vginfo()