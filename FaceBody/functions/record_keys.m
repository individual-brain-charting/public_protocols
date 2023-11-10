function [keys, is_empty, exitKey] = record_keys(start_time, dur, device_num)
% Collects all keypresses for a given duration (in secs).
% Written by KGS Lab
% Edited by AS 8/2014

exitKey = 0;
% wait until keys are released
keys = [];
while KbCheck(device_num)
    if (GetSecs - start_time) > dur
        break
    end
end

% check for pressed keys
while 1
    [key_is_down, ~, key_code] = KbCheck(device_num);
    if key_is_down
        if strcmp(KbName(key_code), 'ESCAPE') == 1  % IBC change: escape key exit
            exitKey = 1;
            break
        else
            keys = [keys KbName(key_code)];
            exitKey = 0;
            while KbCheck(device_num)
                if (GetSecs - start_time) > dur
                    break
                end
            end
        end
    end
    if (GetSecs - start_time) > dur
        break
    end
end

% label null responses and store multiple presses as an array
if isempty(keys)
    is_empty = 1;
elseif iscell(keys)
    keys = num2str(cell2mat(keys));
    is_empty = 0;
else
    is_empty = 0;
end

end
