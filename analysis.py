from vgStruct import *
from volStruct import *
from drivePerfStruct import *

## Volume Analysis


def analyze_vol_io_profile(vol, group):
    """
    Performs I/O profile analysis for RAID 5, 6, 1, and 10 and prints the results.
    @param vol: Pointer to RAIDVolume to perform analysis on
    @param group: Pointer to the VolumeGroup the RAIDVolume is a member of
    """
    cluster_size = int(vol.get_value_with_keys(INFO, 'segment_size'))
    stripe_width = int(vol.get_value_with_keys(INFO, 'stripe_size'))
    cb_size = int(vol.get_value_with_keys(CACHE, 'cache_block'))
    data_pieces = int(stripe_width) / int(cluster_size)
    raid_level = int(vol.get_value_with_keys(INFO, 'raid_level'))

    read_count = int(vol.get_combined_iostats_with_keys('reads', 'io'))
    write_count = int(vol.get_combined_iostats_with_keys('writes', 'io'))
    avg_sm_read_size = int(vol.get_combined_iostats_with_keys('avg_blocks', 'sm_reads'))
    avg_sm_write_size = int(vol.get_combined_iostats_with_keys('avg_blocks', 'sm_writes'))
    #avg_lg_read_size = int(vol.get_iostats_with_keys('avg_blocks', 'lg_reads'))
    #avg_lg_write_size = int(vol.get_iostats_with_keys('avg_blocks', 'lg_writes'))

    read_art_a = int(vol.get_iostats_with_keys_a('response', 'read_art'))
    read_art_b = int(vol.get_iostats_with_keys_b('response', 'read_art'))
    write_art_a = int(vol.get_iostats_with_keys_a('response', 'write_art'))
    write_art_b = int(vol.get_iostats_with_keys_b('response', 'write_art'))

    vol.print_vol_info()
    vol.print_vol_cache()
    vol.show_io_share()
    print " WRITE Analysis:\n"  # Perform WRITE Analysis

    if write_count > 0:

        print "     Request Count       : %d" % write_count
        print "     Avg. Request Size   : %d blocks" % avg_sm_write_size

        if raid_level in {5, 6}:

            print "     Write Algorithms    :"
            print "         [FULL] %d [FSWT] %d [PARTIAL] %d [RMW] %d [RMW2] %d [NO_PARITY] %d" % (
                int(vol.get_combined_iostats_with_keys('write_algorithm', 'full')),
                int(vol.get_combined_iostats_with_keys('write_algorithm', 'FSWT')),
                int(vol.get_combined_iostats_with_keys('write_algorithm', 'partial')),
                int(vol.get_combined_iostats_with_keys('write_algorithm', 'RMW')),
                int(vol.get_combined_iostats_with_keys('write_algorithm', 'RMW2')),
                int(vol.get_combined_iostats_with_keys('write_algorithm', 'no_parity')))

            print " "
            write_drives_per_req = evaluate_ratio(vol.get_combined_iostats_with_keys('writes', 'clusters'), write_count)
            write_stripes_per_req = evaluate_ratio(vol.get_combined_iostats_with_keys('writes', 'stripes'), write_count)

            analyze_stripe_ratio(write_stripes_per_req, stripe_width, avg_sm_write_size, cluster_size)
            analyze_cluster_ratio(write_drives_per_req, data_pieces)

            print ""
            print "     Response Times -\n"
            print "        Controller A: %.03f ms" % (convert_to_millisec(write_art_a))
            print "        Controller B: %.03f ms" % (convert_to_millisec(write_art_b))

        elif raid_level is 1:

            mirrorwidth = int(group.act_drv) / 2

            if mirrorwidth is 1:
                print " "
                print "     Stripe width is a single spindle (RAID 1).\n"

            else:
                print " "
                print "     NOTE: Stripe width is %d spindles (RAID 10).\n" % (int(mirrorwidth))

                # Commented out for now, since RAID10 isn't really a stripe the only real concern is how many
                # drives are used for each request.
                #write_stripes_per_req = evaluate_ratio(vol.get_iostats_with_keys('writes', 'stripes'), write_count)
                #analyze_stripe_ratio(write_stripes_per_req, stripe_width, avg_sm_write_size, cluster_size)

                write_drives_per_req = evaluate_ratio(vol.get_combined_iostats_with_keys('writes', 'clusters'), write_count)
                analyze_cluster_ratio(write_drives_per_req, data_pieces)

            print ""
            print "     Response Times -\n"
            print "        Controller A: %.03f ms" % (convert_to_millisec(write_art_a))
            print "        Controller B: %.03f ms" % (convert_to_millisec(write_art_b))

        else:
            print "     No requests to perform analysis on.\n"

    print " "

    print " READ Analysis:\n"       # Perform READ ANALYSIS

    if read_count > 0:

        print "     Request Count       : %d" % read_count
        print "     Avg. Request Size   : %d blocks" % avg_sm_read_size
        print " "

        if raid_level in {5, 6}:

            read_drives_per_req = evaluate_ratio(vol.get_combined_iostats_with_keys('reads', 'clusters'), read_count)
            read_stripes_per_req = evaluate_ratio(vol.get_combined_iostats_with_keys('reads', 'stripes'), read_count)

            analyze_stripe_ratio(read_stripes_per_req, stripe_width, avg_sm_read_size, cluster_size)
            analyze_cluster_ratio(read_drives_per_req, data_pieces)

            print ""
            print "     Response Times -\n"
            print "        Controller A: %.03f ms" % (convert_to_millisec(read_art_a))
            print "        Controller B: %.03f ms" % (convert_to_millisec(read_art_b))

        elif raid_level is 1:

            mirrorwidth = int(group.act_drv) / 2

            if mirrorwidth is 1:
                print " "
                print "     Stripe width is a single spindle (RAID 1).\n"

            else:
                print " "
                print "     NOTE: Stripe width is %d spindles (RAID 10).\n" % (int(mirrorwidth))

                # Commented out for now, since RAID10 isn't really a stripe the only real concern is how many
                # drives are used for each request.
                #read_stripes_per_req = evaluate_ratio(vol.get_iostats_with_keys('reads', 'stripes'), read_count)
                #analyze_stripe_ratio(read_stripes_per_req, stripe_width, avg_sm_read_size, cluster_size)

                read_drives_per_req = evaluate_ratio(vol.get_combined_iostats_with_keys('reads', 'clusters'), read_count)
                analyze_cluster_ratio(read_drives_per_req, data_pieces)

            print ""
            print "     Response Times -\n"
            print "        Controller A: %.03f ms" % (convert_to_millisec(read_art_a))
            print "        Controller B: %.03f ms" % (convert_to_millisec(read_art_b))

    else:
        print "     No requests to perform analysis on.\n"

    print "\n"


