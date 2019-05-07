function [  ] = display_Rating( WindowPtr,x,y,yscale,rating)
%DISPLAY_RATING shows the effort rating scale
% "rating" indicates the position of the cursor, between 0 and 100.


% Define graduations
ngrad=100;
segment=800/(ngrad-1);

% define y coordinates for the scale
%yscale=400;


% Draw the line and the cursor
xarrow= (x-400+(rating-1)*segment);
yarrow= y+yscale;

Screen('FillPoly', WindowPtr, [255 153 0], [xarrow yarrow; xarrow+20 yarrow+30; xarrow-20 yarrow+30] ,[1]); % Cursor
Screen('DrawLine',WindowPtr,[255 255 255],(x-400), (y+yscale), (x+400), (y+yscale),1); % Line
Screen('TextSize', WindowPtr, 30);

% Draw the zero and the max
Screen('FillRect',WindowPtr,[255 255 255],[(x-400-2) (y+yscale-10) (x-400+2) (y+yscale+10)]); % Limit bar : left
Screen('FillRect',WindowPtr,[255 255 255],[(x+400-2) (y+yscale-10) (x+400+2) (y+yscale+10)]); % Limit bar : right


end

