from __future__ import print_function
import os
import errno
import gdal
import numpy as np
import matplotlib.pylab as plt
#plt.switch_backend('agg')
import scipy.optimize as optimize
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pybob.GeoImg import GeoImg
from pybob.ICESat import ICESat
from pybob.image_tools import create_mask_from_shapefile
from IPython import embed

def get_slope(geoimg):
    slope_ = gdal.DEMProcessing('', geoimg.gd, 'slope', format='MEM')
    return GeoImg(slope_)


def get_aspect(geoimg):
    aspect_ = gdal.DEMProcessing('', geoimg.gd, 'aspect', format='MEM')
    return GeoImg(aspect_)


def false_hillshade(dH, title, pp):
    niceext = np.array([dH.xmin, dH.xmax, dH.ymin, dH.ymax])/1000.
    fig = plt.figure(figsize=(7, 5))
    ax = plt.gca()
    im1 = ax.imshow(dH.img, extent=niceext)
    im1.set_clim(-20, 20)
    im1.set_cmap('Greys')
    fig.suptitle(title, fontsize=14)
    numwid = max([len('{:.1f} m'.format(np.nanmean(dH.img))),
                  len('{:.1f} m'.format(np.nanmedian(dH.img))), len('{:.1f} m'.format(np.nanstd(dH.img)))])
    plt.annotate('MEAN:'.ljust(8) + ('{:.1f} m'.format(np.nanmean(dH.img))).rjust(numwid), xy=(0.65, 0.95),
                 xycoords='axes fraction', fontsize=12, fontweight='bold', color='red', family='monospace')
    plt.annotate('MEDIAN:'.ljust(8) + ('{:.1f} m'.format(np.nanmedian(dH.img))).rjust(numwid),
                 xy=(0.65, 0.90), xycoords='axes fraction', fontsize=12, fontweight='bold',
                 color='red', family='monospace')
    plt.annotate('STD:'.ljust(8) + ('{:.1f} m'.format(np.nanstd(dH.img))).rjust(numwid), xy=(0.65, 0.85),
                 xycoords='axes fraction', fontsize=12, fontweight='bold', color='red', family='monospace')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im1, cax=cax)

    plt.tight_layout()
    pp.savefig(fig, bbox_inches='tight', dpi=200)
    return


def create_stable_mask(img, mask1, mask2):
    # if we have no masks, just return an array of true values
    if mask1 is None and mask2 is None:
        return np.ones(img.img.shape) == 0  # all false, so nothing will get masked.
    elif mask1 is not None and mask2 is None:  # we have a glacier mask, not land
        mask = create_mask_from_shapefile(img, mask1)
        return mask  # returns true where there's glacier, false everywhere else
    elif mask1 is None and mask2 is not None:
        mask = create_mask_from_shapefile(img, mask2)
        return np.logical_not(mask)  # false where there's land, true where there isn't
    else:  # if none of the above, we have two masks.
        gmask = create_mask_from_shapefile(img, mask1)
        lmask = create_mask_from_shapefile(img, mask2)
        return np.logical_or(gmask, np.logical_not(lmask))  # true where there's glacier or water


def preprocess(stable_mask, slope, aspect, master, slave):

    if isinstance(master, GeoImg):
        stan = np.tan(np.radians(slope)).astype(np.float32)
        dH = master.copy(new_raster=(master.img-slave.img))
        dH.img[stable_mask] = np.nan
        master_mask = isinstance(master.img, np.ma.masked_array)
        slave_mask = isinstance(slave.img, np.ma.masked_array)

        if master_mask and slave_mask:
            dH.mask(np.logical_or(master.img.mask, slave.img.mask))
        elif master_mask:
            dH.mask(master.img.mask)
        elif slave_mask:
            dH.mask(slave.img.mask)
        
        if dH.isfloat:
            dH.img[stable_mask] = np.nan

        dHtan = dH.img / stan
        mykeep = ((np.absolute(dH.img) < 200.0) & np.isfinite(dH.img) &
                  (slope > 7.0) & (dH.img != 0.0) & (aspect >= 0))
        dH.img[np.invert(mykeep)] = np.nan
        xdata = aspect[mykeep]
        ydata = dHtan[mykeep]
        sdata = stan[mykeep]

    elif isinstance(master, ICESat):
        slave_pts = slave.raster_points(master.xy)
        dH = master.elev - slave_pts
        
        slope_pts = slope.raster_points(master.xy)
        stan = np.tan(np.radians(slope_pts))
        
        aspect_pts = aspect.raster_points(master.xy)
        smask = stable_mask.raster_points(master.xy) > 0
        
        dH[smask] = np.nan

        dHtan = dH / stan

        mykeep = ((np.absolute(dH) < 200.0) & np.isfinite(dH) &
                  (slope_pts > 3.0) & (dH != 0.0) & (aspect_pts >= 0))
        
        dH[np.invert(mykeep)] = np.nan
        xdata = aspect_pts[mykeep]
        ydata = dHtan[mykeep]
        sdata = stan[mykeep]


    return dH, xdata, ydata, sdata


