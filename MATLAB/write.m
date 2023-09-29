clc
clear all
close all
instrreset

if(exist('s1') == 1)
    fclose(s1)  
end

seriallist
s1 = serial('COM11')
s1.Baudrate = 9600
s1.Terminator = 'CR'

fopen(s1)
%creation of frame
frame = [hex2dec('7E') hex2dec('00') hex2dec('10') hex2dec('17') hex2dec('01') hex2dec('00') hex2dec('13') hex2dec('A2') hex2dec('00') hex2dec('41') hex2dec('53') hex2dec('13') hex2dec('46') hex2dec('FF') hex2dec('FE') hex2dec('02') hex2dec('44') hex2dec('30') hex2dec('05') hex2dec('CD')]

%for cycle for sending frame
for(i = 1:20)
    frame(i);
    %sending single byte
    fwrite(s1,frame(i))
end
%bufferRead = fread(s1);
%disp(bufferRead')

fclose(s1)
delete(s1)
clear s1
