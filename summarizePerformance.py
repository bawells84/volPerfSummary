from optparse import OptionParser
import sys
from analysis import *


def main():

    usage = "usage: %prog [-f] [-v]"

    parser = OptionParser(usage)
    parser.add_option("-f", "--file", action="store", type="string", dest="filename",
                      help="state-capture-data file from the ASUP", metavar="STATE-CAPTURE-DATA")
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose",
                      help="Print more execution detail, default is off")

    (options, args) = parser.parse_args()
    if options.filename:
        file_descriptor = options.filename
    else:
        print "\nERROR: Requires input state-capture-data filename\n"
        parser.print_help()
        sys.exit(0)

    initialize_data(file_descriptor)
    run_analysis()


def initialize_data(file_descriptor):

    statecapture = open(file_descriptor)

    build_drives(statecapture)
    print "Drives Found: %d" % (len(Drive._instances))

    VolumeGroup.build_volume_groups(statecapture)
    print "Volume Groups Found: %d" % (len(VolumeGroup._instances))

    RAIDVolume.build_raid_volumes(statecapture)
    print "Volumes Found: %d\n" % (len(RAIDVolume._instances))

    VolumeGroup.find_and_add_all_volumes()

    RAIDVolume.get_vdall(statecapture)

def run_analysis():

    for g in VolumeGroup._instances:

        print " #### VOLUME GROUP: %s ####\n" % g.label
        g.print_info()

        print " ### DRIVE PERFORMANCE ###\n"
        analyze_drive_group(g)

        if len(g.volumes) > 0:
            print "\n"
            print " ### VOLUME PERFORMANCE ###\n"
            for v in g.volumes:
                analyze_vol_io_profile(v, g)
        else:
            print ""
            print "No RAIDVolumes to perform analysis on!\n"

if __name__ == "__main__":
    main()