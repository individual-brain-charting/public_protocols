function[resultname] = identification_batmotiv(taskName, subid, runname)
%% identification_batmotiv
%
% INPUTS
% taskName: name of task
% subid: subject number as a string
% runname: run/session name as a string
%
% OUTPUTS
% resultname: name of the main results folder
%
% script initially made by Nicolas Borderies, changed to function by
% Nicolas Clairis - february 2017.
% Sorry but I hate scripts in scripts, better use functions where you know inputs and ouputs.

% useless in my case => commented but may be useful again in the future
% if exist('subid') ~= 1
%     subid = input('subject identification number? ','s');
% end
% 
% if exist('nrun') ~= 1
%     nrun = input('run number ?');
% end
% 
% if exist('study.mat','file') == 2
%     load('study.mat');
% else
studyName = 'MBB_battery';
% end

resultname = strcat(studyName,'_',taskName,'_sub-',num2str(subid),'_run',runname);
clck = clock;
time = [num2str(clck(2)) '_' num2str(clck(3)) '_' num2str(clck(1)) '_' num2str(clck(4)) 'h' num2str(clck(5)) 'min' ];
resultname = [resultname '_' time];

end
