from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
import sys
from amfi.download_data_files import AmfiDownload
from amfi.parse_amfi_files import AmfiParse
from amfi.amfi_mong import AmfiMongo
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG,
                     handlers=[logging.StreamHandler(sys.stdout)])
root_logger = logging.getLogger()
