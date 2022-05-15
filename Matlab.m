s = serial('COM6');
set(s,'BaudRate',230400);
s.InputBufferSize = 20000;
s.Terminator ='';
fopen(s);
s.Status
s.ReadAsyncMode = 'continuous';
fprintf(s,'conf s:10000;c:1;\n');

data = [];
for i=0:10
    data = [data fread(s)'];
    disp('.');
end
data = uint8(data);
if(length(findstr(data, 'StartUp!')) == 1)
    data = data(findstr(data, 'StartUp!')+10:end);
end




foundBeginingOfFrame = 0;
result = [];
for i=1:2:length(data)-1
    if(foundBeginingOfFrame==0)
        if(uint8(data(i))>127)
            foundBeginingOfFrame = 1;
            intout = uint16(uint16(bitand(uint8(data(i)),127)).*128);
            i = i+1;
            intout = intout + uint16(uint8(data(i)));
            result = [result intout];
        end
    else
        intout = uint16(uint16(bitand(uint8(data(i)),127)).*128);
        i = i+1;
        intout = intout +uint16( uint8(data(i)));
        result = [result intout];
    end
end
fclose(s);
delete(s);
clear s
plot(result);