import gbvision as gbv
import gbrpi

from algorithms import BaseAlgorithm
from constants import CAMERA_PORT
from constants import TABLE_IP, TABLE_NAME, OUTPUT_KEY, SUCCESS_KEY
from utils.gblogger import GBLogger

LOGGER_NAME = 'vision_master'


def main():
    logger = GBLogger(LOGGER_NAME)
    conn = gbrpi.TableConn(ip=TABLE_IP, table_name=TABLE_NAME)
    logger.debug('initialized conn')
    camera = gbv.USBCamera(CAMERA_PORT, gbv.LIFECAM_3000)  # rotate the camera here if needed
    logger.debug('initialized camera')

    all_algos = BaseAlgorithm.get_algorithms()

    possible_algos = {key: all_algos[key](OUTPUT_KEY, SUCCESS_KEY, conn) for key in all_algos}
    current_algo = None

    logger.info('starting...')
    while True:
        ok, frame = camera.read()
        algo_type = conn.get('algorithm')
        if algo_type is not None:
            if algo_type not in possible_algos:
                logger.warning(f'Unknown algorithm type: {algo_type}')
            if algo_type != current_algo:
                possible_algos[algo_type].reset(camera)
            algo = possible_algos[algo_type]
            algo(frame, camera)
        current_algo = algo_type


if __name__ == '__main__':
    main()
