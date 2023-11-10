function training(name, trigger, stim_set, num_runs, task_num, start_run)
% Executes training protocol for IBC version of functional localizer experiment 
% used to define regions in high-level visual cortex
% selective to faces, places, bodies, and printed characters.
%
% Inputs :
%   1) name -- subject number
%   2) flip_or -- 1-back image flip orientation (1 = upside-down, 2 = left-right)
%
% Version IBC 06/2021
% Himanshu Aggarwal (himanshu.aggarwal@inria.fr)

%% add paths and check inputs

addpath('functions');

% session name
if nargin < 1
    name = [];
    while isempty(deblank(name))
        name = input('Subject number : ', 's');
    end
end
name = ['pract_' name];

% Flip orientation  % IBC Change: 1-back flip orie
% if nargin < 2
%     flip_or = -1;
%     while ~ismember(flip_or, 1:2)
%         flip_or = input('Flip orientation? (1 = upside-down, 2 = left-right) ');
%     end
% end
flip_or = 2;

% option to trigger scanner
% if nargin < 2
%     trigger = -1;
%     while ~ismember(trigger, 0:1)
%         trigger = input('Trigger scanner? (0 = no, 1 = yes) : ');
%     end
% end
trigger = 0;

% which stimulus set/s to use
% if nargin < 3
%     stim_set = -1;
%     while ~ismember(stim_set, 1:3)
%         stim_set = input('Which stimulus set? (1 = standard, 2 = alternate, 3 = both) : ');
%     end
% end
stim_set = 3;

% number of runs to generate
% if nargin < 4
%     num_runs = -1;
%     while ~ismember(num_runs, 1:24)
%         num_runs = input('How many runs? : ');
%     end
% end
num_runs = 2;  % Enter double the number of runs required %IBC change: longer runs

% which task to use
% if nargin < 5
%     task_num = -1;
%     while ~ismember(task_num, 1:3)
%         task_num = input('Which task? (1 = 1-back, 2 = 2-back, 3 = oddball) : ');
%     end
% end
task_num = 1;

% which run number to begin executing (default = 1)
if nargin < 6
    start_run = 1;
end


%% initialize session object and execute experiment

% setup fLocSession and save session information
session = fLocSession(name, trigger, stim_set, num_runs, task_num, flip_or);
session = load_seqs(session);
session_dir = (fullfile(session.exp_dir, 'data', session.id));
if ~exist(session_dir, 'dir') == 7
    mkdir(session_dir);
end
fpath = fullfile(session_dir, [session.id '_fLocSession.mat']);
save(fpath, 'session', '-v7');

% execute all runs from start_run to num_runs and save parfiles
fname = [session.id '_fLocSession.mat'];
fpath = fullfile(session.exp_dir, 'data', session.id, fname);
for rr = start_run:num_runs   % IBC change: longer runs
    [session, exitKey] = run_exp(session, rr);  % IBC change: escape key exit
    save(fpath, 'session', '-v7');
    if exitKey  % IBC change: escape key exit
        break;
    end
end
write_parfiles(session);

end
