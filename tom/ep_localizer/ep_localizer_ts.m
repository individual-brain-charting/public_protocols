function ep_localizer_ts(subjID, run)
%% Version: November 25, 2015
%__________________________________________________________________________
%
% This script will localize theory-of-mind network areas and pain matrix
% areas by contrasting activation during stories in which characters are
% suffering from emotional pain (EP) and physical pain (PP).
%
% There are blocks of emotional pain (EP) stories, in which a story is told
% involving a false belief, which is presented for 12 seconds, then a
% response prompt appears for 4 seconds in which the subject is required to rank
% the protagonists' level of suffering.
%
% To run this script, you need Matlab and the PsychToolbox, which is available
% as a free download. 
%
%__________________________________________________________________________
%
%							INPUTS
%
% - subjID: STRING The string you wish to use to identify the participant. 
%			"PI name"_"study name"_"participant number" is a common
%			convention. This will be the name used to save the files.
% - run   : NUMBER The current run number. (e.g., 1) 
%
% Example usage: 
%					ep_localizer('SAX_EPL_01',1)
%
%__________________________________________________________________________
%
%							OUTPUTS
%	The script outputs a behavioural file into the behavioural directory.
%	This contains information about the IPS of the scan, when stories were
%	presented, reaction time, and response info. It also contains
%	information necessary to perform the analysis with SPM. The file is
%	saved as subjectID.eploc.run#.m
%
%	In the event of a crash, the script creates a running behavioural file
%	of partial data after each trial. 
%__________________________________________________________________________
%
%						  CONDITIONS 
%
%				1 - EP - Emotional Pain stories (10 total)
%				2 - PP - Physical Pain stories (10 total)
%
%__________________________________________________________________________
%
%							TIMING
%
% The run length can be calculated according to the following:
%
% (trials per run)*(fixation duration + story duration)+(fixation duration)
% 
% The phrases used above are related to the variable values according to
% the following:
%
% trials per run = trialsPerRun
% fixation duration = fixDur
% story duration = storyDur
%
% The default configuration is:
%
% (10 trials per run) * (12 sec fixation + 16 sec story) + (12 sec
% fixation) =
%
% 10 * (12 + 16) + 12 = 292 seconds, 146 ips (given 2 sec TR)
%__________________________________________________________________________
%
%							NOTES
%
%	Note 1
%		Make sure to change the inputs in the 'Variables unique to scanner/
%		computer' section of the script. 
%
%	Note 2
%		The use of intersect(89:92, find(keyCode)) determines if the
%		keystroke found by KbCheck is one of the proper response set. Of
%		course, these intersection values are a consequence of the workings
%		of our MRI response button. Your response button may differ. 
%		Use KbCheck() to determine which button pushes from the response box
%		correspond to numbers 1:4. Otherwise, you may not retain any 
%		behavioural data.
%
%	Note 3
%		For simplicity, we have set up the experiment so that the order of
%		items and conditions is identical for every subject - they see
%		design 1 in run 1, with stimuli 1 - 5 form each condition, in that 
%		order. In our own research, we typically counterbalance the order 
%		of items within a run, and the order of designs across runs, across
%		subjects (so half of our participants see design 1 in run 2). If 
%		you are comfortable enough with matlab, we encourage you to add 
%		this counterbalancing back into the experiment - and make sure to 
%		save separate variables for each subject tracking the order of 
%		items and conditions across runs.
%__________________________________________________________________________
%
%					ADVICE FOR ANALYSIS
%	We analyze this experiment by modelling each trial as a block with a
%	boxcar lasting 16 seconds, during the whole period from the initial
%	presentation of the story to the end of the reponse presentation.
%	These boxcars are flanked by non-jittered rest periods of 12 seconds
%	each (the fixation duration in the script).
%
%	Analysis consists of five primary steps:
%		1. Motion correction by rigid rotation and translation about the 6 
%		   orthogonal axes of motion.
%		2. (optional) Normalization to the MNI template. 
%		3. Smoothing, FWHM, 5 mm smoothing kernel if normalization has been
%		   performed, 8 mm otherwise.
%		4. Modeling
%				- Each condition in each run gets a parameter, a boxcar
%				  plot convolved with the standard HRF.
%				- The data is high pass filtered (filter frequency is 128
%				  seconds per cycle)
%		5. A simple contrast and a map of t-test t values is produced for 
%		   analysis in each subject. We look for activations thresholded at
%		   p < 0.001 (voxelwise) with a minimum extent threshold of 10
%		   contiguous voxels. 
%
%	Random effects analyses show significant results with n > 10
%	participants, though it should be evident that the experiment is
%	working after 3 - 5 individuals.
%__________________________________________________________________________
%
%					SPM Parameters
%
%	If using scripts to automate data analysis, these parameters are set in
%	the SPM.mat file prior to modeling or design matrix configuration. 
%
%	SPM.xGX.iGXcalc    = {'Scaling'}		global normalization: OPTIONS:'Scaling'|'None'
%	SPM.xX.K.HParam    = filter_frequency   high-pass filter cutoff (secs) [Inf = no filtering]
%	SPM.xVi.form       = 'none'             intrinsic autocorrelations: OPTIONS: 'none'|'AR(1) + w'
%	SPM.xBF.name       = 'hrf'				Basis function name 
%	SPM.xBF.T0         = 8                 	reference time bin - samples to the middle of TR 
%	SPM.xBF.UNITS      = 'scans'			OPTIONS: 'scans'|'secs' for onsets
%	SPM.xBF.Volterra   = 1					OPTIONS: 1|2 = order of convolution; 1 = no Volterra
%__________________________________________________________________________
%
%	Stimuli created by Rebecca Saxe & Emile Bruneau
%	Script by Nir Jacoby (jacobyn@mit.edu), November 2015
%
% Adapted for the Individual Brain Charting Project by Ana Luisa Pinho
% email: ana.pinho@inria.fr
% January 2018
%__________________________________________________________________________
%
%					Changelog
% 
%__________________________________________________________________________
%
%% Variables unique to scanner / computer

