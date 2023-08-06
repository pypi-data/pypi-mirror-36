from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, dict, object, range, map, input, str
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open

import pickle
import os.path
import numpy as np
from rfpipe import state, preferences, util, source, metadata, candidates
import rfpipe.search  # explicit to avoid circular import
import logging
logger = logging.getLogger(__name__)


def oldcands_read(candsfile, sdmscan=None):
    """ Read old-style candfile and create new-style candcollection
    Returns a list of tuples (state, dataframe) per scan.
    """

    with open(candsfile, 'rb') as pkl:
        try:
            d = pickle.load(pkl)
            ret = pickle.load(pkl)
        except UnicodeDecodeError:
            d = pickle.load(pkl, encoding='latin-1')
            ret = pickle.load(pkl, encoding='latin-1')
        if isinstance(ret, tuple):
            loc, prop = ret
        elif isinstance(ret, dict):
            loc = np.array(list(ret.keys()))
            prop = np.array(list(ret.values()))
        else:
            logger.warn("Not sure what we've got in this here cands pkl file...")

    if sdmscan is None:  # and (u'scan' in d['featureind']):
#        scanind = d['featureind'].index('scan')
        scanind = 0
        scans = np.unique(loc[:, scanind])
    elif sdmscan is not None:
        scans = [sdmscan]

    ll = []
    for scan in scans:
        try:
            st, cc = oldcands_readone(candsfile, scan)
            ll.append((st, cc))
        except AttributeError:
            pass

    return ll


def oldcands_readone(candsfile, scan=None):
    """ Reads old-style candidate files to create new state and candidate
    collection for a given scan.
    Parsing merged cands file requires sdm locally with bdf for given scan.
    If no scan provided, assumes candsfile is from single scan not merged.
    """

    with open(candsfile, 'rb') as pkl:
        try:
            d = pickle.load(pkl)
            ret = pickle.load(pkl)
        except UnicodeDecodeError:
            d = pickle.load(pkl, encoding='latin-1')
            ret = pickle.load(pkl, encoding='latin-1')
        if isinstance(ret, tuple):
            loc, prop = ret
        elif isinstance(ret, dict):
            loc = np.array(list(ret.keys()))
            prop = np.array(list(ret.values()))
        else:
            logger.warn("Not sure what we've got in this here cands pkl file...")

    # detect merged vs nonmerged
    if 'scan' in d['featureind']:
        locind0 = 1
    else:
        locind0 = 0

    # merged candsfiles must be called with scan arg
    if scan is None:
        assert locind0 == 0, "Set scan if candsfile has multiple scans."

    inprefs = preferences.oldstate_preferences(d, scan=scan)
    inprefs.pop('gainfile')
    inprefs.pop('workdir')
    inprefs.pop('fileroot')
    inprefs['segmenttimes'] = inprefs['segmenttimes']
    sdmfile = os.path.basename(d['filename'])

    try:
        assert scan is not None
        st = state.State(sdmfile=sdmfile, sdmscan=scan, inprefs=inprefs)
    except:
        meta = metadata.oldstate_metadata(d, scan=scan)
        st = state.State(inmeta=meta, inprefs=inprefs, showsummary=False)

    if 'rtpipe_version' in d:
        st.rtpipe_version = float(d['rtpipe_version'])  # TODO test this
        if st.rtpipe_version <= 1.54:
            logger.info('Candidates detected with rtpipe version {0}. All '
                        'versions <=1.54 used incorrect DM scaling.'
                        .format(st.rtpipe_version))

    if scan is None:
        assert locind0 == 0, "Set scan if candsfile has multiple scans."
        scan = d['scan']

    logger.info('Calculating candidate properties for scan {0}'.format(scan))

    if locind0 == 1:
        loc = loc[np.where(loc[:, 0] == scan)][:, locind0:]

    print(st.features, st.prefs.searchtype)
    fields = [str(ff) for ff in st.search_dimensions + st.features]
    types = [str(tt) for tt in len(st.search_dimensions)*['<i4'] + len(st.features)*['<f4']]
    dtype = np.dtype({'names': fields, 'formats': types})
    features = np.zeros(len(loc), dtype=dtype)
    for i in range(len(loc)):
        features[i] = tuple(list(loc[i]) + list(prop[i]))
    cc = candidates.CandCollection(features, st.prefs, st.metadata)

    return st, cc


