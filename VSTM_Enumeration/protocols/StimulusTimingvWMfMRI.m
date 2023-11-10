function [ITI_jit, delay, trial_start, checksum1, checksum2, checksum3] = StimulusTimingvWMfMRI(TR, n_trials)

%% jitter = TR * (1/16);
ITI = 6;
fixed_trial_durations   = 0.5 + 0.1 + 1 + 1.7;
%                       = fixation + stimulus + mask + max_RT ==> 3.5

time_limit = 0;
count_runs =0;
trial_per_block  = n_trials/3;
while time_limit ==0
    count_runs = count_runs +1;
    for i = 1:n_trials
        ITI_jit(i) = floor((10)*rand+5) * 0.1; % 500 - 1500
        delay(i) = floor((15-5+1)*rand+10)*0.1; % 1000 - 2000
    end
    
    checksum1 = sum(ITI_jit(1:trial_per_block));
    checksum2 = sum(ITI_jit(trial_per_block+1:trial_per_block * 2));
    checksum3 = sum(ITI_jit(2*trial_per_block+1:n_trials));
    
    check1 = (checksum1 >= trial_per_block-1 && checksum1 <=trial_per_block+1);
    check2 = (checksum2 >= trial_per_block-1 && checksum2 <=trial_per_block+1);
    check3 = (checksum3 >= trial_per_block-1 && checksum3 <=trial_per_block+1);
     
    if (((check1 ==1) && (check2 == 1) && (check3 ==1)) && ( (mean(delay)>1.4 )&& (mean(delay) <= 1.6)));
        time_limit = 1;
    else
        time_limit = 0;
    end
end
count_runs

start = 0;
for i=1:n_trials-1
    trial_start(i+1) = start + ITI + (ITI_jit(i)) + delay(i) + fixed_trial_durations;
    start = trial_start(i+1);
end

% postpone the beginning of the very first trial (and all subsequent ones)
% by two seconds.
trial_start = trial_start+2;