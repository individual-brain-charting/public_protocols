function Enum_EnumWM_CTRL_fMRI(subject, run_group, log_file)
%%% version containing only 1 saliency level
%%% mean trial length = 12secs

% Disable Matlab short-circuit evaluation in Octave
do_braindead_shortcircuit_evaluation (0)

% Clear Matlab/Octave window:
clc;

% check for Opengl compatibility, abort otherwise:
AssertOpenGL;

% Check if all needed parameters given:
if nargin < 3
    error('Must provide required input parameters "subjectNumber", "run-group number" and "log-file number"!');
end

% Reseed the random-number generator for each expt.
rand('state',sum(100*clock));

KbName('UnifyKeyNames');

thumbKey            = KbName('b'); % thumb in the FORP-USB response box
indexKey            = KbName('y'); % index finger in the FORP-USB response box
middleKey           = KbName('g'); % middle finger in the FORP-USB response box
ringKey             = KbName('r'); % ring finger in the FORP-USB response box

%thumbKey            = KbName('y');  % index finger in the FORP-USB response box
%indexKey            = KbName('g');  % middle finger in the FORP-USB response box
%middleKey           = KbName('r');  % ring finger in the FORP-USB response box
%ringKey             = KbName(',<'); % little finger in the FORP-USB response box

escapeKey           = KbName('escape');
triggerKey          = KbName('t');
pauseKey            = KbName('p');
resumeKey           = KbName('s');
TR                  = 2;
ntrials             = 12;
fixITI              = 7.8;        % fixer Antail des ITI.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Synchronizing to MR scanner  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%% L O G F I L E   &   S T I M U L I    P A T H S %%%%%%%%%%%%%%%%%%%%%%%%
% Define paths:
imgdir = fullfile(pwd, '/');
logdir = fullfile(imgdir, 'log_files/enumeration_ts/');

%logdir             = '~/ibc_repos/cognitive_protocols/knops/log_files/enumeration/';
%imgdir             = '~/ibc_repos/cognitive_protocols/knops/';

if ~exist(logdir) 
    mkdir(logdir); 
end

% Define filenames of input files and result file:
datafilename = strcat(logdir, 'Enum_ts_',num2str(subject),'_',num2str(run_group),'_',num2str(log_file),'.dat'); % name of data file to write to

% check for existing result file to prevent accidentally overwriting
% files from a previous subject/session (except for subject numbers > 99):
if fopen(datafilename, 'rt')~=-1
    fclose('all');
    error('Result data file already exists! Choose a different subject number.');
else
    datafilepointer = fopen(datafilename,'wt'); % open ASCII file for writing
end

title = myCreateStringToWrite({'subject', 'run_group_no.', 'log_file_no.', 'task', 'trial', 'stim_x', 'numerosity', 'version', 'size or surf',  'testitem(ti)', 'ti_flipped', ...
                               'response','correctYN',  'rt', ...
                               't1-trial_t', 't2-trial_t',  't3-trial_t', 't4-trial_t','real_t1', 'real_t2', 'real_t3', 'real_t4', ...
                               'trial_start', 'mem_file'});
fprintf(datafilepointer,'%s\n',title);

%% S O M E    D E F I N I T I O N S %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% calculate numerosity: trial_x =rem(i,maxnum)+1;
% calculate salience: trial_x =rem(i,salience)+1;

% [trial_x, numerosities, saliences, flips, ss] = StimRandomizationvWMfMRI;
% 11.11.13: too complicated. I will simply shuffle the nums within a functinal run

numerosities = [ones(1,48);ones(1,48);ones(1,48);ones(1,48)];
for i = 1:4
    numstmp =  repmat([1,2,3,4,5,6,7,8],1,6); 
    numerosities(i,:) = numstmp;
end
trial_x = Shuffle(linspace(1,ntrials,ntrials));

ss = repmat([1,2,1,2],1,48);
sizesurfs = {'area', 'size'};

mirror = repmat([1,2,2,1],1,48); % mirrored version of test or not.
mirrorS = {'', '2'}; % stimuli start with nothing or "2" for mirrored version.

for i=1:ntrials
    a               = floor((0-41+1)*rand+41); % between 1 and 40!
    version(i)      = a;
end

%%  T I M I N G   %%%%%%%%%%%%%%%%%%%%%%
fixation_t  = 0.500; % fixation time before memory item
mem_t       = 0.150; % duration of the memory item
target_t    = 1.7;   % duration of the target item (= max RT)
%mask_t      = 1.0;
ITI_t       = 2.0; 
pause_dur   = 0;
%delay_t     = 1.0; % blank period between test & probe

