function disp_text(window, text, textcolour, backcolour, rect)


%Setup boundary defaults
if ~exist('rect', 'var')
    rect=Screen('Rect',0);            % Window-coordinates, e.g. [0 0 1024 768]
end

%Get centre of writing area
xcenter=round((rect(1)+rect(3))/2);
ycenter=round((rect(2)+rect(4))/2);

%Measure text size
[normboundsrect, offsetboundsrect]=Screen('TextBounds', window, text);

%DRAW TEXT
Screen('fillrect',window, backcolour, rect);                                                                %Background colour
Screen('DrawText', window, text, xcenter-normboundsrect(3)/2, ycenter-0.75*normboundsrect(4), textcolour);  %Text
%Note: the y normboundsrect doesn't quite work properly - 0.75 above is a scaling factor that has been found to work
%for vertical centring