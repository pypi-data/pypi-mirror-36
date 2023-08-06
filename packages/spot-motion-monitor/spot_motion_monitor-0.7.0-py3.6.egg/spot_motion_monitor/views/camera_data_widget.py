#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from PyQt5.QtWidgets import QWidget

from spot_motion_monitor.utils import NO_DATA_VALUE
from spot_motion_monitor.views.ui_camera_data import Ui_CameraData

__all__ = ["CameraDataWidget"]

class CameraDataWidget(QWidget, Ui_CameraData):

    """This class handles the interactions from the Camera Data Widget on
       the MainWindow.
    """

    def __init__(self, parent=None):
        """Initalize the class.

        Parameters
        ----------
        parent : None, optional
            Top-level widget.
        """
        super().__init__(parent)
        self.setupUi(self)

    def formatFloat(self, value):
        """Format a float to 2 digits of precision.

        Parameters
        ----------
        value : float
            The value to format.

        Returns
        -------
        str
            The formatted float.
        """
        return "{:.2f}".format(value)

    def updateFullFrameData(self, fullFrameInfo):
        """Update the labels with full frame information.

        Parameters
        ----------
        fullFrameInfo : .FullFrameInformation
            The instance containing the full frame information.
        """
        self.centroidXLabel.setText(str(fullFrameInfo.centerX))
        self.centroidYLabel.setText(str(fullFrameInfo.centerY))
        self.fluxValueLabel.setText(self.formatFloat(fullFrameInfo.flux))
        self.maxAdcValueLabel.setText(self.formatFloat(fullFrameInfo.maxAdc))

        # Full frames do not set any of this information
        self.accumPeriodValueLabel.setText(NO_DATA_VALUE)
        self.rmsXLabel.setText(NO_DATA_VALUE)
        self.rmsYLabel.setText(NO_DATA_VALUE)

    def updateRoiFrameData(self, roiFrameInfo):
        """Update the labels with ROI frame information,

        Parameters
        ----------
        roiFrameInfo : .RoiFrameInformation
            The instance containing the ROI frame information.
        """
        if roiFrameInfo is None:
            return

        self.accumPeriodValueLabel.setText(self.formatFloat(roiFrameInfo.validFrames[1]))
        self.centroidXLabel.setText(self.formatFloat(roiFrameInfo.centerX))
        self.centroidYLabel.setText(self.formatFloat(roiFrameInfo.centerY))
        self.rmsXLabel.setText(self.formatFloat(roiFrameInfo.rmsX))
        self.rmsYLabel.setText(self.formatFloat(roiFrameInfo.rmsY))
        self.fluxValueLabel.setText(self.formatFloat(roiFrameInfo.flux))
        self.maxAdcValueLabel.setText(self.formatFloat(roiFrameInfo.maxAdc))
