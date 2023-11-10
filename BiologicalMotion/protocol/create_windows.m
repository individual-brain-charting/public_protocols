function [window, colour]=create_windows

%[window, colour]=create_windows
%
%Open display window and also set colour shortcuts
%
%OUTPUTS
%window     pointer to display window
%colour     colour shortcuts which are [R G B] CLUT indeces: colour.red, .white, .darkblue, .lightblue, .green, .black

%Create colour shortcuts (RGB, or equipixel CLUT row index scalar)
colour.red=[150 0 0];
colour.white=[255,255,255];
colour.darkblue=[0 0 200];
colour.lightblue=[0 100 255];
colour.green=[0 200 0];
colour.black=[0,0,0];

Screen('Preference', 'VisualDebuglevel', 3);
Screen('Preference', 'SkipSyncTests', 1);

%Open window
Screen('closeall');
window=Screen('OpenWindow',0,colour.black);
%window=Screen('OpenWindow',max(Screen('Screens')),colour.black);
Screen('flip',window);                      %Clear screen
HideCursor