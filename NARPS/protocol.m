%% NARPS Mixed Gambles Protocol (more info in README.md)
%% Modified for IBC by Himanshu Aggarwal - April-May 2021
%% Email - himanshu.aggarwal@inria.fr
%%

%function protocol(sub_id,run_number,inputDevice,experimenter_device,Scan)
clear all; %%%NEW

Screen('Preference', 'SkipSyncTests', 1);
Screen('Preference', 'VisualDebugLevel', 0);  %%%NEW
KbName('UnifyKeyNames');

sub_id=input('Enter subject Number: ','s');
Scan=1;% MRI

if Scan==1
    run_number=input('Enter run number (1-4): '); 
    while run_number<1 || run_number>4
        run_number=input('INVALID ENTRY - Enter run number (1-4): ');
    end
else
    run_number=1;
end

scannerKey = KbName('t');
escapeKey = KbName('ESCAPE');

WorkingDir=pwd;

% fprintf(['\n\nsubjectID is: ' num2str(sub_id) '\n']);
% fprintf(['Run # is: ' num2str(run_number) '\n']);
% fprintf(['Scan is: ' num2str(Scan) '\n']);
% fprintf('\n')

% GoOn=input('are all variables ok? (1-yes, 0-no)');
% if GoOn==0
%     error('please check you numbers and start again')
% end

%%
[script_name]='Mixed-Gambles Task'; %Risk Acceptability'; % 4 runs decision only: by Sabrina Tom, modified by Eliza Congdon
script_version='ibc';
revision_date='May 2021';

fprintf('%s %s (revised %s)\n',script_name, script_version, revision_date);

%%  read in subject information

ConditionName = 'equalRange';

%Assigns condition for the 4 runs
SubNum=str2double(sub_id);
SubNumStr=SubNum;
% SubNumStr(end-floor(log10(SubNum)):end)=num2str(SubNum);
Order=1; % assigns randomization (IBC change: only using first randomization for all subjects)
gain_side='left'; % (IBC change: gain always on left)
Task='MGT'; % 

%% Load Hebrew instructions image files
%  --------------------------------------------
% if Scan==1 % MRI
%     Instructions=dir([WorkingDir '/Instructions/*MGT.jpg']);
% else % DEMO
%     Instructions=dir([WorkingDir '/Instructions/*MGT_demo.jpg']);
% end

% Trigger = dir([WorkingDir '/Instructions/Trigger.jpg' ]);
% Trigger_image = imread([WorkingDir '/Instructions/' Trigger(1).name]);
% Instructions_name=struct2cell(rmfield(Instructions,{'date','bytes','isdir','datenum'}));
% Instructions_image=imread([WorkingDir '/Instructions/' sprintf(Instructions_name{1})]);


%% write trial-by-trial data to a text logfile
c=clock;
hr = sprintf('%02d', c(4));
minutes = sprintf('%02d', c(5));
timestamp = [date,'_',hr,'h',minutes,'m'];

Current_folder=WorkingDir;


% Assign output folders
if Scan==1 % MRI
    logsFolder=[Current_folder '/logs/'];
    OutputsFolder=[Current_folder '/Outputs/'];
else
    logsFolder=[Current_folder '/logs/demo/'];
    OutputsFolder=[Current_folder '/Outputs/demo/'];
end

logfile=[logsFolder sprintf('NRPS_sub-%d.log',SubNumStr)];
OutputFile=[OutputsFolder sprintf('sub-%d_task-%s_run-0%d.txt',SubNumStr,Task,run_number)];

exitExp = 0;

fprintf('A log of this session will be saved to %s\n',logfile);
fid1=fopen(logfile,'a');
if fid1<1       %%%%NEW
    error('could not open logfile!');
end            %%%%NEW

fprintf(fid1,'\n\n\n\n%s %s (revised %s)\n',script_name,script_version, ...
    revision_date);
fprintf(fid1,'Run #%d\nStarted: %s %2.0f:%2.0f\n',run_number,date,c(4),c(5));
fid2=fopen(OutputFile,'W'); % formated output file
fprintf(fid2,'subjectID\tCondition\tOrder\tRunNum\tTrialNum\tonsettime\tTrialStart\tWinSum\tLoseSum\tGainSide\tRT\tResponseKey\tResponse\tBinaryResp\n'); %write the header line

fprintf('Setting up the screen - this may take several seconds...\n');
WaitSecs(1);

if run_number>4
    run_number=run_number-4;
end

%% reads list of prospect numbers to present for each of 4 runs (IBC change: only load equal range).
load('equalRange_design.mat');


%% setting up stuff (standard to all programs)
%% pixelSize=32;

stim_duration=4;
delay=0.5;

