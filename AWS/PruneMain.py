from VolSnap import prune_old_snaps

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
logger.propagate = False

if __name__ == "__main__":
    prune_old_snaps.main()