[rootdir b c]		= fileparts(mfilename('fullpath'));			% path to the directory containing the behavioural / stimuli directories. If this script is not in that directory, this line must be changed. 

% keys
triggerKey			= 't';										% this is the value of the key the scanner sends to the presentation computer
ans_none        = 'a';
ans_little      = 'z';
ans_moderate    = 'o';
ans_a_lot       = 'p';

KbName('UnifyKeyNames');

%% Numeric values of the keys
key_ans_none     = KbName(ans_none);
key_ans_little   = KbName(ans_little);
key_ans_moderate = KbName(ans_moderate);
key_ans_a_lot    = KbName(ans_a_lot);
key_escape       = KbName('escape');
key_enter        = KbName('return')(1);
trigger_code     = KbName(triggerKey);

%% Set up necessary variables
orig_dir			= pwd;
stimdir			  = fullfile(rootdir, 'training_sess_french');
behavdir			= fullfile(rootdir, 'behavioural');
designs				= [ 1 2 2 1 ; ];
design				= designs(run,:);
conds				  = {'EP','PP'};

% === Original values for duration of the conditions
fixDur				= 12;									% fixation duration
storyDur			= 12;								  % story duration
responseDur		=  6;									% probe duration
% === Values of conditions for debugging
% fixDur				= 4;
% storyDur			= 4;
% responseDur		= 2;

trialsPerRun		= length(design);
key					    = zeros(trialsPerRun,1);
RT					    = zeros(trialsPerRun,1);
items				    = zeros(trialsPerRun,2);
trialsOnsets    = zeros(trialsPerRun,1);                                      % trial onsets in seconds
ips					    = ((trialsPerRun) * (fixDur + storyDur + responseDur) + (fixDur))/2;


%% Verify that all necessary files and folders are in place. 
if isempty(dir(stimdir))
	uiwait(warndlg(sprintf('Your stimuli directory is missing! Please create directory %s and populate it with stimuli. When Directory is created, hit ''Okay''',stimdir),'Missing Directory','modal'));
