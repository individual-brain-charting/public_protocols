scenario_type = fMRI;
scan_period=2500;
pulse_code = 255;
pulses_per_scan=1;

scenario = "loca_mveb_bis";   

#$my_width=1200;
#$my_height=940;

$my_duration_fix1 = 1000;
$duration_cross = 500;
$duration_pic = 1500;
$duration_blank = 3000;
$duration_response = 1500;

$duration_cross_long = 6500;

$my_cross_size = 36;
$my_font_size=50;
#$my_font="Calibri";
$my_font="Arial";

$my_intersound_duration = 3000;
$pause_init = 2000;
$pause_mid = 23000;
$pause_end = 5000;
$my_duration_fix1 = 10000;

active_buttons = 2;
button_codes = 1,2;
no_logfile = false;

# first button = happy detection in bloc 1, fear detection in bloc 2
# JP . check with Carolina

write_codes = true; # pour pouvoir envoyer les codes des evenements a Neuroscan 
#pulse_width = 6;    # largeur des pulses envoyes a Neuroscan

pcl_file = "loca_mveb_mat1.pcl";
default_background_color = 150, 150, 150;
default_text_color = 50, 50, 50;


begin;

text { caption = "+"; font = $my_font; font_size = $my_cross_size;} c_cross;
text { caption = " "; font = $my_font; font_size = $my_cross_size;} c_blank;
text { caption = " "; font = $my_font; font_size = $my_font_size;} c_pic;
text { caption = " "; font = $my_font; font_size = $my_font_size;} c_response;

picture {
   text c_cross;
    x = 0;y = 0; 
} p_fix1;

picture {
   text c_cross;
    x = 0;y = 0; 
} p_cross;

picture {
   text c_cross;
    x = 0;y = 0; 
} default;

picture {
   text c_blank;
    x = 0;y = 0; 
} p_blank;

picture {
   text c_pic;
    x = 0;y = 0; 
} p_pic;

picture {
   text c_response;
    x = 0;y = 0; 
} p_response;


# pause section
nothing {
    default_code = "pause";    # whatever
    default_port_code = 100;      # whatever
} n_pause;

sound { wavefile { filename = "detente_start.wav"; preload = true; } ; } w_pause_start;
sound { wavefile { filename = "detente_stop.wav"; preload = true; } ; } w_pause_stop;

#text { caption = "+"; font_size = 90;} c_cross;


#picture {
 #  text c_cross;
#    x = 0;y = 0; 
#} p_fix1;

trial {
   start_delay = 0;
   trial_duration = stimuli_length;
     trial_type = fixed ;
   
   stimulus_event {
      picture p_cross;
      time = 0;
      duration = $my_duration_fix1;
      code = "p_startup";
      port_code = 1;
   } s_startup;

} t_startup;

# Pre TTL yellow fixation

text { caption = "+";  font_color = 255,0,0; font_size = 40; text_align = align_center;} y_fix;
picture {
   text y_fix;
   x = 0;
   y = 0;   
} TTL_fix;

trial {
	trial_duration = '$pause_init + $pause_mid + $pause_end';

	stimulus_event {
		sound w_pause_start;
		time = $pause_init;
		code = "start_pause";
	};
	
   # then we show 35 nothing stimuli, just to send codes
   LOOP $i 35; # to be adjusted
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


trial {
   start_delay = 0;
   trial_duration = stimuli_length;
   trial_type = fixed ;

   stimulus_event {
      picture p_cross;
      time = 0;
      duration = 400;
      code = "cross";
   } s_cross;
   
   stimulus_event {
      picture p_pic;
      deltat = $duration_cross;
      duration = $duration_pic;
      code = "pic";
   } s_pic;

   stimulus_event {
      picture p_cross;
      deltat = $duration_pic;
      duration = $duration_blank;
      code = "cross";
   } s_blank1;

	# three empty pulses to facilitate the SEEG analysis
   stimulus_event {
      nothing {};
      deltat = $duration_blank;
      code = "during_maintenance";
      duration = 1500;
      port_code = 1; # will be adjusted
   } se_no1;   



   stimulus_event {
      picture p_response;
      deltat = 1500;
      duration = $duration_response;
      code = "response";
   } s_response;

   
   stimulus_event {
      picture p_blank;
      deltat = $duration_response;
      duration = $duration_blank;
      code = "blank2";
   } s_blank2;
   
} t_trial;

