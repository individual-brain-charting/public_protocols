function[root, resultdir, subdir, behaviordir, fMRIScansDir] = setDir(subid, IRM)
% setDir
% function which creates different results folders.
% INPUTS:
% subid: string indicating subject number
% IRM: indicate whether fMRI run (1) or not (0)
% If yes, also creates a folder to store fMRI data
%
% OUPUT
% root: folder from script was launched
% resultdir: big results folder where all subjects data will be stored
% subdir: subject folder where data will be stored for this particular
% subject
% behaviordir: folder with behavioral data for this subject (store all
% behavioral data of all tasks here)
% fMRIScansDir: folder where fMRI data should be stored if IRM = 1
%
% script initially made by Battery people (Nicolas Borderies?) and
% re-adapted as a function by Nicolas Clairis - february 2017

root = pwd;
% create global results folder for all subjects
%resultdir = [root '\resultats'];
resultdir = [root filesep 'results'];
if exist(resultdir,'dir') ~= 7
    mkdir(resultdir)
end
% create folder for the current subject
subdir = [resultdir [filesep 'sub-' subid]];
if exist(subdir,'dir') ~= 7
    mkdir(subdir);
end
% create behavior folder for current subject to store behavioral data
behaviordir = [subdir, filesep 'behavior'];
if exist(behaviordir,'dir') ~= 7
    mkdir(behaviordir);
end
% create fMRI folder for current subject if task made in the fMRI
if IRM == 1
    fMRIScansDir = [subdir, filesep 'fMRI_scans'];
    if exist(fMRIScansDir,'dir') ~= 7
        mkdir(fMRIScansDir);
    end
else
    fMRIScansDir = '';
end

disp(subdir);

end