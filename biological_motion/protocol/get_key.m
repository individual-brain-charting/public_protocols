function [answer, anstime]=get_key(keys, wait, response_end);

%[answer, anstime]=get_key(keys, wait);
%
%Get keyboard-input from user - waits for a key press as defined in input variable 'keys' OR just checks once
%
%INPUTS
%keys       key numbers we are looking for. scalar for one key, or row vector of key numbers
%           key numbers are as defined by KbCheck function
%wait       if = 1 waits for input for unlimited. if = 2 waits only 1 s for input; if = 0 looks for it just at this instant
%          
%OUTPUTS
%answer     scalar keyboard code
%           0 = no key pressed (if wait = 0)
%anstime    time answer returned, 0 = no key pressed (if wait=0)


if wait==1          %waits until key is pressed
    answer=[];
    while isempty(answer)
        [kch, anstime, code] = KbCheck;
        answer=intersect(find(code),keys);
    end;
elseif wait == 2 %we wait for a fixed response duration
    answer = [];
    while isempty(answer);
        
        if GetSecs < response_end;
            [kch, anstime, code] = KbCheck;
            answer=intersect(find(code),keys);
        end
        
        if GetSecs > response_end
            answer = -1;
            anstime = response_end;
        end
        
        %if getsecs > t0+1;
        %    answer = -1; %time's up
        %end
        %Cancel display on Esc
        [k, t, c] = KbCheck;
        esc=find(c);
        if any(esc==27)
            Screen('CloseAll')
            error('Display halted by ESC key')
        end
    end 
else
    
    [kch, anstime, code] = KbCheck;
    answer=intersect(find(code),keys);
    if isempty(answer)
        answer=0;
        anstime=0;
    end
end