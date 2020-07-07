function [maskwalker, mperiods, mphases, nscrdots] = mmprepare_randmask(maskdata, nd, plotsize, mazimuth, msize, minvert, mscrambleoption, mmultiply)

% DC: added output "nscrdots", "nd" now = "nscrdots", added "mmultiply",
% "mwalkersoppo", etc. to equate local motion direction of display + mask

%[maskwalker, mperiods, mphases] = mmprepare_randmask(maskdata, nd, plotsize, mazimuth, msize, minvert, mscrambleoption)
%
%Prepares a walker to use as a scrambled mask
%
%INPUTS
%maskdata                   mm matrix with mask walker to scramble
%nd                         # mask dots
%plotsize
%mazimuth                   if invert=2 or 3 so that half the dots are rotated by 90 deg and the other half by =90 deg:
%							a vector of azimuths for each marker
%                           otherwise just a single azimuth for all, as usual
%msize                      size factor to multiply walker by - effectively determines amplitude of random point 
%                           oscillations
%minvert                    invert mask walker (1), split +90/-90 deg mask (2), invert AND split (3)
%mscrambleoption            controls whether phases or phases and periods are scrambled in addition to offsets
%
%OUTPUTS
%maskwalker                 finished scrambled mask walker mm matrix with all mask dots
%mperiods                   vector of periods for each mask dot - scrambled if selected
%mphases                    vector of phases for each mask dot - scrambled if selected

%INTERNAL
%maskmarkers                # markers in mask walker
%mwalkers                   # complete walkers (rounded down) contributing to mask dots
%remain                     # remaining number of dots after complete walkers necessary to complete mask
%maskwalker                 full mm matrix consisting of 'mwalkers' replicates of
%                           maskdata with rows for 'remain' markers also filled in.
%period                     original mask walker period
%mfactor                    original mask walker size factor from mm data
%theta                      random cylindrical coords for scrambling within volume
%rad
%z
%randdots
%middot
%randdots1
%randdots2
%mazimuth                   either a scalar with mask azimuth
%                           or for +90/-90 deg split, a vector of azimuths for each marker
%
%PARAMETERS
pdev=2;                     %if marker periods are scrambled, veridical speed of each marker is multiplied by
                            %a different random number between 1/pdev and pdev (0.5 and 2 default) sampled from
                            %a logarithmic uniform distribution
screenscale=10;             %screen scaling factor for eventual display


%COORDINATE SYSTEM
%The walker begins walking in the positive x direction, upright in the z direction
%A positive azimuth is a rotation about the z axis from the positive x to the positive y axis

%Initialize variables
period=maskdata(end,1);
mfactor=maskdata(end,2);
maskmarkers = (size(maskdata,1)-1)/3;  

%Number of scrambled mask dots
%mmultiply = 3;
nscrdots = maskmarkers*mmultiply;
mwalkers = floor(nscrdots/maskmarkers);
remain = rem(nscrdots,maskmarkers);

mwalkerssamedir = floor(mmultiply/2);
mwalkersoppodir = mmultiply - mwalkerssamedir;


%CREATE COMPLETE MM MATRIX FOR MASK BY REPLICATING THE MASK WALKER AS MANY
%TIMES AS NECESSARY AND THEN FILLING IN REMAINING DOTS
%Replicate and insert x coords
maskwalker=repmat(maskdata(1:maskmarkers,:),mwalkers,1);
maskwalker=[maskwalker; maskdata(1:remain,:)];

%change direction to equate local motion -- changed 2009-04-01 in case of remaining
%dots
maskwalker(1:(maskmarkers*mwalkersoppodir + remain/2),:) = maskwalker(1:(maskmarkers*mwalkersoppodir + remain/2),:).*-1;
%maskwalker(1:maskmarkers*mwalkersoppodir,:) = maskwalker(1:maskmarkers*mwalkersoppodir,:).*-1;

