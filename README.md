# home assistant helm chart
<a href="https://github.com/small-hack/home-assistant-chart/releases"><img src="https://img.shields.io/github/v/release/small-hack/home-assistant-chart?style=plastic&labelColor=blue&color=green&logo=GitHub&logoColor=white"></a><br />
Who doesn't need more home assistant helm charts?

#### Features

- Put a default configuration.yaml in place of your choosing.
- Kept up to date by RenovateBot

## TLDR

```bash
# add the chart repo to your helm repos
helm repo add home-assistant https://small-hack.github.io/home-assistant-chart

# download the values.yaml and edit it with your own values such as YOUR hostname
helm show values home-assistant/home-assistant > values.yaml

# install the chart
helm install --namespace home-assistant --create-namespace home-assistant/home-assistant --values values.yaml
```

## Tips

### Using your own configuration.yaml ConfigMap

For the ConfigMap, make sure your ConfigMap has a key called `configuration.yaml` with in-line yaml data like this:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-home-assistant-configmap
  namespace: home-assistant
data:
  configuration.yaml: |
    http:
      trusted_proxies:
      - 10.0.0.0/8
      use_x_forwarded_for: true
```

Then, you'd specify the name of your ConfigMap in your `values.yaml` like this:

```yaml
homeAssistant:
  existingConfigMap: "my-home-assistant-configmap"
```


### External Devices

Make sure your device is accessible, which in the case of a USB device e.g. conbee II, will require you to install the [generic device plugin](https://github.com/squat/generic-device-plugin):

```bash
kubectl apply -f https://raw.githubusercontent.com/squat/generic-device-plugin/main/manifests/generic-device-plugin.yaml
```

#### Values.yaml

Tip from [pajikos/home-assistant](https://github.com/pajikos/home-assistant) for passing in USB devices via `values.yaml`:

```yaml
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

## Status
Seemingly stable. Feel free to submit PRs and Issues.
