%% Create Serial Port Object
% This example shows how to create a serial port object.

% Copyright 2018 The MathWorks, Inc.

%% Find available serial ports.
% Use the seriallist function to find your available serial ports.
seriallist
%% Create a serial port object and assign port.
% This example creates the serial port object s and associates it with the serial port COM1. You must specify the port as the first argument to create a serial port object.  
s = serial('COM4')
%% Create a serial port object and specify properties.
% This example creates the serial port object s2, associated with the serial port COM3, and sets properties. You can optionally set communication properties by specifying name-value pairs during object creation, after the port argument. This example sets the baud rate to 4800 and the terminator to CR. You can see these values in the object output.      
s2 = serial('COM3','BaudRate',8800,'Terminator','CR')
