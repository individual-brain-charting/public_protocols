function [session,condition,onset,duration] = specif_model_saccadeslents(rootdir, sub)
%Returns paradigm details (about events to be modelled) from subject for
% whose directory is 'rootdir'.
%
% This function is being called by lcogn_single_firstlevel.m during
% 'model specification' or  'contrasts specification'.
%
% The outputs that this function must provide are:
%  o session  : vector providing, for each trial, the session (integer number)
%  o condition: vector providing, for each trial, the experimental condition (integer number) 
%  o onset    : vector providing, for each trial, the onset time (number of milliseconds 
%               elapsed from the start of the session)
%  o duration : vector providing, for each trial, its duration (in milliseconds)

%-Read subject-specific data from E-prime
%-----------------------------------------------------------------------
%rootdir  = spm_select('CPath', fullfile('..','..'), pwd);
% s = regexp(rootdir,'([/\\]?)([a-z_A-Z0-9_\-]*)([/\\]?)','tokens');
% excelfile = spm_select('CPath',[s{end}{2} '.xls'],fullfile(rootdir,'excel'));
% 
% runs = getnumdatafromexcel(excelfile,'ListOfRuns');

%-
%-----------------------------------------------------------------------
clear session;
clear condition;
clear onset;
clear duration; 
clear begin;
clear onset;

nses = 2;

%%%% read subject-specific data from E-prime
warning OFF;
s=sprintf('%s_SaccadesLents_Excel.xls',sub);
excelfile = fullfile(rootdir,('..'),'Excel',s)
[datanum,datatext]=xlsread(excelfile);

%%% find the cycle number
f=find(strcmp(datatext,'ListOfRuns.Sample'));
[a,b]=ind2sub(size(datatext),f(1));
session=datanum(:,b-1);

%%% get the positions and compute the directions of the eye movements
f=find(strcmp(datatext,'SaccadeDirection'));  %%% X location of the target
[a,b]=ind2sub(size(datatext),f(1));
SaccadeDirection=datatext(2:length(datatext),b);

%%% find the type of trial (here called condition for experimental condition)  
%%% using directions from e-prime, but the exact data could be used 

condition = zeros(length(SaccadeDirection),1);
sel = (strcmp(SaccadeDirection,'Right')); %%%rightward saccade
condition(sel)=1;
sel = (strcmp(SaccadeDirection,'Left')); %%%leftward saccade
condition(sel)=2;

%%% find the beginning of the block
f=find(strcmp(datatext,'Fixation.OnsetTime'));  %%% beginning of the block
[a,b]=ind2sub(size(datatext),f(1));
begin=datanum(:,b-1);

%%% find the onset of the trials
f=find(strcmp(datatext,'SaccadeTarget1.OnsetTime'));  %%% onset of the target
[a,b]=ind2sub(size(datatext),f(1));
onset=datanum(:,b-1);
onset = onset - begin;

%%% set the duration of the trials
f=find(strcmp(datatext,'TargetDuration'));  %%% onset of the target
[a,b]=ind2sub(size(datatext),f(1));
duration=datanum(:,b-1);