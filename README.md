# home assistant helm chart
<a href="https://github.com/small-hack/home-assistant-chart/releases"><img src="https://img.shields.io/github/v/release/small-hack/home-assistant-chart?style=plastic&labelColor=blue&color=green&logo=GitHub&logoColor=white"></a>
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

## tips

### Using your own configuration.yaml

make sure your ConfigMap has a key called `configuration.yaml` with in-line yaml data like this:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: home-assistant
  namespace: home-assistant
data:
  configuration.yaml: |
    http:
      trusted_proxies:
      - 10.0.0.0/8
      use_x_forwarded_for: true
```


### External Devices

tip from pajikos/home-assistant for passing in usb devices via values.yaml:

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

## status
demo and toy. feel free to submit PRs and Issues
