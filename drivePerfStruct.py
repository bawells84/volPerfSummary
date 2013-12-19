import StringIO
import string
from regexes import *
from types import DictType

class ItnData(DictType):

    global IOCOUNT, ERRCOUNT, REDUNDANCY, PERFORMANCE

    IOCOUNT = int(0)
    ERRCOUNT = int(1)
    REDUNDANCY = int(2)
    PERFORMANCE = int(3)

    def __init__(self):

        self[IOCOUNT] = {'r_success': '0',
                         'r_blks_xfer': '0',
                         'w_success': '0',
                         'w_blks_xfer': '0',
                         'queue_depth': '0',
                         'queued': '0',
                         'open_io': '0'
                         }

        self[ERRCOUNT] = {'ch_errs': '0',
                          'hid_abts': '0',
                          'lid_det': '0',
                          'edc': '0',
                          'recovered': '0',
                          'not_ready': '0',
                          'medium': '0',
                          'hw': '0',
                          'ill_req': '0',
                          'unit_attn': '0',
                          'abt_cmd': '0',
                          'other': '0',
                          'busy': '0',
                          'resv_conf': '0',
                          'q_full': '0',
                          'aca_actv': '0',
                          'abort': '0'
                          }

        self[REDUNDANCY] = {'o': '0',
                            'r': '0',
                            'p': '0',
                            'chn0_state': '0',
                            'chn1_state': '0',
                            'chn2_state': '0',
                            'chn3_state': '0'
                            }

        self[PERFORMANCE] = {'r_art': '0',
                             'r_mrt': '0',
                             'w_art': '0',
                             'w_mrt': '0',
                             'old_cmd_age': '0',
                             'bsy_time': '0'
                             }


class IterInstancesDrive(type):
    def __iter__(cls):
        return iter(cls._instances)


