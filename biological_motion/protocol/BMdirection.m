function BMdirection(subjectname, runnum, runtype)

%e.g., BMdirection('TEST', 1, 1)

% 12 mini blocks per run, (see below) each consisting of four main block
% types repeated 3 times.  Must run both run types to acquire complete set.
 
%runtypes:  1 IdealCutting/BMLscramble  x   Upright/Inverted
%           2 BMLscramble/Modifiedscramble x Upright/Inverted


%% INITIALIZATION

load walkerdata.mat;

nd = 0; %place holder; for scrambled mask, change mmultiply; for linear mask, change in pptwalk
dotsize=6;%6;
leng=.5;
iti=1.5; % this will actually be used to wait for fixed response period.  Currently essentially the isi.
trans=0;
mix=0;
mmultiply = 1; % takes care of number scrambled walkers in mask. Linear mask (if used) currently set at 1*nwalkerdots
fc=[1 1];
clc

%% GENERATE TEST TRIALS

% Create trials
if runtype == 1
    blocks = [2 4 5 7 2 4 5 7 2 4 5 7];
elseif runtype == 2
    blocks = Shuffle([5 7 6 8 5 7 6 8 5 7 6 8]);
end

alltrials = GenerateBlocks(blocks);

% Check if we're at the scanner or in the lab
valid=0; 
while (valid==0);
    user_entry = input('Are we at the Scanner? (y/n)', 's');
    if(user_entry == 'y')
        disp('We are scanning!');
        pause(1);
        test = 0;
        valid=1;
    elseif (user_entry == 'n')
        disp('In the lab');
        pause(1);
        test = 1;
        valid=1;
    else
        disp('Press y or n!');
        finish;
    end    
end

% Run trials
alltrials = RunTrials(alltrials, walkerdata, iti, trans, fc, mmultiply, nd, dotsize, leng, test);

% Prep Data File
Dat.SubjectID = subjectname;
Dat.BlockCond = blocks;
Dat.RunType = runtype;
Dat.RunNum = runnum;
Dat.Trials = alltrials;
Dat.StimulusDuration = leng;
Dat.StimulusDistance = 98; %cm %% please change accordingly

err = CreateDataFile(Dat);

clear trials

