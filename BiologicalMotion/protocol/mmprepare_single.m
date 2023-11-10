function [mm, markers, wperiods, wphases, xcenterw, ycenterw] = mmprepare_single(mm, scrambleoption, scramblex, scrambley, invert, trans, offx, offy, plotsize, xcenter, ycenter)        

%DC: if invert == 5, invert z;

%[mm, markers, wperiods, wphases, xcenterw, ycenterw] = mmprepare_single(mm, scrambleoption, scramblex, scrambley, invert, trans, offx, offy, plotsize, xcenter, ycenter)        
%
%Prepares an mm walker before display by applying all transformations that are not specific to a single frame of 
%animation: applies all scrambling, centres walker in coordinate system, inverts walker,
%restores walker to original coordinate system (mm units), and calculates final walker centre on screen
%
%INPUTS
%mm                 mm walker data
%scrambleoption     scramble option from plw
%                   0=no scrambling, 1=shuffle structure/markers, 2=scramble all markers across circular plot area
%                   10, 11, 12 = as above but phases scrambled too
%                   20, 21, 22 = as above but phases and periods scrambled too
%scramblex          from plw: 0-1: multiplying factor for how much of horizontal display is open to random
%                   offset scrambling occurs within a cylinder, and this informs the radius
%scrambley
%invert             invert option from plw: 0 = no inversion, 1 = walker upside down
%trans              (x,y) vector containing margins for random walker translation (pixels)
%plotsize           plot area for mask (pixels) set in pptwalk_singleNEW
%xcenter            screen centre coords
%ycenter
%
%OUTPUTS
%mm                 Prepared mm matrix
%wperiods           vector of periods for each marker (scaled by 1/120 s)
%wphases            vector of phases for each marker (rad)
%xcenterw           final display horizontal centre of walker
%ycenterw           final display vertical centre of walker
%markers

%INTERNAL
%period             walker period extracted from last row/col 1 of mm data (scaled in 1/120 s)
%wfactor            Size factor included in mm data
%x_trans            random walker translation horizontally across monitor (multiplier x plot area)
%y_trans            random walker translation vertically across monitor (multiplier x plot area)
%rad                random radii used for scrambling walker within cylinder
%theta              random angles used for scrambling walker within cylinder
%z                  random z used for scrambling walker within cylinder
%
%PARAMETERS
pdev=2;            %if marker periods are scrambled, veridical speed of each marker is multiplied by
                   %a different random number between 1/pdev and pdev (0.5 and 2 default) sampled from
                   %a logarithmic uniform distribution
                   
%Note: Rotation routine must occur at each frame -> in mmcomputepositions
%      Rotation routine rotates walker about the origin
%      Therefore centring the final walker display on screen must occur after rotation (if we centred on screen
%      here the walker would no longer be at centred at (0,0) -> rotation about (0,0) would then move the walker
%      away from screen centre)
%      However, in this routine we still calculate final walker centre on screen


%EXTRACT INFO TO VARS
period      =mm(end,1);         %Extract original walker period
wfactor     =mm(end,2);         %Extract mm data size factor
markers     =(size(mm,1)-1)/3;  %Get # markers
x_trans     =trans(1);          %Extract x margin
y_trans     =trans(2);          %Extract y margin

%CREATE MARKER PERIODS VECTOR - SCRAMBLED IF SELECTED
if scrambleoption >= 20                                     %Scramble periods             
    %Scramble periods
    %Speed is multiplied (i.e. period is divided by) a number between 1/pdev and pdev sampled from a 
    %logarithmic uniform distribution.
    %The equation below is simplified using the identity log(1/x)=-log(x)
    wperiods=period./exp(rand(markers,1)*(2*log(pdev))-log(pdev));
else                                                        %Don't scramble - all markers have the same veridical period
    wperiods=ones(markers,1)*period;  
end 

%CREATE MARKER PHASES VECTOR - SCRAMBLED IF SELECTED
if scrambleoption >= 10                                   
    wphases=2*pi*rand(markers,1);                           %Random phase for each marker
else                                                     
    wphases=2*pi*rand*ones(markers,1);                      %Uniform random starting phase for all markers
end

%SCRAMBLE OFFSETS IF SELECTED
if (scrambleoption==1) || (scrambleoption==11) || (scrambleoption==21) 
    %Shuffle structure of walker - i.e. shuffle markers
    randmarkers=randperm(markers);
    temp=[mm(randmarkers,1); mm(markers+randmarkers,1); mm(2*markers+randmarkers,1)];
    mm(1:end-1,1)=temp;
elseif (scrambleoption==2) || (scrambleoption==12) || (scrambleoption==22)
    %Scramble within a cylinder
    %Projection onto screen (yz projection) is always a rectangular cross-section of the cylinder
    %cylinder axis = z axis
    %cylinder radius projected as width of rectangle - scaled by scramblex - max 1 = whole plot area
    %cylinder height projected as height of rectangle - scaled by scrambley
    %Cylinder is used because then if the scrambled walker rotates the depth of the volume the dots can inhabit
    %remains constant

    %Create random cylindrical coords
    rad=rand(markers,1)*scramblex*plotsize/2;                                   %radii
    theta=rand(markers,1)*2*pi;                                                 %cylinder angles
    z=(-1+2*rand(markers,1))*plotsize/2*scrambley;                              %cylinder z
    
    %Scramble markers within cylinder
    mm(1:markers,1)=rad.*cos(theta);                                            %x coords
    mm(markers+1:markers*2,1)=rad.*sin(theta);                                  %y coords
    mm(markers*2+1:markers*3,1)=z;                                              %z coords
end;

if scrambleoption~=2 && scrambleoption~=12 && scrambleoption~=22
    %INVERSION (MIRROR FLIP)
    if invert==1 || invert==5
        mm(2*markers+1:markers*3,:)=-mm(2*markers+1:markers*3,:);
    end;
    
    %Restore walker to native coordinates (mm units)
    mm(1:3*markers,:)=mm(1:3*markers,:)*wfactor;    
    
    %CENTRE WALKER ABOUT (0,0,0)
    %Necessary because rotation in mmcompute positions is about origin
    %Only need to look at mean walker component here
    mm(1:markers,1)=mm(1:markers,1)-mean(mm(1:markers,1));                                      %Centre x 
    mm(markers+1:markers*2,1)=mm(markers+1:markers*2,1)-mean(mm(markers+1:markers*2,1));        %Centre y
    mm(markers*2+1:markers*3,1)=mm(markers*2+1:markers*3,1)-mean(mm(markers*2+1:markers*3,1));  %Centre z
else
    %For walker scrambled across screen brand new mean points are created
    %->only harmonics need to be inverted and sized
    %->new points are already centred about screen (0,0)

    %INVERSION
    if invert==1 || invert==5
        mm(2*markers+1:markers*3,2:end)=-mm(2*markers+1:markers*3,2:end);
    end;

    %Restore walker to native coordinates (mm units)
    mm(1:3*markers,2:end)=mm(1:3*markers,2:end)*wfactor;
end

%CALCULATE EVENTUAL WALKER CENTRE ON DISPLAY
%Here x and y refer to eventual screen x & y axes
xcenterw = xcenter+offx+(-1+2*rand)*x_trans*0.5*plotsize;                      
ycenterw = ycenter-offy+(-1+2*rand)*y_trans*0.5*plotsize;