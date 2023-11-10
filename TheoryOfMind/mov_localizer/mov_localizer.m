function mov_localizer(subjID)

%% Version: Nov 25, 2015
%__________________________________________________________________________
%
% This script will localize theory-of-mind network areas and pain matrix
% areas by contrasting activation during scenes in which characters are
% engaging in mentalizing (mental) and action/pain sequences (pain).
%
% To run this script, you need Matlab and the PsychToolbox, which is available
% as a free download. Make sure to follow the GStreamer instructions if prompted 
% in order to make movie screening from PsychToolbox work.
%
% In addition, you will need to purchase the movie "Partly Cloudy" from
% Pixar Animation Studios. Save a copy of "Partly Cloudy" in the stimuli folder 
% as "partly_cloudy.mov". For timing purposes, the movie file is 5:49
% seconds.
%__________________________________________________________________________
%
%							INPUTS
%
% - subjID: STRING The string you wish to use to identify the participant. 
%			"PI name"_"study name"_"participant number" is a common
%			convention. This will be the name used to save the files.
%
% Example usage: 
%					mov_localizer('SAX_MOV_01')
%
%__________________________________________________________________________
%
%							OUTPUTS
%	The script outputs a behavioural file into the behavioural directory.
%	This contains information about the IPS of the scan, and the coded 
%   timing of events in the movie. It also contains information necessary 
%   to perform the analysis with SPM. The file is saved as 
%   subjectID.mov.1.m
%
%__________________________________________________________________________
%
%						  CONDITIONS 
%
%				1 - mental - characters mentalizing (events)
%				2 - pain - characters in physical pain (events)
%               3 - social - non-main characters interacting (events)
%               4 - control - scenery, no focus on characters (events)
%
%__________________________________________________________________________
%
%							TIMING
%
%   time = 5:59 - including fixation before movie and credits
%   IPS = 180 - can be made shorter if you stop scan during credits
%__________________________________________________________________________
%
%							NOTES
%
%	Note 1
%		Make sure to change the inputs in the 'Variables unique to scanner/
%		computer' section of the script. 
%
%__________________________________________________________________________
%
%					ADVICE FOR ANALYSIS
%	We analyze this experiment by modelling coded events as a trial block 
%   with a boxcar lasting the event duration.
%
%	Analysis consists of five primary steps:
%		1. Motion correction by rigid rotation and translation about the 6 
%		   orthogonal axes of motion.
%		2. (optional) Normalization to the SPM template. 
%		3. Smoothing, FWHM, 5 mm smoothing kernel if normalization has been
%		   performed, 8 mm otherwise.
%		4. Modeling
%				- Each condition in each run gets a parameter, a boxcar
%				  plot convolved with the standard HRF.
%				- The data is high pass filtered (filter frequency is 128
%				  seconds per cycle)
%		5. A simple contrast and a map of t-test t values is produced for 
%		   analysis in each subject. We look for activations thresholded at
%		   p < 0.001 (voxelwise) with a minimum extent threshold of 5
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
%   SPM.xBF.T0         = 8                 	reference time bin - samples to the middle of TR 
%	SPM.xBF.UNITS      = 'scans'			OPTIONS: 'scans'|'secs' for onsets
%	SPM.xBF.Volterra   = 1					OPTIONS: 1|2 = order of convolution; 1 = no Volterra
%__________________________________________________________________________
%
%	Created by Jorie Koster-Hale and Nir Jacoby
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
[rootdir b c]		= fileparts(mfilename('fullpath'));			% path to the directory containing the behavioural / stimuli directories. If this script is not in that directory, this line must be changed 
triggerKey			= 't';										% this is the value of the key the scanner sends to the presentation computer

KbName('UnifyKeyNames');
key_escape = KbName('escape');

%% Set up necessary variables
orig_dir			= pwd;
stimdir       = fullfile(rootdir, 'stimuli');
behavdir			= fullfile(rootdir, 'behavioural');
moviefName    = fullfile(stimdir, 'partly_cloudy.mp4');

restDur = 10;  %fixation time before movie. we stopped scanning in the middle of credits, so no post movie fixation
movieDur = 336;
TR = 2;
ips = (restDur + movieDur)/TR;  

%% check if it was run before shuffle order of stories
bfname = [subjID '.movloc.1.mat'];
if exist(fullfile(behavdir,bfname),'file')
    rerunflag = questdlg('Behavioural file already exist, do you want to re-run the current subject/run? Old behavioural file will be overwritten','Run again?','Yes','No','No');
    if ~strcmp(rerunflag,'Yes')
        error('Repeated subject/run command aborted');
    end
end

%% Verify that all necessary files and folders are in place. 
if isempty(dir(stimdir))
	uiwait(warndlg(sprintf('Your stimuli directory is missing! Please create directory %s and populate it with stimuli. When Directory is created, hit ''Okay''',stimdir),'Missing Directory','modal'));
