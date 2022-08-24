## Edited for IBC Dec, 2021 ##
## Himanshu Aggarwal, himanshu.aggarwal@inria.fr ##

## GEZICHTEN TAAKJE VOOR PIOP STUDIE -- 10 MAART 2015 -- SUZANNE OOSTERWIJK ##

## HEADERS ##

scenario_type = fMRI;
pulses_per_scan = 180;
pulse_code = 30;
default_background_color = 0,0,0;
response_matching = simple_matching;
default_font_size = 28;
default_font = "arial";
active_buttons = 4;
button_codes = 1,2,3,4;

response_logging = log_all;
no_logfile = false;   

###################################### SDL ############################################

begin; 

text {
			caption = 	"Vous allez maintenant voir une série de courtes vidéos d'expressions faciales pour 6 minutes. 
			Vous n'êtes pas obligé de répondre dans cette série.

			Regardez les vidéos et essayez de vous souvenir 
			des VISAGES ET des EXPRESSIONS.
			
			Nous vous demanderons plus tard si vous les avez déjà vus.

			Appuyez sur le bouton sous votre index pour commencer"; 
			font = "arial";		
} introduction;

picture {text introduction; x = 0; y = 0;} introduction_picture;

text {caption = "FIN";font="arial"; font_color= 255,255,255; font_size = 60;} end;

picture {text { caption = "+"; font="arial"; font_color= 255,0,0; font_size = 60;}; x=0; y=0;} pulsetrial;

## INTRO TRIAL ##

trial {
	all_responses		= true; 
	trial_type 			= first_response;
	trial_duration 	= forever;
	stimulus_event {picture introduction_picture; time = 0;} introduction_event;
} introduction_trial;

## DEFAULT VOOR ITI ##

picture {background_color = 0,0,0;} default;

## VIDEO TRIAL ##

trial {
	trial_duration = 4000; 
		stimulus_event {
			video {
				filename = "A03.avi";
				release_on_stop = false;
			} vid;
			code = " ";
		} showvideo;
	} videotrial; 

## EINDE TRIAL ##

picture {text end; x = 0; y = 0;} end_picture;

trial {
	trial_duration = 4000; 
	stimulus_event {
		picture end_picture;
	} end_event;
} end_trial;

###################################### PCL ############################################

begin_pcl;

## INTRO EN WACHTEN OP PULSE ##

introduction_trial.present();

pulsetrial.present();
int currentpulse_count=pulse_manager.main_pulse_count();
loop until pulse_manager.main_pulse_count()-currentpulse_count>0 begin                 
end;

## STIMULUS ARRAYS ##

# creer gerandomiseerde array met video's. 
			
array <string> video_array[40] =
{"J11.avi", "J03.avi", "J07.avi", "N08.avi",
 "A03.avi", "N15.avi", "N12.avi", "N04.avi",
 "A08.avi", "P04.avi", "J08.avi", "A16.avi",
 "P16.avi", "C16.avi", "J15.avi", "P07.avi",
 "A12.avi", "P03.avi", "C15.avi", "N03.avi",
 "C07.avi", "C03.avi", "J16.avi", "N07.avi",
 "P12.avi", "N16.avi", "P11.avi", "C11.avi",
 "C12.avi", "J04.avi", "N11.avi", "A04.avi",
 "A07.avi", "A11.avi", "A15.avi", "P15.avi",
 "P08.avi", "C08.avi", "C04.avi", "J12.avi"};