def coreg_fitting(xdata, ydata, sdata, title, pp):
    xdata = xdata.astype(np.float64)  # float64 truly necessary?
    ydata = ydata.astype(np.float64)
    sdata = sdata.astype(np.float64)
    # fit using equation 3 of Nuth and Kaeaeb, 2011

    def fitfun(p, x): return p[0] * np.cos(np.radians(p[1] - x)) + p[2]

    def errfun(p, x, y): return fitfun(p, x) - y
    
    if xdata.size > 20000:
        mysamp = np.random.randint(0, xdata.size, 20000)
    else:
        mysamp = np.arange(0, xdata.size)
    mysamp=mysamp.astype(np.int64)
    
    
    #embed()
    #print("soft_l1")
    lb = [-200, 0, -300]
    ub = [200, 180, 300]
    p0 = [1, 1, -1]
    #p1, success, _ = optimize.least_squares(errfun, p0[:], args=([xdata], [ydata]), method='trf', bounds=([lb],[ub]), loss='soft_l1', f_scale=0.1)
    #myresults = optimize.least_squares(errfun, p0, args=(xdata, ydata), method='trf', loss='soft_l1', f_scale=0.5)    
    myresults = optimize.least_squares(errfun, p0, args=(xdata[mysamp], ydata[mysamp]), method='trf', loss='soft_l1', f_scale=0.1,ftol=1E-4,xtol=1E-4)    
    #myresults = optimize.least_squares(errfun, p0, args=(xdata[mysamp], ydata[mysamp]), method='trf', bounds=([lb,ub]), loss='soft_l1', f_scale=0.1,ftol=1E-8,xtol=1E-8)    
    p1 = myresults.x
    # success = myresults.success # commented because it wasn't actually being used.
    # print success
    # print p1
    # convert to shift parameters in cartesian coordinates
    xadj = p1[0] * np.sin(np.radians(p1[1]))
    yadj = p1[0] * np.cos(np.radians(p1[1]))
    zadj = p1[2] * sdata.mean(axis=0)

    xp = np.linspace(0, 360, 361)
    yp = fitfun(p1, xp)


    
    fig = plt.figure(figsize=(7, 5), dpi=600)
    fig.suptitle(title, fontsize=14)
    plt.plot(xdata[mysamp], ydata[mysamp], '^', ms=0.5, color='0.5', rasterized=True, fillstyle='full')
    plt.plot(xp, np.zeros(xp.size), 'k', ms=3)
    plt.plot(xp, yp, 'r-', ms=2)

    plt.xlim(0, 360)
    #plt.ylim(-200,200)
    ymin, ymax = plt.ylim((np.nanmean(ydata[mysamp]))-2*np.nanstd(ydata[mysamp]),
                          (np.nanmean(ydata[mysamp]))+2*np.nanstd(ydata[mysamp]))
    # plt.axis([0, 360, -200, 200])
    plt.xlabel('Aspect [degrees]')
    plt.ylabel('dH / tan(slope)')
    numwidth = max([len('{:.1f} m'.format(xadj)), len('{:.1f} m'.format(yadj)), len('{:.1f} m'.format(zadj))])
    plt.text(0.05, 0.15, '$\Delta$x: ' + ('{:.1f} m'.format(xadj)).rjust(numwidth),
             fontsize=12, fontweight='bold', color='red', family='monospace', transform=plt.gca().transAxes)
    plt.text(0.05, 0.1, '$\Delta$y: ' + ('{:.1f} m'.format(yadj)).rjust(numwidth),
             fontsize=12, fontweight='bold', color='red', family='monospace', transform=plt.gca().transAxes)
    plt.text(0.05, 0.05, '$\Delta$z: ' + ('{:.1f} m'.format(zadj)).rjust(numwidth),
             fontsize=12, fontweight='bold', color='red', family='monospace', transform=plt.gca().transAxes)
    pp.savefig(fig, bbox_inches='tight', dpi=200)

    return xadj, yadj, zadj