class Drive():

    __metaclass__ = IterInstancesDrive

    _instances = []

    def __init__(self):

        self.devnum = ''
        self.tray = ''
        self.slot = ''
        self.role = ''
        self.pi = ''
        self.capacity = ''
        self.blksize = ''
        self.itncnt = ''
        self.onlineitncnt = ''
        self.wwn = ''
        self.ctrla = ItnData()
        self.ctrlb = ItnData()

        Drive._instances.append(self)

    def new_with_drive(self, drive_data):
        pass

    def print_all(self):

        print " [ (0x%s) Tray: %s Slot: %s ITN Count: %s Online ITNs: %s Type: %s ]" % (self.devnum, self.tray, self.slot, self.itncnt, self.onlineitncnt, self.role)
        print ""
        print "  [Controller A]\n"
        print "               READS  - Requests: ( %s )  Blocks: ( %s )  ART: ( %s ms )  MRT: ( %s ms )" % (string.rjust(self.ctrla[IOCOUNT]['r_success'], 12),
                                                                                                            string.rjust(self.ctrla[IOCOUNT]['r_blks_xfer'], 12),
                                                                                                            string.rjust(str(convert_to_millisec(int(self.ctrla[PERFORMANCE]['r_art']))), 8),
                                                                                                            string.rjust(str(convert_to_millisec(int(self.ctrla[PERFORMANCE]['r_mrt']))), 8))
        print "               WRITES - Requests: ( %s )  Blocks: ( %s )  ART: ( %s ms )  MRT: ( %s ms )" % (string.rjust(self.ctrla[IOCOUNT]['w_success'], 12),
                                                                                                            string.rjust(self.ctrla[IOCOUNT]['w_blks_xfer'], 12),
                                                                                                            string.rjust(str(convert_to_millisec(int(self.ctrla[PERFORMANCE]['w_art']))), 8),
                                                                                                            string.rjust(str(convert_to_millisec(int(self.ctrla[PERFORMANCE]['w_mrt']))), 8))
        print ""
        print "        DRIVER ERRORS -   Chn Rel: ( %s )  HID Abort: ( %s )    LID Det: ( %s )        EDC: ( %s )" % (string.rjust(self.ctrla[ERRCOUNT]['ch_errs'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['hid_abts'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['lid_det'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['edc'], 4))
        print "     CHECK CONDITIONS - Recovered: ( %s )  Not Ready: ( %s )     Medium: ( %s )   Hardware: ( %s )" % (string.rjust(self.ctrla[ERRCOUNT]['recovered'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['not_ready'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['medium'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['hw'], 4))
        print "                         Ill. Req: ( %s )  Unit Attn: ( %s )      Abort: ( %s )      Other: ( %s )" % (string.rjust(self.ctrla[ERRCOUNT]['ill_req'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['unit_attn'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['abt_cmd'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['other'], 4))
        print "          SCSI STATUS -      Busy: ( %s ) Resv. Conf: ( %s )     Q Full: ( %s )    Aborted: ( %s )" % (string.rjust(self.ctrla[ERRCOUNT]['busy'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['resv_conf'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['q_full'], 4),
                                                                                                                      string.rjust(self.ctrla[ERRCOUNT]['abort'], 4))
        print ""
        print "  [Controller B]\n"
        print "               READS  - Requests: ( %s )   Blocks: ( %s )  ART: ( %s ms )  MRT: ( %s ms )" % (string.rjust(self.ctrlb[IOCOUNT]['r_success'], 12),
                                                                                                             string.rjust(self.ctrlb[IOCOUNT]['r_blks_xfer'], 12),
                                                                                                             string.rjust(str(convert_to_millisec(int(self.ctrlb[PERFORMANCE]['r_art']))), 8),
                                                                                                             string.rjust(str(convert_to_millisec(int(self.ctrlb[PERFORMANCE]['r_mrt']))), 8))

        print "               WRITES - Requests: ( %s )   Blocks: ( %s )  ART: ( %s ms )  MRT: ( %s ms )" % (string.rjust(self.ctrlb[IOCOUNT]['r_success'], 12),
                                                                                                             string.rjust(self.ctrlb[IOCOUNT]['r_blks_xfer'], 12),
                                                                                                             string.rjust(str(convert_to_millisec(int(self.ctrlb[PERFORMANCE]['r_art']))), 8),
                                                                                                             string.rjust(str(convert_to_millisec(int(self.ctrlb[PERFORMANCE]['r_mrt']))), 8))
        print ""
        print "        DRIVER ERRORS -   Chn Rel: ( %s )  HID Abort: ( %s )    LID Det: ( %s )        EDC: ( %s )" % (string.rjust(self.ctrlb[ERRCOUNT]['ch_errs'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['hid_abts'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['lid_det'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['edc'], 4))
        print "     CHECK CONDITIONS - Recovered: ( %s )  Not Ready: ( %s )     Medium: ( %s )   Hardware: ( %s )" % (string.rjust(self.ctrlb[ERRCOUNT]['recovered'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['not_ready'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['medium'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['hw'], 4))
        print "                         Ill. Req: ( %s )  Unit Attn: ( %s )      Abort: ( %s )      Other: ( %s )" % (string.rjust(self.ctrlb[ERRCOUNT]['ill_req'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['unit_attn'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['abt_cmd'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['other'], 4))
        print "          SCSI STATUS -      Busy: ( %s ) Resv. Conf: ( %s )     Q Full: ( %s )    Aborted: ( %s )" % (string.rjust(self.ctrlb[ERRCOUNT]['busy'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['resv_conf'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['q_full'], 4),
                                                                                                                      string.rjust(self.ctrlb[ERRCOUNT]['abort'], 4))
        print ""


# Parses out first ionShow 12 output found in the state capture
# Returns an ionShow 12 blob


def get_ionshow12(statecapture):

    statecapture.seek(0)
    ionshow12 = StringIO.StringIO()
    start_found = False

    for line in statecapture:

        start = find_ionshow12.search(line)
        end = find_executing.search(line)

        if start and not start_found:
            start_found = True
            continue

        if start_found and end:
            return ionshow12.getvalue()

        elif start_found:
            ionshow12.write(line)


# Use passed in state-capture-data.txt to generate drive objects
#  - Calls state-capture-data to get_ionshow12() to get drive list
#  - Calls populate_drives_by_ctrl() to add drive data

def build_drives(statecapture):

    buf = get_ionshow12(statecapture)

    for line in StringIO.StringIO(buf):

        match = ionshow12_drive.search(line)

        if match:

            if match.group(5) == 'Open':

                drv = Drive()
                drv.devnum = match.group(1)
                drv.tray = match.group(2)
                drv.slot = match.group(3)
                drv.role = match.group(4)
                drv.capacity = match.group(6)
                drv.pi = match.group(7)
                drv.blksize = match.group(8)
                drv.itncnt = match.group(9)
                drv.onlineitncnt = match.group(10)
                drv.wwn = match.group(11)

            else:
                continue
        else:
            continue

    populate_drives_by_ctrl(statecapture, 'a')
    populate_drives_by_ctrl(statecapture, 'b')

# Takes a state-capture-data.txt to get ionShow 99 output for each controller (ctrl_slot) and
# passes this to the process_luall functions to get the relevent data and add them to
# their respective Drive objects.


def populate_drives_by_ctrl(statecapture, ctrl_slot):

    ionshow99 = StringIO.StringIO()
    start_found = False
    statecapture.seek(0)

    if ctrl_slot is 'a':

        for line in statecapture:

            start = find_ionshow99_a.search(line)
            end = find_executing.search(line)

            if start and not start_found:
                start_found = True
                continue

            if start_found and end:
                break

            elif start_found:
                ionshow99.write(line)

    elif ctrl_slot is 'b':

        for line in statecapture:

            start = find_ionshow99_b.search(line)
            end = find_executing.search(line)

            if start and not start_found:
                start_found = True
                continue

            if start_found and end:
                break

            elif start_found:
                ionshow99.write(line)

    process_luall0(ionshow99.getvalue(), ctrl_slot)
    process_luall2(ionshow99.getvalue(), ctrl_slot)
    process_luall3(ionshow99.getvalue(), ctrl_slot)

# Takes ionShow99 output (buf) and a ctrl_slot ('a' or 'b') and populates a Drive object's relative stats
# from the luall 0 output (ORP, Channel states, queue depth and queued commands, open commands, oldest command age)


def process_luall0(buf, ctrl_slot):

    temp = StringIO.StringIO()
    start_found = False

    for line in StringIO.StringIO(buf):

        start = find_luall0.search(line)
        end = nextionshowcommand.search(line)

        if start and not start_found:
            start_found = True
            continue

        if start_found and end:
            luall0 = temp.getvalue()
            del temp
            break

        elif start_found:
            temp.write(line)

    for line in StringIO.StringIO(luall0):

        match = luall0_drive.search(line)

        if match:

            for d in Drive._instances:

                if d.devnum == match.group(1):

                    if ctrl_slot is 'a':

                        d.ctrla[IOCOUNT]['queue_depth'] = match.group(13)
                        d.ctrla[IOCOUNT]['queued'] = match.group(14)
                        d.ctrla[IOCOUNT]['open_io'] = match.group(15)
                        d.ctrla[REDUNDANCY]['o'] = match.group(5)
                        d.ctrla[REDUNDANCY]['r'] = match.group(6)
                        d.ctrla[REDUNDANCY]['p'] = match.group(7)
                        d.ctrla[REDUNDANCY]['chn0_state'] = match.group(8)
                        d.ctrla[REDUNDANCY]['chn1_state'] = match.group(9)
                        d.ctrla[REDUNDANCY]['chn2_state'] = match.group(10)
                        d.ctrla[REDUNDANCY]['chn3_state'] = match.group(11)
                        d.ctrla[PERFORMANCE]['old_cmd_age'] = match.group(18)

                    elif ctrl_slot is 'b':

                        d.ctrlb[IOCOUNT]['queue_depth'] = match.group(13)
                        d.ctrlb[IOCOUNT]['queued'] = match.group(14)
                        d.ctrlb[IOCOUNT]['open_io'] = match.group(15)
                        d.ctrlb[REDUNDANCY]['o'] = match.group(5)
                        d.ctrlb[REDUNDANCY]['r'] = match.group(6)
                        d.ctrlb[REDUNDANCY]['p'] = match.group(7)
                        d.ctrlb[REDUNDANCY]['chn0_state'] = match.group(8)
                        d.ctrlb[REDUNDANCY]['chn1_state'] = match.group(9)
                        d.ctrlb[REDUNDANCY]['chn2_state'] = match.group(10)
                        d.ctrlb[REDUNDANCY]['chn3_state'] = match.group(11)
                        d.ctrlb[PERFORMANCE]['old_cmd_age'] = match.group(18)
                else:
                    continue

# Takes ionShow99 output (buf) and a ctlr_slot ('a' or 'b') and populates a Drive object's relative stats
# from the luall 2 output (SCSI errors, SCSI statuses, HID and LID stats)


def process_luall2(buf, ctrl_slot):

    temp = StringIO.StringIO()
    start_found = False

    for line in StringIO.StringIO(buf):

        start = find_luall2.search(line)
        end = nextionshowcommand.search(line)

        if start and not start_found:
            start_found = True
            continue

        if start_found and end:
            luall2 = temp.getvalue()
            del temp
            break

        elif start_found:
            temp.write(line)

    for line in StringIO.StringIO(luall2):

        match = luall2_drive.search(line)

        if match:

            for d in Drive._instances:

                if d.devnum == match.group(1):

                    if ctrl_slot is 'a':

                        d.ctrla[ERRCOUNT]['ch_errs'] = match.group(5)
                        d.ctrla[ERRCOUNT]['hid_abts'] = match.group(6)
                        d.ctrla[ERRCOUNT]['lid_det'] = match.group(7)
                        d.ctrla[ERRCOUNT]['edc'] = match.group(8)
                        d.ctrla[ERRCOUNT]['recovered'] = match.group(9)
                        d.ctrla[ERRCOUNT]['not_ready'] = match.group(10)
                        d.ctrla[ERRCOUNT]['medium'] = match.group(11)
                        d.ctrla[ERRCOUNT]['hw'] = match.group(12)
                        d.ctrla[ERRCOUNT]['ill_req'] = match.group(13)
                        d.ctrla[ERRCOUNT]['unit_attn'] = match.group(14)
                        d.ctrla[ERRCOUNT]['abt_cmd'] = match.group(15)
                        d.ctrla[ERRCOUNT]['other'] = match.group(16)
                        d.ctrla[ERRCOUNT]['busy'] = match.group(17)
                        d.ctrla[ERRCOUNT]['resv_conf'] = match.group(18)
                        d.ctrla[ERRCOUNT]['q_full'] = match.group(19)
                        d.ctrla[ERRCOUNT]['aca_actv'] = match.group(20)
                        d.ctrla[ERRCOUNT]['abort'] = match.group(21)

                    elif ctrl_slot is 'b':

                        d.ctrlb[ERRCOUNT]['ch_errs'] = match.group(5)
                        d.ctrlb[ERRCOUNT]['hid_abts'] = match.group(6)
                        d.ctrlb[ERRCOUNT]['lid_det'] = match.group(7)
                        d.ctrlb[ERRCOUNT]['edc'] = match.group(8)
                        d.ctrlb[ERRCOUNT]['recovered'] = match.group(9)
                        d.ctrlb[ERRCOUNT]['not_ready'] = match.group(10)
                        d.ctrlb[ERRCOUNT]['medium'] = match.group(11)
                        d.ctrlb[ERRCOUNT]['hw'] = match.group(12)
                        d.ctrlb[ERRCOUNT]['ill_req'] = match.group(13)
                        d.ctrlb[ERRCOUNT]['unit_attn'] = match.group(14)
                        d.ctrlb[ERRCOUNT]['abt_cmd'] = match.group(15)
                        d.ctrlb[ERRCOUNT]['other'] = match.group(16)
                        d.ctrlb[ERRCOUNT]['busy'] = match.group(17)
                        d.ctrlb[ERRCOUNT]['resv_conf'] = match.group(18)
                        d.ctrlb[ERRCOUNT]['q_full'] = match.group(19)
                        d.ctrlb[ERRCOUNT]['aca_actv'] = match.group(20)
                        d.ctrlb[ERRCOUNT]['abort'] = match.group(21)
        else:
            continue

# Takes ionShow99 output (buf) and a ctrl_slot ('a' or 'b') and populates a Drive object's relative stats
# from the luall 3 output (IO Counts, Performance information)


def process_luall3(buf, ctrl_slot):

    temp = StringIO.StringIO()
    start_found = False

    for line in StringIO.StringIO(buf):

        start = find_luall3.search(line)
        end = nextionshowcommand.search(line)

        if start and not start_found:
            start_found = True
            continue

        if start_found and end:
            luall3 = temp.getvalue()
            del temp
            break

        elif start_found:
            temp.write(line)

    for line in StringIO.StringIO(luall3):

        match = luall3_drive.search(line)

        if match:

            for d in Drive._instances:

                if d.devnum == match.group(1):

                    if ctrl_slot is 'a':

                        d.ctrla[IOCOUNT]['r_success'] = match.group(4)
                        d.ctrla[IOCOUNT]['r_blks_xfer'] = match.group(5)
                        d.ctrla[PERFORMANCE]['r_art'] = match.group(6)
                        d.ctrla[PERFORMANCE]['r_mrt'] = match.group(7)
                        d.ctrla[IOCOUNT]['w_success'] = match.group(8)
                        d.ctrla[IOCOUNT]['w_blks_xfer'] = match.group(9)
                        d.ctrla[PERFORMANCE]['w_art'] = match.group(10)
                        d.ctrla[PERFORMANCE]['w_mrt'] = match.group(11)
                        d.ctrla[PERFORMANCE]['bsy_time'] = match.group(14)

                    elif ctrl_slot is 'b':

                        d.ctrlb[IOCOUNT]['r_success'] = match.group(4)
                        d.ctrlb[IOCOUNT]['r_blks_xfer'] = match.group(5)
                        d.ctrlb[PERFORMANCE]['r_art'] = match.group(6)
                        d.ctrlb[PERFORMANCE]['r_mrt'] = match.group(7)
                        d.ctrlb[IOCOUNT]['w_success'] = match.group(8)
                        d.ctrlb[IOCOUNT]['w_blks_xfer'] = match.group(9)
                        d.ctrlb[PERFORMANCE]['w_art'] = match.group(10)
                        d.ctrlb[PERFORMANCE]['w_mrt'] = match.group(11)
                        d.ctrlb[PERFORMANCE]['bsy_time'] = match.group(14)

            else:
                continue

# Find a drive in the Drive object list by devnum
# Returns the matching drive object if found


def find_drive_by_devnum(devnum):

    for drive in Drive._instances:

        if devnum == drive.devnum:
            return drive

# Find a drive in the Drive object list by wwn
# Returns the matching drive object if found

def find_drive_by_wwn(wwn):

    for drive in Drive._instances:

        if wwn == drive.wwn:
            return drive


def convert_to_millisec(num):
    time = float(num)
    factor = float(0.001)

    result = time * factor

    return result