end
if isempty(dir(behavdir))
	outcome = questdlg(sprintf('Your behavioral directory is missing! Please create directory %s.',behavdir),'Missing Directory','Okay','Do it for me','Do it for me');
	if strcmpi(outcome,'Do it for me')
		mkdir(behavdir);
		if isempty(dir(behavdir))
			warndlg(sprintf('Couldn''t create directory %s!',behavdir),'Missing Directory');
			return
		end
	else
		if isempty(dir(behavdir))
			return
		end
	end
end
cd(stimdir);
load('PP_ts.mat'); load('EP_ts.mat'); 

%% Psychtoolbox
%  Here, all necessary PsychToolBox functions are initiated and the
%  instruction screens are set up.
try
  %% Use only for Matlab
	% PsychJavaTrouble;
  Screen('Preference', 'SkipSyncTests', 1);
	disp        = max(Screen('Screens'));
  %% Full screen
	[w, wRect]  = Screen('OpenWindow',disp,0);
  %% For debugging
  %[w, wRect] = Screen('OpenWindow', disp(1), [], [100, 100, 800, 600]);
  HideCursor()
	[x0 y0]		= RectCenter(wRect);   % Screen center.
	Screen('Preference', 'SkipSyncTests', 0);     %might need to change to 1, depending on your operating system
  % On Windows, use (uncomment) the next command line
  Screen('Preference','TextEncodingLocale','UTF-8');
	Screen(w, 'TextFont', 'Helvetica');                         
	Screen(w, 'TextSize', 45);
  Screen(w, 'TextStyle', 1);
    instr_1 = sprintf("Lisez les histoires suivantes. Lorsque le message s'affiche sur l'écran,");
    instr_2 = sprintf("appuyez sur le bouton selon le niveau de douleur ou de souffrance"); 
    instr_3 = sprintf("que le protagoniste de l'histoire ressent à ce moment.");    
    instr_4 = sprintf("Le niveau de douleur ou de souffrance ressenti par le protagoniste est:");
    Screen(w, 'DrawText', instr_1, x0-700, y0-200, [255]);
    Screen(w, 'DrawText', instr_2, x0-700, y0-150,[255]);
    Screen(w, 'DrawText', instr_3, x0-700, y0-100,[255]);
    Screen(w, 'DrawText', instr_4, x0-700, y0+30, [255]);
    Screen(w, 'Flip');			% Instructional screen is presented.
    while 1
      [keyIsDown, secs, keyCode] = KbCheck;
      if keyIsDown == 1 && keyCode(key_ans_none) == 1;
        break
      end
    end
    Screen(w, 'DrawText', instr_1, x0-700, y0-200, [255]);
    Screen(w, 'DrawText', instr_2, x0-700, y0-150,[255]);
    Screen(w, 'DrawText', instr_3, x0-700, y0-100,[255]);
    Screen(w, 'DrawText', instr_4, x0-700, y0+30, [255]);  
    instr_5 = sprintf("(1) Aucun");
    Screen(w, 'DrawText', instr_5, x0-700, y0+80, [255]);
    Screen(w, 'Flip');			% Instructional screen is presented.
    while 1
      [keyIsDown, secs, keyCode] = KbCheck;
      if keyIsDown == 1 && keyCode(key_ans_little) == 1;
        break
      end
    end
    Screen(w, 'DrawText', instr_1, x0-700, y0-200, [255]);
    Screen(w, 'DrawText', instr_2, x0-700, y0-150,[255]);
    Screen(w, 'DrawText', instr_3, x0-700, y0-100,[255]);
    Screen(w, 'DrawText', instr_4, x0-700, y0+30, [255]);
    Screen(w, 'DrawText', instr_5, x0-700, y0+80, [255]);
    instr_6 = sprintf("(2) Faible");
    Screen(w, 'DrawText', instr_6, x0-400, y0+80, [255]);
    Screen(w, 'Flip');			% Instructional screen is presented.
    while 1
      [keyIsDown, secs, keyCode] = KbCheck;
      if keyIsDown == 1 && keyCode(key_ans_moderate) == 1;
        break
      end
    end
    Screen(w, 'DrawText', instr_1, x0-700, y0-200, [255]);
    Screen(w, 'DrawText', instr_2, x0-700, y0-150,[255]);
    Screen(w, 'DrawText', instr_3, x0-700, y0-100,[255]);
    Screen(w, 'DrawText', instr_4, x0-700, y0+30, [255]);
    Screen(w, 'DrawText', instr_5, x0-700, y0+80, [255]);
    Screen(w, 'DrawText', instr_6, x0-400, y0+80, [255]);
    instr_7 = sprintf("(3) Modéré");
    Screen(w, 'DrawText', instr_7, x0-100, y0+80, [255]);
    Screen(w, 'Flip');			% Instructional screen is presented.
    while 1
      [keyIsDown, secs, keyCode] = KbCheck;
      if keyIsDown == 1 && keyCode(key_ans_a_lot) == 1;
        break
      end
    end
    Screen(w, 'DrawText', instr_1, x0-700, y0-200, [255]);
    Screen(w, 'DrawText', instr_2, x0-700, y0-150,[255]);
    Screen(w, 'DrawText', instr_3, x0-700, y0-100,[255]);
    Screen(w, 'DrawText', instr_4, x0-700, y0+30, [255]);
    Screen(w, 'DrawText', instr_5, x0-700, y0+80, [255]);
    Screen(w, 'DrawText', instr_6, x0-400, y0+80, [255]);
    Screen(w, 'DrawText', instr_7, x0-100, y0+80, [255]);  
    instr_8 = sprintf("(4) Beaucoup");
    Screen(w, 'DrawText', instr_8, x0+200, y0+80, [255]);
	  Screen(w, 'Flip');		 % Instructional screen is presented.
    %% Block to load cross image and wait for the TTL %%
    while 1
      [keyIsDown, secs, keyCode] = KbCheck;
      if keyIsDown == 1 && keyCode(key_enter) == 1;
        break
      end
    end
    % load cross
    pic_cross = Screen('MakeTexture', w, imread('../../Cross.bmp'));
    rect_cross = CenterRectOnPoint(Screen('Rect',pic_cross),x0,y0);
    Screen(w,'DrawTexture',pic_cross,[],rect_cross);
    Screen(w, 'Flip');
    %% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