end
if ~exist(moviefName)
    error('Your stimuli is missing. please copy the movie file to the stimuli folder and try again.');
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

%% Psychtoolbox
%  Here, all necessary PsychToolBox functions are initiated and the
%  instruction screens are set up.
try
  %% Use only for Matlab
	%PsychJavaTrouble;
    Screen('Preference', 'SkipSyncTests', 1);
	displays    = Screen('screens');
  %% Full screen
  [w, wRect]  = Screen('OpenWindow',displays(end),0);
  %% For debugging
  %[w, wRect] = Screen('OpenWindow', displays(end), 0, [100, 100, 800, 600]);
  HideCursor()
	scrnRes     = Screen('Resolution',displays(end));               % Get Screen resolution
	[x0 y0]		= RectCenter([0 0 scrnRes.width scrnRes.height]);   % Screen center.
	Screen(   'Preference', 'SkipSyncTests', 0);                       
	Screen(w, 'TextFont', 'Helvetica');                         
	Screen(w, 'TextSize', 22);
  Screen(w, 'TextStyle', 1);
  instructions = 'Veuillez patienter pendant le chargement du film.';  
  DrawFormattedText(w, instructions, 'center' , 'center', 255,70);  % original instructions was "Get Ready!" size 40
	Screen(w, 'Flip');												% Instructional screen is presented.
  %% Block to load cross image and wait for the TTL %%
  while 1
    [keyIsDown, secs, keyCode] = KbCheck;
    if keyIsDown == 1 && keyCode(KbName('return')) == 1;
      break
    end
  end
  % load cross
  pic_cross = Screen('MakeTexture', w, imread('../Cross.bmp'));
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

%% Open movie file
[movie movieduration fps imgw imgh] = Screen('OpenMovie', w, moviefName);
rate = 1;
%% wait for the 1st trigger pulse
while 1
  [keyIsDown, secs, keyCode] = KbCheck;
  if keyIsDown == 1 && keyCode(KbName(triggerKey)) == 1;
    break
  end
end
Screen(w, 'Flip');


%% Main Experiment
experimentStart = GetSecs;

% pause for opening fixation
while GetSecs - experimentStart < restDur; 
  [keyIsDown,secs,keyCode]	= KbCheck;	% check to see if a ESC key is being pressed
  if keyCode(key_escape) == 1
    break;
  end;
end 

%% present movie

% Set the fifth argument to 1.0 if you want to unmute the video
Screen('PlayMovie', movie, rate, 0, 0);
trialStart = GetSecs;
timing_adjustment = trialStart - experimentStart;

while(GetSecs - trialStart < movieDur -.2)
    [keyIsDown,secs,keyCode]	= KbCheck;	% check to see if a ESC key is being pressed
    if keyCode(key_escape) == 1
      break;
    end;
    % Wait for next movie frame, retrieve texture handle to it
    tex = Screen('GetMovieImage', w, movie);
    % Valid texture returned? A negative value means end of movie reached:
    if tex<=0
        % done, break
        break;
    end;
    % Draw the new texture immediately to screen:
    Screen('DrawTexture', w, tex);
    % Update display:
    Screen(w, 'Flip');
    % Release texture:
    Screen('Close', tex);
end

Screen('CloseMovie', movie);
Screen(w, 'Flip');

%% Rest period before finishing acquisition
movieEnd = GetSecs;

while GetSecs - movieEnd < restDur; 
  [keyIsDown,secs,keyCode]	= KbCheck;	% check to see if a ESC key is being pressed
  if keyCode(key_escape) == 1
    break;
  end;
end 

experimentEnd		= GetSecs;
experimentDuration	= experimentEnd - experimentStart;

%% Analysis Info

% Movie coding for official pixar file by conditions. 
% Original coding as we used in the analysis reported in Jacoby et al (2015). 
% All timings in seconds and assume 10 sec fixation before movie
conds(1).names = 'mental';
conds(2).names = 'pain';
conds(1).onsets = [80, 93, 124, 184, 249, 262, 306]; % mental
conds(2).onsets = [69, 85, 106, 134, 172, 210, 236, 276, 332]; % pain
conds(1).durs = [10, 16, 6, 14, 8, 10, 4]; % mental
conds(2).durs = [10, 18, 12, 6, 6, 10, 4, 4, 4]; % pain


try
	sca
    cd(behavdir);
	save(bfname,'subjID','timing_adjustment','trialStart','experimentStart','experimentDuration','ips','conds','restDur');
	ShowCursor;
	cd(orig_dir);
catch exception
	sca
	ShowCursor;
	warndlg(sprintf('The experiment has encountered the following error while saving the behavioral data: %s',exception.message),'Error');
	cd(orig_dir);
end

end %main function
