#
# Copyright 2008-2018 Universidad Complutense de Madrid
#
# This file is part of PyEmir
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

from __future__ import division


import sys
import math
import logging
import itertools

import numpy as np
import matplotlib.pyplot as plt
import sep
import skimage.filters as filt

import skimage.feature as feat
from scipy import ndimage as ndi
from numina.array.utils import coor_to_pix_1d
from numina.array.bbox import BoundingBox
from numina.array.offrot import fit_offset_and_rotation
from numina.array.peaks.peakdet import refine_peaks
from numina.core import Requirement, Result
from numina.types.qc import QC
import numina.types.array as tarray
from numina.core.requirements import ObservationResultRequirement
import numina.core.query as qmod

from emirdrp.core import EMIR_NBARS, EMIR_PLATESCALE_PIX, EMIR_PLATESCALE
from emirdrp.core import EMIR_PIXSCALE
from emirdrp.core.recipe import EmirRecipe
from emirdrp.processing.combine import basic_processing_, combine_images
from emirdrp.processing.combine import process_ab, process_abba
import emirdrp.requirements as reqs
import emirdrp.products as prods
import emirdrp.instrument.distortions as dist
from emirdrp.instrument.csuconf import TargetType
import emirdrp.instrument.csuconf as csuconf


def comp_centroid(data, bounding_box, debug_plot=False, plot_reference=None, logger=None):
    from matplotlib.patches import Ellipse

    if logger is None:
        logger = logging.getLogger(__name__)

    region = bounding_box.slice
    ref_x = region[1].start
    ref_y = region[0].start
    logger.debug('region ofset is %s, %s', ref_x, ref_y)
    subimage = data[region].copy()
    bkg = sep.Background(subimage)
    data_sub = subimage - bkg
    objects = sep.extract(data_sub, 1.5, err=bkg.globalrms)
    # Select brightest object
    logger.debug('%d object found', len(objects))

    if len(objects) == 0:
        # print('No objects')
        return None

    iadx = objects['flux'].argmax()
    # plot background-subtracted image
    maxflux = objects[iadx]

    if debug_plot:
        fig, ax = plt.subplots()
        m, s = np.mean(data_sub), np.std(data_sub)
        im = ax.imshow(data_sub, interpolation='nearest', cmap='gray',
                       vmin=m - s, vmax=m + s, origin='lower',
                       extent=bounding_box.extent)
        if plot_reference:
            e = Ellipse(xy=(plot_reference[0], plot_reference[1]),
                        width=6,
                        height=6,
                        angle=0)
            e.set_facecolor('none')
            e.set_edgecolor('green')
            ax.add_artist(e)

        # plot an ellipse for each object
        for idx, obj in enumerate(objects):
            e = Ellipse(xy=(obj['x'] + ref_x, obj['y'] + ref_y),
                        width=6 * obj['a'],
                        height=6 * obj['b'],
                        angle=obj['theta'] * 180. / np.pi)
            e.set_facecolor('none')
            if idx == iadx:
                e.set_edgecolor('blue')
            else:
                e.set_edgecolor('red')
            ax.add_artist(e)
        return maxflux['x'], maxflux['y'], ax
    else:
        return maxflux['x'], maxflux['y']


