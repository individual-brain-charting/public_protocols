scenario = "loca_lec1_ts";   

scenario_type = fMRI;
scan_period=2500;
pulse_code = 255;
pulses_per_scan=1;

$my_size=700;
$my_font_size=60;
$my_font="Verdana";

$lag_x = 200;
$lag_y = 100;

$pause_init = 2000;
$pause_mid = 33000;
$pause_end = 5000;

$my_baselinefix_duration = 20000;
$my_feedback_duration = 500;

write_codes = true; # should be commented out for use with Micromed 
pcl_file = "loca_lec1_ts.pcl";
default_background_color = 0, 0, 0;

active_buttons = 2;
button_codes = 1,2;

response_matching = simple_matching;

# the task consists in deciding whether the presented string is a living entity (words)
# first button = yes. living
# second button = no

# or whether the presented string has two or one syllable (for pseudo-words)
# first button = yes. two
# second button = no

# or whether the presented string is in upper of lower case (for random strings)
# first button = yes. upper
# second button = no


begin;

##############
# A. STIMULI #
##############


# here specify a bitmap for the string
text { caption = "dummy"; font_size = $my_font_size; font = $my_font; font_color = 255,255,255;  text_align = align_center;} c_string;

# three types of fixation cross
text { caption = "+"; font_size = $my_font_size; font = $my_font; font_color = 150,150,150; text_align = align_center;} c_fix_sem;
text { caption = "+"; font_size = $my_font_size; font = $my_font; font_color = 150,150,150; text_align = align_center;} c_fix_pho;
text { caption = "+"; font_size = $my_font_size; font = $my_font; font_color = 150,150,150; text_align = align_center;} c_fix_vis;


                                                                                                   
picture {
   text c_fix_sem;
   x = '-1*$lag_x';
   y = '1.5*$lag_y';   
   text c_fix_sem;
   x = '1*$lag_x';
   y = '1.5*$lag_y';   
   text c_fix_pho;
   x = '-1*$lag_x';
   y = 0;   
   text c_fix_pho;
   x = '1*$lag_x';
   y = 0;   
   text c_fix_vis;
   x = '-1*$lag_x';
   y = '-1.5*$lag_y';   
   text c_fix_vis;
   x = '1*$lag_x';
   y = '-1.5*$lag_y';   
} default;

picture {
   text c_fix_sem;
   x = '-1*$lag_x';
   y = '1.5*$lag_y';   
   text c_fix_sem;
   x = '1*$lag_x';
   y = '1.5*$lag_y';   
   text c_fix_pho;
   x = '-1*$lag_x';
   y = 0;   
   text c_fix_pho;
   x = '1*$lag_x';
   y = 0;   
   text c_fix_vis;
   x = '-1*$lag_x';
   y = '-1.5*$lag_y';   
   text c_fix_vis;
   x = '1*$lag_x';
   y = '-1.5*$lag_y';   

   text c_string;
   x = 0;
   y = 0; # this position will be changed   

} p_string;

text { caption = "turbulu"; font_size = 40; font = "Arial"; font_color = 255,255,255;  text_align = align_center;} c_score;
bitmap { filename = "fb_1.jpg"; preload = false; width = 120;height = 160; } b_score;

picture {
   text c_score;
   x = 0;
   y = 200;   
   bitmap b_score;
   x = 0;
   y = 0;   
} p_score;


############
# B. PAUSE #
############

# baseline fixation trial
text { caption = "+";  font_color = 180,180,180; font_size = 70; text_align = align_center;} c_fix;
picture {
   text c_fix;
   x = 0;
   y = 0;   
} p_fix;

trial {
   start_delay = 0;
   trial_duration = $my_baselinefix_duration;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_fix;
      time = 0;
      duration = $my_baselinefix_duration; 
		code = "Bfix";
		port_code = 110;
   };
} baselinefix;

#################
# C. CUT / INIT #
#################

# cut section - just to indicate the real beginning of the sequence
nothing {
    default_code = "cut";    # whatever
    default_port_code = 99;      # whatever
} n_cut;

trial {
   start_delay = 1500;
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

trial {
   start_delay = 0;
   trial_duration = 2500;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_string;
      time = 500; 
      duration = 2000;  
      code = "string"; # adjust
      port_code = 1; # adjust
   } s_string;

} t_trial;


trial {
   start_delay = 0;
   trial_duration = 2500;
   trial_type = fixed ;
   
   stimulus_event {
      picture default;
      time = 0; 
      duration = 2500;  
      code = "change"; # adjust
		port_code = 1; # will be adjusted in pcl
   } s_change;

} t_change;


trial {
   start_delay = 0;
   trial_duration = 3000;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_score;
      time = 0; 
      duration = 1000;  
      code = "score"; # adjust
      port_code = 50; # adjust
   } se_score;

} t_score;
   
   
                                                                                        
