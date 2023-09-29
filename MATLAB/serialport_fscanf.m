clear all;
close all;
clc
instrreset
s2=serial('COM7','BaudRate',115200)
fopen(s2)

%% 
array=uint8.empty
i=1
while i<200
flushinput(s2)
flushinput(s2)
%data=fscanf(s2,'%u',3)
data1= fread(s2,3,'uint8')
%array(i)=data
i=i+1
pause(0.1)
end
%% 

fclose(s2)
delete(s2)