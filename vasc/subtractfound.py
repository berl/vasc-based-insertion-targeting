#!/usr/local/bin/python

import numpy as np
import tiff.tifffile as tiff
from SWC import Piece
from os.path import splitext
from compare import compare_masked_to_source_imgs

def invert_mask(mask):
    return ~mask.astype(bool)

def crop_mask(mask, bound, im_shape):
    newmins = (np.around(bound['x'][0]), np.around(bound['y'][0]), 
               np.around(bound['z'][0]))
    print bound
    print newmins
    print im_shape
    print mask.shape
    cropped_mask = mask[-newmins[2]:-newmins[2]+im_shape[0], 
                        -newmins[1]:-newmins[1]+im_shape[1],
                        -newmins[0]:-newmins[0]+im_shape[2]]
    return cropped_mask

def find_bounds(vascswc, cylinder=True):
    with open(vascswc, 'rb') as swc:
        i = 0
        for line in swc:
            line = line.strip()
            if line[0] == '#':
                pass
            else:
                entry = Piece.from_string(line, cylinder) 
                if i == 0: 
                    xmin = entry.get_dimmin('x')
                    ymin = entry.get_dimmin('y')
                    zmin = entry.get_dimmin('z')
                    
                    xmax = entry.get_dimmax('x')
                    ymax = entry.get_dimmax('y')
                    zmax = entry.get_dimmax('z')
            
                    margin = 0

                    i += 1
                else: 
                    xmin = min(xmin, entry.get_dimmin('x'))
                    ymin = min(ymin, entry.get_dimmin('y'))
                    zmin = min(zmin, entry.get_dimmin('z'))

                    xmax = max(xmax, entry.get_dimmax('x'))
                    ymax = max(ymax, entry.get_dimmax('y'))
                    zmax = max(zmax, entry.get_dimmax('z'))

                    margin = max(margin, entry.rad + 0.5)

    if cylinder:
        bounds = {'x':(xmin - margin, xmax + margin), 
                  'y':(ymin - margin, ymax + margin), 
                  'z':(zmin - margin, zmax + margin)}
    else: 
        bounds = {'x':(xmin, xmax), 'y':(ymin, ymax), 'z':(zmin, zmax)}
     
    return bounds

def resize_mask(swcpath, cylinder=True, maskpath=None, imgpath=None, 
                imshape=None):
    bounds = find_bounds(swcpath, cylinder)
    if imgpath is None and imshape is None:
        raise IOError('need to be given either imgpath or imshape')
    elif imgpath is not None and imshape is None:
        imshape = tiff.imread(imgpath)
    if maskpath is None:
        print 'cannot resize mask, no path given'
        print '---- orig img ----'
        x = -np.around(bounds['x'][0])
        print 'x : '+str(x)+' to '+str(x+imshape[2])
        y = -np.around(bounds['y'][0])
        print 'y : '+str(y)+' to '+str(y+imshape[1])
        z = -np.around(bounds['z'][0])
        print 'z : '+str(z)+' to '+str(z+imshape[0])
    else:
        mask = tiff.imread(maskpath)
        cropped_mask = crop_mask(mask, bounds, img.shape)
        tiff.imsave(splitext(maskpath)[0] + '-cropped.tif', cropped_mask)
    return

def mask_findings(imgpath, maskpath, swcpath, cylinder):
    
    bounds = find_bounds(swcpath, cylinder) 
    mask = tiff.imread(maskpath)
    inverted_mask = invert_mask(mask)
    img = tiff.imread(imgpath)
    cropvert_mask = crop_mask(inverted_mask, bounds, img.shape)

    masked_img = cropvert_mask * img

    compare_masked_to_source_imgs(masked_img, img)
    tiff.imsave(splitext(imgpath)[0] + '_masked.tif', masked_img)
    return