class MaskCheckRecipe(EmirRecipe):

    """
    Acquire a target.

    Recipe for the processing of multi-slit/long-slit check images.

    **Observing modes:**

        * MSM and LSM check

    """

    # Recipe Requirements
    #
    obresult = ObservationResultRequirement(
        query_opts=qmod.ResultOf(
            'STARE_IMAGE.frame',
            node='children',
            id_field="resultsIds"
        )
    )
    master_bpm = reqs.MasterBadPixelMaskRequirement()

    bars_nominal_positions = Requirement(
        prods.NominalPositions,
        'Nominal positions of the bars'
    )

    # Recipe Products
    slit_image = Result(prods.ProcessedImage)
    object_image = Result(prods.ProcessedImage)
    offset = Result(tarray.ArrayType)
    angle = Result(float)

    def run(self, rinput):
        self.logger.info('starting processing for image acquisition')
        # Combine and masking
        flow = self.init_filters(rinput)

        # count frames
        frames = rinput.obresult.frames

        nframes = len(frames)
        if nframes not in [1, 2, 4]:
            raise ValueError("expected 1, 2 or 4 frames, got {}".format(nframes))

        interm = basic_processing_(frames, flow, self.datamodel)

        if nframes == 1:
            hdulist_slit = combine_images(interm[:], self.datamodel)
            hdulist_object = hdulist_slit
            # background_subs = False
        elif nframes == 2:
            hdulist_slit = combine_images(interm[0:], self.datamodel)
            hdulist_object = process_ab(interm, self.datamodel)
            # background_subs = True
        elif nframes == 4:
            hdulist_slit = combine_images(interm[0::3], self.datamodel)
            hdulist_object = process_abba(interm, self.datamodel)
            # background_subs = True
        else:
            raise ValueError("expected 1, 2 or 4 frames, got {}".format(nframes))

        self.set_base_headers(hdulist_slit[0].header)
        self.set_base_headers(hdulist_object[0].header)

        self.save_intermediate_img(hdulist_slit, 'slit_image.fits')

        self.save_intermediate_img(hdulist_object, 'object_image.fits')

        # Get slits
        # Rotation around (0,0)
        # For other axis, offset is changed
        # (Off - raxis) = Rot * (Offnew - raxis)
        crpix1 = hdulist_slit[0].header['CRPIX1']
        crpix2 = hdulist_slit[0].header['CRPIX2']

        rotaxis = np.array((crpix1 - 1, crpix2 - 1))

        self.logger.debug('center of rotation (from CRPIX) is %s', rotaxis)

        csu_conf = self.load_csu_conf(hdulist_slit, rinput.bars_nominal_positions)

        # IF CSU is completely open OR there are no refereces,
        # this is not needed
        if not csu_conf.is_open():
            self.logger.info('CSU is configured, detecting slits')
            slits_bb = self.compute_slits(hdulist_slit, csu_conf)

            image_sep = hdulist_object[0].data.astype('float32')

            self.logger.debug('center of rotation (from CRPIX) is %s', rotaxis)

            offset, angle, qc = compute_off_rotation(
                image_sep, csu_conf, slits_bb,
                rotaxis=rotaxis, logger=self.logger,
                debug_plot=True, intermediate_results=True
            )
        else:
            self.logger.info('CSU is open, not detecting slits')
            offset = [0.0, 0.0]
            angle = 0.0
            qc = QC.GOOD

        # Convert mm to m
        offset_out = np.array(offset) / 1000.0
        # Convert DEG to RAD
        angle_out = np.deg2rad(angle)
        result = self.create_result(
            slit_image=hdulist_slit,
            object_image=hdulist_object,
            offset=offset_out,
            angle=angle_out,
            qc=qc
        )
        self.logger.info('end processing for image acquisition')
        return result

    def load_csu_conf(self, hdulist, bars_nominal_positions):
        # Get slits
        hdr = hdulist[0].header
        # Extract DTU and CSU information from headers

        dtuconf = self.datamodel.get_dtur_from_header(hdr)

        # coordinates transformation from DTU coordinates
        # to image coordinates
        # Y inverted
        # XY switched
        # trans1 = [[1, 0, 0], [0,-1, 0], [0,0,1]]
        # trans2 = [[0,1,0], [1,0,0], [0,0,1]]
        trans3 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]  # T3 = T2 * T1

        vec = np.dot(trans3, dtuconf.coor_r) / EMIR_PIXSCALE
        self.logger.debug('DTU shift is %s', vec)

        self.logger.debug('create bar model')
        barmodel = csuconf.create_bar_models(bars_nominal_positions)
        csu_conf = csuconf.read_csu_2(hdr, barmodel)

        if self.intermediate_results:
            # FIXME: coordinates are in VIRT pixels
            self.logger.debug('create bar mask from predictions')
            mask = np.ones_like(hdulist[0].data)
            for i in itertools.chain(csu_conf.lbars, csu_conf.rbars):
                bar = csu_conf.bars[i]
                mask[bar.bbox().slice] = 0
            self.save_intermediate_array(mask, 'mask_bars.fits')

            self.logger.debug('create slit mask from predictions')
            mask = np.zeros_like(hdulist[0].data)
            for slit in csu_conf.slits.values():
                mask[slit.bbox().slice] = slit.idx
            self.save_intermediate_array(mask, 'mask_slit.fits')

            self.logger.debug('create slit reference mask from predictions')
            mask1 = np.zeros_like(hdulist[0].data)
            for slit in csu_conf.slits.values():
                if slit.target_type == TargetType.REFERENCE:
                    mask1[slit.bbox().slice] = slit.idx
            self.save_intermediate_array(mask1, 'mask_slit_ref.fits')

        return csu_conf

    def compute_slits(self, hdulist, csu_conf):

        self.logger.debug('finding borders of slits')
        self.logger.debug('not strictly necessary...')
        data = hdulist[0].data
        self.logger.debug('dtype of data %s', data.dtype)

        self.logger.debug('median filter (3x3)')
        image_base = ndi.filters.median_filter(data, size=3)

        # Cast as original type for skimage
        self.logger.debug('casting image to unit16 (for skimage)')
        iuint16 = np.iinfo(np.uint16)
        image = np.clip(image_base, iuint16.min, iuint16.max).astype(np.uint16)

        self.logger.debug('compute Sobel filter')
        # FIXME: compute sob and sob_v is redundant
        sob = filt.sobel(image)
        self.save_intermediate_array(sob, 'sobel_image.fits')
        sob_v = filt.sobel_v(image)
        self.save_intermediate_array(sob_v, 'sobel_v_image.fits')

        # Compute detector coordinates of bars
        all_coords_virt = np.empty((110, 2))
        all_coords_real = np.empty((110, 2))

        # Origin of coordinates is 1
        for bar in csu_conf.bars.values():
            all_coords_virt[bar.idx - 1] = bar.xpos, bar.y0

        # Origin of coordinates is 1 for this function
        _x, _y = dist.exvp(all_coords_virt[:, 0], all_coords_virt[:, 1])
        all_coords_real[:, 0] = _x
        all_coords_real[:, 1] = _y

        # FIXME: hardcoded value
        h = 16
        slit_h_virt = 16.242
        slit_h_tol = 3
        slits_bb = {}

        mask1 = np.zeros_like(hdulist[0].data)

        for idx in range(EMIR_NBARS):
            lbarid = idx + 1
            rbarid = lbarid + EMIR_NBARS
            ref_x_l_v, ref_y_l_v = all_coords_virt[lbarid - 1]
            ref_x_r_v, ref_y_r_v = all_coords_virt[rbarid - 1]

            ref_x_l_d, ref_y_l_d = all_coords_real[lbarid - 1]
            ref_x_r_d, ref_y_r_d = all_coords_real[rbarid - 1]

            width_v = ref_x_r_v - ref_x_l_v
            # width_d = ref_x_r_d - ref_x_l_d

            if (ref_y_l_d >= 2047 + h) or (ref_y_l_d <= 1 - h):
                # print('reference y position is outlimits, skipping')
                continue

            if width_v < 5:
                # print('width is less than 5 pixels, skipping')
                continue

            plot = False
            regionw = 12
            px1 = coor_to_pix_1d(ref_x_l_d) - 1
            px2 = coor_to_pix_1d(ref_x_r_d) - 1
            prow = coor_to_pix_1d(ref_y_l_d) - 1

            comp_l, comp_r = calc0(image, sob_v, prow, px1, px2, regionw, h=h,
                                   plot=plot, lbarid=lbarid, rbarid=rbarid,
                                   plot2=False)
            if np.any(np.isnan([comp_l, comp_r])):
                self.logger.warning("converting NaN value, border of=%d", idx + 1)
                self.logger.warning("skipping bar=%d", idx + 1)
                continue

            region2 = 5
            px21 = coor_to_pix_1d(comp_l)
            px22 = coor_to_pix_1d(comp_r)

            comp2_l, comp2_r = calc0(image, sob_v, prow, px21, px22, region2,
                                     refine=True,
                                     plot=plot, lbarid=lbarid, rbarid=rbarid,
                                     plot2=False)

            if np.any(np.isnan([comp2_l, comp2_r])):
                self.logger.warning("converting NaN value, border of=%d", idx + 1)
                comp2_l, comp2_r = comp_l, comp_r
            # print('slit', lbarid, '-', rbarid, comp_l, comp_r)
            # print('pos1', comp_l, comp_r)
            # print('pos2', comp2_l, comp2_r)

            xpos1_virt, _ = dist.pvex(comp2_l + 1, ref_y_l_d)
            xpos2_virt, _ = dist.pvex(comp2_r + 1, ref_y_r_d)

            y1_virt = ref_y_l_v - slit_h_virt - slit_h_tol
            y2_virt = ref_y_r_v + slit_h_virt + slit_h_tol
            _, y1 = dist.exvp(xpos1_virt + 1, y1_virt)
            _, y2 = dist.exvp(xpos2_virt + 1, y2_virt)
            # print(comp2_l, comp2_r, y1 - 1, y2 - 1)
            cbb = BoundingBox.from_coordinates(comp2_l, comp2_r, y1 - 1, y2 - 1)
            slits_bb[lbarid] = cbb
            mask1[cbb.slice] = lbarid

        self.save_intermediate_array(mask1, 'mask_slit_computed.fits')
        return slits_bb