def final_histogram(dH0, dHfinal, pp):
    fig = plt.figure(figsize=(7, 5), dpi=600)
    plt.title('Elevation difference histograms', fontsize=14)
    
    j1, j2 = np.histogram(dH0[np.isfinite(dH0)], bins=100, range=(-60, 60))
    k1, k2 = np.histogram(dHfinal[np.isfinite(dHfinal)], bins=100, range=(-60, 60))
    
    stats0 = [np.nanmean(dH0), np.nanmedian(dH0), np.nanstd(dH0), RMSE(dH0)]
    stats_fin = [np.nanmean(dHfinal), np.nanmedian(dHfinal), np.nanstd(dHfinal), RMSE(dHfinal)]    
    
    plt.plot(j2[1:], j1,'k-', linewidth=2)
    plt.plot(k2[1:], k1,'r-', linewidth=2)
    #plt.legend(['Original', 'Coregistered'])
    
    plt.xlabel('Elevation difference [meters]')
    plt.ylabel('Number of samples')
    plt.xlim(-50,50)
    
    #numwidth = max([len('{:.1f} m'.format(xadj)), len('{:.1f} m'.format(yadj)), len('{:.1f} m'.format(zadj))])
    plt.text(0.05, 0.90, 'Mean: ' + ('{:.1f} m'.format(stats0[0])),
             fontsize=12, fontweight='bold', color='black', family='monospace', transform=plt.gca().transAxes)
    plt.text(0.05, 0.85, 'Median: ' + ('{:.1f} m'.format(stats0[1])),
             fontsize=12, fontweight='bold', color='black', family='monospace', transform=plt.gca().transAxes)
    plt.text(0.05, 0.80, 'Std dev.: ' + ('{:.1f} m'.format(stats0[2])),
             fontsize=12, fontweight='bold', color='black', family='monospace', transform=plt.gca().transAxes)
    plt.text(0.05, 0.75, 'RMSE: ' + ('{:.1f} m'.format(stats0[3])),
             fontsize=12, fontweight='bold', color='black', family='monospace', transform=plt.gca().transAxes)


    plt.text(0.4, 0.90, 'Mean: ' + ('{:.1f} m'.format(stats_fin[0])),
             fontsize=12, fontweight='bold', color='red', family='monospace', transform=plt.gca().transAxes)
    plt.text(0.4, 0.85, 'Median: ' + ('{:.1f} m'.format(stats_fin[1])),
             fontsize=12, fontweight='bold', color='red', family='monospace', transform=plt.gca().transAxes)
    plt.text(0.4, 0.80, 'Std dev.: ' + ('{:.1f} m'.format(stats_fin[2])),
             fontsize=12, fontweight='bold', color='red', family='monospace', transform=plt.gca().transAxes)
    plt.text(0.4, 0.75, 'RMSE: ' + ('{:.1f} m'.format(stats_fin[3])),
             fontsize=12, fontweight='bold', color='red', family='monospace', transform=plt.gca().transAxes)
    pp.savefig(fig, bbox_inches='tight', dpi=200)
    
    
def RMSE(indata): 
    """ Return root mean square of indata."""
    myrmse = np.sqrt(np.nanmean(indata**2))
    return myrmse
    
    
def get_geoimg(indata):
    if type(indata) is str or type(indata) is gdal.Dataset:
        return GeoImg(indata)
    elif type(indata) is GeoImg:
        return indata
    else:
        raise TypeError('input data must be a string pointing to a gdal dataset, or a GeoImg object.')


