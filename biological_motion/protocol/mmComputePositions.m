function walkerdots = mmComputePositions(mm, markers, periods, phases, azimuth, angvel, t, lintrans, speed, scrambleoption, walkersize, xcenterw, ycenterw,invert);

%DC: added input parameter "invert". If invert == 5, 6, switch x and z

%walkerdots = mmComputePositions(mm, markers, periods, phases, azimuth, angvel, t, lintrans, speed, scrambleoption, walkersize, xcenterw, ycenterw)
%
%Computes the array of dots to draw as the current frame of the walker
%
%INPUTS
%mm                         walker in mm format
%markers                    # markers
%periods:                   vector of periods for each marker (scaled in 1/120 s) - uniform or random
%phases:                    vector of phases for each marker (rad) - scrambled or uniform, includes random starting phase
%azimuth:                   initial viewing angle
%angvel                     angular velocity
%t                          time of current frame
%lintrans                   if lintrans = 1, then the walker translates with a linear velocity
%                           if lintrans = 0, then walker walks in place
%speed                      walker speed factor from plw_w
%scrambleoption             scramble option parameter from plw_w
%walkersize                 walker size factor from plw_w
%xcenterw, ycenterw:        center of walker
%
%OUTPUTS
%walkerdots                 final array of dots to draw.
%                           row 1 = screen x coords, row 2 = screen y coords, columns = dots

%INTERNAL
%alpha                      current azimuth (accounting for rotation) in radians
%harmonics                  number of Fourier components in this mm data
%mmr                        3D mm data rotated and translated
%mm2D                       mmr data projected onto yz plane (screen)
%                           format as mm data except now only y and z components
%PARAMETERS
%The following parameters are used to implement perspective if the walker has a linear
%velocity that is causing it to advance toward or recede from the screen:
walkerdi=6500;              %Initial walker distance from screen (mm, along x axis before 2D projection)
walkervisangi=4*2*pi/360;   %Initial walker visual angle (visual angle at walkerd)


%COORDINATE SYSTEM
%The walker begins at a negative x position, walking in the positive x direction, upright in the z direction
%x=0 is the screen
%A positive azimuth is a rotation about the z axis from the positive x to the positive y axis


%Get variables
screenscale=10;                             %Scale factor to accomodate screen size (10 default)
angvel=angvel*2*pi/360;
azimuth=azimuth*2*pi/360;
harmonics=(size(mm,2)-1)/2;


if lintrans==1 & ~any(scrambleoption==[2 12 22])
    linvel=mm(end,3)*speed*120;              %Was in mm/frame - convert to mm/s and scale by speed parameter
                                             %Also scale by walker size for natural looking
                                             %motion
else
    linvel=0;
end

%Calculate current azimuth
alpha=azimuth+angvel*t;

%Rotate walker about its body axis to current azimuth
mmr(1:markers,:)=-cos(alpha).*mm(1:markers,:)+sin(alpha).*mm(markers+1:2*markers,:);
mmr(markers+1:2*markers,:)=cos(alpha).*mm(markers+1:2*markers,:)+sin(alpha).*mm(1:markers,:);
mmr(2*markers+1:3*markers,:)=mm(2*markers+1:3*markers,:);

%Translate walker due to linvel
%Note: It is not possible to simply iterate the walker's change in position onto its previous
%position based on headings and speed because the walker's position is not retained frame-to-frame.
%As a result, the walker's position must be calculated as a point on a line or a circle (if there 
%is non-zero angular velocity) as a function of time. Therefore, two different cases are
%necessary:
if angvel==0
    %Walker walks in a straight line at an arbitrary angle
    mmr(1:markers,1)=mmr(1:markers,1)+linvel*t*cos(alpha);
    mmr(markers+1:2*markers,1)=mmr(markers+1:2*markers,1)+linvel*t*sin(alpha);
else
    %Walker walks in a circle, radius a function of angvel and linvel, centred at walker
    %display centre
    %Walker position at any point in time is computing separately from its heading
    %Note: |linvel/angvel|=radius, but this fraction is not made absolute value because the
    %signum of angvel happens to accommodate for the two different directions the walker
    %can circle in (clockwise/counterclockwise)
    mmr(1:markers,1)=mmr(1:markers,1)+linvel/angvel*sin(alpha);
    mmr(markers+1:2*markers,1)=mmr(markers+1:2*markers,1)-linvel/angvel*cos(alpha);
end

%Apply initial position behind screen to walker
mmr(1:markers,1)=mmr(1:markers,1)-walkerdi; 

%LINES OF CODE WHICH ARE COMMENTED OUT BELOW IMPLEMENT DEPTH/PERSPECTIVE FOR A WALKER
%WHICH IS TRANSLATING TOWARDS OR AWAY FROM THE SCREEN. UNCOMMENT TO REENABLE THIS
%FUNCTIONALITY.

%if mmr(1,1)>0
    %Walker has walked through the front of the screen
    %walkerdots=[];
%else
    %Adjust walkersize parameter to implement perspective if walker is receding or advancing 
    %due to linvel  
    %walkersize=atan(walkerdi/abs(mmr(1,1))*tan(walkervisangi))/walkervisangi*walkersize;

    %Project walker onto yz plane (the screen)
    %NOTE: From here on in we work in a new coord system for the SCREEN, which is an xy plane
    %new x axis = old y axis
    %new y axis = -old z axis
    %(0,0) of screen coords is at top left hand corner, (1024,768) is at bottom RH corner
    
    %% check orientation
    if invert==0 || invert==1
        mm2D(1:markers,:)=mmr(markers+1:2*markers,:);
        mm2D(markers+1:2*markers,:)=-mmr(2*markers+1:3*markers,:);
    elseif invert==5 || invert==6
        mm2D(1:markers,:)=-mmr(2*markers+1:3*markers,:);
        mm2D(markers+1:2*markers,:)=mmr(markers+1:2*markers,:);
    end
    
    

    %Size walker
    if ~any(scrambleoption==[2 12 22])
        mm2D(1:2*markers,:)=mm2D(1:2*markers,:)*walkersize/screenscale;
    else
        mm2D(1:2*markers,2:end)=mm2D(1:2*markers,2:end)*walkersize/screenscale;
    end

    %Fill the mean posture into the final dot matrix
    walkerdots=reshape(mm2D(1:2*markers,1),markers,2);

    %Compute all Fourier harmonics and add to final dot matrix
    for i=1:harmonics
        walkerdots(:,1) = walkerdots(:,1) + mm2D(1:markers,2*i).*sin(i*(2*pi*120*speed*t./periods+phases)) + mm2D(1:markers,2*i+1).*cos(i*(2*pi*120*speed*t./periods+phases));
        walkerdots(:,2) = walkerdots(:,2) + mm2D(markers+1:2*markers,2*i).*sin(i*(2*pi*120*speed*t./periods+phases)) + mm2D(markers+1:2*markers,2*i+1).*cos(i*(2*pi*120*speed*t./periods+phases));
    end

    %Reshape for drawdots routine to be called later
    walkerdots=walkerdots';
    %-----------------

    %Finally translate walker to xcenterw, ycenterw
    walkerdots(1,:)=walkerdots(1,:)+xcenterw;
    walkerdots(2,:)=walkerdots(2,:)+ycenterw;
%end