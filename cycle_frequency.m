clear all; close all; clc;

directory = '';
signal = readabf(fullfile(directory, ''.abf')); % Ephys signal to analyze.

figure
plot(signal)


Fs = 20000; % Sampling frequency

omr_start = [10 30 60 80 110 130]; % seconds
omr_end = omr_start+10;
omr_start_idx = Fs*omr_start;
omr_end_idx = Fs*omr_end;



% FFT per segment
    
    sig = signal(omr_start_idx(6):omr_end_idx(6));
    figure
    plot(sig)
    signal_centred=sig-mean(sig);%zero centered
    signal_detrend=detrend(signal_centred);%detrend

    time=(omr_start_idx(6):omr_end_idx(6))*(1/20000);
    b=medfilt1(signal_detrend,10,Fs);
    %b=medfilt1(sig,100,Fs);
    
    
    y=highpass(b,10,Fs);% remove low freq oscillation
    
    l = length(y);
    figure
    plot(time,sig);hold on; plot(time,y); plot(time,b)
    
    lpad=2*length(y);%zero padding
    
    sig_fft = fft(y,lpad);
    sig_fft = sig_fft(1:lpad/2+1);
    sig_fft=sig_fft/length(y);
    sig_fft(2:end-1) = 2*sig_fft(2:end-1);
    power =abs(sig_fft).^2/l; 
  
    %frequency = (0:l-1)*(Fs/l);
    frequency= 0:Fs/length(y):Fs/2;
    figure
    plot(frequency(150:1000),power(150:1000))
    
     
    title('Spectral Analysis - Fourier Transform');
    xlabel('Frequency (Hz)');
    ylabel('Power');
    set(gca, 'XScale', 'log');
     
    %get peak frequency
    [~,loc]=max(power);
    Freq_estimate=frequency(loc)


