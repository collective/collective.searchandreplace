from AccessControl import ModuleSecurityInfo
import logging
import sys

logger = logging.getLogger("getSearchandReplace")
security = ModuleSecurityInfo('collective.searchandreplace.getSearchandReplaceFiles')

security.declarePublic('getFiles')
def getFiles(batch):
    
    lists = {}
    for o in batch:
        lists[o.getURL()] = o
        #logger.info("URL is %s" % str(o.getURL())) 
    batch = lists.values()
    #logger.info("list length is %d" % len(batch)) 
    from Products.CMFPlone import Batch
    batch = Batch(batch, sys.maxint, 0, orphan=0)
    return batch

