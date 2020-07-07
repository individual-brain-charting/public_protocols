function [answer, anstime, twstart, jitter] = PresentStimulus(data, datatypes, w1, mask, leng, dotsize, nd, trans, nwd, fc, xcenter, ycenter, window, colour, mmultiply)

% PARAMETERS
plotsize = 300;        %plot area of the mask (pixels) //altered
timeout=600;            %timeout length of trial if length = 0 // altered

%Initialize these variables so if we leave the function without an answer it won't complain
anstime=0;
answer=0;

%Is a response allowed during the display?
if leng==0;                             %Then yes
    waitkey=1;                          %Set flag for later
    leng=timeout;                       %length of display = 60 s
else
    waitkey=0;
end;                             

rand('state',sum(100*clock));           %Initialise the random generator

%EXTRACT WALKER AND MASK PARAMETERS
%Extract walker parameters from w1 (if walker is to be shown)
walkerindex         =w1(1); %which walker
maskindex           =mask(1);%what type of mask
maskdir             =mask(2);
maskori             =mask(3);
maskcoh             =mask(4);

if maskindex == 0; %no mask
    
    mindex = 0;
    nd = 0; % fixed mask, depends on stimulus. of coherent, then scrambled stim, if scrambled stim , then linear mask
    
else %there is a mask of some sort, let's define nd first, as nwalker dots
    %define ndots
    if walkerindex == 1 || walkerindex == 2 || walkerindex == 3
        nd = 11*1;
    end
end


if walkerindex>0
    azimuth         =w1(2);
    angvel          =0;
    speed           =1; 
    walkersize      =2;%1.5;
    scrambleoption  =w1(4);
    invert          =w1(3);
    scramblex       =0.4;
    scrambley       =0.8;
    offx			=0;
    offy			=0;
    lintrans        =0;
end

%%if fixed mask, check walker to determine which mask
%%%if coherent, use modified scrambled mask to equate local motion
%%%direction of display

if maskindex == -1; %mask is fixed and yoked to stim
    
    if scrambleoption == 0 %coherent walker
        mindex = walkerindex; %same as target walker
        mazimuth = azimuth; %opposing direction to walker -- it will be done in mmprepare_randmask / mdprepare_randmask
        mspeed = speed; %same as target walker
        msize = walkersize; %same as target walker
        minvert = invert; %same as target walker
        mscrambleoption = 12; %always scramble mask spatially and temporally
        
        %%%if scrambled, use flickering mask
    elseif scrambleoption == 2 %scrambled walker
        mindex = -1;
        mminspeed = 0;
        mmaxspeed = 0;
        mlifetime = 0.250;
    end
end

if maskindex == 1; % linear mask
    mindex = -1;
    mminspeed = 0;
    mmaxspeed = 0;
    mlifetime = 0.250;
elseif maskindex == 2 %scrambled mask
    mindex = walkerindex; %same as target walker
    
    if maskdir == -1; %fixed and yoked to stim.
        mazimuth = azimuth; %opposite to walker -- it will be done in mmprepare_randmask/mdprepare_randmask
    else
        mazimuth = maskdir;
    end
    
    mspeed = speed; %same as target walker
    msize = walkersize; %same as target walker
    
    if maskori == -1; %fixed and yoked to stim
        minvert = invert; %same as target walker
    else
        minvert = maskori;
    end
    
    mscrambleoption = 12; %always scramble mask spatially and temporally


    %flag if scrambled walker + scrambled mask, then we are checking
    %orientation of the mask, and fixing the azimuth

    if maskori == 5
        mazimuth = 90;
    elseif maskori == 6
        mazimuth = 90;
    end

end
    



%EXTRACT WALKER DATA AND PREPARE WALKER
if walkerindex > 0
    switch datatypes{walkerindex}           %Extract walker data
        case {'cellmm','cellmd'}
            w1data=data{walkerindex};
        case 'mmw'
            w1data=data(:,:,walkerindex);
        case {'mm','md'}
            w1data=data;
    end

    if strcmp(datatypes{walkerindex},'cellmm') || strcmp(datatypes{walkerindex},'mmw') || strcmp(datatypes{walkerindex},'mm')
        [mm2, markers, wperiods, wphases, xcenterw, ycenterw] = mmprepare_single(w1data, scrambleoption, scramblex, scrambley, invert, trans, offx, offy, plotsize, xcenter, ycenter);
    else %for md data
        [md2D, markers, xcenterw, ycenterw] = mdprepare_single(w1data, azimuth, invert, trans, offx, offy, plotsize, walkersize, xcenter, ycenter, scrambleoption, scrambleoption);
    end
end

