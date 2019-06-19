scenario = "loca_audi_ts";

scenario_type = fMRI;
scan_period=2500;
pulse_code = 255;
pulses_per_scan=1;

active_buttons = 1;
button_codes = 1 ; # check that this is correct

default_background_color = 0, 0, 0;

pcl_file = "loca_audi_ts.pcl";

# uncomment next lines to send codes on the port
write_codes = true;


$my_width=800;
$my_height=800;

$my_intersound_duration = 3000;
#$pause_init = 2000;
#$pause_mid = 33000;
#$pause_end = 5000;

$my_intersound_duration_plus_loop = 14000; #will be adjusted in pcl (si ça marche)
$my_baseline_duration = 6000;


#$my_pre_trial_duration = 1500;

begin;

##############
# A. STIMULI #
##############

sound { wavefile { filename = "poinpoin.wav"; preload = false; } w_mywave; } w_mysound;
sound { wavefile { filename = "question.wav"; preload = true;} ;} w_question;
sound { wavefile { filename = "test1_yes.wav"; preload = true;} ;} w_test1_yes;
sound { wavefile { filename = "test2_yes.wav"; preload = true;} ;} w_test2_yes;
sound { wavefile { filename = "test3_yes.wav"; preload = true;} ;} w_test3_yes;
sound { wavefile { filename = "test1_no.wav"; preload = true;} ;} w_test1_no;
sound { wavefile { filename = "test2_no.wav"; preload = true;} ;} w_test2_no;
sound { wavefile { filename = "test3_no.wav"; preload = true;} ;} w_test3_no;

text { caption = "+";  font_color = 180,180,180; font_size = 40; text_align = align_center;} c_fix;
picture {
   text c_fix;
   x = 0;
   y = 0;   
} p_fix;

nothing {
    default_code = "parol";    # whatever
    default_port_code = 1;      # whatever
} n_pulse_10;

nothing {
    default_code = "rever";    # whatever
    default_port_code = 2;      # whatever
} n_pulse_20;

nothing {
    default_code = "suomi";    # whatever
    default_port_code = 3;      # whatever
} n_pulse_30;

nothing {
    default_code = "alpha";    # whatever
    default_port_code = 4;      # whatever
} n_pulse_40;

nothing {
    default_code = "human";    # whatever
    default_port_code = 5;      # whatever
} n_pulse_50;

nothing {
    default_code = "pleur";    # whatever
    default_port_code = 6;      # whatever
} n_pulse_60;

nothing {
    default_code = "rires";    # whatever
    default_port_code = 7;      # whatever
} n_pulse_70;

nothing {
    default_code = "yawny";    # whatever
    default_port_code = 8;      # whatever
} n_pulse_80;

nothing {
    default_code = "cough";    # whatever
    default_port_code = 9;      # whatever
} n_pulse_90;

nothing {
    default_code = "music";    # whatever
    default_port_code = 10;      # whatever
} n_pulse_100;

nothing {
    default_code = "envir";    # whatever
    default_port_code = 11;      # whatever
} n_pulse_110;

nothing {
    default_code = "animo";    # whatever
    default_port_code = 12;      # whatever
} n_pulse_120;

nothing {
    default_code = "silen";    # whatever
    default_port_code = 20;      # whatever
} n_pulse_200;


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


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 101;
	};

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_10;
      time = '$my_intersound_duration + int($i * 500) + 1000'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi10;

} t_trial_10;

trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 102;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_20;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi20;

} t_trial_20;

trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 103;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_30;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi30;

} t_trial_30;

trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 104;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_40;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi40;

} t_trial_40;


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
		time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 105;
   };

	
   # then we show 20 nothing stimuli during the sound, just to send codes (code=type de son)
   LOOP $i 20;
      nothing n_pulse_50;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
	} s_isi50;
} t_trial_50;


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 106;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_60;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi60;

} t_trial_60;


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 107;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_70;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi70;
		
} t_trial_70;


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 108;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_80;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi80;

} t_trial_80;


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 109;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_90;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi90;

} t_trial_90;


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 110;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_100;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi100;
		
} t_trial_100;


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 111;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_110;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi110;

} t_trial_110;


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
		port_code = 112;
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_120;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi120;

} t_trial_120;


trial {  
   #trial_duration = 15000;
   stimulus_event {
      sound w_mysound;
      time = $my_intersound_duration;
      code = "start_sound"; 
   };

   # then we show 20 nothing stimuli, just to send codes
   LOOP $i 20;
      nothing n_pulse_200;
      time = '$my_intersound_duration + int($i * 500) + 1500'; # start at 1500 after sound onset, stops at 11000 after sound onset 
    ENDLOOP;

	stimulus_event {
			picture p_fix;
			duration = 500; # will be adjusted in pcl
		} s_isi200;

} t_trial_200;


############
# BASELINE #
############

#reste à déterminer si on prend la baseline avec une croix ou "pause"
/*text { caption = "+";  font_color = 180,180,180; font_size = 40; text_align = align_center;} c_fix;
picture {
   text c_fix;
   x = 0;
   y = 0;   
} p_fix;*/

text { caption = "pause" ; font_color = 180,180,180; font_size = 40; font = "Verdana"; text_align = align_center;} c_pause;
picture {
	text c_pause;
	x = 0;
	y = 0;
} p_pause;

trial {
   start_delay = 0;
   trial_duration = $my_baseline_duration;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_pause;
      time = 0;
      duration = $my_baseline_duration; 
		code = "Bfix";
		port_code = 110;
   } s_baselinefix ;

} t_baselinefix;

#############
# QUESTIONS #
#############

/*trial {  
   trial_duration = stimuli_length;
   trial_type = fixed ;

   stimulus_event {
      sound w_question;
      time = 3000;
      code = "start_question"; 
   };

   stimulus_event {
      sound w_test1_yes;
      deltat = 8000;
      code = "test1_yes";
      target_button = 1; 
   };

   stimulus_event {
      sound w_test1_no;
      deltat = 3000;
      code = "test1_no";
   };

   stimulus_event {
      sound w_test2_no;
      deltat = 3000;
      code = "test2_no";
   };

   stimulus_event {
      sound w_test2_yes;
      deltat = 3000;
      code = "test2_yes";
      target_button = 1; 
   };

   stimulus_event {
      sound w_test3_yes;
      deltat = 3000;
      code = "test3_yes";
      target_button = 1; 
   };

   stimulus_event {
      sound w_test3_no;
      deltat = 3000;
      code = "test3_no";
   };

} t_question; */

trial {
    picture {
        text { caption = "+"; font_size = 48; };
        x = 0; y = 0;
    } fix_pic;
    duration = 10000;
    code = "fix";
} initialfixation;





