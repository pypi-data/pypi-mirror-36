import logging
import textwrap
import traceback

import numpy as np

from mtwaffle import mt
from mtwaffle import mtsite


logger = logging.getLogger(__name__)



EDI_TEMPLATE = ''' >HEAD

   DATAID="<name>"
   X=<easting>
   Y=<northing>
   EASTING=<easting>
   NORTHING=<northing>
   ZONE=<zone>
   LAT=<lat>
   LONG=<lon>
   ELEV=<elev>

 >INFO   MAXLINES=1000

 >=DEFINEMEAS

   MAXCHAN=6
   MAXRUN=999
   MAXMEAS=99999
   UNITS=M
   REFTYPE=CART
   REFX=<easting>
   REFY=<northing>
   REFEASTING=<easting>
   REFNORTHING=<northing>
   REFZONE=<zone>
   REFLAT=<lat>
   REFLONG=<lon>
   REFELEV=<elev>

 >HMEAS ID= 1001.001 CHTYPE=HX X = 0.0 Y = 0.0 AZM = 0.0
 >HMEAS ID= 1002.001 CHTYPE=HY X = 0.0 Y = 0.0 AZM = 90.0
 >EMEAS ID= 1003.001 CHTYPE=EX X = 0.0 Y = 0.0  X2 = 47.0 Y2 = 0.0
 >EMEAS ID= 1004.001 CHTYPE=EY X = 0.0 Y = 0.0  X2 = 0.0  Y2 = 40.0
 >HMEAS ID= 1005.001 CHTYPE=HX X = 0.0 Y = 0.0 AZM = 0.0
 >HMEAS ID= 1006.001 CHTYPE=HY X = 0.0 Y = 0.0 AZM = 90.0

 >=MTSECT
   SECTID=114
   NFREQ=<nfreq>
   HX = 1001.001
   HY = 1002.001
   EX = 1003.001
   EY = 1004.001
   RX = 1005.001
   RY = 1006.001

 >!****FREQUENCIES****!
 >FREQ NFREQ=<nfreq>  ORDER=INC //          <nfreq>
<freqs>
 >!****IMPEDANCES****!
 >ZXXR //          <nfreq>
<zxxreal>
 >ZXXI //          <nfreq>
<zxximag>
 >ZXX.VAR //          <nfreq>
<zxxvar>
 >ZXYR //          <nfreq>
<zxyreal>
 >ZXYI //          <nfreq>
<zxyimag>
 >ZXY.VAR //          <nfreq>
<zxyvar>
 >ZYXR //          <nfreq>
<zyxreal>
 >ZYXI //          <nfreq>
<zyximag>
 >ZYX.VAR //          <nfreq>
<zyxvar>
 >ZYYR //          <nfreq>
<zyyreal>
 >ZYYI //          <nfreq>
<zyyimag>
 >ZYY.VAR //          <nfreq>
<zyyvar>

 >END'''


def read_edi(fn, name=None, **kwargs):
    '''Read EDI *fn* into an mtwaffle.mt.Site object.

    Keyword arguments are passed to mtwaffle.edi.read_mt_data

    '''
    edi_contents = read_edi_dict(fn)
    if name is None:
        try:
            name = str(edi_contents['HEAD']['DATAID'])
        except:
            name = fn
    freqs, zs, zes = read_mt_data(edi_contents, **kwargs)
    return mtsite.Site(freqs, zs, name=name, datasource={
        'EDI': edi_contents
    })


