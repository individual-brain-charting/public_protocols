clear%% 

% Abstraction project (at 7T), generic code. 
% theo.morfoisse@gmail.com

% Central presentation;

% Task : detect a star, 10 stars for 72 stimuli.
% Response time: RT is computed upon star presentation.

% Edited for IBC at 3T scanner, 18th May 2022
% combined test and scanner version
% himanshu.aggarwal@inria.fr

clear;
close all;


%% Parameters for psychtoolbox
sca;
KbName('UnifyKeyNames');

AssertOpenGL;
skipscreencheck = 0; % skip psychtoolbox screen test 1 or not 0. ???
mainscreen = 0;

%% Collect subject info (maybe already presented in the category localizer?)

subjno = datetime('now','Format','yyyyMMdd_HHmmss');
debug = input('Run on 0 - scanner or 1 - debug mode:', 's');
subjname = input('Please input subject number:', 's');
inputrunnum = input('Please input the run number (1-8):', 's');
runnum = str2double(inputrunnum); % the current run number

debug = str2double(debug);
debugrect = [];
if debug 
    debugrect = [100 100 900 700];
end


dirdata = pwd;
log_dir = 'log';
resultfolder = sprintf('sub-%s_run-%s_%s', subjname, inputrunnum, subjno);

%% Values specific to the scanner environnement

% Defined screen size
distance = 89; % in cm
screenwid_hor = 60; % in cm (69.84cm * 39.29 cm)
screenwid_ver = 45;
screenpx_hor = 1920; % in px  (1920 px * 1080 px)
screenpx_ver = 1080;

% Calculations of the visual angle
%visual_angle_hor = 2 * atand(screenwid_hor/(2*distance));
%visual_angle_ver = 2 * atand(screenwid_ver/(2*distance));

% Calculations of the dimension of the images depending of the visual angle
% wanted.
% visual_angle_wanted = 3; % 3 degrees;
% dimension_max = 2 * distance * tand(visual_angle_wanted/2); % in cm
% proportion_max = dimension_max / screenwid_ver; % in proportion of the screen size.
% 

%% Parameters of the stimulation protocol

%number_runs = 5; % Number of runs.
number_stimuli = 72; % Number of stimuli.
number_stars = 5; % Number of stars.
number_total_images_per_run = (number_stimuli + number_stars);

%% Contents of the instruction screen, modify, here.

% textstart = 'Waiting for the scanner trigger'; % lower line
% textinstruct = 'Please fixate on the fixation dot throughout the experiment'; % upper line
ttlCross = '+';

%% Define the corresponding keys of the button box here
% use KbName('KeyNames') to check the key correspondance in the current
% system

if ~debug
    % Check FORP key devices and get device indices
    clear PsychHID;
    [keyboardIndices, productNames, allInfos] = GetKeyboardIndices;
    [logicalTrig, locationTrig] = ismember({'Current Designs, Inc. TRIGI-USB'}, productNames); % trigger device
    %[logicalButt, locationButt] = ismember({'Arduino LLC Arduino Leonardo'}, productNames); % 2-button device
    [logicalButt, locationButt] = ismember({'Current Designs, Inc. 932'}, productNames); % 4-button device
    [logicalKey, locationKey] = ismember({'Dell Dell USB Keyboard'}, productNames); % PC keyboard

    devicenumtrigger = allInfos{locationTrig}.index; % temporary
    devicenumresp = allInfos{locationButt}.index;
    devicenumkey = allInfos{locationKey}.index;
end

trigger = 't'; % scanner trigger key
esckey = 'ESCAPE'; % escape key
spacekey = 'space'; % space key
button1 = 'b'; % MR response buttons
button2 = 'y';
button3 = 'g';
button4 = 'r';
button5 = ',<';

% mapping response buttons defined above. 
% here, b, y, g, r, ,< mapped to value 1-5;
keysOfInterestResp = zeros(1,256);
keysResp = {esckey,button1,button2,button3,button4,button5}; 
keysOfInterestResp(KbName(keysResp)) = 1;
keycodemapping = zeros(1,256);
keycodemappingind = zeros(1,length(keysResp)-1);

for kmind = 2 : length(keysResp)
    keycodemappingind(kmind-1) = KbName(keysResp{kmind});
    keycodemapping(KbName(keysResp{kmind})) = kmind-1;
end


%% Stimuli size definition

