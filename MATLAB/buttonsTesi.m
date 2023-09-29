...
% --- Executes on button press in Button1High.
function Button1High_Callback(hObject, eventdata, handles)
% hObject    handle to Button1High (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    instrreset
    
    if(exist('s1') == 1)
        fclose(s1)  
    end

    seriallist

    s1 = serial('COM5')
    s1.Baudrate = 9600
    s1.Terminator = 'CR'
    
    fopen(s1)
    
    frame = [hex2dec('7E') hex2dec('00') hex2dec('10') hex2dec('17') hex2dec('01') hex2dec('00') hex2dec('13') hex2dec('A2') hex2dec('00') hex2dec('41') hex2dec('53') hex2dec('13') hex2dec('46') hex2dec('FF') hex2dec('FE') hex2dec('02') hex2dec('44') hex2dec('30') hex2dec('05') hex2dec('CD')]

    %for cycle for sending frame
    for(i = 1:20)
        frame(i);
        %sending single byte
        fwrite(s1,frame(i))
    end
    
    fclose(s1)
    delete(s1)
    clear s1
    
...

% --- Executes on button press in Button1Low.
function Button1Low_Callback(hObject, eventdata, handles)
% hObject    handle to Button1Low (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    instrreset
    
    if(exist('s1') == 1)
        fclose(s1)  
    end

    seriallist

    s1 = serial('COM5')
    s1.Baudrate = 9600
    s1.Terminator = 'CR'
    
    fopen(s1)
    
    frame = [hex2dec('7E') hex2dec('00') hex2dec('10') hex2dec('17') hex2dec('01') hex2dec('00') hex2dec('13') hex2dec('A2') hex2dec('00') hex2dec('41') hex2dec('53') hex2dec('13') hex2dec('46') hex2dec('FF') hex2dec('FE') hex2dec('02') hex2dec('44') hex2dec('30') hex2dec('04') hex2dec('CE')]

    %for cycle for sending frame
    for(i = 1:20)
        frame(i);
        %sending single byte
        fwrite(s1,frame(i))
    end
    
    fclose(s1)
    delete(s1)
    clear s1