catch exception
	ShowCursor;
	sca;
	warndlg(sprintf('PsychToolBox has encountered the following error: %s',exception.message),'Error');
	return
end

%% Wait for the trigger.
%  If your scanner does not use a '+' as a trigger pulse, change the value 
%  of triggerKey accordingly. 

while 1
  [keyIsDown, secs, keyCode] = KbCheck;
  if keyIsDown == 1 && keyCode(trigger_code) == 1;
    break
  end
end

%% Main Experimental Loop
counter				= zeros(1,2)+(5*(run-1));
experimentStart		= GetSecs;
try
	for trial = 1:trialsPerRun
		cd(stimdir);
		trialStart		= GetSecs;
		empty_text		= ' ';
		Screen(w, 'DrawText', empty_text,x0,y0);
		Screen(w, 'Flip');
		counter(1,design(trial)) = counter(1,design(trial)) + 1;

		%%%%%%%%% Prepare Story for presentation while displaying fixation %%%%%%%%%
		trialT = char(conds(design(trial)));
        storynumber = counter(1,design(trial));
        story = eval(sprintf('%s{%d}',trialT,storynumber));
        items(trial,1)	= design(trial);
		items(trial,2)	= storynumber;
        
        spaces = find(story == ' ');
        breakpoint = spaces(ceil(length(spaces)/5));
        spaces_index = find(spaces==breakpoint);
        line_1 = story(1:spaces(spaces_index)-1);
        line_2 = story(spaces(spaces_index)+1:spaces(spaces_index*2) - 1);
        line_3 = story(spaces(spaces_index*2)+1:spaces(spaces_index*3) - 1);
        line_4 = story(spaces(spaces_index*3)+1:spaces(spaces_index*4) - 1);
        line_5 = story(spaces(spaces_index*4)+1:end);
    
		while GetSecs - trialStart < fixDur;    % wait for fixation period to elapse
      [keyIsDown,secs,keyCode]	= KbCheck;	% check to see if a ESC key is being pressed
      assert(keyCode(key_escape) == 0);     % raise exception if ESC key was pressed
    end					
        
        %%%%%%%%% Display Story %%%%%%%%% 
        %Screen('Preference','TextEncodingLocale','fr_FR.utf8')
        Screen(w,'TextSize',45);
        Screen(w,'DrawText',line_1,x0-700,y0-250,255);
        Screen(w,'DrawText',line_2,x0-700,y0-200,255);
        Screen(w,'DrawText',line_3,x0-700,y0-150,255);
        Screen(w,'DrawText',line_4,x0-700,y0-100,255);
        Screen(w,'DrawText',line_5,x0-700,y0-50,255);
        %Screen('Preference','Verbosity', 10)
		Screen(w, 'Flip');										
        trialsOnsets (trial,1) = GetSecs-experimentStart;
        
        while GetSecs - trialStart < fixDur + storyDur; 
          [keyIsDown,secs,keyCode]	= KbCheck;	% check to see if a ESC key is being pressed
          assert(keyCode(key_escape) == 0);     % raise exception if ESC key was pressed
        end			% wait for story presentation period
		
        %%%%%%%%% Prepare  Response %%%%%%%%%
        question = sprintf('Le niveau de douleur ou de souffrance ressenti par le protagoniste est:');
        answers = sprintf('(1) Aucun    (2) Faible    (3) Modéré    (4) Beaucoup');
        
        Screen(w,'TextSize',45);
        Screen(w,'DrawText',line_1,x0-700,y0-250,255);
        Screen(w,'DrawText',line_2,x0-700,y0-200,255);
        Screen(w,'DrawText',line_3,x0-700,y0-150,255);
        Screen(w,'DrawText',line_4,x0-700,y0-100,255);
        Screen(w,'DrawText',line_5,x0-700,y0-50,255);
        Screen(w,'DrawText',question,x0-700, y0+50,255);
        Screen(w,'DrawText',answers,x0-700,y0+100,255);

		%%%%%%%%% Display Response %%%%%%%%%
		Screen(w, 'Flip');

		responseStart	= GetSecs;

		%%%%%%%%% Collect Response %%%%%%%%%
		while ( GetSecs - responseStart ) < responseDur 
			[keyIsDown,secs,keyCode]	= KbCheck;					% check to see if a ESC key is being pressed
      assert(keyCode(key_escape) == 0);             % raise exception if ESC key was pressed
			%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			%--------------------------SEE NOTE 2-----------------------------%
			%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			button						= intersect([key_ans_none,key_ans_little,key_ans_moderate,key_ans_a_lot], find(keyCode));   
			if(RT(trial,1) == 0) & ~isempty(button)
				RT(trial,1)				= GetSecs - responseStart;