stimcolor = [128, 128, 128]; % font color
instructsize = 80; % instruction font size
fixwidth = 8; % width of the fixation point
fixcolor = [26, 167, 19]; % fixation color

%% Temporal paramaters

fixationStart = 6; % fixation at the start of the run. Set to 0 when debugging.
fixationEnd = 6; % fixation after the last ITI.
fix_duration = 0.2; % in seconds.
minresp = 0.3;
maxresp = 1.3;

duration_stimuli = 0.3; % Stimulus duration in seconds. 0.3 s in real experiment
%duration_inter_stimuli = 5.7; % Inter-stimulus duration in seconds.  5.7 s in real experiment

% jitter_values = [4, 6, 8];
% jitter_interStimulus = repmat(jitter_values,1,round(number_total_images_per_run/3));
% jitter_interStimulus = cat(2,jitter_interStimulus,ones(1,2)*6);
% jitter_interStimulus = jitter_interStimulus(randperm(number_total_images_per_run,number_total_images_per_run));
jitter_file = fullfile('stim',sprintf('jitter_protocol_%d_split.mat', runnum));
jitter_interStimulus = load(jitter_file);
jitter_interStimulus = jitter_interStimulus.jitter_interStimulus;
mean(jitter_interStimulus)
% This computes the length of the run.
% approx_duration = duration_stimuli * number_total_images_per_run + ...
%     duration_inter_stimuli * (number_total_images_per_run - 1) + ...
%     fixationStart + fixationEnd;


approx_duration = duration_stimuli * number_total_images_per_run + ...
    mean(jitter_interStimulus) * number_total_images_per_run + ...
    fixationStart + fixationEnd;

%% Load stimuli file

%stimuli = dir(['stimuli/*.png']);
stim_pics = fullfile('stim','stimuli_Abstraction7T.mat');
stimuli_structure = load(stim_pics);
stimuli_structure = stimuli_structure.stimuli_Abstraction7T;

% Set the rand method
rng('shuffle'); 

%% Block randomization

% Randomization of the stimuli presentation : in each run we present in
% random order twice each images (the 72 stimuli and the 5 stars).

number_to_randomize = number_stimuli + number_stars;

% list_order_stimuli_allRuns = cell(4,1);
% for run = 1:4
%     list_order_stimuli_1 = randperm(number_to_randomize,number_to_randomize);
%     list_order_stimuli_2 = randperm(number_to_randomize,number_to_randomize);
%     list_order_stimuli = [list_order_stimuli_1,list_order_stimuli_2];
%     list_order_stimuli_allRuns{run} = list_order_stimuli;
% end
% 
% save('list_order_stimuli.mat','list_order_stimuli_allRuns')
stim_seq = fullfile('stim','sequence_split.mat');
list_order_stimuli_allRuns = load(stim_seq).list_order_stimuli_allRuns;
list_order_stimuli = list_order_stimuli_allRuns{runnum};

