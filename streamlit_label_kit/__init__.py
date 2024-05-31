IS_RELEASE = True

from .LabelToolKit.detection import detection, convert_bbox_format, absolute_to_relative, relative_to_absolute
from .LabelToolKit.annotation import annotation

__version__ = "0.0.9"
