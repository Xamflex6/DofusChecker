import mss
import numpy as np


def capture_zone(sct, zone):
    """Capture une zone ecran en RAM et retourne une image numpy (BGRX)."""
    return np.array(sct.grab(zone))
