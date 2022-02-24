[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]

[![GitHub Activity][commits-shield_y]][commits]
[![GitHub Activity][commits-shield_m]][commits]
[![GitHub Activity][commits-shield_w]][commits]


[![Validate][validate-shield]][validation]

<!--
[!Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]
-->

# Zeversolar inverter integration for Home Assistant

<!--_Component to integrate with [zeversolar_local][zeversolar_local]._ -->
_Component to integrate with a Zeversolar inverter using its local API._

**This component will set up the following platform.**

Platform | Description
-- | --
`sensor` | Show information from the Zeversolar inverter.

<!-- ![example][exampleimg] -->

## Installation

1. If you do not have a `custom_components` directory (folder) there, you need to create it.
2. In the `custom_components` directory (folder) create a new folder called `zeversolar_local`.
3. Download _all_ the files from the `custom_components/zeversolar_local/` directory (folder) in this repository.
4. Place the files you downloaded in the new directory (folder) you created.
5. Restart Home Assistant
6. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Zeversolar Inverter - local"

## Configuration is done in the UI

1. Input the IP address of your inverter: e.g. 192.168.5.101
2. You can configure the default poll interval (30s) using the configuration link of the integration. It can be set between 10 and 3600 seconds.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

You should use Visual Studio Code to develop in a container. In this container you
will have all the tools to ease your python development and a dedicated Home
Assistant core instance to run your integration. See `.devcontainer/README.md` for more information.
Run the appropriate requirement task to install the requirements for development or test.

# Notice

This integration is under construction.
Some functions are missing yet.


### Room for improvements
I am uncertain how to deal if the inverter is powered off (in the night). The actual implementation is to change the entities to unavailable. So the entities will disappear from the dashboards.
Showing the last state is definitively wrong for the actual power and will lead to curious history graphs for power and summarized energy on the next day until the inverter reconnects.
The inverter itself has the problem that it looses the summarized (daily) values on a power failure and the counting starts at zero.

# Thanks
I'll want to thank @mletenay for creating the [Godwee inverter integration](https://www.home-assistant.io/integrations/goodwe/) that motivated me to implement this integration and to Aaron Godfrey for his [blog](https://aarongodfrey.dev/home%20automation/building_a_home_assistant_custom_component_part_1/) to create an integration.

Also thanks for instructions, blueprints, container etc. that are very helpful for me:
- Development container: https://github.com/ludeeus/hassio-homeassistant
- Instructions: https://developers.home-assistant.io/docs/creating_component_index/
- Blueprint for integrations: https://github.com/custom-components/integration_blueprint

***

<!-- HACS-Default-orange.svg?style=for-the-badge -->
[releases-shield]: https://img.shields.io/github/v/release/NECH2004/zeversolar_local?style=for-the-badge
[releases]: https://github.com/NECH2004/zeversolar_local/releases

[commits-shield_y]: https://img.shields.io/github/commit-activity/y/NECH2004/zeversolar_local?style=for-the-badge
[commits-shield_m]: https://img.shields.io/github/commit-activity/m/NECH2004/zeversolar_local?style=for-the-badge
[commits-shield_w]: https://img.shields.io/github/commit-activity/w/NECH2004/zeversolar_local?style=for-the-badge
[commits]: https://github.com/NECH2004/zeversolar_local/commits/dev

[validate-shield]: https://github.com/NECH2004/zeversolar_local/actions/workflows/validate.yml/badge.svg?branch=dev
[validation]: https://github.com/NECH2004/zeversolar_local/actions/workflows/validate.yml

[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]:https://img.shields.io/github/license/NECH2004/zeversolar_local?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Christian%20Neumeier%20%40NECH2004?style=for-the-badge

[zeversolar_local]: https://github.com/NECH2004/zeversolar_local
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/

