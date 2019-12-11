%% Analyse fictive swim data
clear all; close all; clc;

%% Get directory information etc.
directory = '';
filename = ''.abf';
signal = readabf(fullfile(directory, filename));
signal = signal-mean(signal);
signal = detrend(signal);
plot(signal)
Fs = 20000; % Sampling frequency
omr_start = [10 30 60 80 110 130]; % second
omr_end = omr_start+10;
omr_start_idx = Fs*omr_start;
omr_end_idx = Fs*omr_end;

%% omr
sig1 = (signal(omr_start_idx(6):omr_end_idx(6)));
t1 =(omr_start_idx(6):omr_end_idx(6))*(1/20000); 
t1=t1';
figure(2)
plot(t1,sig1)
spk = detectspike(sig1, t1, 5, 10, 2);
hold on
plot(spk.tms, spk.amp, 'r.');
gdspk = selectspike(spk);
plot(gdspk.tms, gdspk.amp, 'g*');
save selectedspikes6R.mat gdspk
amplitude= [spk.amp];
amplitude = amplitude (amplitude>0);
mean_amplitude = mean(amplitude)
max_amplitude = max(amplitude)
%% Calculate instantaneous firing rate
load selectedspikes6R.mat
ifr = instantfr(gdspk.tms,t1);
figure(3)
hist(ifr);

%% burst detection
bi = burstinfo(gdspk.tms, 0.1, 200001); 
clf; hold on
plot(gdspk.tms, gdspk.amp / max(gdspk.amp), 'k.');
figure(4)
plot(bi.t_start, 1.1, 'r<');
plot(bi.t_end, 1.1, 'r>');
burst_start=[bi.t_start];
period=diff(burst_start);
freq= 1./period;
freq_corrected=freq(freq<80 & freq>20);
tbf_2=mean(freq_corrected)
max_tbf = max(freq_corrected)
burst_duration=[bi.dur]*1000 % in ms
bout_number = length(bi.t_start)
spikes_per_burst = [bi. n]
