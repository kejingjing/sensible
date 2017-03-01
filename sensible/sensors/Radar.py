from sensible.util.sensible_threading import SensorThread, StoppableThread


class Radar(SensorThread):

    def __init__(self, name="Radar"):
        super(Radar, self).__init__(name, msg_len=0)

    @staticmethod
    def topic():
        return "Radar"

    def push(self, msg):
        """

        :param msg:
        :return:
        """
        pass