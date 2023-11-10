function [answer, anstime]=get_mouse(wait)

%[answer, anstime]=get_mouse(boxrects, wait)
%
%Checks if an option box has been clicked and returns the answer and the time
%Or waits for an option box to be clicked.
%
%INPUTS
%window     window pointer to main display
%boxrects   matrix of rects for each option box. rows = option boxes, cols = rect coords
%wait       Either wait for a mouse button to be clicked (1) or just check
%           at this instant if one is depressed (0)
%
%OUTPUTS
%answer     the box number that is clicked (numbers defined by order of box coords in the input coord vectors), or =0
%           if no boxes are clicked
%anstime    time of mouse click (or of check if wait==0)


%MAIN MOUSE CHECK
if wait==1                      %Wait for a mouse click in one of the boxes
    answer=[];
    while isempty(answer)
        [x, y, buttons]=getmouse;
        if buttons(1)
            
           answer=0; %left button clicked
           anstime=getsecs;
            
        elseif buttons(3)
            
           answer = 1; %right button clicked
           anstime = getsecs;
            
        end
    end
else
    [x, y, buttons]=getmouse;   %Check once for a mouse click in one of the boxes
    if buttons(1)
        answer=0; %left button clicked
        anstime=getsecs;
    elseif buttons(3)
        answer = 1; %right button clicked
        anstime = getsecs;
    else
        answer=0;
        anstime=0;
    end
end