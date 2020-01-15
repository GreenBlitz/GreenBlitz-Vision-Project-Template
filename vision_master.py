import gbvision as gbv
import gbrpi

from algorithms import BaseAlgorithm
from constants import CAMERA_PORT, TCP_STREAM_PORT
from constants import TABLE_IP, TABLE_NAME, OUTPUT_KEY, SUCCESS_KEY
from utils.gblogger import GBLogger

LOGGER_NAME = 'vision_master'


def main():
    logger = GBLogger(LOGGER_NAME, use_file=True)
    logger.allow_debug = BaseAlgorithm.DEBUG
    conn = gbrpi.TableConn(ip=TABLE_IP, table_name=TABLE_NAME)
    logger.info('initialized conn')
    camera = gbv.USBCamera(CAMERA_PORT, gbv.LIFECAM_3000)  # rotate the camera here if needed
    camera.set_auto_exposure(False)
    # camera.rescale(0.5)
    logger.info('initialized camera')

    all_algos = BaseAlgorithm.get_algorithms()

    logger.debug(f'Algorithms: {", ".join(all_algos)}')

    possible_algos = {key: all_algos[key](OUTPUT_KEY, SUCCESS_KEY, conn) for key in all_algos}
    current_algo = None

    logger.info('starting...')

    if BaseAlgorithm.DEBUG:
        stream = gbv.TCPStreamBroadcaster(TCP_STREAM_PORT)
    else:
        stream = None

    while True:
        ok, frame = camera.read()
        if BaseAlgorithm.DEBUG:
            stream.send_frame(frame)
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
