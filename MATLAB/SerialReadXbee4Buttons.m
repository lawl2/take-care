clc
clear all
close all
instrreset

if(exist('s1') == 1)
    fclose(s1)  
end

% if(exist('s2') == 1)
%     fclose(s2)
% end

seriallist
s1 = serial('COM6')  %era com11
s1.Baudrate = 115200
s1.Terminator = 'CR'
% 
% s2 = serial('COM11')
% s2.Baudrate = 9600
% s2.Terminator = 'CR'

%tic
fopen(s1)
fileID = fopen('serialread.txt','w');
byte = 0;

%infinite loop for reading serial comunications
s = 1;
while (s>0)
    %serial read
    %current date and time
    date = datestr(now);
    bufferRead = fread(s1,14);
    disp(bufferRead')
    %len = numel(bufferRead);
    %disp(i)
    %reading byte of interest
    byteDec = bufferRead(13);
    if(byteDec == 15)
        %no connection with VSS (GROUND)
        byte = 0;
    elseif(byteDec == 14)
        %I01 connected
        byte = 1;
    elseif(byteDec == 13)
        %I02 connected
        byte = 2;
    elseif(byteDec == 11)
        %I03 connected
        byte = 3;
    elseif(byteDec == 7)
        %I04 connected
        byte = 4;
    end
    fprintf(fileID,'Button pressed: %d   %s\n',byte,date);
end

fclose(s1)
delete(s1)
clear s1

% fclose(s2)
% delete(s2)
% clear s2
fclose(fileID)