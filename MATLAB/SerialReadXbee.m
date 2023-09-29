clc
clear all
close all
instrreset

if(exist('s1') == 1)
    fclose(s1)  
end

if(exist('s2') == 1)
    fclose(s2)
end


seriallist
s1 = serial('COM10')
s1.Baudrate = 9600
s1.Terminator = 'CR'
% 
% s2 = serial('COM11')
% s2.Baudrate = 9600
% s2.Terminator = 'CR'

tic
fopen(s1)
%fileID = fopen('serialread.txt','w');

%infinite loop for reading serial comunications
s = 1;
while (s>0)
    %serial read
    %for i= 0:1
        %disp(i)
        bufferRead = fread(s1);
        disp(bufferRead')
        %fprintf(fileID,'%d\n',string);
        %lenght of string serial
        len = numel(bufferRead);
        byteDec = bufferRead(len-1);
        if(byteDec == 16)
            %normally is HIGH (16 in HEX is 10) no connection with VSS
            byte = 1
        %is LOW (00 in HEX is 00)
        else
            byte = 0
        end
    %end
end

fclose(s1)
delete(s1)
clear s1

% fclose(s2)
% delete(s2)
% clear s2
%fclose(fileID)
