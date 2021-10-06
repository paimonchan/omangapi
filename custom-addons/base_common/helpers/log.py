import sys

def _log(self, message, level='info'):
    frame = sys._getframe(2)
    line_number = frame.f_lineno
    func_name = frame.f_code.co_name
    with self.pool.cursor() as cr:
        cr.execute("""
            INSERT INTO ir_logging(create_date, create_uid, type, dbname, name, level, message, path, line, func)
            VALUES (NOW() at time zone 'UTC', %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (self.env.uid, 'server', self._cr.dbname, self._name, level, message, "action", line_number, func_name))

def error(self, message):
    _log(self, message, level='error')

def info(self, message):
    _log(self, message, level='info')