screennum = max(Screen('Screens'));
%[w] = Screen('OpenWindow',screennum,[],[0 0 900 600],32); %debug Screen
[w, screenRect] = Screen(screennum,'OpenWindow',[],[],32);
HideCursor;

black=BlackIndex(w); % Should equal 0.
gray=WhiteIndex(w)/2;
white=WhiteIndex(w); % Should equal 255.
green=[0 210 0]; %0 220 0
red=[240 0 0];

% set up screen positions for stimuli
[wWidth, wHeight]=Screen('WindowSize', w); %new command taken from naomi's script.
xcenter=wWidth/2;
ycenter=wHeight/2;

Screen('FillRect', w, gray); %creates blank, Gray screen
Screen('Flip', w);

stim_rect=[xcenter-180 ycenter-180 xcenter+180 ycenter+180];
%spin_screen=Screen('OpenOffscreenWindow',w,white, screenRect);
Screen('TextSize',w,48);
Screen('TextFont',w,'Arial');

% Here we set the size of the arms of our fixation cross
fixCrossDimPix = 40;

% Now we set the coordinates (these are all relative to zero we will let
% the drawing routine center the cross in the center of our monitor for us)
xCoords = [-fixCrossDimPix fixCrossDimPix 0 0];
yCoords = [0 0 -fixCrossDimPix fixCrossDimPix];
allCoords = [xCoords; yCoords];

% Set the line width for our fixation cross
lineWidthPix = 7;

