clear all
close all
cd c:\urvashi\Secondary;
load_data
fig = figure;
omr1_begin = 10;
omr1_end = 20;
omr2_begin = 30;
omr2_end = 40;
charge = [];
idx1 = (omr1_begin-2)/samplingInt;
idx2 = (omr1_end+2)/samplingInt;
idx3 = (omr2_begin-2)/samplingInt;
idx4 = (omr2_end+2)/samplingInt;
filename = [file(1:8),'.txt']
%first analyse 10s to 20s
for i = 1:3
    plot(timeAxis(idx1:idx2), data(idx1:idx2,i));
    dcm_obj = datacursormode(fig);
    set(dcm_obj,'DisplayStyle','datatip',...
    'SnapToDataVertex','off','Enable','on')
    disp('Click on a point, then press Return.')
    pause 
    base_strt = getCursorInfo(dcm_obj);
    disp('Click on a point, then press Return.')
    pause     
    base_end = getCursorInfo(dcm_obj);
    x = [base_strt.Position(1), base_end.Position(1)]
    y = [base_strt.Position(2), base_end.Position(2)]
    p = polyfit(x,y,1)
    bias = polyval(p, timeAxis)';
    adj_data = data(:,i)-bias;
    t = timeAxis((omr1_begin/samplingInt):(omr1_end/samplingInt));
    SynCurr = adj_data((omr1_begin/samplingInt):(omr1_end/samplingInt));
    plot(t, SynCurr)
    charge(i) = trapz(t, SynCurr)
    dlmwrite(filename, charge(i), '-append', 'delimiter', '\t');
end  
disp('now analysing second omr epoch')
%next analyse 30s to 40s
for j = 1:3
    plot(timeAxis(idx3:idx4), data(idx3:idx4,j));
    dcm_obj = datacursormode(fig);
    set(dcm_obj,'DisplayStyle','datatip',...
    'SnapToDataVertex','off','Enable','on')
    disp('Click on a point, then press Return.')
    pause 
    base_strt = getCursorInfo(dcm_obj);
    disp('Click on a point, then press Return.')
    pause     
    base_end = getCursorInfo(dcm_obj);
    x = [base_strt.Position(1), base_end.Position(1)]
    y = [base_strt.Position(2), base_end.Position(2)]
    p = polyfit(x,y,1)
    bias = polyval(p, timeAxis)';
    adj_data = data(:,j)-bias;
    t = timeAxis((omr2_begin/samplingInt):(omr2_end/samplingInt));
    SynCurr = adj_data((omr2_begin/samplingInt):(omr2_end/samplingInt));
    plot(t, SynCurr)
    charge(j)= trapz(t, SynCurr)
    dlmwrite(filename, charge(j), '-append','delimiter', '\t');
end
close
