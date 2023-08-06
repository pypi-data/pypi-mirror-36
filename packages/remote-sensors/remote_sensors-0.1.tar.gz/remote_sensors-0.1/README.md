# Remote Sensors API protocol library

This library translates raw bytearrays into the Remote Sensors API models.

This implementation uses the [XBee Python library](https://github.com/digidotcom/python-xbee).
And translates the incoming device messages into a Remote Sensors Request and Response.

This library uses similar syntax than Sanic or Flask.

## Usage

```python
import remote_sensors

from digi.xbee.devices import XBeeDevice

import my_settings as settings


@remote_sensors.bind_to_device()
@remote_sensors.request()
def access_log(request: remote_sensors.Request, *args, **kwargs):
    """Simple Access Logger method."""
    logger.info(f'Request: {request.method} - {request.uri}')


@remote_sensors.bind_to_device()
@remote_sensors.request(method='REGISTRATION')
def handle_registration(request: remote_sensors.Request, *args, **kwargs):
    """Handles the registration request."""
    response = remote_sensors.Response(status='ACK',
                                       transaction=request.transaction)

    # do something about it :D
    payload = {
        'request': request.as_dict(),
        'response': response.as_dict(),
        'completed': False,
    }

    logger.debug(f'Replying with {response.status} to {sensor_message.addresses}')

    # send the response to the device
    return response


@remote_sensors.bind_to_device()
@remote_sensors.request(method='END_REGISTRATION', pass_message=True)
def handle_registration_end(request: remote_sensors.Request, sensor_message: remote_sensors.SensorRequest,
                            *args, **kwargs):
    """Handles the end of registration."""
    response = remote_sensors.Response(status='ACK',
                                       transaction=request.transaction)

    # do something about it :D
    payload = {
        'device': sensor_message.as_dict(),
        'request': request.as_dict(),
        'response': response.as_dict(),
        'completed': True,
    }

    logger.debug(f'Device ({sensor_message.addresses}) has finished registration')

    return response


device = XBeeDevice(settings.SERIAL_PORT, settings.BAUD_RATE)

def main():
    device.open()
    remote_sensors.app.init(device)

    while True:
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    finally:
        if device.is_open():
            device.close()

```

## Contact

Arnulfo Solis Ramirez

* arnulfojr94@gmail.com
