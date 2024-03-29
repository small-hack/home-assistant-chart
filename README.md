# Home Assistant helm chart
<a href="https://github.com/small-hack/home-assistant-chart/releases"><img src="https://img.shields.io/github/v/release/small-hack/home-assistant-chart?style=plastic&labelColor=blue&color=green&logo=GitHub&logoColor=white"></a><br />
Who doesn't need more home assistant helm charts? This is a generic home assistant chart with basic features. It was written for use via [this Argo CD app](https://github.com/small-hack/argocd-apps/tree/main/home-assistant) which we deploy on metal with [`smol-k8s-lab`](https://github.com/small-hack/smol-k8s-lab).

#### Features

- Put a default configuration.yaml in place of your choosing with either:
  - your own ConfigMap
  - specifying an in-line yaml string for us to render as a ConfigMap for you
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


### Unit system, Temp Unit, and Time Zone

```yaml
homeAssistant:
  configuration: |
    homeassistant:
      time_zone: Europe/Amsterdam
      temperature_unit: C
      unit_system: metric
```

### Making Ingress Nginx work for public domains

I had to add the IP range of the k8s cluster to my trusted proxies in my home assistant `configuration.yaml` (also since this was public, I needed to declare an `external_url`).
This is what I added to my `values.yaml` to do that through this chart:

```yaml
homeAssistant:
  configuration: |
    # this sets your extenral url
    homeassistant:
      external_url: 'https://iot.examplesforgooddogs.com'

    # this enables proxies such as the ingress nginx controller
    http:
      use_x_forwarded_for: true
      trusted_proxies:
        - 10.0.0.0/8
```


### Using an existing ConfigMap for configuration.yaml

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


### USB Devices

If you're on metal, make sure your device is accessible, which in the case of a USB device e.g. conbee II, will require you to install the [generic device plugin](https://github.com/squat/generic-device-plugin):

```bash
kubectl apply -f https://raw.githubusercontent.com/squat/generic-device-plugin/main/manifests/generic-device-plugin.yaml
```

#### Values.yaml

Tip from [pajikos/home-assistant](https://github.com/pajikos/home-assistant) for passing in USB devices via `values.yaml`:

```yaml
extraVolumes:
  - name: usb
    hostPath:
      path: >-
        /dev/serial/by-id/usb-ITEAD_SONOFF_Zigbee_3.0_USB_Dongle_Plus_V2_20230509111242-if00
      type: CharDevice

extraVolumeMounts:
  - name: usb
    mountPath: /dev/ttyACM0
    # note that this is readonly to prevent security issues
    readOnly: true
```

### Bluetooth devices

If you're on metal and using a USB bluetooth apator of some sort, the process is a little different from the above USB Devices section. You probably want to mount dbus. See a `values.yaml` example here:

```yaml
extraVolumes:
  - name: bluetooth
    hostPath:
      path: /run/dbus

extraVolumeMounts:
  - name: bluetooth
    mountPath: /run/dbus
    # note that this is readonly to prevent security issues
    readOnly: true
```

### Mobile config

If you're new to home assistant, you may be wondering how you connect to the companion app on your phone. This requires you to put a key with no value called `mobile:` in the `configuration.yaml`. This would break your values.yaml depending on the gitops solution you're using, so we take the configuration as an in-line yaml block string instead like this:

```yaml
homeAssistant:
  configuration: |
    # this has no value
    mobile:
```

## Status
Seemingly stable. Feel free to submit PRs and Issues though :)
