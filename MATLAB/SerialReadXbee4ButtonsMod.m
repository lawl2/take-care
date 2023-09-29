clc
clear all
close all
instrreset

%controlling and opening connection
if(exist('s1') == 1)
    fclose(s1)  
end

seriallist
s1 = serial('COM7')  %era com11
s1.Baudrate = 115200
s1.Terminator = 'CR'

fopen(s1)
fileID = fopen('serialread.txt','w');

%defining the torque
torqueDetect = 0;

%infinite loop for reading serial communications
s = 1;
while (s>0)
    %serial read
    %current date and time
    date = datestr(now);
    bufferRead = fread(s1,1);
    
    disp(bufferRead')
    
    %reading byte of interest
    if(bufferRead(1) == 69)
        %open button
        fprintf(fileID,'Button pressed: E   %s\n',date);
    elseif(bufferRead(1) == 68)
        %close button
        fprintf(fileID,'Button pressed: D   %s\n',date);
    elseif(bufferRead(1) == 84)
        %contact detected Torque Mode
        fprintf(fileID, 'Contact detected      %s\n',date);
        torqueDetect = 1
        k = 1;
    else
        %no button pressed
        fprintf(fileID, 'No button pressed    %s\n',date);
    end
    
    %calculating and showing the load
    
    if(torqueDetect == 1)
        tString(k) = bufferRead(1) - 48
        k = k + 1
    end
end

fclose(s1)
delete(s1)
clear s1

fclose(fileID)
%% 
k=1
len = size(tString,2);
for j=1:len-1
    array(j)=tString(j+1)
    j=j+1
end%% 
for k=1:len-1
    if array(k) > 11
        array(k)=0
    end
    k=k+1
end

len1=size(array,2)
len2=mod(len1,5)
len1=len1-len2
%
for h=1:len1
    array2(h)=array(h)
end

%
c=num2cell(reshape(array2,5,(len1)/5),1)
%
length(c)
for i=1:length(c)
    load(i)=c{i}(1)*1000+c{i}(2)*100+c{i}(3)*10+c{i}(4)
    i=i+1
end
plot(load)