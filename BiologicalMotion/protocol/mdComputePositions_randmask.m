function walkerdots = mdComputePositions(md2D, markers, tw, speed, xcenterw, ycenterw, fr, invert);

%walkerdots = mdComputePositions(md2D, markers, tw, speed, xcenterw, ycenterw, fr)
%
%Computes the array of dots to draw as the current frame of the walker.
%Loops walker when we get to the end of the md data set
%
%INPUTS
%md2D           prepared walker in md format - already projected onto 2D
%               format: dim1=frames
%                       dim2=markers
%                       dim3(1)=x, dim3(2)=y (screen coords)
%markers        # markers
%tw             time of current frame
%speed          walker speed factor from plw_w
%xcenterw, ycenterw:    center of walker
%fr
%
%OUTPUTS
%walkerdots     final array of dots to draw.
%               row 1 = screen x coords, row 2 = screen y coords, columns = dots

%INTERNAL
%frames         # frames contained in md data
%wfr            What frame of the md data are we on? Depends on time, speed factor, etc.
%LOOP           which loop of the walker are we on? starts at loop 1. as walker proceeds, it loops over and over


persistent LOOP
if fr==1; LOOP=1; end

%Get total # frames in md data set
frames=size(md2D,1);

if invert == 5;
    temp1 = md2D(:,:,1);
    temp2 = md2D(:,:,2);
    md2D(:,:,1) = temp2;
    md2D(:,:,2) = temp1;
end

if invert == 6;
    temp1 = md2D(:,:,1);
    temp2 = md2D(:,:,2);
    md2D(:,:,1) = -temp2;
    md2D(:,:,2) = temp1;
end
    

%Get md frame we are on
wfr=ceil(tw*120*speed)-(LOOP-1)*frames+1;
if wfr > frames                             %We are at the end of animation -> loop over
    LOOP=LOOP+1;
    wfr=wfr-frames;
end

%Populate dot array and centre to (xcenterw, ycenterw)
for i=1:markers
    walkerdots(1,i)=md2D(wfr,i,1)+xcenterw;
    walkerdots(2,i)=md2D(wfr,i,2)+ycenterw;
end;

walkerdots(2,:)=-walkerdots(2,:)+2*ycenterw;			%invert y coords since screen y coords = - geometric y coords
walkerdots(1,:)=-walkerdots(1,:)+2*xcenterw;