def dem_coregistration(masterDEM, slaveDEM, glaciermask=None, landmask=None, outdir='.', pts=False, full_ext=False):
    """
    Iteratively co-register elevation data, based on routines described in Nuth and Kaeaeb, 2011.

    Parameters
    ----------
    masterDEM : string or GeoImg
        Path to filename or GeoImg dataset representing "master" DEM.
    slaveDEM : string or GeoImg
        Path to filename or GeoImg dataset representing "slave" DEM.
    glaciermask : string, optional
        Path to shapefile representing points to exclude from co-registration
        consideration (i.e., glaciers).
    landmask : string, optional
        Path to shapefile representing points to include in co-registration
        consideration (i.e., stable ground/land).
    outdir : string, optional
        Location to save co-registration outputs.
    pts : bool, optional
        If True, program assumes that masterDEM represents point data (i.e., ICESat),
        as opposed to raster data. Slope/aspect are then calculated from slaveDEM.
        masterDEM should be a string representing an HDF5 file continaing ICESat data.
    full_ext : bool, optional
        If True, program writes full extents of input DEMs. If False, program writes
        input DEMs cropped to their common extent. Default is False.
    """
    # if the output directory does not exist, create it.
    outdir = os.path.abspath(outdir)
    try:
        os.makedirs(outdir)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(outdir):
            pass
        else:
            raise
    # make a file to save the coregistration parameters to.
    paramf = open(outdir + os.path.sep + 'coreg_params.txt', 'w')
    # create the output pdf
    pp = PdfPages(outdir + os.path.sep + 'CoRegistration_Results.pdf')

    if full_ext:
        print('Writing full extents of output DEMs.')
    else:
        print('Writing DEMs cropped to common extent.')

    if type(masterDEM) is str:
        mfilename = os.path.basename(masterDEM)
    else:
        mfilename = masterDEM.filename

    if type(slaveDEM) is str:
        sfilename = os.path.basename(slaveDEM)
    else:
        sfilename = slaveDEM.filename

    slaveDEM = get_geoimg(slaveDEM)
    # if we're dealing with ICESat/pt data, change how we load masterDEM data
    if pts:
        masterDEM = ICESat(masterDEM)
        masterDEM.project('epsg:{}'.format(slaveDEM.epsg))
        mybounds=[slaveDEM.xmin, slaveDEM.xmax, slaveDEM.ymin, slaveDEM.ymax]
        masterDEM.clip(mybounds)
        masterDEM.clean()
        slope_geo = get_slope(slaveDEM)
        aspect_geo = get_aspect(slaveDEM)

        slope_geo.write('tmp_slope.tif', out_folder=outdir)
        aspect_geo.write('tmp_aspect.tif', out_folder=outdir)

        smask = create_stable_mask(slaveDEM, glaciermask, landmask)
        slaveDEM.mask(smask)
        stable_mask = slaveDEM.copy(new_raster=smask)  # make the mask a geoimg
    else:
        masterDEM = get_geoimg(masterDEM)
        
        masterDEM = masterDEM.reproject(slaveDEM)  # need to resample masterDEM to cell size of slave.
        #masterDEM.img[masterDEM.img<1]=np.nan
        stable_mask = create_stable_mask(masterDEM, glaciermask, landmask)

        slope_geo = get_slope(masterDEM)
        aspect_geo = get_aspect(masterDEM)
        slope_geo.write('tmp_slope.tif', out_folder=outdir)
        aspect_geo.write('tmp_aspect.tif', out_folder=outdir)
        masterDEM.mask(stable_mask)

    slope = slope_geo.img
    aspect = aspect_geo.img

    mythresh = np.float64(200)  # float64 really necessary?
    mystd = np.float64(200)
    mycount = 0
    tot_dx = np.float64(0)
    tot_dy = np.float64(0)
    tot_dz = np.float64(0)
    magnthresh = 200
    magnlimit=1
    mytitle = 'DEM difference: pre-coregistration'
    if pts:
        this_slave = slaveDEM
        this_slave.mask(stable_mask.img)
    else:
        this_slave = slaveDEM.reproject(masterDEM)
        this_slave.mask(stable_mask)

    while mythresh > 2 and magnthresh > magnlimit:
        if mycount != 0:
            # slaves.append(slaves[-1].reproject(masterDEM))
            # slaves[-1].mask(stable_mask)
            mytitle = "DEM difference: After Iteration {}".format(mycount)
        mycount += 1
        print("Running iteration #{}".format(mycount))
        print("Running iteration #{}".format(mycount), file=paramf)
        
        # if we don't have two DEMs, showing the false hillshade doesn't work.
        if not pts:
            dH, xdata, ydata, sdata = preprocess(stable_mask, slope, aspect, masterDEM, this_slave)
            false_hillshade(dH, mytitle, pp)
            dH_img = dH.img
        else:
            dH, xdata, ydata, sdata = preprocess(stable_mask, slope_geo, aspect_geo, masterDEM, this_slave)
            dH_img = dH

        if mycount == 1:
            dH0 = dH_img

        # calculate threshold, standard deviation of dH
        #mythresh = 100 * (mystd-np.nanstd(dH_img))/mystd
        #mystd = np.nanstd(dH_img)
        # USE RMSE instead ( this is to make su that there is improvement in the spread)
        mythresh = 100 * (mystd-RMSE(dH_img))/mystd
        mystd = RMSE(dH_img)

        mytitle2 = "Co-registration: Iteration {}".format(mycount)
        dx, dy, dz = coreg_fitting(xdata, ydata, sdata, mytitle2, pp)
        tot_dx += dx
        tot_dy += dy
        tot_dz += dz
        magnthresh = np.sqrt(np.square(dx)+np.square(dy)+np.square(dz))
        print(tot_dx, tot_dy, tot_dz)
        print(tot_dx, tot_dy, tot_dz, file=paramf)
        # print np.nanmean(slaves[-1].img)

        # print slaves[-1].xmin, slaves[-1].ymin

        # shift most recent slave DEM
        this_slave.shift(dx, dy)  # shift in x,y
        # print tot_dx, tot_dy
        # no idea why slaves[-1].img += dz doesn't work, but the below seems to.
        zupdate = np.ma.array(this_slave.img.data + dz, mask=this_slave.img.mask)  # shift in z
        this_slave = this_slave.copy(new_raster=zupdate)
        if pts:
            this_slave.mask(stable_mask.img)
            slope_geo.shift(dx, dy)
            aspect_geo.shift(dx, dy)
            stable_mask.shift(dx, dy)
        else:
            this_slave = this_slave.reproject(masterDEM)
            this_slave.mask(stable_mask)

        print("Percent-improvement threshold and Magnitute threshold:")
        print(mythresh, magnthresh)
        
        # slaves[-1].display()
        if mythresh > 2 and magnthresh > magnlimit:
            dH = None
            dx = None
            dy = None
            dz = None
            xdata = None
            ydata = None
            sdata = None
        else:
            if not pts:
                dH, xdata, ydata, sdata = preprocess(stable_mask, slope, aspect, masterDEM, this_slave)
                mytitle = "DEM difference: After Iteration {}".format(mycount)
                #adjust final dH
                #myfadj=np.nanmean([np.nanmean(dH.img),np.nanmedian(dH.img)])
                #myfadj=np.nanmedian(dH.img)
                #tot_dz += myfadj
                #dH.img = dH.img-myfadj
                
                false_hillshade(dH, mytitle, pp)
                dHfinal = dH.img
            else:
                mytitle2 = "Co-registration: FINAL"
                dH, xdata, ydata, sdata = preprocess(stable_mask, slope_geo, aspect_geo, masterDEM, this_slave)
                dx, dy, dz = coreg_fitting(xdata, ydata, sdata, mytitle2, pp)
                dHfinal = dH
 
    # Create final histograms pre and post coregistration
    # shift = [tot_dx, tot_dy, tot_dz]  # commented because it wasn't actually used.
    final_histogram(dH0, dHfinal, pp)

    # create new raster with dH sample used for co-registration as the band
    # dHSample = dH.copy(new_raster=dHpost_sample)
    # dHSample.write(outdir + os.path.sep + 'dHpost_sample.tif') # have to fill these in!
    # save full dH output
    # dHfinal.write('dHpost.tif', out_folder=outdir)
    # save adjusted slave dem
    if sfilename is not None:
        slaveoutfile = '.'.join(sfilename.split('.')[0:-1]) + '_adj.tif'
    else:
        slaveoutfile = 'slave_adj.tif'
    
    if pts:
        outslave = slaveDEM.copy()
    else:        
        if full_ext:
            outslave = get_geoimg(slaveDEM)
        else:
            outslave = slaveDEM.reproject(masterDEM)
    
    outslave.shift(tot_dx, tot_dy)
    outslave.img = outslave.img + tot_dz
    outslave.write(slaveoutfile, out_folder=outdir)
    outslave.filename=slaveoutfile

    
    if not pts:
        if mfilename is not None:
            mastoutfile = '.'.join(mfilename.split('.')[0:-1]) + '_adj.tif'
        else:
            mastoutfile = 'master_adj.tif'
        if full_ext:
            masterDEM = get_geoimg(mfilename)
        masterDEM.write(mastoutfile, out_folder=outdir)

    if pts:
        slope_geo.write('tmp_slope.tif', out_folder=outdir)
        aspect_geo.write('tmp_aspect.tif', out_folder=outdir)

    # Final Check --- for debug
    dH, xdata, ydata, sdata = preprocess(stable_mask, slope, aspect, masterDEM, outslave)
    false_hillshade(dH, 'FINAL CHECK', pp)


    pp.close()
    print("Fin.")
    print("Fin.", file=paramf)
    paramf.close()

    out_offs = [tot_dx, tot_dy, tot_dz]

    return masterDEM, outslave, out_offs
