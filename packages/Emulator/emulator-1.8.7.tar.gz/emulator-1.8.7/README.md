<img src="https://github.com/futurehomeno/Emulator/blob/master/docs/emulator.PNG" height="50%" width="100%">

# Emulator

Emulator is a web application used for creating fake IoT devices for testing. It is written in Python and uses Flask micro web framework.
<br/>
Currently, the application supoorts only a few ZWave devices such as a smoke alarm, flood sensor, dimmer, an LED light bulb, a motion sensor and a switch. 
<br/>
## Workflow:
The web pages use javascript, html and css to render the front-end and backend functionality. The emulator acts as both a mobile/web application used to control and get stats of devices from the core, and also as the devices themselves. This combines two different pathways as shown in the figure below.

![alt text](https://github.com/futurehomeno/emulator/blob/master/docs/SystemOverview.png)

* When a device is added, 
  * the device is given a random id which is generated using the Math.random() function
  * its inclusion report is generated having the device id as the device address and service as ```emul``` for emulator
  * the generated inclusion report is published to the core
  * the inclusion report of the device is stored locally to update the properties of the device in the properties panel

* When an added device is clicked,
  * the device id is sent to the backend to retrieve the properties of the device
  * the properties of the device is extracted from the json dump and is dynamically loaded to the frontend

* When properties of a device is modified,
  * the properties are sent to the backend with the device id 
  * the properties of the device is updated to incorporate the changes in the local file
  * if any alarms or sensors are set, a trigger report is generated
  * the trigger report is published to the core as a FIMP message over MQTT

* When a device is removed,
  * the device id is sent to the backend to remove the device 
  * the device properties is retrieved and removed from the local file having all added devices
  * an exclusion report is generated for the device with its device id
  * the exclusion report is published to the core to remove the device

## New features
* An evt.state.report is generated when the device is switched on/off. Now, the added device has to be switched on to generate an UP event, after which any service or sensor modified or added will generate an event. The device cannot generate any event if it is in a DOWN state which is the switched off state.

* AC/FLiR devices can be pinged at anytime and an evt.ping.report is generated with their status. This facility is now available in the emulator. While AC devices have power source as AC and wakeup interval set to -1, FLiR devices are battery powered and have their power source set to battery, but since they need to be awake for any event at any time, their wakeup interval is -1. This is the major difference between AC and FLiR devices. And hence, FLiR devices are used for critical applications such as for smoke sensors and door locks.

* Battery devices have a wakeup interval set to some value which is usually in seconds. Every 'wakeup interval' seconds, the battery devices send an 'I'm alive' report having their status and battery level. Now, in the emulator, this wakeup interval is a configurable parameter and the battery device reports can be analyzed.

Thus, this workflow explains the app and device characteristics embedded in the single interface of the emulator.

## Dependencies:

* This application is developed in python3.6 and needs pip3 to install it. Please check the versions and install the application. 
* Since the application is developed in Flask, the main dependency is to have Flask installed. 
* The application is dependent on MQTT to publish appropriate messages to the core when a device comes up (switching on the device) and alarms or sensor values are set. Please check is MQTT broker is running using ```ps -ef | grep mosquitto```

## Example of using the application:
Install the python repository ```emulator``` using ```pip3 install emulator``` and from the python shell, enter,

```
from emulator.views import main
main()
```

This starts the web application waiting for requests to send the appropriate response. In a web browser, open localhost:5000 since emulator listens at port 5000. 
<br/>
<br/>
There are two panes in the frontend - one for the available devices to add, and the other to display added devices. The whole workflow of using the emulator is explained below by using a fire alarm trigger as an example. Click on a device in the right pane to add it to the left pane.

![alt text](https://github.com/futurehomeno/Emulator/blob/master/docs/emulator%20main%20page.PNG)

When the device is added, it is displayed in the left pane as a faded image. 

![alt text](https://github.com/futurehomeno/Emulator/blob/master/docs/smoke%20sensor.PNG)

Click on the faded device in the left pane to display the properties. Switch on the device and select the alarms or enter values for sensors and click ok. 

![alt text](https://github.com/futurehomeno/Emulator/blob/master/docs/smoke%20sensor%20properties.PNG)

For alarms selected, a message will be sent to the core to set the alarms, and for sensor values, a message will be sent to the core to set the value of sensors for that device. 

![alt text](https://github.com/futurehomeno/Emulator/blob/master/docs/smoke.PNG)

The alarm in vinculum/core can be seen to be set. 

![alt text](https://github.com/futurehomeno/Emulator/blob/master/docs/smoke%20alarm%20in%20vinculum.PNG)

## Tests:
The emulator has inclusion reports from actual devices as a reference to generate appropriate inclusion reports for the devices since it is highly important for the correct interfaces and topics to be present, both in the inclusion reports and trigger reports and for them to match precisely for an event to be generated. 
<br/>
<br/>
The following devices are supported by the emulator presently:
* Smart switch
* Smoke sensor
* Flood sensor
* Motion sensor
* LED bulb
* Dimmer
* Door lock
* Window strips
* Climax smoke sensor
<br/>
<br/>

## Files:
The application needs the following files:
* images of all the supported devices
* inclusion reports of all supported devices
<br/>
The application generates the following files:
* selected_devices.json - has all the added devices
* log.log if the debug option is set to true - this is not applicable for releases
