## Edited for IBC Dec, 2021 ##
## Himanshu Aggarwal, himanshu.aggarwal@inria.fr ##

## GEZICHTEN TAAKJE VOOR PIOP STUDIE -- 10 MAART 2015 -- SUZANNE OOSTERWIJK ##

## HEADERS ##

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
			caption = 	"Vous allez à nouveau voir une série de courtes vidéos d'expressions faciales pour 2 minutes.
			Vous venez d'en voir quelques-unes.

			Répondre avec L'INDEX si vous les AVEZ VUES 
            et avec LE MAJEUR si vous ne les AVEZ PAS VUES.
			
			Rappelez-vous qu'ils doivent être exactement les mêmes (visages et expressions)

			Appuyez sur le bouton sous votre index pour commencer."; 
			font = "arial";		
} introduction;

picture {text introduction; x = 0; y = 0;} introduction_picture;

text {caption = 	"FIN";font="arial"; font_color= 255,255,255; font_size = 60;} end;

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
    trial_type = first_response;
		stimulus_event {
			video {
				filename = "A01.avi";
				release_on_stop = false;
			} vid;
            target_button = 2;
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

## STIMULUS ARRAYS ##

# creer gerandomiseerde array met video's. 
			
array <string> video_array[6] =
{"Disgust-05.avi", "Fear-10.avi", "N13.avi", "J-M09.avi", "C-F05.avi", "A02.avi"}; 

###################################### TRIAL LOOP ############################################
	
	# Eerst drie herhalingen van zelfde video. 
	
	int code = 0; 
	
	int start_trial = clock.time() + 5000;								   # 5 seconden pauze om volgende video in te laden.	
	logfile.add_event_entry("ITI");						

	vid.set_filename(video_array[1]);										# klaarzetten video voor trial 1. 
	string vidname = video_array[1];
	vid.prepare();
	
	if (vidname=="A02.avi" || vidname=="N13.avi") then
	code = 100; 
	elseif (vidname=="Disgust-05.avi" || vidname=="Fear-10.avi") then
	code = 200;
	elseif (vidname=="C-F05.avi" || vidname=="J-M09.avi") then
	code = 300;
	end;
	
	default.present();
	loop until clock.time() > start_trial begin end;				# vaste ITI die maximaal 2 (video) + 5 sec duurt

#Loop voor random videos

loop int i = 1 until i > 5 begin;

	int t_end = clock.time() + 9000;
	
	logfile.add_event_entry(vidname + " ;startvideo" );		# set event code in logfile voor start video
	showvideo.set_event_code(string(code)); 						# code	
	videotrial.present();												# tonen video				 
	
	logfile.add_event_entry("ITI");						
	
	vid.set_filename(video_array[i+1]);								# inladen video voor volgende trial tijdens ITI
	vidname = video_array[i+1];
	vid.prepare();
	
	if (vidname=="A02.avi" || vidname=="N13.avi") then
    code = 100; 
    elseif (vidname=="Disgust-05.avi" || vidname=="Fear-10.avi") then
    code = 200;
    elseif (vidname=="C-F05.avi" || vidname=="J-M09.avi") then
    code = 300;
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