%% Add trial info to the log file (I don't think it is necessary).

data(number_total_images_per_run).category = [];  % categories, values: 1-6

% Definition of the data fields
%data(1).order_stimuli = [];     % randomized list of trials
data(1).index_stimuli = [];     % index of the stimuli
data(1).name_image = [];        % name of the stimuli
data(1).renderingId = [];       % renderings, values: 1-4
data(1).renderingName = [];     % rendering name: photos, edges, geometries, others
data(1).trialStart = [];        % trial onset time, time lapsed from the first scanner trigger.
data(1).endStimuli = [];        % stimuli duration time, this is just for verification.
data(1).ResponseTime = [];      % first button press RT fro the stimulus onset.
data(1).ResponseTimeRun = [];   % button press time from the first scanner trigger.
data(1).key_pressed = [];       % first pressed button by the participant.
data(1).star = [];              % 1 = star ; 0 = no star;
data(1).SDT = [];               % 0.3<resp<1.3 : 1= hit; otherwise : 2 = miss;


%% Parameters for the display in psychtoolbox

Priority(MaxPriority(mainscreen));
LoadPsychHID;
Screen('Preference','SkipSyncTests',skipscreencheck);
PsychImaging('PrepareConfiguration');
%W = 960; H = 540;
% W = 1920; H = 1080;
[window,rect] = PsychImaging('OpenWindow',mainscreen, [0,0,0]); % black background.
Screen('BlendFunction',window,GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA); % ???
Screen('Preference','DefaultFontSize',instructsize);
Screen('Preference','DefaultFontStyle',1);
Screen('Preference','TextRenderer',1);
Screen('Preference','DefaultFontName','Courier New');
Screen('Preference','VisualDebugLevel',3) % skip the psychtoolbox welcome screen.
HideCursor;
sxsize = rect(3); % window size
sysize = rect(4);
cx = sxsize/2; % center of screen
cy = sysize/2;
% cy_new = sysize * 1/3; % avoid 1/3 of the bottom of the screen - fMRI constraints.
% not needed for 3T

%ovalrects = [cx - fixwidth/2; cy - fixwidth/2; cx + fixwidth/2; cy + fixwidth/2]; % fixation point (circle);
ovalrects = [cx - fixwidth/2; cy - fixwidth/2; cx + fixwidth/2; cy + fixwidth/2]; % fixation point (circle);

% VBL
hz = Screen('FrameRate',window); % stimuli are presented by number of frames
%ifi = Screen('GetFlipInterval',window,100);
ifi = Screen('GetFlipInterval',window);
stim_numFrames = round(duration_stimuli/ifi) - 0.5;
%interStim_numFrames = round(duration_inter_stimuli/ifi) - 0.5;

%% Instruction Screen

Screen('TextSize',window,instructsize); % Not necesary ? 
Screen('TextStyle',window,1);% Not necesary ?
Screen('TextFont',window,'Courier New');% Not necesary ?

% wtinstruct = RectWidth(Screen('TextBounds',window,textinstruct));
% htinstruct = RectHeight(Screen('TextBounds',window,textinstruct));
% wtstart = RectWidth(Screen('TextBounds',window,textstart));
% htstart = RectHeight(Screen('TextBounds',window,textstart));


%Screen('DrawText', window, textinstruct, cx - ceil(wtinstruct/2), cy - ceil(htinstruct/2) - 30, [255,255,255])
%Screen('DrawText', window, textstart, cx - ceil(wtinstruct/2), cy - ceil(htinstruct/2) + 30, [255,255,255])
% Screen('DrawText', window, textinstruct, cx - ceil(wtinstruct/2), cy - ceil(htinstruct/2) - 30, [255,255,255])
% Screen('DrawText', window, textstart, cx - ceil(wtinstruct/2), cy - ceil(htinstruct/2) + 30, [255,255,255])
wtTTL = RectWidth(Screen('TextBounds',window,ttlCross));
htTTL = RectHeight(Screen('TextBounds',window,ttlCross));
Screen('DrawText', window, ttlCross, cx - ceil(wtTTL/2), cy - ceil(htTTL/2), [255,0,0])

Screen('Flip',window)

%% Get the trigger from the scanner (Not sure to understand the meaning of this section)

keysOfInterest=zeros(1,256);
keysOfInterest(KbName({spacekey,esckey,trigger}))=1; % initialize keys for the trigger

if ~debug
    PsychHID('KbQueueCreate',devicenumtrigger,keysOfInterest);
    PsychHID('KbQueueCreate',devicenumkey,keysOfInterest);

    PsychHID('KbQueueStart',devicenumtrigger);
    PsychHID('KbQueueStart',devicenumkey);
else 
    PsychHID('KbQueueCreate',-1,keysOfInterest);
    PsychHID('KbQueueStart',-1);
end

% Get the trigger from the scanner
TTL = 0; % flag of starting the experiment
exp_term = 0; % flag for exiting
while TTL == 0
    if ~debug
        [KeyIsDown, firstPress] = PsychHID('KbQueueCheck',devicenumtrigger); % Wait for FORP TTL (from scanner)
    else
        [KeyIsDown, firstPress] = PsychHID('KbQueueCheck',-1); % Collect keyboard events since KbQueueStart was invoked
    end
    if KeyIsDown
        pressedKey = find(firstPress);
        keyname = KbName(pressedKey);
        presstime = firstPress(pressedKey);
        for n = 1 : size(pressedKey)
            if strcmp(KbName(pressedKey),trigger) == 1 % TTL
                TTL = 1;    % Start the experiment
                session_starttime = GetSecs;
                if ~debug
                    PsychHID('KbQueueStop',devicenumtrigger);
                    PsychHID('KbQueueRelease',devicenumtrigger);
                else
                    PsychHID('KbQueueStop',-1);
                    PsychHID('KbQueueRelease',-1);
                end
                break;
            elseif strcmp(KbName(pressedKey),esckey) == 1
                exp_term = 1;
                if ~debug
                    PsychHID('KbQueueStop',devicenumtrigger);
                    PsychHID('KbQueueRelease',devicenumtrigger);
                else
                    PsychHID('KbQueueStop',-1);
                    PsychHID('KbQueueRelease',-1);
                end
                break;
            else
                TTL = 0;
            end
        end
    end
    
    % [KeyIsDown, firstPress] = PsychHID('KbQueueCheck',devicenumkey); % Wait for key presses from keyboard (for exiting)
    % if KeyIsDown
    %     pressedKey = find(firstPress);
    %     keyname = KbName(pressedKey);
    %     presstime = firstPress(pressedKey);
    %     for n = 1 : size(pressedKey)
    %         if strcmp(KbName(pressedKey),trigger) == 1 % TTL
    %             TTL = 1;    % Start the experiment
    %             session_starttime = GetSecs;
    %             PsychHID('KbQueueStop',devicenumkey);
    %             PsychHID('KbQueueRelease',devicenumkey);
    %             break;
    %         elseif strcmp(KbName(pressedKey),esckey) == 1
    %             exp_term = 1;
    %             PsychHID('KbQueueStop',devicenumkey);
    %             PsychHID('KbQueueRelease',devicenumkey);
    %             break;
    %         else
    %             TTL = 0;
    %         end
    %     end
    % end
    
    
    if exp_term
        Priority(0);
        ShowCursor;
        Screen('CloseAll');
        return;
    end
end

%% Fixation Start 

run_starttime = GetSecs; % Start of the run

% indStar = find([stimuli_structure.ind] == 73);
% theStar = stimuli_structure(indStar).img;
indGrey = 78;
theGrey = stimuli_structure(indGrey).img;
[s1, s2, s3] = size(theGrey);
%baseRect = [0 0 s1 s2] * proportion_max; 
baseRect = [0 0 s1 s2]; 

rect = CenterRectOnPointd(baseRect, cx, cy);


pictureGrey = Screen('MakeTexture',window,theGrey); % Normally shoud be a blank screen
%pictureStar = Screen('MakeTexture',window,theStar); % star
Screen('DrawTexture', window, pictureGrey, [], rect);
Screen('FillOval', window, fixcolor, ovalrects, fixwidth/2 + 2);

Screen('Flip',window)
WaitSecs(fixationStart); % starting fixation 

%% Block loop

%PsychHID('KbQueueCreate',-1); % initizalize response buttons
if ~debug   
    PsychHID('KbQueueCreate',devicenumresp,keysOfInterestResp); % initizalize response buttons
    PsychHID('KbQueueCreate',devicenumkey,keysOfInterestResp);
else
    PsychHID('KbQueueCreate',-1,keysOfInterestResp); % initizalize response buttons
end

% Loop on the number of images per run ((72 + 5) * 2)
for trial = 1 : number_total_images_per_run

    j = list_order_stimuli(trial); % random order

    if ~debug
        PsychHID('KbQueueStart',devicenumresp)
        PsychHID('KbQueueStart',devicenumkey)
    else
        PsychHID('KbQueueStart',-1)
    end

    % Loading of the image
    %nameImage = stimuli(j).name;
    %nameImage = strcat('stimuli/',nameImage);
    %theImage = imread(nameImage);
    theImage = stimuli_structure(j).img;
    
    % Make the image into a texture
    imageTexture = Screen('MakeTexture', window, theImage);
    
    % Size of the stimulus display
    [s1, s2, s3] = size(theImage);
    %baseRect = [0 0 s1 s2] * proportion_max;
    baseRect = [0 0 s1 s2];
    rect = CenterRectOnPointd(baseRect, cx, cy);
    
    % Display the stimulus
    Screen('DrawTexture', window, imageTexture, [], rect);
    Screen('FillOval', window, fixcolor, ovalrects, fixwidth/2 + 2); % fixation
    if trial == 1
        vbl = Screen('Flip', window);
    else
        interStim_numFrames = round(jitter_interStimulus(trial-1)/ifi) - 0.5;
        vbl = Screen('Flip',window',vbl + interStim_numFrames * ifi);
    end
    
    %Screen('Flip',window);
    %WaitSecs(duration_stimuli); % Duration of the stimulus display
    
    trial_starttime = GetSecs; % Start of the trial
    
    % Close each stimulus texture to prevent memory overflow. Otherwise
    % they accumulate in the memory.
    Screen('Close',imageTexture);
    
    if exp_term
        Priority(0);
        break;
    end
    
    % Inter-stimulus
    Screen('DrawTexture', window, pictureGrey, [], rect);
    %Screen('FillOval', window, fixcolor, ovalrects, fixwidth/2 + 2); % fixation
    Screen('FillOval', window, fixcolor, ovalrects, fixwidth/2 + 2); % fixation
    vbl = Screen('Flip', window,vbl + stim_numFrames * ifi);
    %Screen('Flip', window);
    %WaitSecs(duration_inter_stimuli);
    
    endStimuli_time = GetSecs;
    
    % Button response check and logging at the end of the block
    % (including the inter-block interval, in case of late button
    % presses).
    if ~debug
        [KeyIsDown,firstPress] = PsychHID('KbQueueCheck',devicenumresp);
    else
        [KeyIsDown,firstPress] = PsychHID('KbQueueCheck',-1);
    end

    if KeyIsDown
        pressedKey = find(firstPress);
        keyname = KbName(pressedKey);
        presstimetemp = firstPress(pressedKey);
        %keys_table_i = {pressedKey, keyname, presstimetemp};
        %keys_table = [keys_table; keys_table_i];
        [pTime, pInd] = sort(presstimetemp,2);
        delta_time = pTime(1) - trial_starttime;
        if delta_time < 0
            data(trial - 1).ResponseTime = pTime(1) - trial_starttime_old;    % first button press RT fro the stimulus onset.
            data(trial - 1).ResponseTimeRun = pTime(1) - run_starttime_old;   % button press time from the first scanner trigger.
            data(trial - 1).key_pressed = keyname(pInd(1));               % first pressed button by the participant.
        else
            data(trial).ResponseTime = pTime(1) - trial_starttime;    % first button press RT fro the stimulus onset.
            data(trial).ResponseTimeRun = pTime(1) - run_starttime;   % button press time from the first scanner trigger.
            data(trial).key_pressed = keyname(pInd(1));               % first pressed button by the participant.
        end
%         data(trial).ResponseTime = pTime(1) - trial_starttime;    % first button press RT fro the stimulus onset.
%         data(trial).ResponseTimeRun = pTime(1) - run_starttime;   % button press time from the first scanner trigger.
%         data(trial).key_pressed = keyname(pInd(1));               % first pressed button by the participant.
        for n = 1 : size(pressedKey,2)
            if strcmp(KbName(pressedKey(n)),esckey) == 1
                exp_term = 1;
                %PsychHID('KbQueueStop',3);
                %PsychHID('KbQueueRelease',3);
                break;
            end
            
        end
    end
    
    if ~debug
        [KeyIsDown_2,firstPress_2] = PsychHID('KbQueueCheck',devicenumkey); % Collect keyboard events since KbQueueStart was invoked at the beginning of the block.
    else
        [KeyIsDown_2,firstPress_2] = PsychHID('KbQueueCheck',-1);
    end
    if KeyIsDown_2
        pressedKey = find(firstPress_2);
        keyname = KbName(pressedKey);
        presstimetemp = firstPress(pressedKey);
        %keys_table_i = {pressedKey, keyname, presstimetemp};
        %keys_table = [keys_table; keys_table_i];
        [pTime, pInd] = sort(presstimetemp,2);
        delta_time = pTime(1) - trial_starttime;
        if delta_time < 0
            data(trial - 1).ResponseTime = pTime(1) - trial_starttime_old;    % first button press RT fro the stimulus onset.
            data(trial - 1).ResponseTimeRun = pTime(1) - run_starttime_old;   % button press time from the first scanner trigger.
            data(trial - 1).key_pressed = keyname(pInd(1));               % first pressed button by the participant.
        else
            data(trial).ResponseTime = pTime(1) - trial_starttime;    % first button press RT fro the stimulus onset.
            data(trial).ResponseTimeRun = pTime(1) - run_starttime;   % button press time from the first scanner trigger.
            data(trial).key_pressed = keyname(pInd(1));               % first pressed button by the participant.
        end
%         data(trial).ResponseTime = pTime(1) - trial_starttime;    % first button press RT fro the stimulus onset.
%         data(trial).ResponseTimeRun = pTime(1) - run_starttime;   % button press time from the first scanner trigger.
%         data(trial).key_pressed = keyname(pInd(1));               % first pressed button by the participant.
        for n = 1 : size(pressedKey,2)
            if strcmp(KbName(pressedKey(n)),esckey) == 1
                exp_term = 1;
                %PsychHID('KbQueueStop',3);
                %PsychHID('KbQueueRelease',3);
                break;
            end
            
        end
        
    end
    %PsychHID('KbQueueStop',3);
    
    if exp_term
        Priority(0);
        if ~debug
            PsychHID('KbQueueStop',devicenumresp);
            PsychHID('KbQueueRelease',devicenumresp);
            PsychHID('KbQueueStop',devicenumkey);
            PsychHID('KbQueueRelease',devicenumkey);
            PsychHID('KbQueueStop',devicenumtrigger);
            PsychHID('KbQueueRelease',devicenumtrigger);
        else
            PsychHID('KbQueueStop',-1);
            PsychHID('KbQueueRelease',-1);
        end
        break;
    end
    
    
    % Add trial info to the data file
    %data(trial).order_stimuli = list_order_stimuli;     % randomized list of trials
    data(trial).index_stimuli = stimuli_structure(j).ind;  % index of the stimuli
    data(trial).name_image = stimuli_structure(j).name;    % name of the stimuli
    data(trial).category = stimuli_structure(j).category;  % categories, values: 1-6
    data(trial).renderingId = stimuli_structure(j).rendering;  % renderings, values: 1-4
    data(trial).renderingName = stimuli_structure(j).renderingName; % rendering name: photos, edges, geometries, others
    data(trial).trialStart = trial_starttime - run_starttime;  % trial onset time, time lapsed from the first scanner trigger.
    data(trial).endStimuli = endStimuli_time - trial_starttime;
        
    trial_starttime_old = trial_starttime;
    run_starttime_old = run_starttime;
    
end


%% Fixation End 

WaitSecs(fixationEnd);
run_endTime = GetSecs;
ShowCursor;
Priority(0);
%PsychHID('KbQueueStop',-1);
%PsychHID('KbQueueRelease',-1);
Screen('CloseAll')

%% Compute hit_miss per trial (logged in the field SDT) 

nHit = 0;
nMiss = 0;

for trial = 1 : number_total_images_per_run
    if strcmp(data(trial).name_image,'star')
        data(trial).star = 1; % 1 = star ; 0 = no star; 
        if data(trial).ResponseTime < maxresp & data(trial).ResponseTime > minresp
            data(trial).SDT = 1;  % 0.3<resp<1.3 : 1= hit; otherwise : 2 = miss;
            nHit = nHit + 1;
        else
            data(trial).SDT = 2;
            nMiss = nMiss + 1;
        end
    else
        data(trial).star = 0;
        data(trial).SDT = 0; 
    end
end


%% Save the data in a file (one run = one file).

% Creation of the structure 
result.subjno = subjno;
result.subjname = subjname;
result.data = data;
result.orderStimuli = list_order_stimuli;
result.duration = run_endTime - run_starttime;
result.nHit = nHit;
result.nMiss = nMiss;

% Creation of the name and path for the file
resultExtension = ".mat";
resultName_num = 0;
resultName = [];
nameFile = sprintf('result_%s_%s_abstraction7T_run_%d', subjno, subjname, runnum); 
nameFile_plus = sprintf('%s%s%s',nameFile,resultName,resultExtension);
logPath = fullfile(dirdata, log_dir, resultfolder);
resultPath = fullfile(logPath, nameFile_plus);

if exist(logPath, 'dir') == 0
    mkdir(logPath);
end

%save('subjAbstraction7T.mat','subjno','subjname','currentoddassing','distance','screenpx','screenwid');

while exist(resultPath,'file')
    resultName_num = resultName_num + 1;
    resultName = sprintf('_%s',string(resultName_num));
    nameFile = sprintf('result_%s_%s_abstraction7T_run_%d', subjno, subjname, runnum); 
    nameFile_plus = sprintf('%s%s%s',nameFile,resultName,resultExtension);
    resultPath = fullfile(logPath, nameFile_plus);
end

% Save the correct file in the correct folder
save(resultPath,'result');

save(fullfile(logPath,'subjAbstraction7T.mat'),'subjno','subjname','distance','screenpx_hor','screenwid_hor');










