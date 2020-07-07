function maskdots=computelinmask(nd, plotsize, xcenter, ycenter, lifetime, min_sp, max_sp, fr)

%maskdots=computelinmask(nd, plotsize, xcenter, ycenter, lifetime, min_sp, max_sp, fr)
%
%Calculates the display dot matrix for a linear mask
%
%INPUTS
%nd                 number of mask dots
%plotsize           
%xcenter            center x coord of display
%ycenter            center y coord of display
%lifetime           lifetime of a dot (0 means infinite lifetime)
%min_sp             minimum dot speed (pixels/s)
%max_sp             maximum dot speed (pixels/s)
%fr                 current frame
%
%OUTPUTS
%maskdots           display dot matrix for linear mask

%INTERNAL
%X                  x coords of mask dots
%Y                  y coords of mask dots
%SP                 speeds of dots (pixels/s)
%D                  directions of dots (rad)
%AGES               ages of dots (set to 0 for infinite lifetime)
%T                  time last frame was drawn
%t                  time of this frame

%vars are persistent so that dots can be updated in each call to computelinmask frame by frame
persistent X
persistent Y
persistent SP
persistent D
persistent AGES
persistent T

if fr==1;                                                           %For the first frame...
    %Random initial positions, speeds, directions, ages
    X = round(rand(nd,1).*plotsize+xcenter-plotsize/2);
    Y = round(rand(nd,1).*plotsize+ycenter-plotsize/2);
    SP = round(min_sp+(max_sp-min_sp)*rand(nd,1));
    D = (2*pi*rand(nd,1));
    if lifetime~=0
        AGES = (lifetime*rand(nd,1));                               %initial lifetime between 0 and lifetime
    else
        AGES=zeros(nd,1);                                           %else dots never age -> infinite lifetime
    end

    T=GetSecs;                                                      %Capture time of this frame
else
    t=GetSecs;                                                      %Capture time of this frame

    %Move dots
    X=(X+sin(D).*SP*(t-T));
    Y=(Y+cos(D).*SP*(t-T));    
    if lifetime~=0; AGES=AGES+(t-T); end                            %Age dots if not infinite lifetime
    
    %Check for dots that need to die and reposition them
    dead=(X < xcenter-plotsize/2) | (X > xcenter+plotsize/2) | (Y < ycenter-plotsize/2) | (Y > ycenter+plotsize/2) | (AGES > lifetime);
    dead=find(dead==1);
    X(dead) = round(rand(size(dead,1),1).*plotsize+xcenter-plotsize/2);  
    Y(dead) = round(rand(size(dead,1),1).*plotsize+ycenter-plotsize/2);
    if lifetime~=0
        AGES(dead)=AGES(dead)-floor(AGES(dead)/lifetime)*lifetime;  %Reset the age of the dots that died
    else
        AGES(dead)=0;
    end
    
    T=t;                                                            %Record time of this frame
end;

%Populate the display dot matrix
for i=1:nd
    maskdots(1,i)=X(i);
    maskdots(2,i)=Y(i);
end