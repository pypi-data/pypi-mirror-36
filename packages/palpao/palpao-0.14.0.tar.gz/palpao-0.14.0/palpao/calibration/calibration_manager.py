
import os
import pyfits
from palpao.calibration.abstract_calibration_manager import \
    AbstractCalibrationManager
from plico.utils.decorator import override, returnsNone, returns, cacheResult
from palpao.types.modal_basis import ModalBasis
from plico.utils.fits_file_based_calibration_manager \
    import FitsFileBasedCalibrationManager



class CalibrationManagerException(Exception):
    pass


class CalibrationManager(AbstractCalibrationManager,
                         FitsFileBasedCalibrationManager):

    def __init__(self, calibrationRootDir):
        self._calibRootDir = calibrationRootDir


    def _checkTag(self, tag):
        if tag is None:
            raise CalibrationManagerException(
                "A tag must be given but is None")
        if len(tag) == 0:
            raise CalibrationManagerException(
                "A tag name must be valid but it is '%s'" % (tag))


    def getModalBasisFileName(self, tag):
        return os.path.join(self._calibRootDir,
                            "modal_basis",
                            "%s.fits" % tag)


    @override
    @returnsNone
    def saveModalBasis(self, tag, modalBasis):
        self._checkTag(tag)
        fileName= self.getModalBasisFileName(tag)
        self._createFoldersIfMissing(fileName)
        pyfits.writeto(fileName,
                       modalBasis.modalToZonalMatrix,
                       clobber=False)


    @override
    @returns(ModalBasis)
    @cacheResult
    def loadModalBasis(self, tag):
        self._checkTag(tag)
        fileName= self.getModalBasisFileName(tag)
        hduList= pyfits.open(fileName)
        return ModalBasis(hduList[0].data)



    def getPiTipTiltCalibrationFileName(self):
        return os.path.join(self._calibRootDir,
                            "modulator/pi_calibration.py")


    def _loadPiTipTiltCalibrationModule(self):
        import imp
        mm= imp.load_source('pi_calibration',
                            self.getPiTipTiltCalibrationFileName())
        return mm.PhysikInstrumenteCalibration()


    @override
    @cacheResult
    def loadPiTipTiltCalibration(self, serialNumber):
        pic= self._loadPiTipTiltCalibrationModule()
        return pic.getCalibrationFor(serialNumber)