def analyze_stripe_ratio(ratio, width, avg_sz, seg_size):
    """
    Performs analysis on a Stripe usage ratio and prints results.
    @param ratio: (Tuple) Ratio of stripe usage
    @param width: Stripe width in blocks
    @param avg_sz: Avg I/O size
    @param seg_size: Segment size in blocks
    """
    is_multiple = avg_sz % width

    if avg_sz < width:

        if avg_sz > ((width - seg_size) + 1):
            print "     Average request size utilizes most of a full stripe."
        else:
            print "     Average request size is less than the stripe width."

    elif avg_sz > width and is_multiple is not 0:
        print "     Average request size is greater than the stripe width using %d.%d stripes per request." % (
            ratio[0], ratio[1])

    elif avg_sz == width or is_multiple is 0:
        print "     Average request size utilizes %d full stripes." % ratio[0]


def analyze_cluster_ratio(ratio, count):
    """
    Performs analysis on Cluster usage ratio and prints results
    @param ratio: (Tuple) Ratio of cluster usage
    @param count: Number of data pieces in the stripe
    @return: None
    """
    if ratio[0] < count:

        if ratio[1] < 1:
            print "     Average request size is serviced by only %d of %d spindles." % (ratio[0], count)

        else:
            rounded_cnt = ratio[0] + 1
            if rounded_cnt == count:
                return
            else:
                print "     Average request size is serviced by only %d of %d spindles." % (rounded_cnt, count)

    if ratio[0] > count:

        exceeds_by = ratio[0] - count

        if ratio[1] < 1:

            print "     Average request size exceeds the stripe width by %d spindles." % exceeds_by

        else:
            rounded_cnt = exceeds_by + 1
            if rounded_cnt == count:
                return
            else:
                print "     Average request size exceeds the stripe width by %d spindles." % rounded_cnt


## Drive Analysis


# noinspection PyProtectedMember
def analyze_drive_group(vol_group):
    if len(Drive._instances) > 0:

        drive_list = []                                 # List of Drive object pointers

        for i in vol_group.pieces:                      # Populate drive_list with Drive object pointers
            devnum = vol_group.pieces[i]['devnum']
            for d in Drive._instances:
                if d.devnum == devnum:
                    d.print_all()
                    drive_list.append(d)

        analyze_drive_group_response_times(drive_list)
        analyze_drive_group_busy_time(drive_list)

    else:
        return False