%Replicate and insert y coords
maskwalker=[maskwalker; repmat(maskdata(maskmarkers+1:maskmarkers*2,:),mwalkers,1)];
maskwalker=[maskwalker; maskdata(maskmarkers+1:maskmarkers+remain,:)];
%Replicate and insert z coords
maskwalker=[maskwalker; repmat(maskdata(2*maskmarkers+1:maskmarkers*3,:),mwalkers,1)];
maskwalker=[maskwalker; maskdata(2*maskmarkers+1:2*maskmarkers+remain,:)];
%Copy in final row to complete mm matrix
maskwalker(nscrdots*3+1,:)=maskdata(end,:);

%CREATE MARKER PERIODS VECTOR - SCRAMBLED IF SELECTED
if mscrambleoption >= 20                                
    %Scramble periods
    %Speed is multiplied (i.e. period is divided by) a number between 1/pdev and pdev sampled from a 
    %logarithmic uniform distribution.
    %The equation below is simplified using the identity log(1/x)=-log(x)
    mperiods=period./exp(rand(nscrdots,1)*(2*log(pdev))-log(pdev));
else                                                    %Don't scramble - all markers have the same veridical period
    mperiods=ones(nscrdots,1)*period;  
end 

%CREATE MARKER PHASES VECTOR - SCRAMBLED IF SELECTED
if mscrambleoption >= 10                                   
    mphases=2*pi*rand(nscrdots,1);                            %Random phase for each marker
else                                                    
    mphases=2*pi*rand*ones(nscrdots,1);                       %Uniform random starting phase for all markers
end

%SCRAMBLE WITHIN WHOLE PLOT VOLUME (CUBE)
%Redefine mean component to scramble - centred at screen (0,0)
maskwalker(1:nscrdots,1)=(-1+2*rand(nscrdots,1))*plotsize/2;		%x coords
maskwalker(nscrdots+1:nscrdots*2,1)=(-1+2*rand(nscrdots,1))*plotsize/2;   %y coords
maskwalker(nscrdots*2+1:nscrdots*3,1)=(-1+2*rand(nscrdots,1))*plotsize/2; %z coords

%INVERSION PARAMETERS
if minvert==1 | minvert==3
    %Flip walker upside down
    maskwalker(2*nscrdots+1:nscrdots*3,2:end)= -maskwalker(2*nscrdots+1:nscrdots*3,2:end);
end;
if minvert==2 | minvert==3
    %Rotate half of the dots by 90 deg, the other half by -90 deg
    randdots=randperm(nscrdots);                              %Set up random marker indeces for +90/-90 deg split
    middot=round(size(randdots,2)/2);
    randdots1=randdots(1:middot);
    randdots2=randdots(middot+1:nscrdots);
    
    h=mazimuth;
    mazimuth(randdots1)=h;                             %Half markers are going on direction
    mazimuth(randdots2)=-h;                            %Other half is going the other direction
    mazimuth=mazimuth';
end;

%APPLY ROTATION OF ALL DOTS LOCALLY
%This must be done BEFORE 2D projection, or else the scrambling into a cube might look more dense in some
%places in some rotated perspectives than others. Thus, for a scrambled mask rotation occurs here and not
%frame-by-frame as for a walker.
%Necessary to do it by columns because azimuth may be a column vector with an azimuth for each marker if 
%+90/-90 deg split for mask is used
alpha=mazimuth*2*pi/360;
temp=maskwalker;
for i=2:size(maskwalker,2)
    maskwalker(1:nscrdots,i)=cos(alpha).*temp(1:nscrdots,i)-sin(alpha).*temp(nscrdots+1:2*nscrdots,i);
    maskwalker(nscrdots+1:2*nscrdots,i)=sin(alpha).*temp(1:nscrdots,i)+cos(alpha).*temp(nscrdots+1:2*nscrdots,i);
end
%(maskwalker z coords and all of mean posture remain the same under rotation - z coords because they are
% invariant, and mean walker because it is scrambled in a cube anyway)

%SIZE
%Just harmonics, since mean posture is all new random points anyway
maskwalker(1:3*nscrdots,2:end) = maskwalker(1:3*nscrdots,2:end)*msize*mfactor/screenscale;	%Scale harmonics