 Embedded Synchronization System
======
## A prototypical IoT system that follows the Device-Gateway-Cloud model
* Two mbed Freedom Development Platforms (FRDM-KL46Z) used as the Device
* Raspberry Pi used as a gateway to synchronize the two mbeds with NTP time
* Cloud based backend using MongoDB to store the sensing for web display and actuation

#### Screenshot
![Screenshot](/assets/screenshots/ss1.png)
## Getting Started

### Installation
* Install the code in /src/device onto the mbed
* Run the code in /src/gateway on a Raspberry Pi
* Upload the files in /src/cloud onto the web

## Contributors

### Contributors on GitHub
* [Anthony Nguyen](https://github.com/resolutedreamer)
* [Jeremy Haugen](https://github.com/jeremyhaugen)
* [Linyi Xia]()

### Third party libraries
*  [thingspeak](https://github.com/iobridge/ThingSpeak)

## License 
* This project is licensed under the Apache License - see the [LICENSE](https://github.com/resolutedreamer/prototypical-iot/blob/master/LICENSE) file for details

## Version 
* Version 1.0

## Contact
#### Anthony Nguyen
* Homepage: www.resolutedreamer.com

Last Updated 2014/12/17
