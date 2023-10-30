# Itho RFT integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

**_!!! This integration is in an early stage of development so use at your own risk and contributions are welcome. !!!_**

**_!!! This integration implements the Itho RFT AUTO (536-0150) remote. Support for other remotes can be added if requested. !!!_**

**_!!! This integration is tested with an Itho HRU ECO300 unit paired to a Itho RFT CO2 sensor. The implemented remote is the Itho RFT AUTO (536-0150). !!!_**

_Home Assistant custom-integration that integrate with the [pyIthoRFT][pyIthoRFT] library._

## Hardware
This integration requires a [evofw3][evofw3] gateway running version 0.7.1. This repository contains links and instructions how to obtain/build a gateway.

I've created my own €16,- gateway including shipping using the following components:
* [Arduino Pro Micro 3.3V 8MHz][microcontroller]
* [EBYTE E07-900M10S][radio]
* [868Mhz 3dBi][antenna]

_TODO: add pictures/description_

## Installation

### Add haIthoRFT as HACS custom repository
* Select HACS (side panel), Integrations.
* Select the three-dots menu on the top-right, select Custom repositories.
* Add the repo URL (https://github.com/GraceGRD/pyIthoRFT), Category is Integration.
* Click the Add button, and close the window (X in top-right).

### Add Itho RFT as integration to Home Assistant
* Select HACS (side panel), Integrations.
* Select Explore & Download Repositories button.
* Search for 'Itho RFT' and select the repository.
* Install the repository by clicking download and confirm.
* Restart Home Assistant (the HA Core)

## Configuration is done in the UI
1. Configure the gateway port e.g. _/dev/ttyACM0_ and press SUBMIT. Under the hood the communication with the gateway is checked. <br/><br/><img src="image/menu_gateway.PNG" alt="drawing" width="300"/><br/><br/>
2. Choose pairing method: <br/> - Automatic pairing randomly generates the remote address which is then used for pairing. <br/> - Manually pairing requires a remote and a unit address. This can be used to re-configure a paired remote, or copy a physical remote. <br/><br/><img src="image/menu_pairing_method.PNG" alt="drawing" width="300"/><br/><br/>
3. Provide the Remote and Unit address in manual pairing mode and press SUBMIT. <br/><br/>
<img src="image/menu_pair_manually.PNG" alt="drawing" width="300"/><br/><br/>
4. Put the unit in pairing mode as described in the manual then press SUBMIT to start the pairing process. <br/><br/>
<img src="image/menu_pair_automatically.PNG" alt="drawing" width="300"/><br/><br/>
5. When pairing succeeded (manual or automatic pairing) the following message should pop up showing the port, remote and unit address. <br/><br/>
<img src="image/menu_pair_success.PNG" alt="drawing" width="300"/><br/><br/>

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***
[pyIthoRFT]: https://github.com/GraceGRD/pyIthoRFT

[evofw3]: https://github.com/ghoti57/evofw3

[releases]: https://github.com/GraceGRD/haIthoRFT/releases
[releases-shield]: https://img.shields.io/github/release/GraceGRD/haIthoRFT.svg?style=for-the-badge
[commits]: https://github.com/GraceGRD/haIthoRFT/commits/main
[commits-shield]: https://img.shields.io/github/commit-activity/y/GraceGRD/haIthoRFT.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/GraceGRD/haIthoRFT.svg?style=for-the-badge

[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[hacs]: https://github.com/hacs/integration
[maintenance-shield]: https://img.shields.io/badge/maintainer-GraceGRD-blue.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/gracegrd
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge

[forum]: https://community.home-assistant.io/
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[microcontroller]: https://nl.aliexpress.com/item/1871481789.html?spm=a2g0o.order_list.order_list_main.21.328179d2nZw4P1&gatewayAdapt=glo2nld
[radio]: https://nl.aliexpress.com/item/1005004753129118.html?spm=a2g0o.order_list.order_list_main.56.328179d2nZw4P1&gatewayAdapt=glo2nld
[antenna]: https://nl.aliexpress.com/item/1005002835673674.html?spm=a2g0o.order_list.order_list_main.55.328179d2nZw4P1&gatewayAdapt=glo2nld