%% vertical offset which moves stimulus up on screen for scanner situation
verticalOffset = 0; % not needed in BCAN (was set to -150 for Mattarello


[ITI, delay, trial_start]=StimulusTimingvWMfMRI(TR, ntrials);



%% E X P E R I M E N T %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Embed core of code in try ... catch statement. If anything goes wrong
% inside the 'try' block (Matlab error), the 'catch' block is executed to
% clean up, save results, close the onscreen window etc.
try
    % Get screenNumber of stimulation display. We choose the display with
    % the maximum index, which is usually the right one, e.g., the external
    % display on a Laptop:
    screens=Screen('Screens');
    screenNumber=max(screens);
    
    % Returns as default the mean gray value of screen:
    gray=GrayIndex(screenNumber); 
    white=WhiteIndex(screenNumber);
    black=BlackIndex(screenNumber);
    green = [0 255 0];

    % Open a double buffered fullscreen window on the stimulation screen
    % 'screenNumber' and choose/draw a gray background. 'w' is the handle
    % used to direct all drawing commands to that window - the "Name" of
    % the window. 'wRect' is a rectangle defining the size of the window.
    % See "help PsychRects" for help on such rectangles and useful helper
    % functions:
    
    %% for testing:
    %[w, wRect]=Screen('OpenWindow',screenNumber, gray, [1000 10 1640 490]);
    %% for real
    [w, wRect]=Screen('OpenWindow',screenNumber, gray);
    [screenwidth, screenheight]=Screen('WindowSize', w);
    
    % Hide the mouse cursor:
    HideCursor()
    
    % On Windows, use (uncomment) the next command line
    Screen('Preference','TextEncodingLocale','UTF-8');
    
    leftedge    = (screenwidth - 700)/2; % compute the edges of the rect of the mask
    rightedge   = ((screenwidth - 700)/2)+700;
    center = [screenwidth/2, screenheight/2];
    % Set text size (Most Screen functions must be called after
    % opening an onscreen window, as they only take window handles 'w' as
    % input:
    Screen('TextSize', w, 32);
    
    % Do dummy calls to GetSecs, WaitSecs, KbCheck to make sure
    % they are loaded and ready when we need them - without delays
    % in the wrong moment:
    KbCheck;
    WaitSecs(0.1);
    GetSecs;
    % ***********************************************************************
    %================  B E G I N N I N G    C O D E   vW M _ f M R I    ==
    

    % ========== N O W   W A I T   F O R   T R I G G E R   ==================
    %========================================================================
    % ***********************************************************************


    [keyIsDown secs keycodes] = KbCheck();
    while isempty(keycodes) || ~keycodes(triggerKey)
        str1 = sprintf("L'expérience va commencer \n\n");
        str2 = sprintf("dans quelques instants.\n\n\n");
        str3 = sprintf("Appuyez sur les boutons \n\n");
        str4 = sprintf("selon le nombre des schémas.\n\n\n");
        str5 = sprintf("Essayez de bouger le moins possible, SVP.");  
        message = [str1 str2 str3 str4 str5];
        DrawFormattedText(w, message, 'center', 100, BlackIndex(w));
        %Screen('DrawText', w, 'Waiting for the trigger...', center(1)-200, center(2));
        Screen('Flip', w);
        [keyIsDown secs keycodes] = KbCheck();
    end;    
    %expTimer = tic();
    %start_trigger = toc(expTimer);
    
    ExpStart_t = GetSecs; % take the time when Exp started 

    % Set priority for script execution to realtime priority:
    priorityLevel=MaxPriority(w);
    Priority(priorityLevel);
    
    % insert if then for two different pradigms (vWM and subitizing)??
    
    %%=====================================================================
    % Start experimental loop:
    %**********************************************************************
   
    for task=2:2 % 1 is WM, 2 is subitizing
        

        % Clear screen to background color (our 'gray' as set at the
        % beginning):
        Screen('Flip', w);
        
        %% Fixation Cross %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        fixrect= OffsetRect(CenterRect([0 0 8 8],wRect), 0, verticalOffset );
        Screen(w, 'FillOval', black, fixrect);	% draw fixation dot
        [VBLTimestamp]=Screen(w, 'Flip');
        %=============================================================
        
        
        %prevTrialTime = ExpStart_t; %first trial
        for trialn = 1:ntrials
            trial = trial_x(trialn);
            %trial_t = 5 + prevTrialTime + pause_dur + (trial_start(trial)/1000); 
            trialstart_t = GetSecs;
            %delay_t = delay(i);
            
            
            %% Fixation Cross %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            t1 = trialstart_t;
            fixrect= OffsetRect(CenterRect([0 0 8 8],wRect), 0, verticalOffset );
            Screen(w, 'FillOval', black, fixrect);	% draw fixation dot
            [VBLTimestamp st1]=Screen(w, 'Flip', [t1]);
            %=============================================================
           
            num         = numerosities(trial);
            vers        = version(trial);
            vers_f      = sprintf('%02d', vers);
            corrMirr = mirrorS{mirror(trial)};
            % size or surface constant
            sizesurf     = ss(trial);
            % which Gabor in display for test
            testItemInDisplay = floor((0-num)*rand+num)+1; % between 1 and num!
   
            
            %%  M E M O R Y    I T E M   %%%%%%%%%%%%%%%%%%%%%%
            t2 = t1+fixation_t;
            memfile = strcat(imgdir, 'test/',sizesurfs{sizesurf},num2str(num),'_0',num2str(vers_f), '.bmp');
            % read stimulus image into matlab matrix 'imdata':
            imdata=imread(char(memfile));
            % make texture image out of image matrix 'imdata'
            mtex=Screen('MakeTexture', w, imdata);
            Screen('DrawTexture', w, mtex);
            fixrect= OffsetRect(CenterRect([0 0 8 8],wRect), 0, verticalOffset );
            Screen(w, 'FillOval', black, fixrect);	% draw fixation dot
            
            [VBLTimestamp st2]=Screen('Flip', w, [t2]);
            %=============================================================
            
            
            
            %% Fixation Cross %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            t3 = t2 + mem_t;
            fixrect= OffsetRect(CenterRect([0 0 8 8],wRect), 0, verticalOffset );
            Screen(w, 'FillOval', green, fixrect);	% draw fixation dot
            [VBLTimestamp StartRTMeasurement] = Screen(w, 'Flip', [t3]);
            %=============================================================
            
#            %% allow break out:
#            FlushEvents('keyDown');
#            [keyIsDown secs keycodes] = KbCheck();
#            
#            while ((GetSecs - st3)< target_t && (keyIsDown==0))
#                [keyIsDown button_t keycodes] = KbCheck();
#                if keycodes(escapeKey)
#                    sca;
#                    fclose(datafilepointer);
#                    ShowCursor;
#                    break
#                end
#            end
#    

            %% R E S P O N S E S %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            % while loop to show stimulus until subjects response or until
            % "duration" seconds elapsed.
            measureRT = 1;
            button_t = GetSecs;
            responsekey = 99;
            correct = 99;
            RT = 99;
            
            FlushEvents('keyDown');
            [keyIsDown secs keycodes] = KbCheck();
            
            counter = 0;
            keys = [];
            button_t0 = 0;
            while ((GetSecs - StartRTMeasurement)<= target_t && (counter<2))
                [keyIsDown button_t keycodes] = KbCheck();
                if (keyIsDown == 1 && counter == 0)
                  button_t0 = button_t;
                end
                if (keyIsDown == 1 && counter == 1 && button_t - button_t0 < 0.2)
                  continue
                end
                if keycodes(thumbKey)
                  keys = [keys 1];
                  counter = counter +1;
                elseif keycodes(indexKey)
                  keys = [keys 2];
                  counter = counter +1;
                elseif keycodes(middleKey)
                  keys = [keys 3];
                  counter = counter +1;
                elseif keycodes(ringKey)
                  keys = [keys 4];
                  counter = counter +1;
                elseif keycodes(escapeKey)
                  sca;
                  fclose(datafilepointer);
                  ShowCursor;
                  break
                end
            end
            
            RT = (button_t0 - StartRTMeasurement); %compute response time
            %=============================================================

            %=============================================================
                        
            if isequal(keys,[1])
                responsekey = 1;
                if num == responsekey
                    correct = 1;
                else
                    correct = 0;
                end
            elseif isequal(keys,[2])
                responsekey = 2;
                if num == responsekey
                    correct = 1;
                else
                    correct = 0;
                end
            elseif isequal(keys,[3])
                responsekey = 3;
                if num == responsekey
                    correct = 1;
                else
                    correct = 0;
                end
            elseif isequal(keys,[4])
                responsekey = 4;
                if num == responsekey
                    correct = 1;
                else
                    correct = 0;
                end
            elseif isequal(keys,[1 1])
                responsekey = 5;
                if num == responsekey
                    correct = 1;
                else
                    correct = 0;
                end
            elseif isequal(keys,[2 2])
                responsekey = 6;
                if num == responsekey
                    correct = 1;
                else
                    correct = 0;
                end
            elseif isequal(keys,[3 3])
                responsekey = 7;
                if num == responsekey
                    correct = 1;
                else
                    correct = 0;
                end
            elseif isequal(keys,[4 4])
                responsekey = 8;
                if num == responsekey
                    correct = 1;
                else
                    correct = 0;
                end
            end
            %=============================================================
            
            %% Fixation Cross %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            t4 = t3 + target_t;
            Screen(w, 'FillOval', black, fixrect);	% draw fixation dot
            [VBLTimestamp st4]=Screen(w, 'Flip', [t4]);
            %============================================================
   
            %% W R I T E   T O    L O G F I L E %%%%%%%%%%%%%%%%%%%%%%%%%%
            %% all timing info is with respect to trigger time (ExpStart_t)
            %% this includes button time ==> subtract trial_start_t to get RT
            %% rt itself is correct, ie with respect to start of
            %% measurement (which is flip time of white fix cross).
            
            logfile_infos = {subject, run_group, log_file, task, trial, trial_x(trial), num, vers, sizesurf,  testItemInDisplay,  corrMirr, ...
                responsekey, correct, RT,...
                t1-ExpStart_t, t2-ExpStart_t, t3-ExpStart_t, t4-ExpStart_t,...
                st1 - ExpStart_t, st2 - ExpStart_t,  StartRTMeasurement - ExpStart_t, st4 - ExpStart_t, ...
                trial_start(trial)/1000, memfile }; 
            sf=myCreateStringToWrite(logfile_infos); % make sure to copy this function in same folder!!
            fprintf(datafilepointer,'%s\n',sf);
            % Close all offscreen windows & textures, leave onscreen ones
            % open.
            Screen('Close');
            
            %% calculate trial length & stuff
            trialend_t = trialstart_t + (GetSecs - trialstart_t) + fixITI + (ITI(trial)/1000); 
            
            %% Fixation Cross %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            fixrect= OffsetRect(CenterRect([0 0 8 8],wRect), 0, verticalOffset );
            Screen(w, 'FillOval', black, fixrect);	% draw fixation dot
            [VBLTimestamp st7]=Screen(w, 'Flip');
            wakeup = WaitSecs('UntilTime', trialend_t);
            FlushEvents('keyDown');
            %============================================================
%             prevTrialTime = GetSecs;
            %=============================================================
            
            
            %%========================================================================
            %% =======   P A U S E  C O D E  =========================================
             if ((trialn == 6) ); %6 12
                 str1 = sprintf('Pause - Continuez ...\n\n\n');
                 str2 = sprintf("Appuyez sur les boutons \n\n");
                 str3 = sprintf("selon le nombre des schémas.\n\n\n");
                 str4 = sprintf("Essayez de bouger le moins possible, SVP.");   
                 message = [ str1 str2 str3 str4];
                 DrawFormattedText(w, message, 'center', 100, BlackIndex(w));
                 %Screen('DrawText', w, 'Waiting for the trigger...', center(1)-200, center(2));
                 Screen('Flip', w);
                 pause_start = GetSecs;
                 FlushEvents('keyDown');
                 [keyIsDown secs keycodes] = KbCheck();
             
                 while keyIsDown==0 && ~keycodes(triggerKey) 
                     [keyIsDown button_t keycodes] = KbCheck();
                 end
                 Screen(w, 'FillOval', black, fixrect);	% draw fixation dot
                 [VBLTimestamp tmp]=Screen(w, 'Flip');
                 
                 
                 pause_end = GetSecs;
                 pause_dur = pause_dur + (pause_end - pause_start);
                 Screen('TextSize', w, 32);
                 trialend_t = GetSecs;
             end
            %=============================================================
        end
    end
    % Cleanup at end of experiment - Close window, show mouse cursor, close
    % result file, switch Matlab/Octave back to priority 0 -- normal
    % priority:
    Screen('CloseAll');
    ShowCursor;
    fclose(datafilepointer);
    
    %delete(instrfindall);
    
    Priority(0);
    
    %% End of experiment:
    return;
catch
    % catch error: This is executed in case something goes wrong in the
    % 'try' part due to programming error etc.:
    
    % Do same cleanup as at the end of a regular session...
    Screen('CloseAll');
    ShowCursor;
    %try 
        
        %delete(instrfindall);
        
    %catch
        fclose('all');
    %end
    Priority(0);
    
    % Output the error message that describes the error:
    psychrethrow(psychlasterror);
end % try ... catch %            

%try 
  
   %delete(instrfindall);
   
%catch
   fclose('all');
%end
%delete(instrfindall);
clear all;
Priority(0);
            

