scenario = "loca_moto";   

scenario_type = fMRI;
scan_period=2500;
pulse_code = 255;
pulses_per_scan=1;

$my_size=150;
$my_font_size=24;
$my_font_size_cross=8;
$my_font="Verdana";
$my_square_size=20;
$my_square_offset=200;

$my_instructions_trial_duration = 6000;
$my_instructions_duration=4000;
$my_go_duration = 1000;# needs to have a random component
$my_go_total_duration = 2500; 

$my_baselinefix_duration = 3000;

write_codes = true; # should be commented out for use with Micromed 
pcl_file = "loca_moto.pcl";
default_background_color = 0, 0, 0;

active_buttons = 2;
button_codes = 1,2;

response_matching = simple_matching;

begin;

##############
# A. STIMULI #
##############

box { height = $my_square_size; width = $my_square_size; color = 100,100,100;} b_bbox_gray;
box { height = $my_square_size; width = $my_square_size; color = 255,255,255;} b_bbox_white;
box { height = $my_square_size; width = $my_square_size; color = 100,100,100;} b_sbox_gray;

picture {
	box b_bbox_gray;
   x = '-1*$my_square_offset';
   y = 0;   
	box b_bbox_gray;
   x = $my_square_offset;
   y = 0;   
	box b_sbox_gray;
   x = 0;
   y = 0;   
} default;

picture {
	box b_bbox_white;
   x = '-1*$my_square_offset';
   y = 0;   
	box b_bbox_gray;
   x = $my_square_offset;
   y = 0;   
	box b_sbox_gray;
   x = 0;
   y = 0;   
} p_left;

picture {
	box b_bbox_gray;
   x = '-1*$my_square_offset';
   y = 0;   
	box b_bbox_white;
   x = $my_square_offset;
   y = 0;   
	box b_sbox_gray;
   x = 0;
   y = 0;   
} p_right;

text { caption = "BOUGEZ LA MAIN"; font = $my_font;  font_color = 250,250,250; font_size = $my_font_size; text_align = align_center;} c_bras;
picture {
   text c_bras;
   x = 0;
   y = 0;   
} p_bras;

text { caption = "CLIQUEZ AVEC LE POUCE"; font = $my_font; font_color = 250,250,250; font_size = $my_font_size; text_align = align_center;} c_index;
picture {
   text c_index;
   x = 0;
   y = 0;   
} p_index;

text { caption = "BOUGEZ LES YEUX SANS BOUGER LA TÊTE"; font = $my_font; font_color = 250,250,250; font_size = $my_font_size; text_align = align_center;} c_yeux;
picture {
   text c_yeux;
   x = 0;
   y = 0;   
} p_yeux;

/*text { caption = "BOUGEZ LA TETE"; font = $my_font; font_color = 250,250,250; font_size = $my_font_size; text_align = align_center;} c_tete;
picture {
   text c_tete;
   x = 0;
   y = 0;   
} p_tete; */

text { caption = "BOUGEZ LÉGÈREMENT LE PIED"; font = $my_font; font_color = 250,250,250; font_size = $my_font_size; text_align = align_center;} c_jambe;
picture {
   text c_jambe;
   x = 0;
   y = 0;   
} p_jambe;

text { caption = "BOUGEZ LA LANGUE"; font = $my_font; font_color = 250,250,250; font_size = $my_font_size; text_align = align_center;} c_bouche;
picture {
   text c_bouche;
   x = 0;
   y = 0;   
} p_bouche;

text { caption = "NE FAITES RIEN, VOS YEUX FIXENT LE CENTRE"; font = $my_font; font_color = 250,250,250; font_size = $my_font_size; text_align = align_center; } c_repos;
picture {
   text c_repos;
   x = 0;
   y = 0;   
} p_repos;

############
# B. PAUSE #
############

# baseline fixation trial
text { caption = "+";  font_color = 180,180,180; font_size = 40; text_align = align_center;} c_fix;
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

# Pre TTL yellow fixation

text { caption = "+";  font_color = 255,0,0; font_size = 40; text_align = align_center;} y_fix;
picture {
   text y_fix;
   x = 0;
   y = 0;   
} TTL_fix;

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


/* PAUSE DE JP
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
*/

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

# instruction : bras
trial {
      start_delay = 0;
      trial_duration = $my_instructions_trial_duration;
      all_responses = false;
      trial_type = fixed ;
		   
      stimulus_event {
			picture p_bras;
			time = 0;
			duration = $my_instructions_duration; # adjust
			code = "Ins_main" ;
			port_code = 9;
		} s_bras;
} t_bras;

# instruction : index
trial {
      start_delay = 0;
      trial_duration = $my_instructions_trial_duration;
      #all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_index;
			time = 0;
			duration = $my_instructions_duration; # adjust
			code = "Ins_index" ;
			port_code = 8;
		} s_index;
} t_index;

# instruction : yeux
trial {
      start_delay = 0;
      trial_duration = $my_instructions_trial_duration;
      all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_yeux;
			time = 0;
			duration = $my_instructions_duration; # adjust
			code = "Ins_yeux" ;
			port_code = 7;
		} s_yeux;
} t_yeux;

# instruction : tete
/*trial {
      start_delay = 0;
      trial_duration = $my_instructions_trial_duration;
      all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_tete;
			time = 1000;
			duration = $my_instructions_duration; # adjust
		} s_tete;
} t_tete;*/

# instruction : jambe
trial {
      start_delay = 0;
      trial_duration = $my_instructions_trial_duration;
      all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_jambe;
			time = 0;
			duration = $my_instructions_duration; # adjust
			code = "Ins_jambe" ;
			port_code = 6;
		} s_jambe;
} t_jambe;

# instruction : bouche
trial {
      start_delay = 0;
      trial_duration = $my_instructions_trial_duration;
      all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_bouche;
			time = 0;
			duration = $my_instructions_duration; # adjust
			code = "Ins_bouche" ;
			port_code = 5;
		} s_bouche;
} t_bouche;

# instruction : repos
trial {
      start_delay = 0;
      trial_duration = $my_instructions_trial_duration;
      all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_repos;
			time = 0;
			duration = $my_instructions_duration; # adjust
			code = "Ins_repos" ;
			port_code = 4;
		} s_repos;
} t_repos;


# stimulus trial - left/right
trial {
      start_delay = 0;
      trial_duration = $my_go_total_duration;
      #all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_left;
			time = 0;
			duration = $my_go_duration;
			code = "go";
			port_code = 1;
		} s_left;

} t_left;

# stimulus trial - left/right
trial {
      start_delay = 0;
      trial_duration = $my_go_total_duration;
      #all_responses = false;
      trial_type = fixed ;
   
      stimulus_event {
			picture p_right;
			time = 0;
			duration = $my_go_duration;
			code = "go";
			port_code = 1;
		} s_right;

} t_right;