def analyze_drive_group_response_times(drive_list):
    ctrla_art_reads = []
    ctrla_art_writes = []

    ctrlb_art_reads = []
    ctrlb_art_writes = []

    for d in drive_list:
        a_read_art = d.ctrla[PERFORMANCE]['r_art']
        b_read_art = d.ctrlb[PERFORMANCE]['r_art']

        a_write_art = d.ctrla[PERFORMANCE]['w_art']
        b_write_art = d.ctrlb[PERFORMANCE]['w_art']

        ctrla_art_reads.append((d.devnum, a_read_art))
        ctrlb_art_reads.append((d.devnum, b_read_art))

        ctrla_art_writes.append((d.devnum, a_write_art))
        ctrlb_art_writes.append((d.devnum, b_write_art))

    ctrla_read_avg = find_average(ctrla_art_reads)
    ctrla_write_avg = find_average(ctrla_art_writes)

    ctrlb_read_avg = find_average(ctrlb_art_reads)
    ctrlb_write_avg = find_average(ctrlb_art_writes)

    ctrla_outliers_reads = find_outlier(ctrla_art_reads, ctrla_read_avg)
    ctrla_outliers_writes = find_outlier(ctrla_art_writes, ctrla_write_avg)

    ctrlb_outliers_reads = find_outlier(ctrlb_art_reads, ctrlb_read_avg)
    ctrlb_outliers_writes = find_outlier(ctrlb_art_writes, ctrlb_write_avg)

    print ""
    print " Average READ Response Time for this Volume Group  -\n"
    print "              Controller A: %.03f ms" % convert_to_millisec(ctrla_read_avg)
    print "              Controller B: %.03f ms" % convert_to_millisec(ctrlb_read_avg)
    print ""
    print "     Drives exceeding those averages (150% > Avg):\n"

    ctrla_drives_r = "              Controller A: "
    if len(ctrla_outliers_reads) > 0:
        for drive in ctrla_outliers_reads:
            ctrla_drives_r += drive[0] + " "
        print ctrla_drives_r
    else:
        ctrla_drives_r += "None"
        print ctrla_drives_r

    ctrlb_drives_r = "              Controller B: "
    if len(ctrlb_outliers_reads) > 0:

        for drive in ctrlb_outliers_reads:
            ctrlb_drives_r += drive[0] + " "
        print ctrlb_drives_r
    else:
        ctrlb_drives_r += "None"
        print ctrlb_drives_r

    print ""
    print " Average WRITE Response Time for this Volume Group -\n"
    print "              Controller A: %.03f ms" % convert_to_millisec(ctrla_write_avg)
    print "              Controller B: %.03f ms" % convert_to_millisec(ctrlb_write_avg)
    print ""
    print "     Drives exceeding those averages (150% > Avg):\n"

    ctrla_drives_w = "              Controller A: "
    if len(ctrla_outliers_writes) > 0:
        for drive in ctrla_outliers_writes:
            ctrla_drives_w += drive[0] + " "
        print ctrla_drives_w
    else:
        ctrla_drives_w += "None"
        print ctrla_drives_w

    ctrlb_drives_w = "              Controller B: "
    if len(ctrlb_outliers_writes) > 0:

        for drive in ctrlb_outliers_writes:
            ctrlb_drives_w += drive[0] + " "
        print ctrlb_drives_w
    else:
        ctrlb_drives_w += "None"
        print ctrlb_drives_w

    print ""


def analyze_drive_group_busy_time(drive_list):

    ctrla_busy_times = []
    ctrlb_busy_times = []

    print " Total drive activity -\n"
    print "       %s | %s | %s" % (string.center('Devnum', 10), string.rjust('A - Busy Time', 15), string.rjust('B - Busy Time', 15))
    print "       ----------------------------------------------"

    for d in drive_list:
        a_b_time = d.ctrla[PERFORMANCE]['bsy_time']
        b_b_time = d.ctrlb[PERFORMANCE]['bsy_time']

        ctrla_busy_times.append((d.devnum, a_b_time))
        ctrlb_busy_times.append((d.devnum, b_b_time))

        print "       %s | %s ms | %s ms" % (string.center(d.devnum, 10), string.rjust(a_b_time, 12), string.rjust(b_b_time, 12))

    a_avg = find_average(ctrla_busy_times)
    b_avg = find_average(ctrlb_busy_times)
    print "       ----------------------------------------------"
    print "       %s | %s ms | %s ms" % (string.rjust('Average ', 10), string.rjust(str(int(a_avg)), 12), string.rjust(str(int(b_avg)), 12))

    a_outliers = find_outlier(ctrla_busy_times, a_avg)
    b_outliers = find_outlier(ctrlb_busy_times, b_avg)



## Helper functions


def convert_to_millisec(num):
    time = float(num)
    factor = float(0.001)

    result = time * factor

    return result


def find_average(set_list):
    summed = float(0)
    count = 0

    for e in set_list:


        if float(e[1]) < float(1):      # Remove zero entries, don't want to throw off the averaging.
            pass
        else:
            summed += float(e[1])
            count += 1

    if count > 0:               # Make sure we didn't empty the list of drives because all ARTs were 0

        avg = summed / float(count)

        return avg

    else:
        return 0


def find_outlier(data, avg):

    outliers = []

    wavg = float(avg) * float(1.50)

    for e in data:

        if float(e[1]) > float(wavg):
            outliers.append(e)

    return outliers


def evaluate_ratio(numerator, denominator):
    """
    Calculates a ratio given the passed in numerator and denominator
    Used primarily for calculating Stripe and Cluster ratios on a per request basis
    @param numerator: Top number (i.e. number of clusters/stripes)
    @param denominator: Bottom number (i.e. number of requests)
    @return: Tuple with index 0 representing the whole number and index 1 the fraction
    """
    if int(denominator) == 0:
        result = (0, 0)
        return result
    else:
        whole = int(numerator) / int(denominator)
        decimal = (((int(numerator) * 100) / int(denominator)) % 100)

        result = (whole, decimal)

        return result
