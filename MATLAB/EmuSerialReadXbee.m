clc
clear all
close all
instrreset

if(exist('s1') ==1)
    fclose(s1)  
end
%{
if(exist('s2') == 1)
    fclose(s2)
end
%}

seriallist
s1 = serial('COM7')
s1.Baudrate = 9600
s1.Terminator = 'CR'

%{
s2 = serial('COM11')
s2.Baudrate = 9600
s2.Terminator = 'CR'
%}
tic
fopen(s1)
%fopen(s2)

fileID = fopen('serialread.txt','w');

%serial read
for i= 0:10
    serial = fscanf(s1)
    pause(1)
    fprintf(fileID,'%s\n',serial);
    %lenght of string serial
    len = numel(serial);
    byte = [serial(len - 4),serial(len-5)]
end


%fprintf(s1,'serial');
%fprintf(fileID,'This is the target string: %s',str2)

fclose(s1)
delete(s1)
clear s1
%{
fclose(s2)
delete(s2)
clear s2
fclose(fileID)
%}