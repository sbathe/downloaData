from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
from amfi.download_data_files import AmfiDownload
from amfi.parse_amfi_files import AmfiParse
from amfi.amfi_mong import AmfiMongo
