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
			caption = "Vous allez maintenant voir une série de courtes vidéos d'expressions faciales pour 6 minutes.
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
				filename = "A01.avi";
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
{"P09.avi", "C02.avi", "A10.avi", "A13.avi",
 "N13.avi", "A09.avi", "J10.avi", "N14.avi",
 "A01.avi", "C14.avi", "P06.avi", "N09.avi",
 "N02.avi", "C10.avi", "P05.avi", "N01.avi",
 "J13.avi", "A02.avi", "C01.avi", "J01.avi",
 "A06.avi", "J05.avi", "J06.avi", "P13.avi",
 "C06.avi", "A14.avi", "P01.avi", "P14.avi",
 "P02.avi", "J02.avi", "C09.avi", "J14.avi",
 "P10.avi", "C13.avi", "A05.avi", "N06.avi",
 "J09.avi", "N10.avi", "N05.avi", "C05.avi"}; 

###################################### TRIAL LOOP ############################################
	
	# Eerst drie herhalingen van zelfde video. 
	
	int code = 0; 
	
	int start_trial = clock.time() + 5000;								   # 5 seconden pauze om volgende video in te laden.	
	logfile.add_event_entry("ITI");						

	vid.set_filename(video_array[1]);										# klaarzetten video voor trial 1. 
	string vidname = video_array[1];
	vid.prepare();
	
	if (vidname=="J01.avi" || vidname=="J02.avi" || vidname=="J09.avi" || vidname=="J10.avi" || vidname=="J05.avi" || vidname=="J06.avi" || vidname=="J13.avi" || vidname=="J14.avi") then
	code = 100; 
	elseif (vidname=="P01.avi" || vidname=="P02.avi" || vidname=="P09.avi" || vidname=="P10.avi" || vidname=="P05.avi" || vidname=="P06.avi" || vidname=="P13.avi" || vidname=="P14.avi") then
	code = 200;
	elseif (vidname=="A01.avi" || vidname=="A02.avi" || vidname=="A09.avi" || vidname=="A10.avi" || vidname=="A05.avi" || vidname=="A06.avi" || vidname=="A13.avi" || vidname=="A14.avi") then
	code = 300;
	elseif (vidname=="C01.avi" || vidname=="C02.avi" || vidname=="C09.avi" || vidname=="C10.avi" || vidname=="C05.avi" || vidname=="C06.avi" || vidname=="C13.avi" || vidname=="C14.avi") then
	code = 400;
	elseif (vidname=="N01.avi" || vidname=="N02.avi" || vidname=="N09.avi" || vidname=="N10.avi" || vidname=="N05.avi" || vidname=="N06.avi" || vidname=="N13.avi" || vidname=="N14.avi") then
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
	
	if (vidname=="J01.avi" || vidname=="J02.avi" || vidname=="J09.avi" || vidname=="J10.avi" || vidname=="J05.avi" || vidname=="J06.avi" || vidname=="J13.avi" || vidname=="J14.avi") then
	code = 100; 
	elseif (vidname=="P01.avi" || vidname=="P02.avi" || vidname=="P09.avi" || vidname=="P10.avi" || vidname=="P05.avi" || vidname=="P06.avi" || vidname=="P13.avi" || vidname=="P14.avi") then
	code = 200;
	elseif (vidname=="A01.avi" || vidname=="A02.avi" || vidname=="A09.avi" || vidname=="A10.avi" || vidname=="A05.avi" || vidname=="A06.avi" || vidname=="A13.avi" || vidname=="A14.avi") then
	code = 300;
	elseif (vidname=="C01.avi" || vidname=="C02.avi" || vidname=="C09.avi" || vidname=="C10.avi" || vidname=="C05.avi" || vidname=="C06.avi" || vidname=="C13.avi" || vidname=="C14.avi") then
	code = 400;
	elseif (vidname=="N01.avi" || vidname=="N02.avi" || vidname=="N09.avi" || vidname=="N10.avi" || vidname=="N05.avi" || vidname=="N06.avi" || vidname=="N13.avi" || vidname=="N14.avi") then
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