Screen('BlendFunction', w, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');



%% define run variables %%%%
%n_blocks=1;
%n_trials=7 % debug
n_trials=length(Prospect{run_number,Order});% should be 64;

if Scan == 0 %If Demo
    n_trials = 4;
end


rt=zeros(n_trials,2); % for each trial, there will 1 row with 2 columns. :,1=absolute start of trial :,2=rt
%reaction time for all trials of block would be rt(:,2)
resp=cell(n_trials,1); % 1 column, 85 rows, each row has one response
resp(:)={'NoResp'};

%
%     %%% FEEDBACK VARIABLES
%     if Scan==1,
%         trigger = KbName('t');
%         strongly_accept = KbName('y');
%         weakly_accept = KbName('g');
%         weakly_reject = KbName('r');
%         strongly_reject = KbName(',<');
%
%     else
%         strongly_accept='1';
%         weakly_accept='2';
%         weakly_reject='3';
%         strongly_reject='4';
%     end;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% get ready to go
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Show Instructions
% Screen('PutImage',w,Instructions_image);
% Screen(w,'Flip');


% noresp = 1;
% while noresp
%     [keyIsDown] = KbCheck(-1); % deviceNumber=keyboard
%     if keyIsDown && noresp
%         noresp = 0;
%     end
% end

if Scan==1 % MRI Scan
  
    fprintf('waiting for trigger...\n');

    % Draw the TTL fixation cross in red, set it to the center of our screen and
    % set good quality antialiasing
    Screen('DrawLines', w, allCoords, lineWidthPix, red, [xcenter ycenter], 2);
    Screen('Flip',w);
    while 1
        [keyIsDown,~,keyCode] = KbCheck(-1);
        if keyIsDown && keyCode(scannerKey)
            break;
        end
    end
    
    fprintf('got it!\n');
   


else % If using the keyboard, allow any key as input
    noresp=1;
    while noresp
        [keyIsDown,secs,keyCode] = KbCheck(-1);
        if keyIsDown && noresp
            noresp=0;
        end
    end
    WaitSecs(1.0);   % prevent key spillover--ONLY FOR BEHAV VERSION
    
end


DisableKeysForKbCheck(KbName('t'));   % So trigger is no longer detected

% -- command doesn't work in OSX? FlushEvents('keyDown');	 % clear any keypresses out of the buffer

% how screen() works:
% first argument: which screen to use (in this case, w, which is the main screen)
% second argument: what to do (in this case, 'DrawText')
% subsequent arguments depend upon what you've chosen to do

% if MRI==1
% noresp=1;
%        while noresp
%            [keyIsDown,secs,keyCode] = KbCheck(inputDevice);
%            if keyIsDown && noresp
% %                tmp=KbName(keyCode); % makes ok to use keyboard collection of 5, otherwise collects 5 but also %
% %                if strcmp(tmp(1),'t') %wait for '5' from trigger to begin
%                noresp=0;
% %                end
%            end
%            WaitSecs(0.001);
%        end


% Screen('DrawLines', w, allCoords, lineWidthPix, black, [xcenter ycenter], 2);
% Screen('Flip',w); % copy blank screen onto main window
% WaitSecs(2)

showme1 = zeros(64,1);
showme2 = zeros(64,1);
showme3 = zeros(64,1);
showme4 = zeros(64,1);
showme5 = zeros(64,1);
showme6 = zeros(64,1);
    
%pointer- runStart=GetSecs;

%%
run_anchor=GetSecs;

Screen('TextSize',w,52);

%%%%% Present trials for decision only phase

%if run_number<3,    %decision only runs are 1&2
runStart=GetSecs;

for trial=1:n_trials
    BinaryResp=0;
    showme6(trial) = GetSecs - run_anchor;
    
    while GetSecs - run_anchor < stimons{run_number,Order}(trial)
    end
    showme1(trial) = GetSecs - run_anchor;
    
    %while GetSecs - run_anchor < stim_onset(t), end; %don't start to execute what follows until the onset time for that trial is reached
    %%%% - need this command? Screen('CopyWindow',blank_screen,spin_screen); %clear screen
    Screen('FillRect', w, gray);
    Screen('Flip', w); % copy blank screen onto main window
    
    showme2(trial) = GetSecs - run_anchor;
    
    %draw gain/loss prospects
    Screen('DrawText',w,sprintf('+%d',Prospect{run_number,Order}(trial,2)),xcenter-150,ycenter-20,green); %gain: for row t (corresponds to trial #) in column 1 (run #)
    Screen('DrawText',w,sprintf('-%d',Prospect{run_number,Order}(trial,3)),xcenter+40,ycenter-20,red); %loss: for row t (corresponds to trial #) in column 1 (run #)
    
    %draw spinner
    Screen('FrameOval',w,black,stim_rect,3,3,[]); %Screen(windowPtr,'FrameOval',[color],[rect],[penWidth],[penHeight],[penMode])
    Screen('DrawLine',w,black,xcenter,ycenter-180,xcenter,ycenter+180,7);
    Screen('Flip',w);

    showme3(trial) = GetSecs - run_anchor;
    
    noresp=1;
    start_time=GetSecs;
    rt(trial,1)=start_time-run_anchor;
    while (GetSecs < start_time + stim_duration)
        [keyIsDown,secs,keyCode] = KbCheck(-1);
        
        if keyIsDown && noresp
            resp(trial)={KbName(keyCode)};
            rt(trial,2)=secs-start_time;
            noresp=0;
            Screen('FillRect', w, gray);
            Screen('Flip', w); % copy blank screen onto main window
        end
       
        WaitSecs(0.1);
    end
    showme4(trial) = GetSecs - run_anchor;  % checked difference between showme4 - showme1 and it equals stim_dur = 4 seconds; Good.
    
    Screen('DrawLines', w, allCoords, lineWidthPix, black, [xcenter ycenter], 2);
    Screen('Flip',w); % copy blank screen onto main window
    if iscell(resp{trial})
        resp{trial}=resp{trial}{1};
    end
    switch resp{trial}
        case {'y'}
            SubResponse = 'strongly_accept';
            BinaryResp=1;
        case {'g'}
            SubResponse = 'weakly_accept';
            BinaryResp=1;
        case {'r'}
            SubResponse = 'weakly_reject';
            BinaryResp=0;
        case {',<'}
            SubResponse = 'strongly_reject';
            BinaryResp=0;
        case {'ESCAPE'}
            exitExp = true;
            break;
        otherwise
            SubResponse ='NoResp';
    end
    if exitExp
        break;
    end
        
    % print trial info to logfile
    fprintf(fid1,'%d\t%d\t%0.3f\t%d\t%d\t%0.3f\t%s\n',trial,stimons{run_number,Order}(trial),rt(trial,1),
        Prospect{run_number,Order}(trial,2),-1*Prospect{run_number,Order}(trial,3),rt(trial,2),resp{trial});
    fprintf(fid2,'%d\t%s\t%d\t%d\t%d\t%0.3f\t%0.3f\t%d\t%d\t%s\t%0.3f\t%s\t%s\t%d\n',
    SubNumStr,ConditionName,Order,run_number,trial,stimons{run_number,Order}(trial),rt(trial,1),
    Prospect{run_number,Order}(trial,2),-1*Prospect{run_number,Order}(trial,3),gain_side,rt(trial,2),
    resp{trial},SubResponse,BinaryResp); %write the header line
    %fprintf('%d\t%s\n',trial,resp{trial});  % print responses to screen
end	%ends trial 'for' loop

if exitExp == 0

    %% End of Run

    Screen('TextSize',w,50);
    Screen('TextFont',w,'Arial');
    Screen('DrawText',w,'Fini',xcenter-200,ycenter);
    Screen('Flip',w);
    WaitSecs(2)
end

sca
fclose('all');
ShowCursor;
