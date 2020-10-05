from akangatu.marker import asMarker
from kururu.tool.communication.log import Log, AbsLog


class Report(asMarker, AbsLog):
    """Report printer.

        Syntax:
        $r prints 'r'
        {attr} prints the Data object attr, e.g.: {failure}
        """