def read_mt_data(edi, sort_freq="asc", errors="VAR", error_floor=0.05,
             f0=None, f1=None):
    """Read an EDI file.

    Args:
        - *fn*: filename
        - *sort_freq*: "asc", "desc", or None
        - *errors*: a string or None. Chooses the value used in the EDI to
          represent errors (unthinking, so you need to be aware yourself
          of whether the *errors* are variances or standard deviations or ...?)
          If None, no attempt to read errors in will be made.
        - *error_floor*: real or complex float or 2 x 2 ndarray. The real and
          imaginary parts are the minimum fractional error on each component
          of the impedance tensor, after *errors* have been read in.
          *error_floor* = None means the minimum error is zero. A 2 x 2 ndarray
          here will apply different errors to each component of Z; a float will
          apply the same error floor to all four components. A real value will
          apply to same error floor to the real and imaginary components.
        - *f0, f1*: min and max freqs (see :func:`between_freqs`)

    Returns: (*freqs*, *Zs*, *Zerrors*)
        - *freqs*: m x 1 ndarray
        - *Zs*: m x 2 x 2 complex ndarray
        - *Zerrors*: m x 2 x 2 ndarray. If *error_floor* was complex, *Zerrors*
          will be complex. If it were real or None, *Zerrors* will be real.

    This function doesn't to work for multi-site EDIs, nor possibly some
    single-site ones given the variation in formats.

    """
    freqs = np.asarray(edi["FREQ"])
    Zs = np.empty((len(freqs), 2, 2), dtype=np.complex)
    if errors:
        Zes = np.empty((len(freqs), 2, 2), dtype=np.complex)
    for i in range(len(edi["FREQ"])):
        Zs[i, 0, 0] = edi["ZXXR"][i] + 1j * edi["ZXXI"][i]
        Zs[i, 0, 1] = edi["ZXYR"][i] + 1j * edi["ZXYI"][i]
        Zs[i, 1, 0] = edi["ZYXR"][i] + 1j * edi["ZYXI"][i]
        Zs[i, 1, 1] = edi["ZYYR"][i] + 1j * edi["ZYYI"][i]
        if errors:
            Zes[i, 0, 0] = edi["ZXX." + errors][i]
            Zes[i, 0, 1] = edi["ZXY." + errors][i]
            Zes[i, 1, 0] = edi["ZYX." + errors][i]
            Zes[i, 1, 1] = edi["ZYY." + errors][i]
    if errors:
        Zerrors = set_error_floor_Z(Zs, Zerrors=Zes, error_floor=error_floor)
    elif error_floor:
        Zerrors = set_error_floor_Z(Zs, error_floor=error_floor)
    else:
        Zerrors = np.zeros_like(Zs, dtype=np.float)
    sort_indices = np.argsort(freqs)
    if sort_freq.lower().startswith("d"): # descending
        sort_indices = sort_indices[::-1]
    freqs = freqs[sort_indices]
    Zs = Zs[sort_indices]
    Zerrors = Zerrors[sort_indices]
    indices = mt.between_freqs(freqs, f0=f0, f1=f1)
    return freqs[indices], Zs[indices], Zerrors[indices]


