scenario = "loca_lec1";   

$my_size=700;
$my_font_size=36;
$my_font="Courier new";

active_buttons = 2;
button_codes = 1,3;

# the task consists in deciding whether the presented string is an actual french word
# first button = yes
# second button = no

pulse_out = true; # pour pouvoir envoyer les codes des evenements a Neuroscan 
pulse_width = 6;    # largeur des pulses envoyes a Neuroscan

pcl_file = "pcl_grubi1.pcl";
default_background_color = 0, 0, 0;

begin;


# here specify a bitmap for the string
text { caption = "blague"; font_size = $my_font_size; font = $my_font;  text_align = align_center;} c_string;

text { caption = "+"; font_size = $my_font_size; font = $my_font; text_align = align_center;} c_fix;
#text { caption = "xhkgsz"; font_size = $my_font_size; font = $my_font; text_align = align_center;} c_fix;
                                                                                                   
picture {
   text c_fix;
   x = 0;
   y = 0;   
} default;
                                                                                                   
picture {
   text c_fix;
   x = 0;
   y = 0;   
} p_fix;

picture {
   text c_string;
   x = 0;
   y = 0;   
} p_string;

trial {
   start_delay = 0;
   trial_duration = stimuli_length;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_fix;
      time = 0;
      duration = 5000; 
   } s_init;
} t_init;

trial {
   start_delay = 0;
   trial_duration = stimuli_length;
   trial_type = fixed ;
   
   stimulus_event {
      picture p_fix;
      time = 0;
      duration = 1000; # adjust
      code = "fix1";
      port_code = 1;
   } s_fix1;

   stimulus_event {
      picture p_string;
      deltat = 1000;  # adjust
      duration = 700; # 200 
      code = "string"; # adjust
      port_code = 1;
   } s_string;

   stimulus_event {
      picture p_fix;
      deltat = 700;
      duration = 1500;
      code = "fix2";
      port_code = 1;
   } s_fix2;
   
} t_trial;

   
   
                                                                                                   
