function draw_fixation(windowPtr, center, color)
% Draws round fixation marker in the center of the window by superimposing
% vertical and horizontal bars.
% Written by KGS Lab
% Edited by AS 8/2014

% find center of window
center_x = center(1);
center_y = center(2);

Screen('DrawDots', windowPtr, [center_x center_y], 10, color, [], 2);


end
