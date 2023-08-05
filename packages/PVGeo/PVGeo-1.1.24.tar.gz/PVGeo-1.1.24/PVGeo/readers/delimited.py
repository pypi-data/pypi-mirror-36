__all__ = [
    'DelimitedTextReader',
    'XYZTextReader'
]

import numpy as np

# Import Helpers:
from ..base import ReaderBase
from .. import _helpers


class DelimitedTextReader(ReaderBase):
    """This reader will take in any delimited text file and make a ``vtkTable`` from it. This is not much different than the default .txt or .csv reader in ParaView, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.
    """
    __displayname__ = 'Delimited Text Reader'
    __category__ = 'reader'
    def __init__(self, nOutputPorts=1, outputType='vtkTable', **kwargs):
        ReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType, **kwargs)

        # Parameters to control the file read:
        #- if these are set/changed, we must reperform the read
        self.__delimiter = kwargs.get('delimiter', ' ')
        self.__useTab = kwargs.get('useTab', False)
        self.__skipRows = kwargs.get('skiprows', 0)
        self.__comments = kwargs.get('comments', '!')
        self.__hasTitles = kwargs.get('HasTitles', True)
        # Data objects to hold the read data for access by the pipeline methods
        self._data = []
        self.__titles = []

    def _GetDeli(self):
        """For itenral use
        """
        if self.__useTab:
            return None
        return self.__delimiter

    #### Methods for performing the read ####

    def _GetFileContents(self, idx=None):
        if idx is not None:
            fileNames = [self.GetFileNames(idx=idx)]
        else:
            fileNames = self.GetFileNames()
        contents = []
        for f in fileNames:
            try:
                contents.append(np.genfromtxt(f, dtype=str, delimiter='\n', comments=self.__comments)[self.__skipRows::])
            except (FileNotFoundError, OSError) as fe:
                raise _helpers.PVGeoError(str(fe))
        if idx is not None: return contents[0]
        return contents

    def _ExtractHeader(self, content):
        """Override this. Removes header from single file's content.
        """
        if len(np.shape(content)) > 2:
            raise _helpers.PVGeoError("`_ExtractHeader()` can only handle a sigle file's content")
        idx = 0
        if self.__hasTitles:
            titles = content[idx].split(self._GetDeli())
            idx += 1
        else:
            cols = len(content[idx].split(self._GetDeli()))
            titles = []
            for i in range(cols):
                titles.append('Field %d' % i)
        return titles, content[idx::]

    def _ExtractHeaders(self, contents):
        """Should NOT be overriden.
        """
        ts = []
        for i in range(len(contents)):
            titles, newcontent = self._ExtractHeader(contents[i])
            contents[i] = newcontent
            ts.append(titles)
        # Check that the titles are the same across files:
        ts = np.unique(np.asarray(ts), axis=0)
        if len(ts) > 1:
            raise _helpers.PVGeoError('Data array titles varied across file timesteps. This data is invalid as a timeseries.')
        return ts[0], contents


    def _FileContentsToDataArray(self, contents):
        """Should NOT need to be overriden
        """
        data = []
        for content in contents:
            data.append(np.genfromtxt((line.encode('utf8') for line in content), delimiter=self._GetDeli(), dtype=None))
        return data

    def _ReadUpFront(self):
        """Should not need to be overridden.
        """
        # Perform Read
        contents = self._GetFileContents()
        self.__titles, contents = self._ExtractHeaders(contents)
        self._data = self._FileContentsToDataArray(contents)
        self.NeedToRead(flag=False)
        return 1

    #### Methods for accessing the data read in #####

    def _GetRawData(self, idx=0):
        """This will return the proper data for the given timestep.
        """
        return self._data[idx]


    #### Algorithm Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used b pipeline to get data for current timestep and populate the output data object.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)
        if self.NeedToRead():
            self._ReadUpFront()
        # Generate the data object
        _helpers.placeArrInTable(self._GetRawData(idx=i), self.__titles, output)
        return 1


    #### Seters and Geters ####


    def SetDelimiter(self, deli):
        """The input file's delimiter. To use a tab delimiter please use ``SetUseTab()``

        Args:
            deli (str): a string delimiter/seperator
        """
        if deli != self.__delimiter:
            self.__delimiter = deli
            self.Modified()

    def SetSplitOnWhiteSpace(self, flag):
        """Set a boolean flag to override the ``SetDelimiter()`` and use any white space as a delimiter.
        """
        if flag != self.__useTab:
            self.__useTab = flag
            self.Modified()

    def SetUseTab(self, flag):
        """Deprecated"""
        self.SetSplitOnWhiteSpace(flag)


    def SetSkipRows(self, skip):
        """The integer number of rows to skip at the top of the file.
        """
        if skip != self.__skipRows:
            self.__skipRows = skip
            self.Modified()

    def GetSkipRows(self):
        return self.__skipRows

    def SetComments(self, identifier):
        """The character identifier for comments within the file.
        """
        if identifier != self.__comments:
            self.__comments = identifier
            self.Modified()

    def SetHasTitles(self, flag):
        """A boolean for if the delimited file has header titles for the data arrays.
        """
        if self.__hasTitles != flag:
            self.__hasTitles = flag
            self.Modified()

    def HasTitles(self):
        return self.__hasTitles

    def GetTitles(self):
        return self.__titles




class XYZTextReader(DelimitedTextReader):
    """A makeshift reader for XYZ files where titles have comma delimiter and data has space delimiter.
    """
    __displayname__ = 'XYZ Text Reader'
    __category__ = 'reader'
    def __init__(self, **kwargs):
        DelimitedTextReader.__init__(self, **kwargs)
        self.SetComments(kwargs.get('comments', '#'))

    # Simply override the extract titles functionality
    def _ExtractHeader(self, content):
        titles = content[0][2::].split(', ') # first two characers of header is '! '
        return titles, content[1::]
