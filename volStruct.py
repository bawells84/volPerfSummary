import StringIO
from regexes import *
from types import DictType


class VolPerformanceData(DictType):

    global REQUESTS, BLOCKS, AVGBLOCKS, READS, WRITES, ALG, RESPONSE

    REQUESTS = int(0)
    BLOCKS = int(1)
    AVGBLOCKS = int(2)
    READS = int(3)
    WRITES = int(4)
    ALG = int(5)
    RESPONSE = int(6)

    def __init__(self):

        self[REQUESTS] = {
                            'sm_reads': '0',
                            'sm_writes': '0',
                            'sm_writesame': '0',
                            'lg_reads': '0',
                            'lg_writes': '0',
                            'lg_writesame': '0',
                            'comp_write': '0',
                            'total': '0',
                            'cache_hits': '0'}

        self[BLOCKS] = {
                            'sm_reads': '0',
                            'sm_writes': '0',
                            'sm_writesame': '0',
                            'lg_reads': '0',
                            'lg_writes': '0',
                            'lg_writesame': '0',
                            'comp_write': '0',
                            'total': '0',
                            'cache_hits': '0'}

        self[AVGBLOCKS] = {
                            'sm_reads': '0',
                            'sm_writes': '0',
                            'sm_writesame': '0',
                            'lg_reads': '0',
                            'lg_writes': '0',
                            'lg_writesame': '0',
                            'comp_write': '0',
                            'total': '0',
                            'cache_hits': '0'}

        self[READS] = {
                            'io': '0',
                            'stripes': '0',
                            'clusters': '0'}

        self[WRITES] = {
                            'io': '0',
                            'stripes': '0',
                            'clusters': '0'}

        self[ALG] = {
                            'full': '0',
                            'partial': '0',
                            'RMW': '0',
                            'no_parity': '0',
                            'RMW2': '0',
                            'FSWT': '0'}

        self[RESPONSE] = {
                            'read_art': '0',
                            'read_mrt': '0',
                            'write_art': '0',
                            'write_mrt': '0'}

    def fill_with_data(self, buf):

        raid_level = vol_raid_level.search(buf)
        requests = vol_io_requests.search(buf)
        blocks = vol_io_blocks.search(buf)
        avg_blocks = vol_io_avg_blocks.search(buf)
        reads = vol_io_reads.search(buf)
        writes = vol_io_writes.search(buf)

        self[REQUESTS] = {
                            'sm_reads': requests.group(1),
                            'sm_writes': requests.group(2),
                            'sm_writesame': requests.group(3),
                            'lg_reads': requests.group(4),
                            'lg_writes': requests.group(5),
                            'lg_writesame': requests.group(6),
                            'comp_write': requests.group(7),
                            'total': requests.group(8),
                            'cache_hits': requests.group(9)}

        self[BLOCKS] = {
                            'sm_reads': blocks.group(1),
                            'sm_writes': blocks.group(2),
                            'sm_writesame': blocks.group(3),
                            'lg_reads': blocks.group(4),
                            'lg_writes': blocks.group(5),
                            'lg_writesame': blocks.group(6),
                            'comp_write': blocks.group(7),
                            'total': blocks.group(8),
                            'cache_hits': blocks.group(9)}

        self[AVGBLOCKS] = {
                            'sm_reads': avg_blocks.group(1),
                            'sm_writes': avg_blocks.group(2),
                            'sm_writesame': avg_blocks.group(3),
                            'lg_reads': avg_blocks.group(4),
                            'lg_writes': avg_blocks.group(5),
                            'lg_writesame': avg_blocks.group(6),
                            'comp_write': avg_blocks.group(7),
                            'total': avg_blocks.group(8),
                            'cache_hits': avg_blocks.group(9)}

        self[READS] = {
                            'io': reads.group(1),
                            'stripes': reads.group(2),
                            'clusters': reads.group(3)}

        self[WRITES] = {
                            'io': writes.group(1),
                            'stripes': writes.group(2),
                            'clusters': writes.group(3)}

        if int(raid_level.group(1)) in {5, 6}:

            write_alg = vol_io_write_alg.search(buf)

            self[ALG] = {
                            'full': write_alg.group(1),
                            'partial': write_alg.group(2),
                            'RMW': write_alg.group(3),
                            'no_parity': write_alg.group(4),
                            'RMW2': write_alg.group(5),
                            'FSWT': write_alg.group(6)}

    def fill_response_times(self, match):

        self[RESPONSE]['read_art'] = match.group(4)
        self[RESPONSE]['read_mrt'] = match.group(5)
        self[RESPONSE]['write_art'] = match.group(8)
        self[RESPONSE]['write_mrt'] = match.group(9)


