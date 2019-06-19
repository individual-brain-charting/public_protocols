scenario = "loca_lec1_test";   

$my_size=700;
$my_font_size=36;
$my_font="Courier new";

$lag_x = 200;
$lag_y = 50;

$pause_init = 2000;
$pause_mid = 33000;
$pause_end = 5000;

$my_feedback_duration = 500;

write_codes = true; # should be commented out for use with Micromed 
pcl_file = "loca_lec1_test.pcl";
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

############
# A. STIMULI
############

# A.1. EXPLANATION
##################

# we start with the explanations pictures
picture {
	bitmap { filename = "\\loca_lec1_exp\\sitive1.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo1;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive2.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo2;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive3.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo3;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive4.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo4;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive5.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo5;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive6.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo6;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive7.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo7;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive8.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo8;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive9.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo9;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive10.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo10;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive11.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo11;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive12.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo12;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive13.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo13;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive14.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo14;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive15.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo15;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive16.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo16;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive17.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo17;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive18.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo18;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive19.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo19;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive20.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo20;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive21.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo21;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive22.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo22;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive23.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo23;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive24.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo24;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive25.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo25;
picture {
	bitmap { filename = "\\loca_lec1_exp\\Diapositive26.jpg"; preload = true;};
   x = 0;
   y = 0;
} p_diapo26;

# A.2. STIMULI
##################

# here specify a bitmap for the string
text { caption = "dummy"; font_size = $my_font_size; font = $my_font; font_color = 255,255,255;  text_align = align_center;} c_string;

# three types of fixation cross
text { caption = "+"; font_size = $my_font_size; font = $my_font; font_color = 150,150,150; text_align = align_center;} c_fix_sem;
text { caption = "+"; font_size = $my_font_size; font = $my_font; font_color = 150,150,150; text_align = align_center;} c_fix_pho;
text { caption = "+"; font_size = $my_font_size; font = $my_font; font_color = 150,150,150; text_align = align_center;} c_fix_vis;


                                                                                                   
picture {
   text c_fix_sem;
   x = '-1*$lag_x';
   y = '1*$lag_y';   
   text c_fix_sem;
   x = '1*$lag_x';
   y = '1*$lag_y';   
   text c_fix_pho;
   x = '-1*$lag_x';
   y = 0;   
   text c_fix_pho;
   x = '1*$lag_x';
   y = 0;   
   text c_fix_vis;
   x = '-1*$lag_x';
   y = '-1*$lag_y';   
   text c_fix_vis;
   x = '1*$lag_x';
   y = '-1*$lag_y';   
} default;

picture {
   text c_fix_sem;
   x = '-1*$lag_x';
   y = '1*$lag_y';   
   text c_fix_sem;
   x = '1*$lag_x';
   y = '1*$lag_y';   
   text c_fix_pho;
   x = '-1*$lag_x';
   y = 0;   
   text c_fix_pho;
   x = '1*$lag_x';
   y = 0;   
   text c_fix_vis;
   x = '-1*$lag_x';
   y = '-1*$lag_y';   
   text c_fix_vis;
   x = '1*$lag_x';
   y = '-1*$lag_y';   

   text c_string;
   x = 0;
   y = 0; # this position will be changed   

} p_string;

text { caption = "turbulu"; font_size = 20; font = "Arial"; font_color = 255,255,255;  text_align = align_center;} c_score;
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
# B. PAUSE 
############

# the pause stimulus
bitmap { filename = "rest.jpg"; preload = true;width = 90;height = 120;} b_pause;
picture {
   bitmap b_pause;
   x = 0;
   y = 0;   
} p_pause;

nothing {
    default_code = "pause";    # whatever
    default_port_code = 100;      # whatever
} n_pause;

sound { wavefile { filename = "\\detente_start.wav"; preload = true; } ; } w_pause_start;
sound { wavefile { filename = "\\detente_stop.wav"; preload = true; } ; } w_pause_stop;

trial {
	trial_duration = '$pause_init + $pause_mid + $pause_end';

	stimulus_event {
		sound w_pause_start;
		time = $pause_init;
		code = "start_pause";
	};
	
	stimulus_event {
		picture p_pause;
		time = '$pause_init + 100';
	};

   # then we show 55 nothing stimuli, just to send codes
   LOOP $i 55; # to be adjusted
      nothing n_pause;
      time = '$pause_init + int($i * 500) + 5000'; # start at 5000 after 'relex' sound onset, stops 1000 before 'back to work' 
    ENDLOOP;

	stimulus_event {
		sound w_pause_stop;
		time = '$pause_init + $pause_mid';
		code = "stop_pause";
	};
} t_pause;
# end of pause section


################
# C. CUT / INIT 
################

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


#####################
# D. TRIAL DEFINITION 
#####################

trial {
   start_delay = 0;
   trial_duration = 3500;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_string;
      time = 1000; 
      duration = 2000;  
      code = "string"; # adjust
      port_code = 1; # adjust
   } s_string;

} t_trial;


trial {
   start_delay = 0;
   trial_duration = 1000;
   trial_type = fixed ;
   
   stimulus_event {
      picture default;
      time = 0; 
      duration = 1000;  
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
   
   
########################
# E. INSTRUCTION TRIALS 
########################

# instruction trials
trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo1;
      time = 0;
      duration = 10000; 
   };
} t_diapo1;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo2;
      time = 0;
      duration = 10000; 
   };
} t_diapo2;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo3;
      time = 0;
      duration = 10000; 
   };
} t_diapo3;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo4;
      time = 0;
      duration = 10000; 
   };
} t_diapo4;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo5;
      time = 0;
      duration = 10000; 
   };
} t_diapo5;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo6;
      time = 0;
      duration = 10000; 
   };
} t_diapo6;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo7;
      time = 0;
      duration = 10000; 
   };
} t_diapo7;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo8;
      time = 0;
      duration = 10000; 
   };
} t_diapo8;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo9;
      time = 0;
      duration = 10000; 
   };
} t_diapo9;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo10;
      time = 0;
      duration = 10000; 
   };
} t_diapo10;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo11;
      time = 0;
      duration = 10000; 
   };
} t_diapo11;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo12;
      time = 0;
      duration = 10000; 
   };
} t_diapo12;
                                                                                                   
trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo13;
      time = 0;
      duration = 10000; 
   };
} t_diapo13;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo14;
      time = 0;
      duration = 10000; 
   };
} t_diapo14;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo15;
      time = 0;
      duration = 10000; 
   };
} t_diapo15;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo16;
      time = 0;
      duration = 10000; 
   };
} t_diapo16;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo17;
      time = 0;
      duration = 10000; 
   };
} t_diapo17;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo18;
      time = 0;
      duration = 10000; 
   };
} t_diapo18;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo19;
      time = 0;
      duration = 10000; 
   };
} t_diapo19;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo20;
      time = 0;
      duration = 10000; 
   };
} t_diapo20;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo21;
      time = 0;
      duration = 10000; 
   };
} t_diapo21;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo22;
      time = 0;
      duration = 10000; 
   };
} t_diapo22;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo23;
      time = 0;
      duration = 10000; 
   };
} t_diapo23;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo24;
      time = 0;
      duration = 10000; 
   };
} t_diapo24;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo25;
      time = 0;
      duration = 10000; 
   };
} t_diapo25;

trial {
   start_delay = 0;
   trial_duration = 10000;
   trial_type = first_response ;
   
   stimulus_event {
      picture p_diapo26;
      time = 0;
      duration = 10000; 
   };
} t_diapo26;

                                                                                                   
