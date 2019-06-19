scenario = "loca_visu";   

#scenario_type = fMRI;
#scan_period=2500;
#pulse_code = 255;
#pulses_per_scan=1;

# Adapte tel quel le scenario est trop long, puisque chaque bloc dure environ 10 min  ###############################
$my_size=150;
$my_font_size=25;
$my_font_size_cross=8;
$my_font="Courier new";
$my_height=390;
$my_width=300;

$my_stimulus_duration=200;
$my_trial_duration = 400;# needs to have a random component
$my_pre_trial_duration = 5000;
$blink_duration = 2000;

$my_intersound_duration = 3000;
$pause_init = 2000;
$pause_mid = 33000;
$pause_end = 5000;

#write_codes = true; # should be commented out for use with Micromed 
pcl_file = "loca_visu.pcl";
default_background_color = 128, 128, 128;

# the task consists in pressing a button each time you see a fruit
active_buttons = 1;
button_codes = 1;

response_matching = simple_matching;

begin;

##############
# A. STIMULI #
##############

text { caption = "+";  font_color = 180,180,180; font_size = 40; text_align = align_center;} c_fix;
picture {
   text c_fix;
   x = 0;
   y = 0;   
} default;

picture {
   text c_fix;
   x = 0;
   y = 0;   
} p_fix;

# the stimulus itself - pictures
bitmap { filename = "mask.jpg"; preload = false; width = $my_width; height = $my_height; } b_pic1;
picture {
   bitmap b_pic1;
   x = 0;
   y = 0;   
} p_pic1;

# the stimulus itself - letter strings
bitmap { filename = "mask.jpg"; preload = true; width = $my_width; height = $my_height; } b_pic2;
text { caption = "+";  font_color = 250,250,250; background_color = 0,0,0; font_size = $my_font_size; text_align = align_center;} c_string;
picture {
   bitmap b_pic2;
   x = 0;
   y = 0;   
   text c_string;
   x = 0;
   y = 0;  
} p_pic2;



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
   LOOP $i 3; # to be adjusted
      nothing n_cut;
      time = 'int($i * 500)'; # start at 5000 after 'relex' sound onset, stops 1000 before 'back to work' 
    ENDLOOP;
} t_cut;
# end of cut section


#######################
# D. TRIAL DEFINITION #
#######################

# stimulus trial - non words
trial {
      start_delay = 0;
      trial_duration = stimuli_length;
      all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_pic1;
			time = 0;
			duration = $my_stimulus_duration; # adjust
			code = "pic1";
			port_code = 1;
		} s_pic1;

      stimulus_event {
			picture p_fix;
			deltat = $my_stimulus_duration;
			duration = 500; # will be adjusted in pcl
		} s_isi1;
		
} t_trial1;


# stimulus trial - letter strings
trial {
      start_delay = 0;
      trial_duration = stimuli_length;
      all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_pic2;
			time = 0;
			duration = $my_stimulus_duration;
			code = "pic2";
			port_code = 1;
		} s_pic2;

      stimulus_event {
			picture p_fix;
			deltat = $my_stimulus_duration;
			duration = 500; # will  be adjusted in pcl
		} s_isi2;

} t_trial2;


# baseline fixation trial
trial {
   start_delay = 0;
   trial_duration = $my_pre_trial_duration;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_fix;
      time = 0;
      duration = $my_pre_trial_duration; 
		code = "Bfix";
		port_code = 110;
   };
} baselinefix;









