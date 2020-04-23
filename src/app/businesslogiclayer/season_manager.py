
# -*- coding: utf-8 -*-
import app.bem

from app.bem import match

import logging
from logging.config import fileConfig
fileConfig('/src/app/logging.ini')
logger = logging.getLogger()

from app.utils import simple_time_tracker

@simple_time_tracker.simple_time_tracker()
def reset_seasons():
    logger.info('- reset_seasons')
    
    #ok we retrieve all prior matchs
    allmatchs = match.Match.objects().all()

    for matchtoset in allmatchs:
        matchtoset.season_id = getSeasonFromMatchId(matchtoset._id)
        matchtoset.save()

    pass

def getSeasonFromMatchId(matchid):
    logger.info('getSeasonFromMatchId ' + str(matchid))
    if int(matchid) < 64:
        return 0
    else:
        return 1
