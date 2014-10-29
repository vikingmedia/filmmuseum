'''
Created on Oct 29, 2014

@author: zking
'''

from fish import Fish
import argparse
import logging
import time
import os
import sys
import glob
import re
import subprocess


################################################################################
# MAIN
################################################################################

if __name__ == '__main__':
    
    ###############################################################################
    # Handle command line arguments
    ###############################################################################
    p = argparse.ArgumentParser(description='Encode proxy file using FFMPEG while scanning.')
    p.add_argument('path', metavar='GLOB', help='input path, e.g. "/path/to/frames/*.dpx" ENCLOSE IN QUOTES!')
    p.add_argument('--logfile', help='logfile location')
    p.add_argument('--verbose', '-v', action='store_true', help='log to terminal')
    p.add_argument('--loglevel', default=10, type=int, help='10: DEBUG, 20: INFO, 30: WARNING, 40: ERROR, 50: CRITICAL')
    args = vars(p.parse_args())
    if not glob.has_magic(args['path']):
        sys.exit('%s is not a valid path, dude! Try something like /path/to/frames/*.dpx' % (args['path'], ))
        
    
    ################################################################################
    # logging
    ################################################################################
    logger = logging.getLogger()
    logger.setLevel(args['loglevel'])
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if args['logfile']:
        # Log to File
        fh = logging.FileHandler('scencode.log')
        fh.setLevel(logging.WARNING)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    if args['verbose']:
        # log to StdOut
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    fish = Fish()
    frames = []
    re_frame_number = re.compile('[0-9]+')
    
    ################################################################################
    # waiting for the frames 
    ################################################################################
    
    print '\nSearching for "%s"' % args['path']
    
    try:
        while not glob.glob(args['path']):
            fish.animate()
            time.sleep(0.0075)
            
        #print 'Frames found:'
        for frame in  glob.glob(args['path']):
            try: 
                frame_number_str = re_frame_number.search(frame).group()
                frame_number = int(frame_number_str)
                
            except (AttributeError, ValueError):
                sys.exit('"%s" doesn\'t contain a number!' % (frame,))
                
            #print '  #' + frame_number_str + ': ' + frame
            
            frames.append((frame_number, frame))
            
        start_frame = sorted(frames, key=lambda x: x[0])[0]
        base_frame = frame
        base_frame_number_str = frame_number_str
        zfill = len(frame_number_str)
        next_frame_number = start_frame[0]+1
        next_frame = (base_frame.replace(base_frame_number_str, str(next_frame_number).zfill(zfill)))
        next_frame_name = os.path.basename(next_frame)
        
        print 'Start frame: #%s (%s)' % start_frame
        #print 'Number format: ' + '#'*zfill
        print
        
        # set up encoding process
        print 'Starting encoding process ...'
        
        
        print '\npress CTRL+C to stop!'
        while True:
            while not os.path.isfile(next_frame):
                fish.animate(amount=next_frame_name)
                time.sleep(0.0075)
                
            # Found next frame
            next_frame_number += 1
            next_frame = (base_frame.replace(base_frame_number_str, str(next_frame_number).zfill(zfill)))
            next_frame_name = os.path.basename(next_frame)
            
            

        
    
    except KeyboardInterrupt:
        print '\n\nSee you next time!'
    