function [trial, answer, anstime] = RunOneTrial(trial, data, iti, trans, fc,  ...
    datatypes, nwd, window, colour, prompt, xcenter, ycenter, mmultiply, nd, dotsize, leng, test)
% Usage:  trial = runOneTrial_single(trial, data, iti, trans, fc, fname, 
%    datatypes, nwd, window, colour, prompt, xcenter, ycenter)
% 
% Runs only one trial, of the "single" type. Called by e.g. runtrials_single
%
% INPUTS
% trial:            one trial passed to it by the equivalent runtrial
% data:             set of plds
% iti:              OPTIONAL: inter-trial-interval (time between trials). default=1
% trans:            OPTIONAL: margin(s) for random walker translation (multiplier x plot area) - if scalar then equal  
%                   x/y margins, if vector then (x,y) margins
% fc:               OPTIONAL: vector where element 1=duration of a centered fixation cross before each 
%							  trial, element 2=keep fixation cross on during trial (1) or not (0). 
%							  default=[0 0]
%                   NOTE: fixation cross time pre-trial counts as part of inter-trial interval time. 
%						  therefore fc(1) <= iti
% fname:            OPTIONAL: name of the file to store the data
%                             answers of subject and reaction times are stored in last two columns
%                             if no fname, no file output
%
% datatypes         cell array of the data type for each walker data set, indexed by data set index
%                   each cell='mm', 'md', 'cellmm', 'cellmd'
% nwd               number of dots in walker (usually 15) = # dots added to mask when walker is absent
% window:           pointer to open display window. if not passed, window is opened in here
% colour            colour shortcuts defined when display window is opened.
% xcenter, ycenter  center coords of window
%
% OUTPUTS
% trial            as input 'trial' except with two more cols:
%                   1	PLW 		1:	data index
%                   2               2:	azimuth, angular velocity
%                   3               3:	speed
%                   4               4:	size
%                   5               5:	scramble option
%                   6               6:	invert
%                   7               7:	scramble x range
%                   8               8:	scramble y range
%                   9               9:	x offset
%                   10              10:	y offset
%                   11              11: linear translation
%                   12	MASK PLW 	1:	SM: data index / LM: -1
%                   13              2:	SM: azimuth / LM: min speed
%                   14              3:	SM: speed / LM: max speed
%                   15              4:	SM: size (amplitude) / LM: dot lifetime
%                   16              5:	SM: scramble option
%                   17              6:	SM: invert/+90/-90 deg split
%                   18              7:	-
%                   19              8:	-
%                   20	# mask dots
%                   21	trial length
%                   22	dotsize(pixels) - if 0 then a default of 3 is used
%                   23	keyboard response code
%                   24	response latency
%
% Trial Parameters: extracted for each trial
%                   w1      index in data for walker
%                   mask    index for mask
%                   nd      # mask dots
%                   leng    length of display
%					dotsize	dot size
%
%Extract trial parameters
w1=trial(1:4);
mask=trial(5:8);
nd=nd;
leng = leng;
dotsize=dotsize;

% trials(tr,1)= walkerindex(m);
% trials(tr,2)= walkerdir(n);
% trials(tr,3)= walkerori(o);
% trials(tr,4)= walkercoh(p);
% trials(tr,5)= masktype(q);
% trials(tr,6)= masktdir(r);
% trials(tr,7)= maskori(s);
% trials(tr,8)= maskcoh(t);

%check orientation for prompt
wori = w1(3);


%Display trial
[answer, anstime, twstart, jitter]=PresentStimulus(data, datatypes, w1, mask, leng, dotsize, nd, trans, nwd, fc, xcenter, ycenter, window, colour, mmultiply);
Screen('FillRect',window,colour.black);                 %Clear screen
Screen('flip',window);

%Get End of Stimulus time
EndStimTime = GetSecs; 
EndTrialTime = EndStimTime + iti; %this will correspond to the isi, not the iti

%Prompt and get response
if leng > 0                                          %(If leng=0 then we did this inside pptwalk)
    
    %insert fixation on start of each response prompt
    if fc(1) > 0;
        %Display the fixation cross
        Screen('Drawline',window, colour.white, xcenter, ycenter-10, xcenter, ycenter+10);
        Screen('Drawline',window, colour.white, xcenter-10, ycenter, xcenter+10, ycenter);
        Screen('flip',window);
        %WaitSecs(fc(1));
    end;
    
    %disp_text(window, text, colour.white, colour.black)
    %disp_prompt(window,wori,colour.white,colour.black);   %Display prompt
    %Screen('flip',window);
    t0=GetSecs;                                         %Start timer for anstime
    
    if 1 == 1%strcmp(computer, 'PCWIN64')
        %get_key(keys, wait, response_end);
        if test == 1; % in the lab
            [answer, anstime]=get_key([37 39 27], 2, EndTrialTime);          %Wait for left- or right-arrow to be pressed
        else
            
            keyscan1 = KbName('y');
            keyscan2 = KbName('g');
            [answer, anstime]=get_key([keyscan1 keyscan2 27], 2, EndTrialTime);
        end
        if answer == 27
            Screen('CloseAll')
            error('Display halted by ESC key')
        end
    else
        [answer, anstime]=get_key([79 80 41], 2, EndTrialTime);
        if answer == 41
            Screen('CloseAll')
            error('Display halted by ESC key')
        end
    end
    
    anstime=anstime-t0;
    %     Screen('FillRect',window,colour.black);             %Clear screen
    %     Screen('flip',window);

    %check and wait for end of trial
    if GetSecs < EndTrialTime
        while GetSecs < EndTrialTime
            %wait it out
        end
    end
end

%Record response and latency / and phase start
trial(9)=answer;
trial(10)=anstime;
trial(11)=twstart;
trial(12)=jitter(1);
trial(13) =jitter(2);