def oldcands_convert(candsfile, scan=None):
    """ Take old style candsfile for a single scan and writes new style file.
    """

    st, cc = oldcands_readone(candsfile, scan=scan)
    with open(st.candsfile, 'wb') as pkl:
        pickle.dump(cc, pkl)


def pipeline_dataprep(st, candloc):
    """ Prepare (read, cal, flag) data for a given state and candloc.
    """

    segment, candint, dmind, dtind, beamnum = candloc

    # propagate through to new candcollection
    st.prefs.segmenttimes = st._segmenttimes.tolist()

    # prep data
    data = source.read_segment(st, segment)
    flagversion = "rtpipe" if hasattr(st, "rtpipe_version") else "latest"
    data_prep = source.data_prep(st, segment, data, flagversion=flagversion)

    return data_prep


def pipeline_datacorrect(st, candloc, data_prep=None):
    """ Prepare and correct for dm and dt sampling of a given candloc
    Can optionally pass in prepared (flagged, calibrated) data, if available.
    """

    if data_prep is None:
        data_prep = pipeline_dataprep(st, candloc)

    segment, candint, dmind, dtind, beamnum = candloc
    dt = st.dtarr[dtind]
    dm = st.dmarr[dmind]

    scale = None
    if hasattr(st, "rtpipe_version"):
        scale = 4.2e-3 if st.rtpipe_version <= 1.54 else None
    delay = util.calc_delay(st.freq, st.freq.max(), dm, st.inttime,
                            scale=scale)

    data_dmdt = rfpipe.search.dedisperseresample(data_prep, delay, dt,
                                                 parallel=st.prefs.nthread > 1,
                                                 resamplefirst=st.fftmode=='cuda')

    return data_dmdt


def pipeline_imdata(st, candloc, data_dmdt=None, cpuonly=False, **kwargs):
    """ Generate image and phased visibility data for candloc.
    Phases to peak pixel in image of candidate.
    Can optionally pass in corrected data, if available.
    """

    segment, candint, dmind, dtind, beamnum = candloc
    dt = st.dtarr[dtind]
    dm = st.dmarr[dmind]

    uvw = util.get_uvw_segment(st, segment)
    wisdom = rfpipe.search.set_wisdom(st.npixx, st.npixy)

    if data_dmdt is None:
        data_dmdt = pipeline_datacorrect(st, candloc)

    fftmode = 'fftw' if cpuonly else st.fftmode
    image = rfpipe.search.grid_image(data_dmdt, uvw, st.npixx, st.npixy, st.uvres,
                                     fftmode, st.prefs.nthread, wisdom=wisdom,
                                     integrations=[candint])[0]

    # TODO: allow dl,dm as args and reproduce detection for other SNRs
    dl, dm = st.pixtolm(np.where(image == image.max()))
    util.phase_shift(data_dmdt, uvw, dl, dm)
    dataph = data_dmdt[max(0, candint-st.prefs.timewindow//2):candint+st.prefs.timewindow//2].mean(axis=1)
    util.phase_shift(data_dmdt, uvw, -dl, -dm)

    canddata = candidates.CandData(state=st, loc=tuple(candloc), image=image,
                                   data=dataph, **kwargs)

    # output is as from searching functions
    return canddata


def pipeline_candidate(st, candloc, candcollection=None):
    """ End-to-end pipeline to reproduce candidate plot and calculate features.
    Can optionally pass in image and corrected data, if available.
    """

    segment, candint, dmind, dtind, beamnum = candloc

    if candcollection is None:
        canddata = pipeline_imdata(st, candloc)

    candcollection = candidates.save_and_plot(canddata)

    return candcollection
