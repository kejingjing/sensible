import argparse
from sensible.util import ops
import xml.etree.cElementTree as ElementTree
import pandas as pd


def parse(msg):
    """Convert msg data from hex to decimal and filter msgs.

    Messages with the Served field set to 1 or that are unreadable
    will be dropped. We assume the messages are arriving in proper XML
    format.

    :param msg:
    :return: parsed_msg
    """
    msg = msg.split("\n", 1)[1]

    try:
        root = ElementTree.fromstring(msg)
    except ElementTree.ParseError:
        raise Exception("Unable to parse msg")

    blob1 = root.find('blob1')
    data = ''.join(blob1.text.split())

    # convert hex values to decimal
    msg_count = int(data[0:2], 16)
    veh_id = int(data[2:10], 16)
    h = ops.verify(int(data[10:12], 16), 0, 23)
    m = ops.verify(int(data[12:14], 16), 0, 59)
    s = ops.verify(int(data[14:18], 16), 0, 60000)  # ms
    lat = ops.verify(ops.twos_comp(int(data[18:26], 16), 32), -900000000, 900000000) * 1e-7
    lon = ops.verify(ops.twos_comp(int(data[26:34], 16), 32), -1799999999, 1800000000) * 1e-7
    heading = ops.verify(int(data[34:38], 16), 0, 28799) * 0.0125
    rms_lat = int(data[38:42], 16)
    rms_lon = int(data[42:46], 16)
    speed = ops.verify(int(data[46:50], 16), 0, 8190) * 0.02  # m/s
    lane = int(data[50:52], 16)
    veh_len = ops.verify(int(data[52:56], 16), 0, 16383) * 0.01  # m
    max_accel = ops.verify(int(data[56:60], 16), 0, 2000) * 0.01  # m/s^2
    max_decel = ops.verify(int(data[60:64], 16), 0, 2000) * -0.01  # m/s^2
    served = int(data[64:66], 16)

    return {
        'msg_count': msg_count,
        'id': veh_id,
        'h': h,
        'm': m,
        's': s,
        'lat': lat,
        'lon': lon,
        'heading': heading,
        'speed': speed,
        'lane': lane,
        'veh_len': veh_len,
        'max_accel': max_accel,
        'max_decel': max_decel,
        'served': served
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', help='Provide a valid path to a DSRC log file')
    parser.add_argument('--dest', help='Provide a valid path to store pickled messages in')

    args = vars(parser.parse_args())

    with open(args['file'], 'rb') as f:
        msgs = f.read().split('<START>')

        results = []
        for msg in msgs:
            if msg == '':
                continue
            try:
                results.append(parse(msg))
            except ValueError as e:
                continue

        df = pd.DataFrame(results)

        ops.dump(df, args['dest'])