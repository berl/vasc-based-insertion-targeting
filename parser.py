
import argparse as ap

def damage_quant_parser():
    parser = ap.ArgumentParser(description='quantify theoretical damage from '
                               'electrode insertion')
    parser.add_argument('pre',help='path to 2-photon pre-data')
    parser.add_argument('post',help='path to 2-photon post-data')
    parser.add_argument('segments', help='path to segment id mask generated by'
                        ' swc2maskBRL')
    parser.add_argument('probe_length',help='length of probe used for '
                        'insertion (in microns)', type=int)
    parser.add_argument('probe_width',help='width of probe used for insertion '
                        '(in microns)', type=int)
    parser.add_argument('probe_depth', help='depth to which the probe was '
                        'inserted (in microns)', type=int)
    parser.add_argument('-m', '--microns_per_pixel', help='multiplicative '
                        'factor by which pixel values can be transformed to '
                        'micron values (default 1)', default=1.0, type=float)
    parser.add_argument('-d', '--debug', help='print (potentially) helpful '
                        'debug info', action='store_true', default=False)
    parser.add_argument('-c', '--cache', help='turns off caching of probe '
                        'location in prestack (on by default)', 
                        action='store_false', default=True)
    parser.add_argument('-C', '--look_cache', help='turns off looking in cache'
                        ' location (on by default)', action='store_false', 
                        default=True)
    
    return parser