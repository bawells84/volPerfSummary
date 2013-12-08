from volStruct import *

# Metaclass impl for iterator over instances list


class IterInstancesVol(type):
    def __iter__(cls):
        return iter(cls._instances)


class VolumeGroup():
    __metaclass__ = IterInstancesVol
    _instances = []

    def __init__(self, buf):

        match = vg_details.search(buf)

        if match:
            self.label = match.group(11)
            self.raid = match.group(1)
            self.vol_cnt = match.group(7)
            self.drv_cnt = int(match.group(5)) + int(match.group(6))
            self.state = match.group(2)
            self.act_drv = match.group(5)
            self.inact_drv = match.group(6)
            self.pieces = dict()
            self.volumes = []

            self.add_pieces(buffer)

            VolumeGroup._instances.append(self)

    ## CLASS METHODS BELOW ##

    # Add a RAIDVolume to a VolumeGroup instance's volumes list

    def add_volume(self, vol):

        self.volumes.append(vol)

    # Add a piece to the VolumeGroup instance's pieces dict which is keyed by piece (pc);
    # value is a dict of drive information itself (drv).

    def add_piece(self, drv, pc):

        if type(drv) is dict:

            self.pieces[pc] = drv
            return True

        else:
            return False

    # Add all pieces of a volume group to a VolumeGroup using a buffer
    # that contains a single volume group's worth of output from vdmShowVGInfo.
    # Calls add_piece and passes a drive

    def add_pieces(self, buf):

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

                self.add_piece(drv, pc)

            else:
                continue

## Functions to parse required output (vdmShowVGInfo) and generate
## VolumeGroup objects from an array's state-capture-data.txt

# Takes a state-capture-data.txt and returns the vdmShowVGInfo command output.


def get_vginfo(statecapture):
    start_found = False
    statecapture.seek(0)
    buf = statecapture.readlines()
    statecapture.seek(0)

    temp = StringIO.StringIO()

    for line in buf:

        cmd_start = find_vdmShowVGInfo.search(line)
        cmd_end = executing.search(line)

        if not start_found:
            if cmd_start:
                start_found = True

        elif start_found:
            if cmd_end:
                vdmshowvginfo = temp.getvalue()
                return vdmshowvginfo

            elif start_found:
                temp.write(line)

# Find and create a VolumeGroup object for all volume groups found.
# Takes a state-capture-data.txt as an argument and passes it to get_vginfo()
# to return only the vdmShowVGInfo output to parse.


def create_volume_groups(statecapture):
    buf = get_vginfo(statecapture)
    temp = StringIO.StringIO()
    start = False

    for line in StringIO.StringIO(buf):

        start_seq = vg_entry_start.search(line)

        if start_seq:
            start = True
            temp.write(line)

        elif len(line) > 1:
            temp.write(line)

        elif len(line) == 1 and start is True:
            VolumeGroup(temp.getvalue())
            del temp
            temp = StringIO.StringIO()
            start = False

        elif len(line) == 1 and start is False:
            continue