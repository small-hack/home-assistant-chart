# home assistant helm chart
who doesn't need more home assistant helm charts?

# tips

tip from pajikos/home-assistant for passing in usb devices via values.yaml:

```bash
volumes:
  - hostPath:
      path: >-
        /dev/serial/by-id/usb-ITEAD_SONOFF_Zigbee_3.0_USB_Dongle_Plus_V2_20230509111242-if00
      type: CharDevice
    name: usb

volumeMounts:
  - mountPath: /dev/ttyACM0
    name: usb
```
