## Edited for IBC Dec, 2021 ##
## Himanshu Aggarwal, himanshu.aggarwal@inria.fr ##

##########################################################################################
####					HEADER PARAMETERS 
##########################################################################################
response_matching = simple_matching;
active_buttons = 4;
button_codes = 1,2,3,4;
event_code_delimiter = "/t";
default_font_size = 24;
default_background_color = 0,0,0;
scenario_type = fMRI;    
#scenario_type = fMRI_emulation;
scan_period = 2000;   
pulses_per_scan = 1; # of 8 met 1 pulse per volume
sequence_interrupt = true; # The value of this parameter determines if a sequence of events with a given "mri_pulse" number can be interrupted by the occurence of a later main pulse with an associated event sequence if the previous event sequence has not completed.
                           # This setting does *NOT* work correctly. It is important to keep the total trial duration lower than the scan_period, especially when a response to the trial is needed.
pulse_code = 255; # dit zorgt ervoor dat fMRI pulses van deze waarde worden ge-logged

begin;
##########################################################################################
####					BUILDING BLOCKS
##########################################################################################
array {
bitmap {filename = "C1.BMP"; trans_src_color = 119,119,119;}A;   
bitmap {filename = "C2.BMP"; trans_src_color =  119,119,119;};
bitmap {filename = "C3.BMP"; trans_src_color =  119,119,119;};
bitmap {filename = "C4.BMP"; trans_src_color =  119,119,119;};
} stimuli;

bitmap {filename = "empty.BMP"; trans_src_color = 0,0,0;} empty;

text { caption = "+"; font_color = 255,0,0; font_size = 60; trans_src_color = 0,0,0;} fixationCross;
text { caption = "+"; font_color = 0,255,0; font_size = 60; trans_src_color = 0,0,0;} fixationCrossAlert;
##########################################################################################
####					PICTURE STIMULI 
##########################################################################################
picture {
	text fixationCross; x = 0; y = 0;
} default;

trial {
	trial_duration = 1000;
	picture default;
	code = "0";
} default_stim;

trial {
	trial_duration = 1000;
	picture {
		background_color = 0,0,0;
		text fixationCrossAlert; x = 0; y = 0;
	};
	code = "10";
} alert;

trial {
	trial_duration = 2000;
	picture {
		background_color = 0,0,0;
		text fixationCross; x = 0; y = 0;
		};
	code = "30";
} fixation;

picture {
	background_color = 120,120,120;
	
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	
	text fixationCross; x = 0; y = 0;
} sample;

picture {
	background_color = 120,120,120;
	
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	bitmap A;	x = 180; y = 208;
	
	text fixationCross; x = 0; y = 0;
} match;

trial {
	trial_duration = 1000;
	picture sample;
	code = "20";		
} sample_stim;

trial {
	trial_duration = 1000;
	picture match;
	code = "40";
} match_stim;

