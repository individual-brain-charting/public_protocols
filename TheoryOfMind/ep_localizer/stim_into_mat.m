%% This script converts the input txt files into mat files
%%
%% Author: Ana Luisa Pinho
%% e-mails: ana.pinho@inria.fr
%%
%% =======================================================

inputs_type = cellstr(["EP"; "PP"]);

%inputs_folder = "stimuli_french_ansi";
inputs_folder = "training_sess_french_ansi";

%inputs_prefix = "stories_";
inputs_prefix = "stories_ts_";

for i = 1:2

  inputs = strcat(inputs_folder,"/",inputs_prefix, inputs_type(i), ".txt");
  fid = fopen(inputs{});

  if i == 1
    EP = cell();
    while ~feof(fid)
      tline = fgetl(fid);
      EP = [EP tline];
    end
    %save([inputs_folder '/EP.mat'], 'EP');
    save([inputs_folder '/EP_ts.mat'], 'EP');
    %save EP.mat EP;
  elseif i == 2
    PP = cell();
    while ~feof(fid)
      tline = fgetl(fid);
      PP = [PP tline];
    end
    %save([inputs_folder '/PP.mat'], 'PP');
    save([inputs_folder '/PP_ts.mat'], 'PP');
    %save PP.mat PP;
  endif

end