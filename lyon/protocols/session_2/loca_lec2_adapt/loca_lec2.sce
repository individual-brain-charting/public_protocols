scenario = "loca_lec2";   

scenario_type = fMRI;
scan_period=2500;
pulse_code = 255;
pulses_per_scan=1;

$my_size=700;
$my_font_size=100;
$my_font="Verdana";
$my_pre_trial_duration=15000;

write_codes = true; # should be commented out for use with Micromed 
pcl_file = "loca_lec2.pcl";
default_background_color = 40, 40, 40;

# the button is only used to move forward in the explanation slides
active_buttons = 0;

# the task consists in reading the dark story and not attending to the bright story

begin;

##############
# A. STIMULI #
##############

# here specify a bitmap for the string
text { caption = "dummy"; font_size = $my_font_size; font = $my_font; font_color = 255,255,255;  text_align = align_center;} c_string;

# three types of fixation cross
text { caption = "+"; font_size = 40; font = $my_font; font_color = 100,100,100; text_align = align_center;} c_fix;

# three types of fixation cross
text { caption = "la suite juste après la pause"; font_size = 40; font = $my_font; font_color = 150,150,150; text_align = align_center;} c_suite;


                                                                                                   
picture {
   text c_fix;
   x = 0;
   y = 0;   
} default;

picture {
   text c_string;
   x = 0;
   y = 0;  
} p_string;

picture {
   text c_suite;
   x = 0;
   y = 0;  
} p_suite;

#Baseline fixation cross

text { caption = "+";  font_color = 255,255,255; font_size = 40; text_align = align_center;} b_fix;
picture {
   text b_fix;
   x = 0;
   y = 0;   
} p_fix;

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
   LOOP $i 3; # to be adjusted
      nothing n_cut;
      time = 'int($i * 500)'; # start at 5000 after 'relex' sound onset, stops 1000 before 'back to work' 
    ENDLOOP;
} t_cut;
# end of cut section


#######################
# D. TRIAL DEFINITION #
#######################

# t_init est à ajuster pour qu'il écrive des instructions à l'écran présentant la manip

#trial {
   #start_delay = 0;
   #trial_duration = stimuli_length;
   #trial_type = fixed ;
   
   #stimulus_event {
   #   picture p_string;
   #   time = 0;
   #   duration = 5000; 
   #} s_init;
#} t_init;

trial {
   start_delay = 0;
   trial_duration = stimuli_length;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_string;
      time = 0; 
      duration = 200;  
      code = "string"; # adjust
      port_code = 1; # adjust
   } s_string;
   
   stimulus_event {
			picture default;
			deltat = 200;
			duration = 500; # will be adjusted in pcl
	} s_isi;

} t_trial;


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

trial {
   start_delay = 0;
   trial_duration = 6000;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_fix;
      time = 0;
      duration = 6000; 
		code = "Bfix";
		port_code = 110;
   };
} finalfix;

trial {
   start_delay = 0;
   trial_duration = 7000;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_suite;
      time = 0;
      duration = 5000; 
		code = "Suite";
		port_code = 115;
   };
} suite;


