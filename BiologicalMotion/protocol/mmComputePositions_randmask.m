function maskdots = mmComputePositions_randmask(wmask, nd, mperiods, mphases, t, mspeed, xcenter, ycenter,invert);

%DC: added input parameter "invert".  If invert == 5, 6, switch x and z

%maskdots = mmComputePositions_randmask(wmask, nd, mperiods, mphases, t, mspeed, xcenter, ycenter);
%
%Computes the array of dots to draw as the current frame of the scrambled walker mask
%
%INPUTS
%wmask                  mask data in mm format
%nd                     # mask dots
%mperiods:              vector of periods for each marker (scaled in 1/120 s) - uniform or random
%phases:                vector of phases for each marker (rad) - scrambled or uniform, includes random starting phase
%t                      time of current frame
%mspeed                 walker speed factor from plw_w
%xcenter, ycenter:      centre of display
%
%OUTPUTS
%maskdots               final array of dots to draw.
%                       row 1 = screen x coords, row 2 = screen y coords, columns = dots

%INTERNAL
%harmonics              number of Fourier components in this mm data
%mm2D                   mm data transformed: basis postures rotated according to current azimuth and projected onto
%                       yz plane (screen)
%                       format as mm data except now only y and z components


%Get variables
harmonics = (size(wmask,2)-1)/2;

%Project walker onto yz plane (the screen)
%NOTE: From here on in we work in a new coord system for the SCREEN, which is an xy plane
%new x axis = old y axis
%new y axis = -old z axis
%(0,0) of screen coords is at top left hand corner, (1024,768) is at bottom RH corner
if invert == 0 || invert == 1
    mm2D(1:nd,:)=wmask(nd+1:2*nd,:);
    mm2D(nd+1:2*nd,:)=-wmask(2*nd+1:3*nd,:);
elseif invert == 5 || invert == 6
    mm2D(1:nd,:)= -wmask(2*nd+1:3*nd,:);
    mm2D(nd+1:2*nd,:)= wmask(nd+1:2*nd,:);
end


%Fill the mean posture into the final dot matrix
maskdots=reshape(mm2D(1:2*nd,1),nd,2);

%Compute all Fourier harmonics and add to final dot matrix
for i=1:harmonics
    maskdots(:,1) = maskdots(:,1) + mm2D(1:nd,2*i).*sin(i*(2*pi*120*mspeed*t./mperiods+mphases)) + mm2D(1:nd,2*i+1).*cos(i*(2*pi*120*mspeed*t./mperiods+mphases));
    maskdots(:,2) = maskdots(:,2) + mm2D(nd+1:2*nd,2*i).*sin(i*(2*pi*120*mspeed*t./mperiods+mphases)) + mm2D(nd+1:2*nd,2*i+1).*cos(i*(2*pi*120*mspeed*t./mperiods+mphases));
end

%Reshape for drawdots routine to be called later
maskdots=maskdots';
%-----------------

%Finally translate walker to xcenter, ycenter
maskdots(1,:)=maskdots(1,:)+xcenter;
maskdots(2,:)=maskdots(2,:)+ycenter;