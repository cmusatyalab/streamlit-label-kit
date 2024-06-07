IS_RELEASE = True

from .LabelToolKit.detection import detection, convert_bbox_format, absolute_to_relative, relative_to_absolute, are_bboxes_equal
from .LabelToolKit.annotation import annotation
from .LabelToolKit.segmentation import segmentation
