import sys
import os
import logging
import time
from threading import Timer
import nanomsg as nn

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)

import lib.remap_utils as remap_utils
import lib.remap_constants as remap_constants
from lib.remap_utils import RemapException
from base_module import FileModule

logging.basicConfig( level=logging.INFO ) 

# logger = logging.getLogger(__name__)
logger = logging.getLogger("Vertex")

def create_manager( workdata, config ):
    return Vertex( workdata, config )

class Vertex(FileModule):
    def __init__(self, workdata, config):
        FileModule.__init__(self,workdata,config)
        self.surveyor = nn.Socket( nn.SURVEYOR )
        self.surveyor.bind( "tcp://0.0.0.0:8688" )
        self.superstep = 0

    def create_job_data( self, filename, idx ):
        inputfile = os.path.join( self.relinputdir, filename )
        jobdata = { "inputfile": inputfile }
        jobdata["jobid"] = self.jobid
        jobdata["appdir"] = self.appname
        jobdata["appconfig"] = self.relconfig_file
        jobdata["type"] = "vertex"
        jobdata["workid"] = "%05d"%( idx )
        return inputfile, jobdata

    def get_work_key( self, data ):
        return data["inputfile"]

    def module_tracks_progress( self ):
        return True

    def all_hands_on_deck( self ):
        return True

    def finish( self ):
        self.surveyor.close()

    def check_progress( self ):
        self.surveyor.send( "%d"%(self.superstep) )

