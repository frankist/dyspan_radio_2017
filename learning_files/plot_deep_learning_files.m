%%
current_file = which(mfilename);%('fullpath')
if isempty(current_file)
    current_file = matlab.desktop.editor.getActiveFilename;
end
[pathstr,name,ext] = fileparts(current_file);
cd([pathstr,'/'])
close all force;
clc;
dbstop if error
clear all;

%% file params
filepath = '../../generated_files/';
no_PU_filename = 'no_PU.bin';
PU_filename = 'PU_scenario_8.bin';%'PU_scenario_4_channel_0_2.bin';

%% params
sample_rate = 10e6;
Nch = 4;

img_size = [64,64];
Navg = 24;

%% Read file

fileID = fopen([filepath, PU_filename]);

while 1
    S = fread(fileID, [img_size(2), Navg*img_size(1)], 'float32').';%read_raw_float_data(fileID, img_size);
    if feof(fileID)
        break;
    end
    
    SdB_norm = preprocess_img(S);
    
    imagesc(SdB_norm);
    pause(0.01);
end

fclose(fileID);

function SdB_norm = preprocess_img(S)
target_dim = [size(S,2), size(S,2)];
n_avg = size(S,1)/size(S,2);

Simg = zeros(target_dim);
for i=1:n_avg
    Simg = Simg + S(i:n_avg:end,:);
end
SdB = 10*log10(Simg);

Smax = max(max(SdB));
Smin = min(min(SdB));
SdB_norm = (SdB-Smin)/(Smax-Smin);
end