###################################### TRIAL LOOP ############################################
	
	# Eerst drie herhalingen van zelfde video. 
	
	int code = 0; 
		
	int start_trial = clock.time() + 5000;								   # 5 seconden pauze om volgende video in te laden.	
	logfile.add_event_entry("ITI");						

	vid.set_filename(video_array[1]);										# klaarzetten video voor trial 1. 
	string vidname = video_array[1];
	vid.prepare();
	
	if (vidname=="J03.avi" || vidname=="J04.avi" || vidname=="J11.avi" || vidname=="J12.avi" || vidname=="J07.avi" || vidname=="J08.avi" || vidname=="J15.avi" || vidname=="J16.avi") then
	code = 100; 
	elseif (vidname=="P03.avi" || vidname=="P04.avi" || vidname=="P11.avi" || vidname=="P12.avi" || vidname=="P07.avi" || vidname=="P08.avi" || vidname=="P15.avi" || vidname=="P16.avi") then
	code = 200;
	elseif (vidname=="A03.avi" || vidname=="A04.avi" || vidname=="A11.avi" || vidname=="A12.avi" || vidname=="A07.avi" || vidname=="A08.avi" || vidname=="A15.avi" || vidname=="A16.avi") then
	code = 300;
	elseif (vidname=="C03.avi" || vidname=="C04.avi" || vidname=="C11.avi" || vidname=="C12.avi" || vidname=="C07.avi" || vidname=="C08.avi" || vidname=="C15.avi" || vidname=="C16.avi") then
	code = 400;
	elseif (vidname=="N03.avi" || vidname=="N04.avi" || vidname=="N11.avi" || vidname=="N12.avi" || vidname=="N07.avi" || vidname=="N08.avi" || vidname=="N15.avi" || vidname=="N16.avi") then
	code = 500;
	end;
	
	default.present();
	loop until clock.time() > start_trial begin end;				# vaste ITI die maximaal 2 (video) + 5 sec duurt

#Loop voor random videos

loop int i = 1 until i > 39 begin;

	int t_end = clock.time() + 9000;
	
	logfile.add_event_entry(vidname + " ;startvideo" );		# set event code in logfile voor start video
	showvideo.set_event_code(string(code)); 						# code	
	videotrial.present();												# tonen video				 
	
	logfile.add_event_entry("ITI");						
	
	vid.set_filename(video_array[i+1]);								# inladen video voor volgende trial tijdens ITI
	vidname = video_array[i+1];
	vid.prepare();
	
	if (vidname=="J03.avi" || vidname=="J04.avi" || vidname=="J11.avi" || vidname=="J12.avi" || vidname=="J07.avi" || vidname=="J08.avi" || vidname=="J15.avi" || vidname=="J16.avi") then
	code = 100; 
	elseif (vidname=="P03.avi" || vidname=="P04.avi" || vidname=="P11.avi" || vidname=="P12.avi" || vidname=="P07.avi" || vidname=="P08.avi" || vidname=="P15.avi" || vidname=="P16.avi") then
	code = 200;
	elseif (vidname=="A03.avi" || vidname=="A04.avi" || vidname=="A11.avi" || vidname=="A12.avi" || vidname=="A07.avi" || vidname=="A08.avi" || vidname=="A15.avi" || vidname=="A16.avi") then
	code = 300;
	elseif (vidname=="C03.avi" || vidname=="C04.avi" || vidname=="C11.avi" || vidname=="C12.avi" || vidname=="C07.avi" || vidname=="C08.avi" || vidname=="C15.avi" || vidname=="C16.avi") then
	code = 400;
	elseif (vidname=="N03.avi" || vidname=="N04.avi" || vidname=="N11.avi" || vidname=="N12.avi" || vidname=="N07.avi" || vidname=="N08.avi" || vidname=="N15.avi" || vidname=="N16.avi") then
	code = 500;
	end;
	
	default.present();														# vaste ITI die maximaal 2 (video) + 5 sec duurt
	loop until clock.time() > t_end begin end;
		
	i = i + 1;
			
end;

	logfile.add_event_entry(vidname + " ;startvideo" );				# set event code in logfile voor start video
	showvideo.set_event_code(string(code)); 								# event code video
	videotrial.present();														# tonen laatste video
	
	int start_final = clock.time() + 5000;	
	default.present();	
	loop until clock.time() > start_final begin end;

end_trial.present();