def pix2virt(pos, origin=1):
    ddef_o = 1
    off = ddef_o - origin
    pos = np.atleast_2d(pos) + off
    nx, ny = dist.pvex(pos[:, 0], pos[:, 1])
    res = np.stack((nx, ny), axis=1)
    return res - off


def compute_off_rotation(data, csu_conf, slits_bb, rotaxis=(0, 0),
                         logger=None, debug_plot=False,
                         intermediate_results=True
                         ):

    if logger is None:
        logger = logging.getLogger(__name__)

    swapped_code = (sys.byteorder == 'little') and '>' or '<'
    if data.dtype.byteorder == swapped_code:
        data = data.byteswap().newbyteorder()

    logger.info('we have %s slits', len(csu_conf.slits))
    refslits = [slit for slit in csu_conf.slits.values() if slit.target_type is TargetType.REFERENCE]
    logger.info('we have %s reference slits', len(refslits))

    p2 = []  # Pos REF VIRT
    p1 = []  # Pos REF DET
    q1 = []  # Pos Measured DET
    q2 = []  # Pos Measured VIRT
    EMIR_REF_IPA = 90.0552

    for this in refslits:
        if this.idx not in slits_bb:
            logger.warning('slit %s not detected, skipping', this.idx)
            continue

        bb = slits_bb[this.idx]
        region = bb.slice
        target_coordinates = this.target_coordinates
        res = comp_centroid(data, bb, debug_plot=debug_plot, plot_reference=target_coordinates)

        logger.debug('in slit %s, reference is %s', this.idx, target_coordinates)

        if res is None:
            logger.warning('no object found in slit %s, skipping', this.idx)
            continue

        if debug_plot and intermediate_results:
            ax = res[2]
            ax.set_title('slit %s' % this.idx)
            plt.savefig('centroid_slit_%s.png' % this.idx)
            # plt.show()

        m_x = res[0] + region[1].start
        m_y = res[1] + region[0].start

        logger.debug('in slit %s, object is (%s, %s)', this.idx, m_x, m_y)
        p1.append(this.target_coordinates)
        p2.append(this.target_coordinates_v)
        q1.append((m_x, m_y))

    logger.info('compute offset and rotation with %d points', len(p1))
    qc = QC.BAD

    if len(p2) == 0:
        logger.warning("can't compute offset and rotation with 0 points")
        offset = np.array([0.0, 0.0])
        rot = np.array([[1, 0], [0, 1]])
        angle = 0.0
    else:
        logger.debug('convert coordinates to virtual, ie, focal plane')
        q2 = pix2virt(q1, origin=0)
        # Move from objects to reference
        logger.debug('compute transform from measured objects to reference coordinates')
        offset, rot = fit_offset_and_rotation(q2, p2)
        logger.debug('rotation matrix')
        logger.debug('%s', rot)
        logger.debug('translation (with rotation around 0)')
        logger.debug('%s', offset)

        logger.debug('center of rotation (from CRPIX) is %s', rotaxis)
        logger.debug('translation (with rotation around rotaxis)')
        newoff = np.dot(rot, offset - rotaxis) + rotaxis
        logger.debug('%s', newoff)

        offset = newoff
        angle = math.atan2(rot[1, 0], rot[0, 0])
        angle = np.rad2deg(angle)
        qc = QC.GOOD
    logger.info('offset is %s', offset)
    logger.info('rot matrix is %s', rot)
    logger.info('rot angle %5.2f deg', angle)

    o_mm = offset * EMIR_PLATESCALE_PIX / EMIR_PLATESCALE
    angle = np.deg2rad(EMIR_REF_IPA)
    ipa_rot = create_rot2d(angle)
    logger.info('OFF (mm) %s', o_mm)
    logger.info('Default IPA is %s', EMIR_REF_IPA)
    o_mm_ipa = np.dot(ipa_rot, o_mm)

    logger.info('=========================================')
    logger.info('Offset Target in Focal Plane Frame %s mm', o_mm_ipa)
    logger.info('=========================================')

    pq1 = np.subtract(p1, q1)
    pq2 = np.subtract(p2, q2)
    if len(pq1) != 0:
        logger.debug('MEAN of REF-MEASURED (ON DETECTOR) %s', pq1.mean(axis=0))
        logger.debug('MEAN pf REF-MEASURED (VIRT) %s', pq2.mean(axis=0))

    return offset, angle, qc