# Metaclass impl for iterator

class IterInstancesVol(type):
    def __iter__(cls):
        return iter(cls._instances)


class RAIDVolume():
    
    __metaclass__ = IterInstancesVol
    global INFO, CACHE, IOSTAT, VGINFO
        
    _instances = []
        
    INFO = int(0)
    CACHE = int(1)
    IOSTAT = int(2)
    VGINFO = int(3)
    
    def __init__(self, buf):

        self.ctrla = VolPerformanceData()
        self.ctrlb = VolPerformanceData()

        self.info = {
                            'ssid': "",
                            'raid_level': "",
                            'user_label': "",
                            'capacity': "",
                            'blocksize': "",
                            'segment_size': "",
                            'stripe_size': "",
                            'pre_read': "",
                            'on_preferred': "",
                            'owned_by': "",
                            'alt_owner': ""
        }
        
        self.cache = {
                            'read_ahead': "",
                            'fast_write': "",
                            'flush_mod': "",
                            'warn_mod': "",
                            'cache_block': "",
        }
        
        self.vginfo = {
                            'vg_label': "",
                            'drive_count': "",
                            'boundary': "",
                            'media_type': ""
        }
        
        voltype = vol_ssid_type.search(buf)
        ctrl_slot = vol_evfshowvol.search(buf)
        
        if voltype:
            
            if voltype.group(2) == "RAIDVolume":

                ssid = voltype.group(1)
                ctrl = ctrl_slot.group(3)

                self.populate_with_buffer(buf, ssid)
                self.populate_performance(buf, ctrl)
                RAIDVolume._instances.append(self)
            else:
                del self

    @classmethod
    def find_vol(cls, ssid):

        if len(RAIDVolume._instances) > 0:

            for vol in RAIDVolume._instances:

                match = vol.info['ssid']
                if ssid == match:
                    return vol
                else:
                    pass
        else:
            pass

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
                        ctrl = vol_evfshowvol.search(evfshow)
                        ssid = vol_ssid_type.search(evfshow)
                        exists = RAIDVolume.find_vol(ssid.group(1))

                        if exists:
                            exists.populate_performance(evfshow, ctrl.group(3))
                            temp = StringIO.StringIO()
                            temp.write(line)
                        else:
                            RAIDVolume(evfshow)
                            temp = StringIO.StringIO()
                            temp.write(line)

                    else:

                        evfshow = temp.getvalue()
                        ctrl = vol_evfshowvol.search(evfshow)
                        ssid = vol_ssid_type.search(evfshow)
                        exists = RAIDVolume.find_vol(ssid.group(1))

                        if exists:
                            start = False
                            exists.populate_performance(evfshow, ctrl.group(3))
                            temp = StringIO.StringIO()
                        else:
                            RAIDVolume(evfshow)
                            start = False
                            temp = StringIO.StringIO()

                elif not start:
                    if start_evfshow.group(1) == "evfShowVol":
                        temp.write(line)
                        start = True

            elif start:
                temp.write(line)

        del buf

    @classmethod
    def get_vdall(cls, statecapture):

        start = False
        ctrl = 0
        temp = StringIO.StringIO()
        statecapture.seek(0)

        for line in statecapture:

            vdall_start = find_vdall.search(line)
            end = find_executing.search(line)

            if vdall_start:
                if vdall_start.group(1) == 'A':
                    ctrl_slot = vdall_start.group(1)
                    temp.write(line)
                    start = True

                elif vdall_start.group(1) == 'B':
                    ctrl_slot = vdall_start.group(1)
                    temp.write(line)
                    start = True

            elif start and end:
                RAIDVolume.add_vdall_data(temp.getvalue(), ctrl_slot)
                temp = StringIO.StringIO()
                start = False

            elif start:
                temp.write(line)

    @classmethod
    def add_vdall_data(cls, vdall, ctrl_slot):

        for line in StringIO.StringIO(vdall):

            entry = vdall_entry.search(line)

            if entry:
                ssid = int(entry.group(1), 16)
                vol = RAIDVolume.find_vol("{0:#x}".format(ssid))

                if vol and ctrl_slot == 'A':
                    vol.ctrla.fill_response_times(entry)

                elif vol and ctrl_slot == 'B':
                    vol.ctrlb.fill_response_times(entry)

    def populate_with_buffer(self, buf, ssid):
        """
        Populate the RAIDVolume instance's dict
        @param buf: A buffer of one volume's evfShowVol output
        @param ssid: The SSID of the RAIDVolume instance to populate
        """
        ctrl = vol_evfshowvol.search(buf)
        user_label = vol_user_label.search(buf)
        raid_level = vol_raid_level.search(buf)
        capacity = vol_capacity.search(buf)
        blksize = vol_blocksize.search(buf)
        seg_size = vol_segment_size.search(buf)
        stripe_sz = vol_stripe_size.search(buf)
        pre_rd = vol_pre_read.search(buf)
        owner = vol_ownership.search(buf)
        pref_own = vol_pref_ownership.search(buf)
        
        self.info['ssid'] = ssid
        self.info['raid_level'] = raid_level.group(1)
        self.info['user_label'] = user_label.group(1)
        self.info['capacity'] = capacity.group(1)
        self.info['blocksize'] = blksize.group(1)
        self.info['segment_size'] = seg_size.group(1)
        self.info['stripe_size'] = stripe_sz.group(1)
        self.info['pre_read'] = pre_rd.group(1)

        if pref_own.group(1) == 'This controller' and owner.group(1) == 'This controller':

            if ctrl.group(3) == 'A':
                self.info['on_preferred'] = 'True'
                self.info['owned_by'] = 'A'
                self.info['alt_owner'] = 'B'
            else:
                self.info['on_preferred'] = 'True'
                self.info['owned_by'] = 'B'
                self.info['alt_owner'] = 'A'

        elif pref_own.group(1) == 'Alternate' and owner.group(1) == 'This controller':

            if ctrl.group(3) == 'A':
                self.info['on_preferred'] = 'False'
                self.info['alt_owner'] = 'B'
                self.info['owned_by'] = 'A'
            else:
                self.info['on_preferred'] = 'False'
                self.info['alt_owner'] = 'A'
                self.info['owned_by'] = 'B'

        elif pref_own.group(1) == 'Alternate' and owner.group(1) == 'Alternate':

            if ctrl.group(3) == 'A':
                self.info['on_preferred'] = 'True'
                self.info['alt_owner'] = 'A'
                self.info['owned_by'] = 'B'
            else:
                self.info['on_preferred'] = 'True'
                self.info['alt_owner'] = 'B'
                self.info['owned_by'] = 'A'

        rd_ahead = vol_cache_read_ahead.search(buf)
        fast_wr = vol_cache_fast_write.search(buf)
        flush_mod = vol_cache_flush_mod.search(buf)
        warn_flush = vol_cache_min_warn_flush.search(buf)
        cache_blk = vol_cache_granularity.search(buf)
        
        self.cache['read_ahead'] = rd_ahead.group(1)
        self.cache['fast_write'] = fast_wr.group(1)
        self.cache['flush_mod'] = flush_mod.group(1)
        self.cache['warn_mod'] = warn_flush.group(1)
        self.cache['cache_block'] = cache_blk.group(1)

        vol_trad = vol_is_trad.search(buf)
        vol_crush = vol_is_crush.search(buf)

        if vol_trad:

            vg_label = vol_vg_label.search(buf)
            drive_cnt = vol_vg_drive_count.search(buf)
            boundary = vol_vg_boundary.search(buf)
            media_type = vol_vg_media_type.search(buf)
            self.vginfo['vg_label'] = vg_label.group(1)
            self.vginfo['drive_count'] = drive_cnt.group(1)
            self.vginfo['boundary'] = boundary.group(1)
            self.vginfo['media_type'] = media_type.group(1)

        elif vol_crush:

            vg_label_crush = vol_vg_label_crush.search(buf)
            drive_cnt_crush = vol_vg_drive_count_crush.search(buf)

            self.vginfo['vg_label'] = vg_label_crush.group(1)
            self.vginfo['drive_count'] = drive_cnt_crush.group(1)
            self.vginfo['boundary'] = 'CRUSH'
            self.vginfo['media_type'] = 'CRUSH'

    def populate_performance(self, buf, ctrl):

        if ctrl == 'A':
            self.ctrla.fill_with_data(buf)

        elif ctrl == 'B':
            self.ctrlb.fill_with_data(buf)

    def get_ssid(self, dec):
        """
        Get a RAIDVolume instance's SSID in hex or decimal
        @param dec: BOOL to return a decimal version of the SSID
        @return: Volume SSID
        """
        if dec:
            s = str(int(self.info['ssid'], 16))
            return s
        else:
            return self.info['ssid']

    def print_vol_info(self):
        """
        Print a RAIDVolume instance's INFO
        """
        ssid_hex = self.get_ssid(False)
        ssid_dec = self.get_ssid(True)
        
        print " SSID              : " + ssid_dec + " (" + ssid_hex + ")"
        print " RAID Level        : " + self.info['raid_level']
        print " User Label        : " + self.info['user_label']
        print " Capacity          : " + self.info['capacity'] + " blocks"
        print " BlockSize         : " + self.info['blocksize'] + " bytes"
        print " Segment Size      : " + self.info['segment_size'] + " blocks"
        print " Stripe Size       : " + self.info['stripe_size'] + " blocks"
        print " Pre-Read          : " + self.info['pre_read']
        print " Cur. Owner        : " + self.info['owned_by']
        print " On Preferred Path : " + self.info['on_preferred']
        print " "

    def print_vol_cache(self):
        """
        Print a RAIDVolume instance's CACHE info
        """
        print " Read Ahead        : " + self.cache['read_ahead']
        print " Fast Write        : " + self.cache['fast_write']
        print " Cache Flush Mod.  : " + self.cache['flush_mod']
        print " Min. Warn Mod.    : " + self.cache['warn_mod']
        k = int(self.cache['cache_block']) * 512 / 1024
        print " Cache Block Size  : %dK (%s blocks)" % (k, self.cache['cache_block'])
        print " "

    def print_vol_vginfo(self):
        """
        Print a RAIDVolume instance's VGINFO
        """
        print " VG Label          : " + self.vginfo['vg_label']
        print " Drive Count       : " + self.vginfo['drive_count']
        print " Boundary          : " + self.vginfo['boundary']
        print " Media Type        : " + self.vginfo['media_type']
        print " "
        
    def show_io_share(self):

        ctrl_a_total = self.get_iostats_with_keys_a('requests', 'total')
        ctrl_b_total = self.get_iostats_with_keys_b('requests', 'total')

        total = ctrl_a_total + ctrl_b_total

        if ctrl_a_total > 0:
            ctrl_a_ratio = (float(ctrl_a_total) / float(total)) * 100
        else:
            ctrl_a_ratio = 0

        if ctrl_b_total > 0:
            ctrl_b_ratio = (float(ctrl_b_total) / float(total)) * 100
        else:
            ctrl_b_ratio = 0

        print " IO Load by Controller -\n"
        print "         Controller A: %d %%" % ctrl_a_ratio
        print "         Controller B: %d %%" % ctrl_b_ratio
        print ""

    def get_value_with_keys(self, cat, key):
        """
        Get the value off a RAIDVolume instance's dict
        @param cat: INFO, CACHE, VGINFO
        @param key: String of the key being requested
        @return: Returns value requested if value of cat meets criteria, otherwise returns False
        """
        if cat in [INFO, CACHE, VGINFO]:
            if cat == INFO:
                return self.info[key]
            elif cat == CACHE:
                return self.cache[key]
            elif cat == VGINFO:
                return self.vginfo[key]
        else:
            return False

    def get_iostats_with_keys_a(self, cat, key):

        if cat is 'reads':
            value = int(self.ctrla[READS][key])
            return value
        elif cat is 'writes':
            value = int(self.ctrla[WRITES][key])
            return value
        elif cat is 'avg_blocks':
            value = int(self.ctrla[AVGBLOCKS][key])
            return value
        elif cat is 'write_algorithm':
            value = int(self.ctrla[ALG][key])
            return value
        elif cat is 'blocks':
            value = int(self.ctrla[BLOCKS][key])
            return value
        elif cat is 'requests':
            value = int(self.ctrla[REQUESTS][key])
            return value
        elif cat is 'response':
            value = int(self.ctrla[RESPONSE][key])
            return value

    def get_iostats_with_keys_b(self, cat, key):

        if cat is 'reads':
            value = int(self.ctrlb[READS][key])
            return value
        elif cat is 'writes':
            value = int(self.ctrlb[WRITES][key])
            return value
        elif cat is 'avg_blocks':
            value = int(self.ctrlb[AVGBLOCKS][key])
            return value
        elif cat is 'write_algorithm':
            value = int(self.ctrlb[ALG][key])
            return value
        elif cat is 'blocks':
            value = int(self.ctrlb[BLOCKS][key])
            return value
        elif cat is 'requests':
            value = int(self.ctrlb[REQUESTS][key])
            return value
        elif cat is 'response':
            value = int(self.ctrlb[RESPONSE][key])
            return value

    def get_combined_iostats_with_keys(self, cat, key):

        if cat is 'reads':
            value = int(self.ctrla[READS][key]) + int(self.ctrlb[READS][key])
            return value
        elif cat is 'writes':
            value = int(self.ctrla[WRITES][key]) + int(self.ctrlb[WRITES][key])
            return value
        elif cat is 'avg_blocks':
            ctrla = (int(self.ctrla[BLOCKS][key]), int(self.ctrla[REQUESTS][key]))
            ctrlb = (int(self.ctrlb[BLOCKS][key]), int(self.ctrlb[REQUESTS][key]))
            data = [ctrla, ctrlb]
            value = calculate_combined_avg(data)
            return value
        elif cat is 'write_algorithm':
            value = int(self.ctrla[ALG][key]) + int(self.ctrlb[ALG][key])
            return value
        elif cat is 'blocks':
            value = int(self.ctrla[BLOCKS][key]) + int(self.ctrlb[BLOCKS][key])
            return value

## Supporting functions not specific to an instance of either class


def calculate_combined_avg(data):

    ctrla = data[0]
    ctrlb = data[1]

    if ctrla[1] < 1:
        if ctrlb[1] > 0:
            avg = ctrlb[0] / ctrlb[1]
            return avg
        else:
            return 0
    elif ctrlb[1] < 1:
        if ctrla[1] > 0:
            avg = ctrla[0] / ctrla[1]
            return avg
        else:
            return 0
    else:
        blocks = ctrla[0] + ctrlb[0]
        requests = ctrla[1] + ctrlb[1]
        avg = blocks / requests
        return avg


def get_raid_volume_instances():
    # Length returned is entries + 1
    c = len(RAIDVolume.instances)
    return c


def print_all_volumes():

    for v in RAIDVolume._instances:
        v.print_vol_info()
        v.print_vol_cache()
        v.print_vol_vginfo()
