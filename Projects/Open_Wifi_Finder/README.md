## **GrovePi Open Wifi Finder**




GrovePi is an open source platform for connecting Grove Sensors to the Raspberry Pi.  Create your Internet of Things devices and inventions without the need for soldering!
![Picture](GrovePi_Plus_By_Dexter_Industries_For_the_Raspberry_Pi.JPG)

 Scan for open wifi networks!  This is a portable wifi hotspot finder.  See our project at www.dexterindustries.com/GrovePi for more information on turning this into a portable wifi hotspot finder.

### How Does it Work?
The GrovePi board slips over the Raspberry Pi.  Connect the Grove Sensors to the GrovePi board.  


 Software Setup Notes:
 	* This example uses https://wifi.readthedocs.org/en/latest/wifi_command.html.  Install with pip install wifi
 	* Wifi dongle must be on wlan0 ; Check this with the command "ifconfig" on the command line.
 Hardware Setup Notes:
 	* Buzzer goes on port 8 of the GrovePi.
 	* LED Goes on port 4 of the GrovePi.
 	* The LCD goes on I2C-1.  Check this with the command "sudo i2cdetect -y 1"

 The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi

 Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi

 LICENSE: 
 These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.


### Raspberry Pi Compatibility
The GrovePi is compatible with the Raspberry Pi models A, A+, B, B+, and 2.

### Programming the GrovePi
The GrovePi can be programmed in Python, C, C#, Go, and NodeJS on the Raspberry Pi.  Simply start with one of our [example projects](http://www.dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/) or [example code](https://github.com/DexterInd/GrovePi/tree/master/Software).  
The GrovePi uses an Arduino to interface between the Raspberry Pi and the Grove Sensors, and comes programmed with a standard firmware.  The firmware can be rewritten from the Raspberry Pi.  

### Getting Help
Need help? We [have a forum here where you can ask questions or make suggestions](http://www.dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/).

These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

See more at the [GrovePi Site](http://dexterindustries.com/GrovePi/)
