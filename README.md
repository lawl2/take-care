# Take Care:  an IoT system for sensitive material transport

The aim of the project is to create a monitoring system for sensble material transport to avoid economic damages but also dispersion of these materials.

## Arduino system

 The Arduino system is defined by a thermistor and a level sensor plus two actuators simulating the fridge and possible problems due to liquid dispersion. There is also a LCD monitor signaling possible problems and the material temeprature. The communication is the standard UART.
 
![image](https://github.com/lawl2/take-care/assets/105045290/d393f3c5-828e-49c8-9e30-e3558f5a1933)

## Bridge

![image](https://github.com/lawl2/take-care/assets/105045290/caab2918-5520-4599-ae1e-b916eb36f47e)

Adafruit is used to send and receives data from arduino system.

## Telegram

There's the developpment of a telegram bot which enables the system to keep messages to the driver when there are any possible problem

![image](https://github.com/lawl2/take-care/assets/105045290/b0b8a36c-fd20-4252-8429-4358c1591594)
![image](https://github.com/lawl2/take-care/assets/105045290/cfe80d4c-c573-4ce2-9047-315db95749a1)

## K-means

the Machine Learning algorithm K-means is used to recognize different kinds of material using color codes. 

![image](https://github.com/lawl2/take-care/assets/105045290/54608b98-ee60-4d54-ac14-5f492f444d0e)
![image](https://github.com/lawl2/take-care/assets/105045290/9d98763b-ce88-48dc-9841-a1e2415729d1)

## The overall system

![image](https://github.com/lawl2/take-care/assets/105045290/6c05a789-6d39-480c-b5cd-cb54aba1d489)