picture {background_color = 0,0,0; text{caption = "REPOND MAINTENANT:
meme                difference
l'index             le majeur

Appuyez avec l'index ou le majeur si vous n'avez rien vu."; font_size = 24;trans_src_color = 0,0,0;}; x = 0; y = 0; } response_screen;
##########################################################################################
####					TRIALS
##########################################################################################
trial {     
  trial_duration = forever;                #de proefpersoon bepaalt wanneer het experiment start. 
  trial_type = specific_response;
  terminator_button = 2;
  picture { text { caption = "INSTRUCTIONS:
	1. Fixer en permanence au centre de l'ecran.
	2. Lorsque la croix devient verte, 6 rectangles vous sont présentes.
	3. Un instant plus tard, un des rectangles réapparaît.
	4. Si son orientation était la MÊME, appuyez avec L'INDEX.
	5. Sinon, appuyez avec LE MAJEUR.
	6. Parfois, les rectangles n'apparaissent pas, appuyez quand meme avec l'index ou le majeur.
		
	Appuyez avec l'index pour demarrer l'experience"; text_align="align_left"; font_size = 30;}; 
  x = 0; y = 0;};
  } instructie;       
     
trial {
   picture {text { caption = "+"; font="arial"; font_color= 255,0,0; font_size = 60;};
   x = 0; y = 0;
   };   
   time = 0;
   duration = next_picture;
  
  picture default;
   mri_pulse = 1;
   duration = 16;  
   code = "0";
} startTrial;         

trial {
   picture {text { caption = "FIN"; font="arial"; font_color= 255,255,255; font_size = 60;}; x=0; y=0;};
   duration = 4000;
} endTrial;

begin_pcl;
##########################################################################################
####					DEFINE ALL VARIABLES USED
##########################################################################################
int cPositions, nPositions = 6, end_time, cTrial, old_response, new_response, last_response, random_location;
double angle, angle_2use, eccentricity = 200.0, xloc, yloc;
array<int> potential_locations[nPositions];
loop cPositions = 1; until cPositions > nPositions begin
		potential_locations[cPositions] = cPositions;
		cPositions = cPositions + 1; 
end;
array<int> conditions[60] = {0,2,0,2,1,0,3,2,0,1,0,2,1,2,2,0,1,1,0,1,3,2,1,0,3,0,1,1,0,1,3,3,0,2,0,2,0,1,2,0,3,1,2,2,1,0,2,2,0,2,2,1,0,3,0,3,0,1,1,0};
array<int> durations[60] = {8,6,6,6,6,4,6,6,4,6,2,6,6,6,6,2,6,6,2,6,6,6,6,2,6,2,6,6,4,6,6,6,4,6,2,6,2,6,6,4,6,6,6,6,6,4,6,6,2,6,6,6,2,6,2,6,10,6,6,8};
array<int> random_locations[60] = {4,3,6,6,1,2,6,6,4,5,4,3,5,4,3,1,1,2,2,6,2,3,3,6,1,2,2,5,3,3,5,3,5,6,1,4,3,1,1,6,5,2,1,4,4,1,5,6,2,2,4,5,1,4,3,4,6,2,5,5};
array<int> potential_orientations[60][8] = {{1,2,4,3,3,2,4,1},{2,1,3,4,4,3,2,1},{1,4,2,3,4,3,2,1},{3,4,2,1,3,1,4,2},{1,4,4,2,3,2,3,1},{1,2,3,4,2,3,4,1},{3,4,1,2,1,4,2,3},{1,2,2,4,4,1,3,3},{1,4,4,2,2,3,1,3},{3,1,4,1,2,2,4,3},{1,4,1,3,4,2,2,3},{2,3,3,2,1,1,4,4},{1,3,4,4,2,1,3,2},{3,4,3,1,2,1,4,2},{4,3,1,3,2,1,2,4},{3,2,1,4,1,2,4,3},{3,2,3,4,2,1,4,1},{4,2,3,3,4,2,1,1},{1,3,2,2,4,1,3,4},{2,1,3,3,4,4,1,2},{3,2,4,3,1,2,1,4},{4,2,2,1,3,3,1,4},{4,1,2,1,3,3,4,2},{4,2,4,3,3,1,1,2},{4,1,3,3,4,2,2,1},{4,2,1,4,2,1,3,3},{3,4,2,4,1,2,3,1},{2,3,2,1,4,1,4,3},{3,4,2,1,3,1,4,2},{1,4,3,2,3,1,2,4},{2,1,4,3,4,1,3,2},{1,3,4,4,2,2,3,1},{1,2,4,2,3,1,3,4},{4,3,4,2,3,2,1,1},{2,2,3,3,4,1,4,1},{4,3,2,2,1,3,1,4},{3,4,1,2,4,1,3,2},{3,4,2,3,4,1,2,1},{2,1,3,1,2,3,4,4},{3,1,2,1,2,4,3,4},{3,2,2,1,4,4,3,1},{4,3,1,2,4,2,3,1},{3,1,2,4,3,4,1,2},{3,3,4,2,4,1,1,2},{3,1,2,1,2,4,3,4},{1,3,2,4,1,2,3,4},{3,1,3,4,2,4,2,1},{3,1,1,4,2,4,2,3},{3,2,4,3,2,1,1,4},{2,2,4,1,4,1,3,3},{4,3,1,3,4,1,2,2},{1,1,3,3,4,2,2,4},{3,2,1,2,4,3,1,4},{4,2,3,1,3,4,1,2},{3,3,2,1,2,4,1,4},{4,2,1,1,2,3,4,3},{3,4,4,1,2,1,3,2},{3,4,2,2,1,4,3,1},{4,3,1,3,2,4,1,2},{4,2,4,1,2,3,3,1}};

output_file out1 = new output_file;
out1.open_append(logfile.subject() + "piop_workingmemory_run1_log.txt");
##########################################################################################
####					DEFINE POSITIONS OF RECTANGLES
##########################################################################################
angle = 0.0;				
loop cPositions = 1; until cPositions >nPositions begin  
		angle_2use = angle/360.0*2.0*pi_value;
		xloc = sin(angle_2use)*eccentricity; 
		yloc = cos(angle_2use)*eccentricity; 
		
		sample.set_part_x(cPositions, xloc);
		sample.set_part_y(cPositions, yloc);
		match.set_part_x(cPositions, xloc);
		match.set_part_y(cPositions, yloc);
		
		angle= angle + 360.0/double(nPositions);
		cPositions = cPositions + 1; 
end;
##########################################################################################
####					DEFINE  ORIENTATION OF RECTANGLES
##########################################################################################
sub
	 createdisplays
begin
	random_location = random_locations[cTrial];
	# SET EVERYTHING TO INVISIBLE FIRST
	loop cPositions = 1; until cPositions > nPositions begin  
		sample.set_part(cPositions, empty);
		match.set_part(cPositions, empty);
		cPositions = cPositions + 1; 
	end;
	if conditions[cTrial] == 1 || conditions[cTrial] == 2 then
		potential_locations.shuffle();
		loop cPositions = 1; until cPositions > nPositions begin  
				sample.set_part(cPositions, stimuli[potential_orientations[cTrial][cPositions]]);
				
				if random_location == cPositions && conditions[cTrial] == 1 then
					match.set_part(cPositions, stimuli[potential_orientations[cTrial][cPositions]]);
				elseif random_location == cPositions && conditions[cTrial] == 2 then
					if potential_orientations[cTrial][cPositions] == 1 then
						match.set_part(cPositions, stimuli[3]);
					elseif potential_orientations[cTrial][cPositions] == 2 then
						match.set_part(cPositions, stimuli[4]);
					elseif potential_orientations[cTrial][cPositions] == 3 then
						match.set_part(cPositions, stimuli[1]);
					elseif potential_orientations[cTrial][cPositions] == 4 then
						match.set_part(cPositions, stimuli[2]);
					end;
				end;
				cPositions = cPositions + 1; 
		end;
	end;
end;
##########################################################################################
####					SUB PRESENT TRIAL
##########################################################################################
sub 
	present_trial
begin
	old_response = response_manager.total_response_count();
	last_response = 0;
	if conditions[cTrial] > 0 then	
			alert.present();	
			sample_stim.present();	
			fixation.present();	
			match_stim.present();
			loop end_time = clock.time() + 1000 until clock.time() >= end_time begin	
				response_screen.present();
				new_response = response_manager.total_response_count();
				if new_response > old_response then
					last_response = response_manager.last_response();
				end;	
			end;
	elseif conditions[cTrial] == 0 then
			default_stim.set_duration(durations[cTrial]*1000);
			default_stim.present();
	end;
end;
##########################################################################################
####					SUB WRITE OUTPUT
##########################################################################################
sub 
	write_output
begin
	out1.print(cTrial);	out1.print("\t");
	out1.print(conditions[cTrial]);	out1.print("\t");
	out1.print(durations[cTrial]); out1.print("\t");
	out1.print(last_response);
	out1.print("\n");
end;
#######################################################################################################################
instructie.present();
startTrial.present();

loop
	cTrial = 1;    
until                                   
	cTrial > conditions.count()
begin
	createdisplays();
	present_trial();
	write_output();
	
	cTrial = cTrial + 1;
end;

endTrial.present();
