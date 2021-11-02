import logging
import re
from pathlib import Path

LOG = logging.getLogger('client.app')
FILES_COUNT = len(sorted(Path('').glob('client*.log')))


FILE_HANDLER = logging.FileHandler(f'client{FILES_COUNT}.log', encoding='utf8')
FILE_HANDLER.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter("%(asctime)-25s %(levelname)s %(module)s | %(message)s")
FILE_HANDLER.setFormatter(FORMATTER)
LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

LOG.info('TestMessage')