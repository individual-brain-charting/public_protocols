% written by Nicolas Clairis - march 2016, adapted january 2017 for
% NeuroSpin study

clear all; close all; clc;
subid = input('subject identification number? ','s');
nsession = input('session number (training:0;task: 1 to 8) ?');
IRM = 1; % 0 outside fMRI or 1 inside fMRI
nbsession = 8; % nber of rating runs (without including the training)
device_number = 7;

%% load images
% define which category you want to use for this particular run (alternate
% order btw subjects)
stimCateg = input('Please define category of stim: 1) Food, 2) Paintings, 3) Faces, 4) Houses');
if stimCateg == 1
  categName = 'food';
  y_shift = 300; % define y coordinates for the image
  yscale = 320; % define y coordinates for the scale
elseif stimCateg == 2
  categName = 'painting';
  y_shift = 300; % define y coordinates for the image
  yscale = 320; % define y coordinates for the scale
elseif stimCateg == 3
  categName = 'face';
  y_shift = 350; % define y coordinates for the image
  yscale = 320; % define y coordinates for the scale
elseif stimCateg == 4
  categName = 'house';
  y_shift = 360; % define y coordinates for the image
  yscale = 320; % define y coordinates for the scale
end
% define which group of stim you want to use (alternate btw subjects for
% A-P or P-A)
if nsession > 0
  stimGroup = input('Check on group A (1) or group B (2)?');
  if stimGroup == 1
     groupName = 'A';
  elseif stimGroup == 2
     groupName = 'B';
   end
  else
    groupName = '';
end
% Comment: stimCateg and stimGroup may be automatized to be automatically
% defined for each subject


% create directory
%setDir;
[root, resultdir, subdir, behaviordir, fMRIScansDir] = setDir(subid, IRM);


%% check if session already made or not (for the task only, not training)
cd(subdir);
run = 1;
run_made_or_not = zeros(1,nbsession);
while run <= nbsession
    sessnber = num2str(run);
    if exist(['MBB_battery_ratings_onsets_sub',subid,'_run',sessnber,'.mat'],'file') > 0
        run_made_or_not(run) = 1;
    end
    run = run + 1;
end
if nsession <= max(find(run_made_or_not==1)) % check if session already exists
    disp('Erreur dans le numero du run ?');
    cd(root);
    clear all; close all; return;
end
cd(root)
%% ratings
if nsession == 0 % training
    total_items = 4;
    ratingRimsummary = zeros(1,total_items);
else % rating task
    total_items = 60;
    ratingRimsummary = zeros(1,total_items); % variable where all the values for each item will be stored
end

%% screen configuration
screens = Screen('Screens');
if IRM == 0
    whichScreen = max(screens);
elseif IRM == 1
    whichScreen = 1; % 1 if 2 screens, 0 if one screen (display on projector)
end
%for debug
whichScreen = max(screens);

% for real
window = Screen('OpenWindow',whichScreen,[0 0 0]);
HideCursor()
% for debugging:
%window = Screen('OpenWindow', whichScreen, [], [100, 100, 800, 600]);

% [window, windowRect] = PsychImaging('OpenWindow', screenNumber, [0 0 0]);
% Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');
Screen('Preference','SkipSyncTests', 0);
Screen('Preference','VisualDebugLevel', 1);
% On Windows, use (uncomment) the next command line
% Screen('Preference','TextEncodingLocale','UTF-8');
Screen('TextSize', window, 36);
Screen('TextFont', window, 'arial');
[L, H] = Screen('WindowSize',whichScreen);
x = L/2;
y = H/2;
% load cross
pic_cross = Screen('MakeTexture',window,imread('Cross.bmp'));
rect_cross = CenterRectOnPoint(Screen('Rect',pic_cross),x,y);

%% Timings
instruction_T = 5;
% jitter from 0.5s to 4.5s 
ITT = 5; % inter-task time (pause between each task, display instructions of the next one)
WaitPressTime = 10; % max time for waiting a response
% display_before_rating_T = 3;
tooslow_fdbk_T = 2;
if nsession == 0 % shorter for training
    ending_T = 5;
else
    ending_T = 10;
end
release_wait = 0.5;

% total duration of the task: if the subject finishes earlier, than we just
% display a fixation cross at the end until this time is achieved
total_time = 496;
total_task_time = total_time - 10;

%% onsets for fMRI
% for fMRI add (if IRM ==1)?
%% events onset
onset.firstTTL = [];
onset.instruction = [];
onset.cross_ITI = []; % intertrial cross
onset.display_ratingscaleRim = []; % IMPORTANT: onset of beginning of the image
onset.cross_ITT = []; %intertask (E/R/R_im) cross
onset.tooslow = []; % in case of too slow reaction
% trials coming after a too slow reaction
onset.tooslowtrial_display_ratingscaleRim = [];
onset.please_release = [];
onset.cross_release = [];
%% events duration
duration.instruction = [];
duration.cross_ITI = [];
duration.display_ratingscaleRim = [];
duration.cross_ITT = [];
duration.tooslow = [];
duration.tooslowtrial = [];
% trials coming after a too slow reaction
duration.tooslowtrial_display_ratingscaleRim = [];
duration.please_release = [];
duration.cross_release = [];

%% TTL trigger
%dummy_scan = 3; % number of dummy scans to wait before starting
% no dummy_scan at NeuroSpin
dummy_scan = 0; % number of dummy scans to wait before starting

