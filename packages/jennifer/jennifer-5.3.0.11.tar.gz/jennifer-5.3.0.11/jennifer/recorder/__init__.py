from .gc import GCRecorder
from .db import DBConnectionRecorder


class Recorder(object):
    def __init__(self):
        self.gc_recorder = GCRecorder()
        self.db_recorder = DBConnectionRecorder()

    def record_self(self):
        gc_time, gc_count, gc_gen_time = self.gc_recorder.record()
        db_connection = self.db_recorder.record()

        return {
            'gc_time': gc_time,
            'gc_count': gc_count,
            'gc_gen_time': gc_gen_time,
            'db_connection': db_connection,
        }
