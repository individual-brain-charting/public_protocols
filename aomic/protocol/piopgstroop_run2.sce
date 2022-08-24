## Edited for IBC Dec, 2021 ##
## Himanshu Aggarwal, himanshu.aggarwal@inria.fr ##

scenario = "piopgstroop_run2";

scenario_type = fMRI;
pulses_per_scan = 1;
pulse_code = 255;
#scenario_type = fMRI_emulation;
#scan_period = 2000;

response_matching = simple_matching; 
active_buttons = 4;
button_codes = 1, 2, 3, 4;
default_background_color = 105,105,105;
default_font_size = 30;
#screen_width = 1024;
#screen_height = 768;
#screen_bit_depth = 32;

begin;

bitmap { filename = "fix.bmp"; } fix;
bitmap { filename = "fix.bmp"; } bitmap1;

text {                
   font_size = 18;
	caption = "text";
   font_color = 255,0,0;
   font = "Arial bold";
   transparent_color = 110,110,110;
   background_color = 110,110,110;
} text1;

text { font_size = 25; caption = "Si homme, appuyez L"; } text2;
text { caption = "filler"; } instruction_text;

picture { default_code = "99"; 	text { caption = "+"; font="arial"; font_color= 255,255,255; font_size = 60;}; x=0; y=0; } default;
picture { default_code = "11";	bitmap bitmap1; 	x = 0; y = 0;
											text text1; 		x = 0; y = -35;} Pic;	

picture { text instruction_text;	x = 0; y = 0; } InstructionPic;

picture { bitmap bitmap1; 	x = 0; y = 0;
          text text1; 		x = 0; y = -35;
          text text2; 		x = 0; y = -250; } ExampPic;


trial{ 
	picture default; # first a fixation cross before the scanner is start
	time = 0;
	duration = 100;
	picture default; # this fixation cross is started by the scanner; then the task begins
	time = 100;
	duration = 900;
	mri_pulse = 1;
}FixTrial;

picture {text { caption = "+"; font="arial"; font_color= 255,0,0; font_size = 60;}; x=0; y=0;} pulsetrial;

trial{
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	picture InstructionPic;
} Instructie;

trial {
	picture default;
	time = 0;
	duration = 500;
	picture Pic;
	time = 500;
	duration = 2000;
	picture default;
	time = 2500;
	duration = 500;
} PicExampTrial1;

trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2,3;
	picture default;
	time = 0;
	duration = 500;
	picture ExampPic;
	time = 500;
} PicExampTrial2;

trial {
	picture Pic;
	target_button = 2,3;
	time = 0;
	duration = 500;
	picture default;
	time = 500;
	duration = 1000;
} PicTrial;

trial{
	#trial_duration = forever;
	#trial_type = specific_response;
	#terminator_button = 1;
	picture InstructionPic;
	duration = 4000;
} EndTask;


begin_pcl;

include "trial_ingredients.pcl";	
include "task_instructions.pcl";
include "main_task-run2.pcl";