%PREPARE SCRAMBLED WALKER MASK
if walkerindex==0; %nd=nd+nwd; end           %Increase number of mask dots if no walker is to be shown
end
if (mindex > 0) && (nd > 0)                  %Extract mask walker data
    switch datatypes{mindex}
        case 'cellmm'
            wmaskdata=data{mindex};
        case 'mmw'
            wmaskdata=data(:,:,mindex);
        case {'mm','md'}
            wmaskdata=data;
    end
    
    if strcmp(datatypes{walkerindex},'cellmm') || strcmp(datatypes{walkerindex},'mmw') || strcmp(datatypes{walkerindex},'mm')
        [wmask, mperiods, mphases, nscrdots] = mmprepare_randmask(wmaskdata, nd, plotsize, mazimuth, msize, minvert, mscrambleoption, mmultiply);

    else %for md data
        [md2Dmask, md2Dmask_markers, md2Dmask_xcenterw, md2Dmask_ycenterw] = mdprepare_single_randmask(w1data, mazimuth, minvert, trans, offx, offy, plotsize, walkersize, xcenter, ycenter,mscrambleoption, mscrambleoption);

    end
end

%DISPLAY STIMULUS
fr=1;                                       %Initialize to frame 1 

t0=GetSecs;                                 %Start timer
tw=0;
maskdots=[];                                %Initialize these so that Matlab knows what they are to create the final 
                                            %dots matrix even if a walker or a mask is not computed
walkerdots=[];

%DC we'll introduce a random start phase, selecting any point within the
%full gait cycle
twstart = [-9];
if walkerindex > 0 
    if strcmp(datatypes{walkerindex},'cellmm') || strcmp(datatypes{walkerindex},'mmw') || strcmp(datatypes{walkerindex},'mm')
        twstart = rand*length(mm2)/120;    %in secs
    else %for md data
        twstart = rand*length(md2D)/120;
    end
end

%DC we need to jitter along horizontal and vertical (and store it)
jitter_range = 10;
jitter_x = floor(rand*jitter_range);
if rand > 0.5
    jitter_x = -jitter_x;
end

jitter_y = floor(rand*jitter_range);
if rand > 0.5
    jitter_y = - jitter_y;
end

jitter = [jitter_x jitter_y];

while tw < leng                             %Each iteration is 1 frame
    
    twcurr = tw + twstart;
    
    if walkerindex > 0
        
            
    %Compute linear mask display dot matrix
    if (mindex == -1) && nd>0 && (mmultiply > 0); 
        maskdots=computelinmask(nd, plotsize, xcenter, ycenter, mlifetime, mminspeed, mmaxspeed, fr); end
    end

    if (mindex > 0) && (nd > 0)
        %Compute scrambled walker mask display dot matrix
        if strcmp(datatypes{walkerindex},'cellmm') || strcmp(datatypes{walkerindex},'mmw') || strcmp(datatypes{walkerindex},'mm')
            maskdots = mmComputePositions_randmask(wmask, nscrdots, mperiods, mphases, twcurr, mspeed, xcenter, ycenter,minvert);
        else
            maskdots = mdComputePositions_randmask(md2Dmask, markers, twcurr, speed, md2Dmask_xcenterw, md2Dmask_ycenterw, fr, minvert);
        end
    end
    

    
    %Compute walker display dot matrix
    if walkerindex > 0
        if strcmp(datatypes{walkerindex},'cellmm') || strcmp(datatypes{walkerindex},'mmw') || strcmp(datatypes{walkerindex},'mm')
            walkerdots = mmComputePositions(mm2, markers, wperiods, wphases, azimuth, angvel, twcurr, lintrans, speed, scrambleoption, walkersize, xcenterw, ycenterw,invert);
        else
            walkerdots = mdComputePositions(md2D, markers, twcurr, speed, xcenterw, ycenterw, fr, invert, jitter);
        end
    end
    
    %Display
    dots=[maskdots walkerdots];
    if ~isempty(dots)
        Screen('drawdots',window,dots,dotsize,colour.white);
    end

    if fc(2)==1
        Screen('Drawline',window, colour.white, xcenter, ycenter-10, xcenter, ycenter+10);
        Screen('Drawline',window, colour.white, xcenter-10, ycenter, xcenter+10, ycenter);
    end
    
    Screen('flip',window);
    
    %If Mid-display response allowed
    if waitkey==1;
        if strcmp(computer, 'PCWIN64')
            [answer, anstime]=get_key([37 39], 0);
        else
            [answer, anstime]=get_key([79 80], 0);
        end
        if answer > 0;
            anstime=anstime-t0;
            disp_efficiency=getdisp_efficiency(fr, tw, window);
            disp(sprintf('Disp efficiency = %f', disp_efficiency));
            return
        end;
    end;
    
    %Cancel display on Esc
    [k, t, c] = KbCheck;
    esc=find(c);
    if strcmp(computer, 'PCWIN64') && any(esc==27) || strcmp(computer, 'MACI64') && any(esc==41)
        Screen('CloseAll')
        error('Display halted by ESC key')
    end
    
    tw=GetSecs-t0;                          %Update time
    fr=fr+1;                                %Next frame
end;

%disp_efficiency=getdisp_efficiency(fr, tw, window);
%disp(sprintf('Disp efficiency = %f', disp_efficiency));