def calc0(image, sob, prow, px1, px2, regionw, h=16, refine=False,
          plot=True, lbarid=0, rbarid=0, plot2=False):
    borders = [px1 - regionw, px1 + regionw, px2 - regionw, px2 + regionw,
               prow - h, prow + h]
    borders = np.clip(borders, 0, 2047)
    cc1l = borders[0]
    cc1r = borders[1]
    cc2l = borders[2]
    cc2r = borders[3]
    py1 = borders[4]
    py2 = borders[5]

    bb = BoundingBox.from_coordinates(cc1l, cc2r, py1, py2)

    lres = []

    # print(cc1l, cc2r, py1, py2)

    steps = range(-3, 3 + 1)
    scale = 3
    for s in steps:
        pr1 = prow + scale * s
        if pr1 < 0 or pr1 >= 2048:
            continue
        val = calc1b(image, sob, pr1, cc1l, cc1r, refine=refine,
                     plot=plot, barid=lbarid, px=px1)
        if val is not None:
            lres.append(val)

    # Average left bar position
    if lres:
        row_l, col_l, colr_l = zip(*lres)
    else:
        row_l, col_l, colr_l = [], [], []
    if refine:
        comp_l = np.mean(colr_l)
    else:
        comp_l = np.median(col_l)

    rres = []
    scale = 3
    for s in steps:
        pr1 = prow + scale * s
        if pr1 < 0 or pr1 >= 2048:
            continue

        val = calc1b(image, sob, pr1, cc2l, cc2r, sign=-1, refine=refine,
                     plot=plot, barid=rbarid, px=px2)
        if val is not None:
            rres.append(val)
    # Average left bar position
    if rres:
        row_r, col_r, colr_r = zip(*rres)
    else:
        row_r, col_r, colr_r = [], [], []

    if refine:
        comp_r = np.mean(colr_r)
    else:
        comp_r = np.median(col_r)

    if plot2:
        plt.imshow(image[bb.slice], extent=bb.extent)
        plt.scatter(colr_l, row_l, marker='+', color='black')
        plt.scatter(colr_r, row_r, marker='+', color='black')
        plt.axvline(px1, color='blue')
        plt.axvline(px2, color='blue')
        plt.axvline(comp_l, color='red')
        plt.axvline(comp_r, color='red')
        plt.show()

    return comp_l, comp_r


