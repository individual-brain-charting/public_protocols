scenario_type = fMRI; #remove this line if you the scanner trigger is not set up to send it sync
scan_period=2500; #remove this line if you the scanner trigger is not set up to send it sync
pulse_code = 255; #remove this line if you the scanner trigger is not set up to send it sync
pulses_per_scan=1; #remove this line if you the scanner trigger is not set up to send it sync

scenario = "loca_mvis";   

$my_width = 400;
$my_heigth = 400;
$my_font_size = 50;
$my_font="Arial";
$my_radius = 80;

$my_probe_duration = 1500; # duration of presentation of the initial stimulus
$my_probe2_duration = 100; # only used in Juan's version
$my_prestim_duration = 400; # duration during which you see the fixation cross before the array appears
$my_duration_fix1 = 8800;# change according to your TR (tr*4)
$my_intersound_duration = 3000;
$pause_init = 2000;
$pause_mid = 23000;
$pause_end = 5000;

active_buttons = 2;
button_codes = 1,2;
no_logfile = false;
# the task consists in deciding whether the presented dot was part of the group shown as probe
# first button = yes


write_codes = true; # send codes to Micromed 
pulse_width = 6;    

pcl_file = "loca_mvis_caro_bis.pcl";
default_background_color = 200, 200, 200;

begin;


# here specify a bitmap for the string
bitmap { filename = "grids.jpg"; preload = true; width = $my_width;height = $my_heigth; } b_grid;
ellipse_graphic {ellipse_width = $my_radius; ellipse_height = $my_radius; color = 255, 255, 0; background_color = 200, 200, 200; } el_d1;
ellipse_graphic {ellipse_width = $my_radius; ellipse_height = $my_radius; color = 255, 255, 0; background_color = 200, 200, 200;} el_d2;
ellipse_graphic {ellipse_width = $my_radius; ellipse_height = $my_radius; color = 255, 255, 0; background_color = 200, 200, 200;} el_d3;
ellipse_graphic {ellipse_width = $my_radius; ellipse_height = $my_radius; color = 255, 255, 0; background_color = 200, 200, 200;} el_d4;
ellipse_graphic {ellipse_width = $my_radius; ellipse_height = $my_radius; color = 255, 255, 0; background_color = 200, 200, 200;} el_d5;
ellipse_graphic {ellipse_width = $my_radius; ellipse_height = $my_radius; color = 255, 255, 0; background_color = 200, 200, 200;} el_d6;
ellipse_graphic {ellipse_width = '0.5*$my_radius'; ellipse_height = '0.5*$my_radius'; color = 0, 255, 255; } el_controle;
ellipse_graphic {ellipse_width = '0.5*$my_radius'; ellipse_height = '0.5*$my_radius'; color = 0, 255, 255; } el_controle2;
ellipse_graphic {ellipse_width = $my_radius; ellipse_height = $my_radius; color = 255, 255, 0; background_color = 200, 200, 200;} el_test;

#text { caption = "+"; font_size = 18; font_color = 100,100,100; } c_defcross;
text { caption = "+"; font_size = 24; font_color = 128,128,128; } c_defcross;

text { caption = "+";  font_color = 180,180,180; font_size = 40; text_align = align_center;} c_fix;
picture {
   text c_fix;
   x = 0;
   y = 0;   
} p_fix;

picture {
   text c_defcross;
   x = 0;y = 0; 
} p_cross;

                                                                                                   
picture {
   bitmap b_grid;
   x = 0;
   y = 0;   
} p_grid;

picture {
   bitmap b_grid;
   x = 0;
   y = 0;   
} default;

picture {
   bitmap b_grid;
   x = 0;
   y = 0;

	ellipse_graphic el_d1;
	x = 0;	# doesn't matter
	y = 0;	# doesn't matter
   
	ellipse_graphic el_d2;
	x = 0;	# doesn't matter
	y = 0;	# doesn't matter

	ellipse_graphic el_d3;
	x = 0;	# doesn't matter
	y = 0;	# doesn't matter

	ellipse_graphic el_d4;
	x = 0;	# doesn't matter
	y = 0;	# doesn't matter

	ellipse_graphic el_d5;
	x = 0;	# doesn't matter
	y = 0;	# doesn't matter

	ellipse_graphic el_d6;
	x = 0;	# doesn't matter
	y = 0;	# doesn't matter

	ellipse_graphic el_controle;
	x = 0;	# doesn't matter
	y = 0;	# doesn't matter

} p_probe;


picture {
   bitmap b_grid;
   x = 0;
   y = 0;

	ellipse_graphic el_controle2;
	x = 0;	# doesn't matter
	y = 0;	# doesn't matter

} p_probe2;

picture {
   bitmap b_grid;
   x = 0;
   y = 0;

	ellipse_graphic el_test;
	x = 0;	# doesn't matter
	y = 0;	# doesn't matter

} p_test;

# pause section
nothing {
    default_code = "pause";    # whatever
    default_port_code = 100;      # whatever
} n_pause;

sound { wavefile { filename = "detente_start.wav"; preload = true; } ; } w_pause_start;
sound { wavefile { filename = "detente_stop.wav"; preload = true; } ; } w_pause_stop;

trial {
   start_delay = 0;
   trial_duration = stimuli_length;
     trial_type = fixed ;
   
   stimulus_event {
      picture p_cross;
      time = 0;
      duration = $my_duration_fix1;
      code = "p_startup";
 #     port_code = 1;
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
   



} t_probe;

trial {
   start_delay = 0;
   trial_duration = stimuli_length;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_probe2;
      time = 0;
      duration = $my_probe2_duration; 
   } se_probe2;
} t_probe2; # only used in Juan's option

trial {
   start_delay = 0;
   trial_duration = stimuli_length;
   trial_type = fixed ;
   
   
   stimulus_event {
      picture p_grid;
      time = 0;
      duration = 400; 
      code = "grid";
   } se_cross;

   stimulus_event {
      picture p_probe;
      time = 400;
      duration = 1500; 
   } se_probe;

   
   stimulus_event {
      picture p_grid;
      time = 1900;
      duration = 3000; # 3000 ms maintenance interval
      code = "maintenance";
   } se_wait;

	# three empty pulses to facilitate the SEEG analysis
   stimulus_event {
      nothing {};
      time = 4900;
      duration = 1500;
      code = "during_maintenance";
      port_code = 1; # will be adjusted
   } se_no1;   



   stimulus_event {
      picture p_test;
      time = 6400;
      duration = 1500;
      code = "test";
   } se_test;
   
} t_test;

   
   
                                                                                                   
