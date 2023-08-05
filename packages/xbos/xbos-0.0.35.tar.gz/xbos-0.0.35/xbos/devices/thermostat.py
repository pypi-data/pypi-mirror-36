
import time
import msgpack

from bw2python.bwtypes import PayloadObject
from bw2python.client import Client
from xbos.util import read_self_timeout

class Thermostat(object):
    def __init__(self, client=None, uri=None):
        self.client = client
        self._uri = uri.rstrip('/')
        self._state = {
         "cooling_setpoint": None,
         "enabled_cool_stages": None,
         "enabled_heat_stages": None,
         "fan_mode": None,
         "fan_state": None,
         "heating_setpoint": None,
         "mode": None,
         "override": None,
         "relative_humidity": None,
         "state": None,
         "temperature": None,
         "time": None,
        }
        def _handle(msg):
            for po in msg.payload_objects:
                if po.type_dotted == (2,1,1,0):
                    data = msgpack.unpackb(po.content)
                    for k,v in data.items():
                        self._state[k] = v
        # check liveness
        liveness_uri = "{0}/!meta/lastalive".format(uri)
        res = self.client.query(liveness_uri)
        if len(res) == 0:
            raise Exception("No liveness message found at {0}. Is this URI correct?".format(liveness_uri))
        alive = msgpack.unpackb(res[0].payload_objects[0].content)
        ts = alive['ts'] / 1e9
        if time.time() - ts > 30:
            raise Exception("{0} more than 30sec old. Is this URI current?".format(liveness_uri))
        print "Got Thermostat at {0} last alive {1}".format(uri, alive['val'])

        self.client.subscribe("{0}/signal/info".format(uri), _handle)
        self.client.subscribe("{0}/stages/info".format(uri), _handle)

    @property
    def cooling_setpoint(self, timeout=30):
        return read_self_timeout(self, 'cooling_setpoint', timeout)

    @property
    def enabled_cool_stages(self, timeout=30):
        return read_self_timeout(self, 'enabled_cool_stages', timeout)

    @property
    def enabled_heat_stages(self, timeout=30):
        return read_self_timeout(self, 'enabled_heat_stages', timeout)

    @property
    def fan_mode(self, timeout=30):
        return read_self_timeout(self, 'fan_mode', timeout)

    @property
    def fan_state(self, timeout=30):
        return read_self_timeout(self, 'fan_state', timeout)

    @property
    def heating_setpoint(self, timeout=30):
        return read_self_timeout(self, 'heating_setpoint', timeout)

    @property
    def mode(self, timeout=30):
        return read_self_timeout(self, 'mode', timeout)

    @property
    def override(self, timeout=30):
        return read_self_timeout(self, 'override', timeout)

    @property
    def relative_humidity(self, timeout=30):
        return read_self_timeout(self, 'relative_humidity', timeout)

    @property
    def state(self, timeout=30):
        return read_self_timeout(self, 'state', timeout)

    @property
    def temperature(self, timeout=30):
        return read_self_timeout(self, 'temperature', timeout)


    def write(self, state, uri='state'):
        po = PayloadObject((2,1,1,0), None, msgpack.packb(state))
        self.client.publish('{0}/slot/{1}'.format(self._uri, uri),payload_objects=(po,))

    def set_heating_setpoint(self, value):
        self.write({'heating_setpoint': value})

    def set_cooling_setpoint(self, value):
        self.write({'cooling_setpoint': value})

    def set_override(self, value):
        self.write({'override': value})

    def set_mode(self, value):
        self.write({'mode': value})

    def set_fan_mode(self, value):
        self.write({'fan_mode': value})

    def set_enabled_heat_stages(self, value):
        self.write({'enabled_heat_stages': value}, 'stages')

    def set_enabled_cool_stages(self, value):
        self.write({'enabled_cool_stages': value}, 'stages')

