scenario = "loca_mcse";   

# chaque partie dure environ 6min

scenario_type = fMRI;
scan_period=2500;
pulse_code = 255;
pulses_per_scan=1;

$my_size=900;# changes the size of the image
$my_font_size=24;

$my_font="Arial";
#$my_go_duration = 1000;# needs to have a random component
#$my_go_total_duration = 2000; 
#$delay_before_letter = 200;
#$duration_square = 200;
#$duration_feedback = 3000;
$color = 200;
$my_square_size = 50;
$my_semi_offset=35;

$my_baseline_duration = 20000;


write_codes = true; # should be commented out for use with Micromed 
pcl_file = "loca_mcse.pcl";
default_background_color = 255, 255, 255;

active_buttons = 2;
button_codes = 1,2;

response_matching = simple_matching;

begin;

##############
# A. STIMULI #
##############


bitmap { filename = "ct.jpg"; preload = true; width = $my_size;height = $my_size; } b_ct ;
bitmap { filename = "ct.jpg"; preload = true; width = $my_size;height = $my_size; } b_array ;
box { height = $my_square_size; width = $my_square_size; color = 0,$color,0;} b_win;


picture {
   bitmap b_ct;
   x = 0;
   y = 0;   
} default;
# use white as default

picture {
   bitmap b_ct;
   x = 0;
   y = 0;   
} fix_point;

picture {
   bitmap b_array;
   x = 0;
   y = 0;   
} p_array;

picture {
   box b_win;
   x = 0;
   y = 0;  
} p_win1;




############
# BASELINE #
############
text { caption = "+";  font_color = 180,180,180; font_size = 40; text_align = align_center;} c_fix;
picture {
   text c_fix;
   x = 0;
   y = 0;   
} p_fix;

trial {
   start_delay = 0;
   trial_duration = $my_baseline_duration;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_fix;
      time = 0;
      duration = $my_baseline_duration; 
		code = "Bfix";
		port_code = 110;
   };
} baselinefix;

# Pre TTL yellow fixation

text { caption = "+";  font_color = 255,0,0; font_size = 40; text_align = align_center;} y_fix;
picture {
   text y_fix;
   x = 0;
   y = 0;   
} TTL_fix;


#################
# C. CUT / INIT #
#################

# cut section - just to indicate the real beginning of the sequence
nothing {
    default_code = "cut";    # whatever
    default_port_code = 99;      # whatever
} n_cut;

trial {
   start_delay = 1000;
   trial_duration = 1000;
   trial_type = fixed ;

	# then we show 3 cut stimuli, just to show the beginning of the file
   #LOOP $i 3; # to be adjusted
      #nothing n_cut;
      #time = 'int($i * 500)'; # start at 5000 after 'relex' sound onset, stops 1000 before 'back to work' 
    #ENDLOOP;
} t_cut;
# end of cut section


#######################
# D. TRIAL DEFINITION #
#######################

trial {
      start_delay = 0;
      trial_duration = stimuli_length;
      all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_array;
			#time = 0;
			deltat = 1000 ;
			duration = 2500; # adjust
			code = "pic1";
			port_code = 1;
		} se_array;

		
} t_trial;

