function [md2D, markers, xcenterw, ycenterw] = mdprepare_single(w1data, azimuth, invert, trans, offx, offy, plotsize, walkersize, xcenter, ycenter,scramblespat, scrambletemp,fr)        

%DC hacked to allow scrambling (spatial and temporal) of the md walker data

%[md2D, markers, xcenterw, ycenterw] = mdprepare_single(w1data, azimuth, invert, trans, offx, offy, plotsize, walkersize, xcenter, ycenter)        
%
%Prepares an md walker before display by applying all transformations that
%are not specific to a single frame of animation
%Applies inversion, size, azimuth, 2D projection, centring
%
%INPUTS
%w1data             mm walker data
%azimuth
%invert             invert option from plw: 0 = no inversion, 1 = walker upside down
%trans              (x,y) vector containing margins for random walker translation (pixels)
%plotsize           plot area for mask (pixels) set in pptwalk_singleNEW
%walkersize         size parameter from plw: 1 = full size
%xcenter            screen centre coords
%ycenter
%
%OUTPUTS
%md2D               Prepared and 2-D projected md data
%                   format: dim1=frames
%                           dim2=markers
%                           dim3(1)=x, dim3(2)=y (screen coords)
%markers            # walker markers
%xcenterw           final display horizontal centre of walker
%ycenterw           final display vertical centre of walker

%INTERNAL
%x_trans            random walker translation horizontally across monitor (multiplier x plot area)
%y_trans            random walker translation vertically across monitor (multiplier x plot area)
%include            Boolean matrix of md elements to be included in preparation. Elements
%                   set to -9999 prior to PLDTools will not be included and are marked
%                   with a 0 in this matrix
%xmean
%ymean
%zmean
%
%PARAMETERS
screenscale=10;    %Scale factor to accomodate screen size (20 default)


%EXTRACT INFO TO VARS
x_trans = trans(1);                                                                         %Extract x margin
y_trans = trans(2);                                                                         %Extract y margin
markers=size(w1data,2);

%Ignore any markers which have coordinates manually set to -9999 - these will not appear
%in the plot.
include=w1data~=-9999;

%INVERSION (MIRROR FLIP) %restoring dc
if invert==0                             
    temp=w1data(:,:,3);
    temp(include(:,:,3))=-temp(include(:,:,3));
    
    w1data(:,:,3)=temp;
    
end    

%In the case of the target walker, we check for vertical layout

if invert == 1 && scramblespat == 2
    %check if we are scrambling in addition to inversion, then inversion means we also retain
    %vertical order, so let's restore it
    
    if scramblespat == 2
        temp=w1data(:,:,3);
        subt = 2.*(mean(temp));
        subt = repmat(subt, length(temp), 1);
        w1data(:,:,3) = temp - subt;
    end
        
end



    
%SIZE
%2 scalings to apply: walkersize parameter input to plw, and constant screenscale factor
w1data(include)=w1data(include)/screenscale*walkersize;
  

%check for scrambling
if scramblespat == 2;
    w1data = mdSpatialScramble(w1data, [100,400,300], 0); %x,y,z
end

if scrambletemp == 2;
    w1data = mdPhaseScramble(w1data);
end

%CENTRE WALKER ABOUT (0,0,0)
%{
temp=w1data(:,:,1);
xmean=mean(temp(include(:,:,1)));
w1data(:,:,1)=w1data(:,:,1)-xmean*include(:,:,1);
temp=w1data(:,:,2);
ymean=mean(temp(include(:,:,2)));
w1data(:,:,2)=w1data(:,:,2)-ymean*include(:,:,2);
%}
temp=w1data(:,:,3);
zmean=mean(temp(include(:,:,3)));
w1data(:,:,3)=w1data(:,:,3)-zmean*include(:,:,3);



%ROTATE TO AZIMUTH AND PROJECT ONTO 2D
%Walker is projected onto yz plane. New x axis=old y axis, new y axis=-old z axis
%From here on markers set to -9999 are included in calculations and we rely on their
%extreme coordinates to not be displayed
md2D(:,:,1)=w1data(:,:,2)*cos((azimuth)*2*pi/360)+w1data(:,:,1)*sin((azimuth)*2*pi/360);
md2D(:,:,2)=-w1data(:,:,3);

%CALCULATE EVENTUAL WALKER CENTRE ON DISPLAY
xcenterw = xcenter+offx+(-1+2*rand)*x_trans*0.5*plotsize;
ycenterw = ycenter-offy+(-1+2*rand)*y_trans*0.5*plotsize;									%off y is negative because
																							%screen y coords =
																							%-geometric y coords