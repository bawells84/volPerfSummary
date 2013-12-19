from volStruct import *

# Metaclass impl for iterator over instances list


class IterInstancesVG(type):
    def __iter__(cls):
        return iter(cls._instances)


class VolumeGroup():
    __metaclass__ = IterInstancesVG
    _instances = []

    def __init__(self, buf):

        raid = vg_raid.search(buf)
        crush =vg_crush.search(buf)
        label = vg_label.search(buf)
        vols = vg_vol_count.search(buf)
        active = vg_act_drives.search(buf)
        inactive = vg_inact_drives.search(buf)
        state = vg_state.search(buf)
        secure = vg_secure.search(buf)
        pi_info = vg_pi_info.search(buf)

        self.label = label.group(1)
        if raid:
            self.raid = raid.group(1)

        elif crush:
            self.raid = 'CRUSH'
        self.vol_cnt = vols.group(1)
        self.drv_cnt = int(active.group(1)) + int(inactive.group(1))
        self.state = state.group(1)
        self.act_drv = active.group(1)
        self.inact_drv = inactive.group(1)
        self.secure = secure.group(1)
        self.pi_enable = pi_info.group(1)
        self.pi_type = pi_info.group(2)
        self.pieces = dict()
        self.volumes = []

        self.add_pieces(buf)

        VolumeGroup._instances.append(self)

    @classmethod
    def build_volume_groups(cls, statecapture):
        """
        Find and create a VolumeGroup object for all volume groups found.
        Takes a state-capture-data.txt as an argument and passes it to get_vginfo()
        to return only the vdmShowVGInfo output to parse.

        Is a classmethod and is called by VolumeGroup.build_volume_groups(statecapture)
        @param statecapture: A state-capture-data.txt file
        """
        buf = get_vginfo(statecapture)
        temp = StringIO.StringIO()
        start = False

        for line in StringIO.StringIO(buf):

            start_seq = vg_entry_start.search(line)

            if start_seq:
                #print "build_volume_groups: start of VG found "
                start = True
                #print line
                temp.write(line)

            elif len(line) > 1:
                #print line
                temp.write(line)

            elif len(line) == 1 and start is True:
                #print "build_volume_groups: calling VolumeGroup()"
                VolumeGroup(temp.getvalue())
                del temp
                temp = StringIO.StringIO()
                start = False

            elif len(line) == 1 and start is False:
                continue

    @classmethod
    def find_and_add_all_volumes(cls):

        """
        Populate the VolumeGroup object's .volumes[] list with their respective RAIDVolume object
        Checks to make sure there are RAIDVolume objects before attempting.

        @return: False if no RAIDVolume objects exist, True otherwise
        """
        if len(RAIDVolume._instances) < 1:
            return False

        else:
            for g in VolumeGroup._instances:

                vglabel = g.label

                for v in RAIDVolume._instances:

                    vollabel = v.get_value_with_keys(VGINFO, 'vg_label')

                    if vglabel == vollabel:
                        g.add_volume(v)

                    else:
                        continue

    ## INSTANCE METHODS ##

    def add_volume(self, vol):
        """
        Adds a RAIDVolume object to a VolumeGroup instance's .volumes[] list.

        @param vol: A RAIDVolume Object
        """
        self.volumes.append(vol)

    def add_piece(self, drv, pc):
        """
        Add a piece dict to the VolumeGroup instance's pieces dict with is keyed by ordinal

        @param drv: A piece structure for a drive
        @param pc: The piece's ordinal
        @return: True if add is successful, False if not
        """
        if type(drv) is dict:

            self.pieces[pc] = drv
            return True

        else:
            return False

    # Add all pieces of a volume group to a VolumeGroup using a buffer
    # that contains a single volume group's worth of output from vdmShowVGInfo.
    # Calls add_piece and passes a drive

    def add_pieces(self, buf):
        """
        Find and add all pieces of a Volume Group to the VolumeGroup instance's
        pieces dictionary.
        @param buf: A single Volume Group worth of output from vdmShowVGInfo
        @return: True if number of pieces added matches drv_cnt for the VG
        """

        count = 0

        for line in StringIO.StringIO(buf):
            match = vg_drive_entry.search(line)

            if match:

                drv = {'piece': match.group(3),
                       'devnum': match.group(2),
                       'tray': match.group(4),
                       'slot': match.group(5),
                       'acc_state': match.group(6),
                       'drv_state': match.group(7)
                }
                pc = int(drv['piece']) - 1

                if self.add_piece(drv, pc):
                    count += 1
            else:
                continue

        if count == self.drv_cnt:
            return True
        else:
            return False

    def print_info(self):
        print " Volume Group Information:"
        print "  Label         : " + self.label
        print "  State         : " + self.state
        print "  RAID Level    : " + self.raid
        print "  Secure (FDE)  : " + self.secure
        print "  T10PI         : " + self.pi_enable
        if self.pi_enable == 'T':
            print "  PI Type       : " + self.pi_type
        print "  Total Drives  : " + str(self.drv_cnt)
        print "  ---Active     : " + self.act_drv
        print "  ---Inactive   : " + self.inact_drv
        print "\n"



## Functions to parse required output (vdmShowVGInfo) and generate
## VolumeGroup objects from an array's state-capture-data.txt

# Takes a state-capture-data.txt and returns the vdmShowVGInfo command output.


def get_vginfo(statecapture):
    """
    Parses the array state capture file for a vdmShowVGInfo output block
    @param statecapture: A state-capture-data.txt
    @return: A buffer of vdmShowVGInfo output from the state-capture-data.txt
    """
    start_found = False
    statecapture.seek(0)
    buf = statecapture.readlines()
    statecapture.seek(0)

    temp = StringIO.StringIO()

    for line in buf:

        cmd_start = find_vdmShowVGInfo.search(line)
        cmd_end = find_executing.search(line)

        if not start_found:
            if cmd_start:
                #print "get_vginfo: Found Start"
                start_found = True

        elif start_found:
            if cmd_end:
                vdmshowvginfo = temp.getvalue()
                #print "Returning vdmshowvginfo"
                return vdmshowvginfo

            elif start_found:
                #print line
                temp.write(line)

