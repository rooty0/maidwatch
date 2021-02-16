import miio
import logging
import yaml

from miio.vacuumcontainers import error_codes
from time import sleep

'''
https://www.reddit.com/r/homeassistant/comments/er7rmt/xiaomi_roborock_s5_carpet_mode_values/
https://support.roborock.com/hc/en-us/articles/360030818571-What-s-the-meaning-of-carpet-boost-mode-in-robot-cleaner-s-setting-

Get token: https://github.com/Maxmudjon/Get_MiHome_devices_token/releases

'''

with open("config.yaml") as file:
    config = yaml.full_load(file)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s', datefmt='%m/%d %H:%M')

vac = miio.Vacuum(config['ip'], config['token'])

logging.info("Connecting to vacuum cleaner...")
status = vac.status()
res = vac.consumable_status()

print("=== Consumables and maintenance ===")
print("Main brush:   {0:20} (left {1})".format(str(res.main_brush), res.main_brush_left))
print("Side brush:   {0:20} (left {1})".format(str(res.side_brush), res.side_brush_left))
print("Filter:       {0:20} (left {1})".format(str(res.filter), res.filter_left))
print("Sensor dirty: {0:20} (left {1})".format(str(res.sensor_dirty), res.sensor_dirty_left))
print()

print("=== Initial status ===")
print("Battery charge level: {0:6} Fan Speed is set to {1}%".format("{}%".format(status.battery), status.fanspeed))
print()

if not status.is_on:  # True if device is currently running/cleaning in any mode
    logging.info("Starting cleanup")
    vac.start()
else:
    logging.info("Vacuum is already cleaning, going to watch it...")

ERROR_COUNTER = {  # errors that allows to retry
    5: 0,  # error 5: Clean a fishing line and bearings of the Main Brush
    8: 0,  # error 8: Clean area around device
}
while True:
    sleep(30)
    status = vac.status()

    logging.info(
        "{0:16} Battery charge level: {1:4}   Cleaning since: {2}   Cleaned area: {3:9}   Carpet mode: {4}".format(
            "[{}]".format(status.state),
            "{}%".format(status.battery),
            status.clean_time,
            "{}m²".format(status.clean_area),
            vac.carpet_mode().enabled
        )
    )

    if status.got_error:  # todo: bypass if battery charge low
        if status.error_code in ERROR_COUNTER.keys():
            logging.info("Oh noo, just caught an error \"{}\", retrying...".format(error_codes[status.error_code]))
            ERROR_COUNTER[status.error_code] += 1

            if status.in_zone_cleaning:
                vac.resume_zoned_clean()
            else:
                vac.start()
        else:
            raise Exception("Unknown error code {}".format(status.error_code))

    for error_num, error_count in ERROR_COUNTER.items():
        if error_count >= config['errors_max_allowed']:
            logging.info("Error \"{}\" occurred too many times... trying to send vacuum to the doc".format(error_codes[error_num]))
            vac.home()
            break

    if status.state_code in [6, 8]:  # "Returning home", "Charging"
        logging.info("All done, vacuum is \"{}\", cya".format(status.state))
        break
