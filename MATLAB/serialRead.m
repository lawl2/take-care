clc
if(exist('s') ==1)
    fclose(s)  
end
clear all
close all

seriallist
s = serial('COM9')
s.Baudrate = 9600
s.Terminator = 'CR'

tic
fopen(s)
fileID = fopen('serialread.txt','w');
str = ''; %total string
str2 = ''; %partial string

while (toc < 20)
    %serial read
    serial = fscanf(s);
    pause(10)
end

%writing on str
str = sprintf('%s',serial)
%find index of '@'
index = strfind(str,'@');
%save the target string
str2 = str(index + 1:index + 26)

fprintf(s,'serial')
fprintf(fileID,'This is the target string: %s',str2)
fclose(s)
fclose(fileID)