def read_edi_dict(fn, **kwargs):
    """Return a dictionary of blocks and values from EDI file."""
    edi = {}
    option_bnames = ['HEAD', 'DEFINEMEAS', 'INFO', 'MTSECT']
    fileobj = open(fn, mode='r')
    lines = fileobj.readlines()
    fileobj.close()
    lines_copy = lines
    for i, line in enumerate(lines):
        try:
            items = line.strip('\n').split()
        except:
            continue
        if not items:
            continue
        if items[0][0] is '>':
            bname = items[0].replace('>', '').replace('=', '')
            if bname in option_bnames:
                # This is an option block.
                logger.debug('{0}: option block {1}'.format(i, bname))
                options = {}
                for j, line2 in enumerate(lines_copy[i + 1:]):
                    line2 = line2.strip('\n').strip('\r')
                    if not line2:
                        continue
                    if line2.strip()[0] is '>':
                        break
                    logger.debug(' {0}: {1}'.format(j + 1, line2))
                    items = line2.split('=')
                    if len(items) == 2:
                        option, value = items
                        value = value.strip().strip('"')
                        option = option.strip()
                        try:
                            value = int(value)
                        except:
                            try:
                                value = float(value)
                            except:
                                pass
                    else:
                        option = items[0].strip(':')
                        value = ''
                    options[option] = value
                    edi[bname] = options
            else:
                # This is a data block.
                logger.debug('{0}: data block {1}'.format(i, bname))
                data = []
                for j, line2 in enumerate(lines_copy[i + 1:]):
                    line2 = line2.strip('\n').strip('\r')
                    if not line2:
                        continue
                    if line2.strip()[0] is '>':
                        break
                    items2 = line2.split()
                    logger.debug(' {0}: {1}'.format(j + i, line2))
                    data += items2
                edi[bname] = data
    nulls = []
    for bname in edi.keys():
        block_value = edi[bname]
        if isinstance(block_value, list) and block_value:
            for i, value in enumerate(block_value):
                if value in ['NaN', '+Inf']:
                    nulls.append(i)

    nulls = list(set(nulls))

    temp = 'Bad values:'
    for null in nulls:
        temp += '%.4f Hz ' % float(edi['FREQ'][null])

    if nulls:
        temp = 'Removing bad values '
        logger.debug(temp)
        for bname in edi.keys():
            block_value = edi[bname]
            if isinstance(block_value, list) and block_value:
                temp += '%s' % bname
                for null_index in nulls:
                    del block_value[null_index]

    logger.debug('Removing blocks with no data...')
    for key in list(edi.keys()):
        if not edi[key]:
            del edi[key]

    for key in edi.keys():
        value = edi[key]
        if isinstance(value, list) and value:
            logger.debug('Converting {0} to floats...'.format(key))
            edi[key] = [float(v) for v in value]

    length = 0
    for key in edi.keys():
        if key in option_bnames:
            logger.debug('{0} option block'.format(key))
            block = edi[key]
            for option in block.keys():
                value = block[option]
                logger.debug(' {0}={1}'.format(option, value))
        else:
            if not length:
                length = len(edi[key])
                # print('NOT length so setting length=%d from key=%s' % (
                #       length, key))
            # if len(edi[key]) != length:
                # print('key=%s expected length=%d actual length=%d' % (
                #       key, length, len(edi[key])))

    logger.debug('Adding standard deviations...')
    variances = ['ZXX.VAR', 'ZXY.VAR', 'ZYX.VAR', 'ZYY.VAR']
    for var in variances:
        if var in edi.keys():
            edi[var.replace('.VAR', '.SDEV')] = np.asarray([np.sqrt(val) for val in edi[var]])

    # # Place properties from HEAD and DEFINEMEAS into the main edi dictionary.
    # propblocks = ['DEFINEMEAS', "HEAD"]
    # for name in propblocks:
    #     block = edi[name]
    #     for prop, value in block.items():
    #         edi[prop] = value

    if 'DATAID' in edi['HEAD']:
        edi['HEAD']['DATAID'] = str(edi['HEAD']['DATAID'])
    # try:
    #     if "LAT" in edi and "LONG" in edi:
    #         edi["LAT"] = convert_geocoord(edi["LAT"])
    #         edi["LONG"] = convert_geocoord(edi["LONG"])
    # except NameError:
    #     pass
    #     # logger.warning('Cannot convert lat/lons: {}'.format(traceback.format_exc()[-1].strip('\n')))

    return edi


def write_edi(data, fn, **kws):
    kws.update(data)
    if not "zes" in data:
        data.zes = set_error_floor_Z(data.zs)
    for key in ["freqs", "zs", "zes"]:
        if key in kws:
            del kws[key]
    return write_edi_file(fn, data.freqs, data.zs, data.zes, **kws)


