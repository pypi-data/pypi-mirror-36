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

* The added device has to be switched on in order to generate an UP event, after which any service or sensor modified or added will generate an event. The device cannot generate any event if it is in a DOWN state which is the switched off state.

Thus, this workflow explains the app and device characteristics embedded in the single interface of the emulator.

## Dependencies:

* Since the application is developed in Flask, the main dependency is to have Flask installed. 
* The application is dependent on MQTT to publish appropriate messages to the core when a device comes up (switching on the device) and alarms or sensor values are set. 

## Example of using the application:
Install the python repository ```emulator``` using ```pip install emulator``` and from the python shell, enter,

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
<br/>
<br/>
Support for the following devices will be added soon:
* Climax smoke sensor

The emulator doesn't support battery events yet, though the UI options are there. It will be added soon.

## Files:
The application needs the following files:
* images of all the supported devices
* inclusion reports of all supported devices
<br/>
The application generates the following files:
* selected_devices.json - has all the added devices
* log.log if the debug option is set to true - this is not applicable for releases