KbName('UnifyKeyNames');
trigger = KbName('t'); %% TTL in keyboard touch t for NeuroSpin
key.escape = KbName('escape');

if IRM == 0
    %% key code configuration for FORP USB response box
    key.left = KbName('g');        % g key for minus // index finger
    key.right = KbName('y');       % y key for plus // middle finger
    key.space = KbName('r');       % r for validation // thumb
    
elseif IRM == 1
    %% key code configuration for FORP USB response box
    key.leftsmall = KbName('y');   % y for minus (small step) // index finger
    key.rightsmall = KbName('g');  % g for plus (small step) // middle finger
    key.left = KbName('r');        % r key for minus // ring finger
    % key.right = 188;       % comma key for plus // baby finger (Win DELL laptop)
    key.right = 59;       % comma key for plus // baby finger (Linux HP laptop)
    key.space = KbName('b');       % b for validation // thumb
    
    % add a cross at the beginning (better for eye tracking)
    Screen('DrawTexture',window,pic_cross,[],rect_cross);
    % onset
    [~,timenow1,~,~,~] = Screen(window,'Flip');
    onset.cross_ITT = [onset.cross_ITT; timenow1];
    
    % ======== fMRI specification==========
    %% TRIGGER
    if nsession > 0 % no trigger for training
        next = 0;
        TTL = []; % TTL TIMES
        % wait 5 first TTL before starting task
        while next < dummy_scan+1        % dummy_scan +1, because for every scan, there will be a trigger. throw away the first 3 scans and register the time when the 4th starts
            [keyisdown, T0IRM, keycode] = KbCheck;
            
            if keyisdown == 1 && keycode(trigger) == 1
                if next == 0
                    T0 = T0IRM;
                end
                next = next + 1;
                disp(next);
                TTL = [TTL; T0IRM];
                while keycode(trigger) == 1
                    [keyisdown, T, keycode] = KbCheck;
                end
            end
        end
        
        % record all subsequent TTL
        keysOfInterest = zeros(1,256);
        keysOfInterest(trigger) = 1;
        
        %for debug
%         # The first argument, i.e. the device index, of the next function
%         # must have to be changed according to the computer in which the
%         # protocol is run.
        KbQueueCreate(device_number,keysOfInterest); % checks TTL only      
        KbQueueStart; % starts checking
    else 
     
    end
    
    % duration starting cross
    timenow2 = GetSecs;
    %dur = timenow2 - timenow1;
    %duration.cross_ITT = [duration.cross_ITT; dur];
end

%% rating task
% launch rating task
taskRatingR_im; % reward (image) ratings

% if escape pressed, go directly to the end of the script without displaying any fixation cross
if nsession > 0
    %% fixation cross for remaining time of the run (not for training)
    if stoptask == 0
        % if it is a training session, we also don't need to wait the
        % total_task_time so 5seconds for final cross is the best
        
        % display a final fixation cross before ending to get a proper BOLD signal
        % at the end of the task
        Screen('DrawTexture',window,pic_cross,[],rect_cross);
        % onset
        [~,timenow1,~,~,~] = Screen(window,'Flip');
        onset.cross_ITT = [onset.cross_ITT; timenow1];
        timenow = GetSecs;
        if timenow - T0 >= total_task_time || nsession == 0 % if they already spent more time than the total limit we fixed, add five more seconds of fixation cross and then stop
            WaitSecs(ITT);
        else % if they finished the task before the total time amount we fixed is reached, keep displaying a fixation cross
            stopTheTask = 0;
            while timenow - T0 < total_task_time && stopTheTask == 0
                [keyisdown, secs, keycode] = KbCheck;
                if keycode(key.escape) == 1
                    stopTheTask = 1;
                end
                timenow = GetSecs;
            end
        end       
        % duration
        timenow2 = GetSecs;
        dur = timenow2 - timenow1;
        duration.cross_ITT = [duration.cross_ITT; dur];
        %% fixation cross (or black screen) at the end of the script
        Screen('DrawTexture',window,pic_cross,[],rect_cross);
        Screen(window,'Flip');
        WaitSecs(ending_T);
    end   
    %% final save
    cd(subdir);
    sessionname = num2str(nsession);
    % save ratings
    save(['ratings_summary_sub-',subid,'_run',sessionname,'_',categName,'group',groupName,'.mat'],'ratingRimsummary');
    % save onsets and durations for fMRI
    if IRM == 1
        % save all TTL in the results file
        while KbEventAvail
            [event, n] = KbEventGet;
            TTL = [TTL; event.Time];
        end
        KbQueueStop;
        KbQueueRelease;
        save(['TTL_sub-',subid,'_run',sessionname,'.mat'],'T0','TTL');
        % record onsets
        onset.firstTTL = TTL;
        save(['MBB_battery_ratings_onsets_sub-',subid,'_run',sessionname,'_',categName,'group',groupName,'.mat'],'onset','duration');
    end
    save(['global_sub-',subid,'_run',sessionname,'_',categName,'group',groupName,'.mat'])
    cd(root);   
end
Screen('CloseAll');

%% Remove unnecessary folders - Octave only
function [status, msg] = rm_rf (dir)
  confirm_recursive_rmdir (false, "local");
  [status, msg] = rmdir (dir, "s");
endfunction
rm_rf(behaviordir);
rm_rf(fMRIScansDir);