def write_edi_file(
            fn, freqs, zs, zes,
            name='unnamed', x='nan', y='nan',
            lat='nan', lon='nan', easting='nan', northing='nan',
            zone='nan', elev='nan', **kwargs):
    '''Write an EDI file.

    Kwargs:
        - *name, lat, lon, easting, northing, x, y, elev*

    '''
    format_list = lambda numbers: textwrap.fill('  '.join(map(str, numbers)))
    replacements = {
        '<freqs>': format_list(freqs),
        '<zxxreal>': format_list(zs[:, 0, 0].real),
        '<zxximag>': format_list(zs[:, 0, 0].imag),
        '<zxxvar>': format_list(zes[:, 0, 0]),
        '<zxyreal>': format_list(zs[:, 0, 1].real),
        '<zxyimag>': format_list(zs[:, 0, 1].imag),
        '<zxyvar>': format_list(zes[:, 0, 1]),
        '<zyxreal>': format_list(zs[:, 1, 0].real),
        '<zyximag>': format_list(zs[:, 1, 0].imag),
        '<zyxvar>': format_list(zes[:, 1, 0]),
        '<zyyreal>': format_list(zs[:, 1, 1].real),
        '<zyyimag>': format_list(zs[:, 1, 1].imag),
        '<zyyvar>': format_list(zes[:, 1, 1]),
        '<name>': name,
        '<lat>': str(lat),
        '<lon>': str(lon),
        '<easting>': str(easting),
        "<northing>": str(northing),
        "<zone>": str(zone),
        '<elev>': str(elev),
        '<nfreq>': str(len(freqs))
        }
    edi_txt = str(EDI_TEMPLATE)
    for placeholder, values in replacements.items():
        edi_txt = edi_txt.replace(placeholder, values)
    with open(fn, mode='w') as f:
        f.write(edi_txt)


def set_error_floor(data, errors=None, floor=0.05, floor_type="fractional"):
    """Calculate error floors or apply a standard error.

    Args:
        - *data*: n x subshape ndarray of real
        - *errors*: optional n x subshape ndarray of existing errors
        - *floor*: float, error floor
        - *floor_type*: "fractional" or "absolute"

    Returns:
        - *errors*: n x subshape ndarray of errors

    """
    data = np.asarray(data)
    shape = data.shape
    if not errors is None:
        errors = np.asarray(errors)
    else:
        errors = np.zeros(data.shape)
    errors = errors.ravel()
    data = data.ravel()
    if floor_type.lower().startswith("f"): # fractional error floor
        min_errors = data * floor
    else:
        min_errors = np.ones(len(data)) * floor
    return np.where(min_errors < errors, errors, min_errors).reshape(shape)


def set_error_floor_Z(Zs, Zerrors=None, error_floor=0.05):
    """Calculate error floors or apply a standard error.

    Args:
        - *Zs*: m x 2 x 2 complex ndarray of impedance tensors
        - *Zerrors*: optional m x 2 x 2 real or complex ndarray of errors
        - *error_floor*: real or complex float or 2 x 2 ndarray. The real and
          imaginary parts are the minimum fractional error on each component
          of the impedance tensor, after *errors* have been read in.
          *error_floor* = None means the minimum error is zero. A 2 x 2 ndarray
          here will apply different errors to each component of Z; a float will
          apply the same error floor to all four components. A real value will
          apply to same error floor to the real and imaginary components.

    Returns: *Zerrors*
        - *Zerrors*: m x 2 x 2 ndarray. If *error_floor* was complex, *Zerrors*
          will be complex. If it were real or None, *Zerrors* will be real.
    """
    Zs = np.asarray(Zs)
    m = Zs.shape[0]
    if Zerrors is None:
        Zerrors = np.zeros((m, 2, 2), dtype=np.complex)
    return_real = False
    if not np.iscomplex(error_floor):
        return_real = True
        error_floor = error_floor + 1j * error_floor
    if np.asarray(error_floor).ndim == 0:
        error_floor = np.array([[error_floor, error_floor],
                                [error_floor, error_floor]])
    assert error_floor.shape == (2, 2)
    Zes = np.empty((m, 2, 2), dtype=np.complex)
    for k in range(m):
        for i in (0, 1):
            for j in (0, 1):
                floor_real = np.abs(Zs[k, i, j] * error_floor[i, j].real)
                if floor_real > Zerrors[k, i, j].real:
                    Zes[k, i, j] = floor_real + 0j
                else:
                    Zes[k, i, j] = Zerrors[k, i, j].real + 0j

                floor_imag = np.abs(Zs[k, i, j] * error_floor[i, j].imag)
                if floor_imag > Zerrors[k, i, j].imag:
                    Zes[k, i, j] += floor_imag * 1j
                else:
                    Zes[k, i, j] += Zerrors[k, i, j].imag * 1j
    if return_real:
        return Zes.real
    else:
        return Zes