%				key(trial,1)			= str2num(KbName(button));
				key(trial,1)			= button;
			end
		end

		%%%%%%%%% Save information in the event of a crash %%%%%%%%%
		cd(behavdir);
		save([subjID '.eploc.' num2str(run) '.mat'],'subjID','run','design','items','key','RT','trialsOnsets','fixDur','storyDur','responseDur');
	end
catch exception
	ShowCursor;
	sca
	warndlg(sprintf('The experiment has encountered the following error during the main experimental loop: %s',exception.message),'Error');
	return
end

%% Final fixation
Screen(w, 'Flip');
trials_end			= GetSecs;
while GetSecs - trials_end < fixDur; end;

experimentEnd		= GetSecs;
experimentDuration	= experimentEnd - experimentStart;
numconds			= length(conds);

try
	sca
	responses = sortrows([items key RT]);
	save([subjID '.eploc.' num2str(run) '.mat'],'subjID','run','design','items','key','RT','trialsOnsets','responses','experimentDuration','ips','fixDur','storyDur','responseDur');
	ShowCursor;
	cd(orig_dir);
catch exception
	sca
	ShowCursor;
	warndlg(sprintf('The experiment has encountered the following error while saving the behavioral data: %s',exception.message),'Error');
	cd(orig_dir);
end					% end main function
cd(pwd)

