## Edited for IBC Dec, 2021 ##
## Himanshu Aggarwal, himanshu.aggarwal@inria.fr ##

scenario = "piopharriri_run2";
no_logfile = false;

default_background_color = 248,248, 248;

# PARAMETERS FOR fMRI:
scenario_type =  fMRI;
scan_period = 2000; #only for emulation
pulse_code = 255;
pulses_per_scan = 1;   
           
# response keys
active_buttons = 4;
button_codes = 1,2,3,4;

response_matching = simple_matching;

#default output port
#default_output_port = 1;

default_delta_time = 0;   
$tdur = 5000;
$pdur = 4800;

# default screen size
#screen_height = 768;
#screen_width = 1024;
#screen_bit_depth = 16;  

begin;

picture {} default;

text{caption="

Dans cette tâche, on va vous montrer des FORMES et des VISAGES.

Lorsqu'une forme apparait, vous devez déterminer elle qui lui
correspond entre les deux examples presentees en-dessous
   
Vous répondrez avec L'INDEX (pour la forme à GAUCHE)
et LE MAJEUR (pour la forme à DROITE).
   
Par example:
   
Ici, c'est DROIT
   
Donc, répondrez avec LE MAJEUR.

";
font = "Arial";
font_size=24;
font_color=0,0,0;
}instr1;

text{caption="

Lorsque vous voyez des visages, appuyez sur le bouton 
correspondant au visage ayant la MÊME ÉMOTION 
que le visage du dessus.

Par example:

Ici, c'est la forme à GAUCHE
   
Donc, répondrez avec L'INDEX

";
font = "Arial";
font_size=24;
font_color=0,0,0;
}instr2;

text{caption="+";
font = "Arial";
font_size=60;
font_color=255,0,0;
}instr3;

picture{
	text instr1;x=0;y=100;
	  bitmap { filename = "Dia1_smaller.png"; };
   x = 0; y = -350;
}waitscan_pic;

picture{
	text instr2;x=0;y=100;
	  bitmap { filename = "Dia2_smaller.png"; };
   x = 0; y = -350;
}waitscan_pic2;

picture{
	text instr3;x=0;y=0;
}waitscan_pic3;


#TEMPLATE "filenames_11thru26.tem";
TEMPLATE "filenames_31thru46.tem";

trial {
trial_duration=forever;
trial_type=first_response;
 picture waitscan_pic;
time=0;
};

trial {
trial_duration=forever;
trial_type=first_response;
 picture waitscan_pic2;
time=0;
};

trial {
trial_type=fixed;
 picture waitscan_pic3;
time=0;
};



trial {
   trial_mri_pulse = 1;
   picture default;
};

TEMPLATE "trials_61thru66.tem"; #control

TEMPLATE "trials_41thru46.tem"; #emo

TEMPLATE "trials_71thru76_2.tem"; # herhaling controle 1, shuffled

TEMPLATE "trials_21thru26.tem"; # emo uit a deel 2

TEMPLATE "trials_51thru56.tem"; #controle

TEMPLATE "trials_31thru36.tem"; #emo

TEMPLATE "trials_71thru76.tem"; #control

TEMPLATE "trials_11thru16.tem"; #emo uit a

trial {
   picture {text { caption = "FIN"; font="arial"; font_color= 0,0,0; font_size = 60;}; x=0; y=0;};
   duration = 4000;
};
