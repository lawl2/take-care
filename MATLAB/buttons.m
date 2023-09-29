
    . . .

% --- Executes on button press in OPEN.
function OPEN_Callback(hObject, eventdata, handles)
% hObject    handle to OPEN (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    serial = handles.serial
    fwrite(serial,'O')
    
% --- Executes on button press in CLOSE.
function CLOSE_Callback(hObject, eventdata, handles)
% hObject    handle to CLOSE (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    serial = handles.serial;
    fwrite(serial,'C');
    
% --- Executes on button press in CONNECT.
function CONNECT_Callback(hObject, eventdata, handles)
% hObject    handle to CONNECT (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

 instrreset
    
 if(exist('s1') == 1)
        fclose(s1)  
 end

 seriallist

 s1 = serial('COM7')
 port = get(handles.port,'String')
 baudrate = str2double(get(handles.baudrate,'String'))
 s1 = serial(port)
 s1.Baudrate = baudrate
 s1.Terminator = 'CR'
    
 fopen(s1)
 handles.serial = s1

 guidata(hObject,handles)

% --- Executes on button press in DISCONNECT.
function DISCONNECT_Callback(hObject, eventdata, handles)
% hObject    handle to DISCONNECT (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

serial = handles.serial
fclose(serial)
delete(serial)
clear serial
seriallist

       . . .
       
       