function alltrials=RunTrials(alltrials, data, iti, trans, fc, mmultiply, nd, dotsize, leng, test);

%
% PARAMETERS
prompt = ' <- | -> '; %Text prompt after each trial

rand('state',sum(100*clock));                               %Initialise the random generator

%Set input variable defaults if necessary
if fc==0; fc=[0 0]; end
%trials(find(trials(:,22)==0),22)=3;                         %Dot size
if fc(1) > iti; fc(1)=iti; end
if length(trans)==1; trans=[trans trans]; end;              %If trans=scalar, generalizes it to an (x,y) pair



%Get data types
datatypes=getdatatypes(data);

%Disable all the lines of warning (usually irrelevant) outputted by Screen.
%oldEnableMode = Screen('Preference', 'SuppressAllWarnings', 1);

%Open window and create colour shortcuts
[window, colour]=create_windows;

%Set font and size
Screen('TextFont',window,'Courier New');
Screen('TextSize',window,40);

%Get window centre
windowsize=Screen('Rect',0);                                % window-coordinates, e.g. [0 0 1024 768]
xcenter=round(windowsize(3)/2);                             % center of window
ycenter=round(windowsize(4)/2);


nwd = 0;

%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Trigger:
% DC @ MNI
% We are using USB box and waiting for a '5' - ie , use GetChar
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Trigger1 = KbName('s');  %'space'
Trigger2 = 13; %'return'
%Trigger3 = 84; %'t'
is_true = 0;

Screen('Drawline',window, colour.red, xcenter, ycenter-10, xcenter, ycenter+10);
Screen('Drawline',window, colour.red, xcenter-10, ycenter, xcenter+10, ycenter);
Screen('flip',window);

if (test)

    while (is_true == 0)
        [keyIsDown,junk4,keyCode] = KbCheck;
        if keyCode(Trigger1) || keyCode(Trigger2)
            is_true = 1;
        end
    end

else  %we're at scanner

    Trigger3 = KbName('t');
    while (is_true == 0)

        [a,b,keyCode] = KbCheck;
        if keyCode(Trigger3)
            is_true = 1;
        end

    end
    FlushEvents('keyDown')
end
%%

Screen('Preference', 'VisualDebuglevel', 3); %HB%

starttime = GetSecs;
%start by fixating

%Display the fixation cross
Screen('Drawline',window, colour.white, xcenter, ycenter-10, xcenter, ycenter+10);
Screen('Drawline',window, colour.white, xcenter-10, ycenter, xcenter+10, ycenter);
Screen('flip',window);
WaitSecs(5 + 16);
%HB% WaitSecs(4);


for a = 1:length(alltrials); %loop through blocks


    trials = alltrials{a};


    blockstarttime = GetSecs;
    blockendtime = blockstarttime + 16 + 16;
    %HB% blockendtime = blockstarttime + 4 + 2;

    for i=1:size(trials,1);                                     %Loops through trials - one row in 'trials' for each trial
        trialResponses(i,:) = RunOneTrial(trials(i,:), data, iti, trans, fc, ...
            datatypes, nwd, window, colour, prompt, xcenter, ycenter, mmultiply, nd, dotsize, leng, test);
        %WaitSecs(iti-fc(1));                                    %Wait for next trial, allowing time for fixation cross if selected
    end;
    trials = trialResponses;
    alltrials{a} = trials;


    %pause and fixate
    %Display the fixation cross
    Screen('Drawline',window, colour.white, xcenter, ycenter-10, xcenter, ycenter+10);
    Screen('Drawline',window, colour.white, xcenter-10, ycenter, xcenter+10, ycenter);
    Screen('flip',window);

    if GetSecs < blockendtime
        while GetSecs < blockendtime
            %wait it out
        end
    end
end


endtime = GetSecs;
totaltime = endtime-starttime
%save totaltime totaltime
Screen('CloseAll')
%Screen('Preference', 'SuppressAllWarnings', oldEnableMode);