def calc1b(image, sob, pr, ccl, ccr, sign=1, refine=False, plot=True, barid=0, px=0):
    cut1 = sob[pr, ccl:ccr + 1]
    mcut1 = image[pr, ccl:ccr + 1]

    res = feat.peak_local_max(sign * cut1, exclude_border=4, num_peaks=2)

    if len(res) != 0:
        res1 = res[:, 0]
    else:
        res1 = []

    if sign > 0:
        bar_s = 'l'
    else:
        bar_s = 'r'

    if plot:
        xdummy = np.arange(ccl, ccr + 1)
        plt.title("{}bar {}, prow={} px={}".format(bar_s, barid, pr, px))
        plt.plot(xdummy, sign * cut1)
        plt.axvline(px, color='g')
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        ax2.plot(xdummy, mcut1, '--')
        for r in res1:
            plt.axvline(ccl + r, color='red')
        for r in res[:, 0]:
            plt.axvline(ccl + r, color='red', linestyle='--')
    xpeak = None
    if len(res1) != 0:
        idx = (sign * cut1)[res1].argmax()
        xpeak = ccl + res1[idx]

    if plot:
        if xpeak:
            plt.axvline(xpeak, color='black')
        plt.show()

    if xpeak:
        if refine:
            x_t, y_t = refine_peaks(sign * sob[pr], np.array([xpeak]), window_width=3)
            xpeak_ref = x_t
        else:
            xpeak_ref = xpeak
        return pr, xpeak, xpeak_ref
    else:
        return None


def create_rot2d(angle):
    ca = math.cos(angle)
    sa = math.sin(angle)
    return np.array([[ca, -sa], [sa, ca]])
