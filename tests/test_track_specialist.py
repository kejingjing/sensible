from __future__ import division
import zmq
import time
import pytest
from sensible.tracking.track_specialist import TrackSpecialist
from sensible.util.sensible_threading import StoppableThread


class MockSensor(StoppableThread):
    """
    A mock class to emulate a sensor publishing a stream of measurements
    for the track specialist
    """
    def __init__(self, port, topic_filters, test_msg, name="MockSensor"):
        super(MockSensor, self).__init__(name)
        self._port = port
        self._topic_filters = topic_filters

        context = zmq.Context()
        self._pub = context.socket(zmq.PUB)
        self._pub.bind("tcp://*:{}".format(port))

        self._test_msg = test_msg

    def run(self):
        while not self.stopped():
            for t_filter in self._topic_filters:
                self._pub.send_string("{} {}".format(t_filter, self._test_msg))


def test_initialize_track_specialist():
    """Test that the TrackSpecialist constructor initializes the connection to a sensor
    correctly with the proper topic filters
    """
    sensor_port = 6667
    topic_filters = ["DSRC", "Radar"]
    run_for = 60  # seconds

    track_specialist = TrackSpecialist(sensor_port, topic_filters, run_for)
    test_message = "test"

    mock_sensor = MockSensor(sensor_port, topic_filters, test_message)
    mock_sensor.start()

    # assert that each connection is open
    attempts = 0
    max_attempts = 10000

    while attempts < max_attempts:
        count = 0
        for (topic, subscriber) in track_specialist.subscribers.items():
            try:
                string = subscriber.recv_string(flags=zmq.NOBLOCK)
                msg_topic, msg = string.split(" ")
                assert msg_topic == topic
                assert msg == test_message
                count += 1
            except zmq.Again as err:
                continue

        if count == 2:
            break

        attempts += 1

    mock_sensor.stop()

    if attempts == max_attempts:
        pytest.fail('Exceeded max attempts to send/recv messages')


def test_vehicle_id_association():
    """This tests whether new measurements can be matched to
    existing tracks based on ID"""
    pytest.fail('Unimplemented test')


def test_vehicle_id_association_no_match():
    """This tests whether an unconfirmed track is created
    when no vehicle ID match is found"""
    pytest.fail('Unimplemented test')


def test_track_creation():
    """This tests whether a new track is created with
    the correct state, i.e., UNCONFIRMED"""
    pytest.fail('Unimplemented test')


def test_radar_to_vehicle_association():
    """This tests whether a new radar detection can be matched
    to an existing DSRC-based track"""
    pytest.fail('Unimplemented test')


def test_radar_no_match():
    """This tests whether a radar detection with no matching
    vehicles correctly associates the detection to a new
    conventional vehicle. A BSM should be generated"""
    pytest.fail('Unimplemented test')


def test_vehicle_bsm_publisher():
    """This tests whether a BSM is generated for each
    CONFIRMED vehicle track that has not yet been served
    a trajectory"""
    pytest.fail('Unimplemented test')


def test_track_state_confirm():
    """This tests that an UNCONFIRMED track becomes
    confirmed after M consecutive messages arrive for that
    track, where M is the threshold."""
    pytest.fail('Unimplemented test')


def test_track_state_zombie():
    """This tests that a CONFIRMED and UNCONFIRMED track
    becomes a ZOMBIE after missing N consecutive messages,
    where N is the zombie threshold."""
    pytest.fail('Unimplemented test')


def test_track_deletion():
    """This tests whether a track is dropped once it misses
    more than the track deletion threshold for measurements"""
    pytest.fail('Unimplemented test')


def test_track_recovery():
    """This tests whether a track can recover from ZOMBIE
    state to UNCONFIRMED if a new message for it arrives
    before it is deleted"""
    pytest.fail('Unimplemented test')
