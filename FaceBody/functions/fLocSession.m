classdef fLocSession
    
    properties
        name      % participant initials or id string
        date      % session date
        trigger   % option to trigger scanner (0 = no, 1 = yes)
        num_runs  % number of runs in experiment
        sequence  % session fLocSequence object
        responses % behavioral response data structure
        parfiles  % paths to vistasoft-compatible parfiles
        flip_or   % 1-back flip orientation % IBC Change: 1-back flip orientation
        train     % training session or not (0 = acquistion, 1 = training session) % IBC Change: training session
        true_onsets % true stim onset times % IBC Change: actual onset time record
        wait_dur = 1;          % seconds to wait for response
    end
    
    properties (Hidden)
        stim_set  % stimulus set/s (1 = standard, 2 = alternate, 3 = both)
        task_num  % task number (1 = 1-back, 2 = 2-back, 3 = oddball)
        input     % device number of input used for resonse collection
        keyboard  % device number of native computer keyboard
        hit_cnt   % number of hits per run
        fa_cnt    % number of false alarms per run
    end
    
    properties (Constant)
        count_down = 12; % pre-experiment countdown (secs)
        stim_size = 768; % size to display images in pixels
    end
    
    properties (Constant, Hidden)
        task_names = {'1back' '2back' 'oddball'};
        exp_dir = pwd;
        fix_color = [255 0 0]; % fixation marker color (RGB)
        text_color = [255 0 0];% ttl fix color
        inst_color = [0 0 0];  % train instruction color
        blank_color = 128;     % baseline screen color (grayscale)v
    end
    
    properties (Dependent)
        id        % session-specific id string
        task_name % descriptor for each task number
    end
    
    properties (Dependent, Hidden)
        hit_rate     % proportion of task probes detected in each run
        instructions % task-specific instructions for participant
    end
    
    methods
        
        % class constructor
        function session = fLocSession(name, trigger, stim_set, num_runs, task_num, flip_or)
            session.name = deblank(name);
            session.trigger = trigger;
            session.flip_or = flip_or; % IBC Change: 1-back flip orientation
            if nargin < 3
                session.stim_set = 3;
            else
                session.stim_set = stim_set;
            end
            if nargin < 4
                session.num_runs = 4;
            else
                session.num_runs = num_runs;
            end
            if nargin < 5
                session.task_num = 3;
            else
                session.task_num = task_num;
            end
            session.date = date;
            session.hit_cnt = zeros(1, session.num_runs/2);  % IBC change:
            session.fa_cnt = zeros(1, session.num_runs/2);   % 2 long runs instead of 4 short runs

            par_str = [session.name '_' session.date];
            exp_str = [session.task_name '_' num2str(session.num_runs/2) 'runs'];
            c=clock;   % IBC change: timestamp in data file names
            hr = sprintf('%02d', c(4));
            minutes = sprintf('%02d', c(5));
            time_str = [hr,'h',minutes,'m'];
            session.id = [par_str '_' time_str '_' exp_str];
        end
        
        % get session-specific id string
        % function id = get.id(session)
        %     par_str = [session.name '_' session.date];
        %     exp_str = [session.task_name '_' num2str(session.num_runs/2) 'runs'];
        %     c=clock;   % IBC change: timestamp in data file names
        %     hr = sprintf('%02d', c(4));
        %     minutes = sprintf('%02d', c(5));
        %     time_str = [hr,'h',minutes,'m'];
        %     id = [par_str '_' time_str '_' exp_str];
        % end

        % training session or not % IBC Change: training session
        function train = get.train(session)
            if strcmp(strsplit(session.name, '_')(1), 'pract')
                train = 1;
            else
                train = 0;
            end
        end
        
        % get name of task
        function task_name = get.task_name(session)
            task_name = session.task_names{session.task_num};
        end
        
        % get hit rate for task
        function hit_rate = get.hit_rate(session)
            num_probes = sum(session.sequence.task_probes);
            hit_rate = session.hit_cnt ./ num_probes;
        end
        
        % get instructions for participant given task
        function instructions = get.instructions(session)
            if session.task_num == 1
                if session.train
                    % Show pracice session instructions
                    line1 = "Appuyez sur Y lorsqu'une image";
                    line2 = "\n\n reapparait en tant qu'image miroir.";
                    line3 = "\n\n\nLes images apparaissent lentement dans la premiere partie de la formation."; 
                    line4 = '\n\n\n\n\n Appuyez sur Espace pour commencer';
                    instructions = [line1 line2 line3 line4];
                else
                    instructions = '+';   % IBC change: TTL cross
                end
            elseif session.task_num == 2
                instructions = 'Fixate. Press a button when an image repeats with one intervening image.';
            else
                instructions = 'Fixate. Press a button when a scrambled image appears.';
            end
        end
        
        % define/load stimulus sequences for this session
        function session = load_seqs(session)
            if session.train
                fname = ['pract_fLocSequence.mat'];  % IBC Change: training session
            else
                fname = ['IBC_' num2str(session.num_runs/2) 'runs_fLocSequence.mat'];   % IBC change: same randomisation all subs
            end
            subname = [session.id '_fLocSequence.mat'];  % IBC change: same randomisation all subs
            fpath = fullfile(session.exp_dir, 'data', fname); % IBC change: same randomisation all subs
            sub_path = fullfile(session.exp_dir, 'data', session.id, subname); % IBC change: same randomisation all subs
            % make stimulus sequences if not already defined for session
            if ~exist(fpath, 'file')
                disp('IBC sequence file missing. Creating a new one...') % IBC change: same randomisation all subs
                seq = fLocSequence(session.stim_set, session.num_runs, session.task_num, session.train);
                seq = make_runs(seq);
                save(fpath, 'seq', '-v7');
                load(fpath);
                mkdir(fileparts(sub_path));
            else
                load(fpath);   % IBC change: same randomisation all subs
                mkdir(fileparts(sub_path));   % IBC change: same randomisation all subs
            end
            session.sequence = seq;
        end
        
        % register input devices
        function session = find_inputs(session)
            KbName('UnifyKeyNames');
            session.keyboard = -1;
            session.input = -1;
        end
        
        % execute a run of the experiment
        function [session, exitKey] = run_exp(session, run_num)
            % get timing information and initialize response containers
            session = find_inputs(session); k = session.input;
            if session.train
                if run_num == 1
                    session.sequence.stim_duty_cycle = 1;
                    session.sequence.task_freq = 1;
                    session.wait_dur = 2;
                else
                    session.sequence.stim_duty_cycle = 0.5;
                    session.sequence.task_freq = 0.5;
                    session.wait_dur = 1;
                end
            end
            sdc = session.sequence.stim_duty_cycle;
            stim_dur = session.sequence.stim_dur;
            isi_dur = session.sequence.isi_dur;
            stim_names = session.sequence.stim_names(:, run_num);
            flipIt = session.sequence.task_probes(:, run_num);   % IBC change: flip image in 1-back
            stim_dir = fullfile(session.exp_dir, 'stimuli');
            bcol = session.blank_color; fcol = session.fix_color;
            resp_keys = {}; resp_press = zeros(length(stim_names), 1);
            % setup screen and load all stimuli in run
            [window_ptr, center] = doScreen;
            if session.train
                tcol = session.inst_color;
                Screen('TextSize', window_ptr, 56);
            else
                tcol = session.text_color;
            end
            center_x = center(1); center_y = center(2); s = session.stim_size / 2;
            stim_rect = [center_x - s center_y - s center_x + s center_y + s];
            img_ptrs = [];
            for ii = 1:length(stim_names)
                if strcmp(stim_names{ii}, 'baseline')
                    img_ptrs(ii) = 0;
                else
                    cat_dir = stim_names{ii}(1:find(stim_names{ii} == '-') - 1);
                    img = imread(fullfile(stim_dir, cat_dir, stim_names{ii}));
                    if flipIt(ii) == 0                                         % IBC change: flip image in 1-back
                        img_ptrs(ii) = Screen('MakeTexture', window_ptr, img); % IBC change: flip image in 1-back
                    else                                                       % IBC change: flip image in 1-back
                        img = flip(img, session.flip_or);                      % IBC change: flip image in 1-back
                        img_ptrs(ii) = Screen('MakeTexture', window_ptr, img); % IBC change: flip image in 1-back
                    end                                                        % IBC change: flip image in 1-back
                end
            end
            % start experiment triggering scanner if applicable
            if session.trigger == 0
                Screen('FillRect', window_ptr, bcol);
                Screen('Flip', window_ptr);
                if session.train && run_num == 2
                    line5 = "Les images apparaitront maintenant au rythme reel."
                    line6 = '\nAppuyez sur Espace pour commencer';
                    instructions = [line5 line6]
                    DrawFormattedText(window_ptr, instructions, 'center', 'center', tcol);
                else
                    DrawFormattedText(window_ptr, session.instructions, 'center', 'center', tcol); % 'flipHorizontal', 1);
                end
                Screen('Flip', window_ptr);
                if session.train
                    get_key('space', session.keyboard);
                else
                    get_key('t', session.keyboard);
                end
            elseif session.trigger == 1
                Screen('FillRect', window_ptr, bcol);
                Screen('Flip', window_ptr);
                DrawFormattedText(window_ptr, session.instructions, 'center', 'center', tcol); % 'flipHorizontal', 1);
                Screen('Flip', window_ptr);
                while 1
                    get_key('g', session.keyboard);
                    [status, ~] = start_scan;
                    if status == 0
                        break
                    else
                        message = 'Trigger failed.';
                        DrawFormattedText(window_ptr, message, 'center', 'center', fcol);
                        Screen('Flip', window_ptr);
                    end
                end
            end
            % display countdown numbers
            % [cnt_time, rem_time] = deal(session.count_down + GetSecs);
            % cnt = session.count_down;
            % while rem_time > 0
            %     if floor(rem_time) <= cnt
            %         DrawFormattedText(window_ptr, num2str(cnt), 'center', 'center', tcol);
            %         Screen('Flip', window_ptr);
            %         cnt = cnt - 1;
            %     end
            %     rem_time = cnt_time - GetSecs;
            % end
            % main display loop
            DisableKeysForKbCheck(KbName('t'));
            start_time = GetSecs;
            true_onsets = [];
            for ii = 1:length(stim_names)
                true_onsets = [true_onsets; GetSecs-start_time];
                % display blank screen if baseline and image if stimulus
                if strcmp(stim_names{ii}, 'baseline')
                    Screen('FillRect', window_ptr, bcol);
                    draw_fixation(window_ptr, center, fcol);
                else
                    Screen('DrawTexture', window_ptr, img_ptrs(ii), [], stim_rect);
                    draw_fixation(window_ptr, center, fcol);
                end
                Screen('Flip', window_ptr);
                % collect responses
                ii_press = []; ii_keys = [];
                [keys, ie, exitKey] = record_keys(start_time + (ii - 1) * sdc, stim_dur, k);  % IBC change: escape key exit
                if exitKey  % IBC change: escape key exit
                    break
                end
                ii_keys = [ii_keys keys]; ii_press = [ii_press ie];
                % display ISI if necessary
                if isi_dur > 0
                    Screen('FillRect', window_ptr, bcol);
                    draw_fixation(window_ptr, center, fcol);
                    [keys, ie] = record_keys(start_time + (ii - 1) * sdc + stim_dur, isi_dur, k);
                    ii_keys = [ii_keys keys]; ii_press = [ii_press ie];
                    Screen('Flip', window_ptr);
                end
                resp_keys{ii} = ii_keys;
                resp_press(ii) = min(ii_press);
            end
            session.true_onsets{run_num} = true_onsets;
            % store responses
            session.responses(run_num).keys = resp_keys;
            session.responses(run_num).press = resp_press;
            fname = [session.id '_backup_run' num2str(run_num) '.mat'];
            fpath = fullfile(session.exp_dir, 'data', session.id, fname);
            save(fpath, 'resp_keys', 'resp_press', '-v7');
            if ~exitKey % IBC change: escape key exit
                % analyze response data and display performance
                session = score_task(session, run_num);
                if session.train && run_num == 1
                    continue
                else
                    endOfRun = 'FIN';
                    DrawFormattedText(window_ptr, endOfRun, 'center', 'center', [255 255 255]);
                    Screen('Flip', window_ptr);
                    get_key('space', session.keyboard);
                end
            end
            ShowCursor;
            Screen('CloseAll');
        end
        
        % quantify performance in stimulus task
        function session = score_task(session, run_num)
            sdc = session.sequence.stim_duty_cycle;
            fpw = session.wait_dur / sdc;
            % get response time windows for task probes
            resp_presses = session.responses(run_num).press;
            resp_correct = session.sequence.task_probes(:, run_num);
            probe_idxs = find(resp_correct);
            hit_windows = zeros(size(resp_correct));
            for ww = 1:ceil(fpw)
                hit_windows(probe_idxs + ww - 1) = 1;
            end
            hit_resp_windows = resp_presses(hit_windows == 1);
            fa_resp_windows = resp_presses(hit_windows == 0);
            % count hits and false alarms
            session.hit_cnt(run_num) = sum(~min(reshape(hit_resp_windows, fpw, [])));
            session.fa_cnt(run_num) = sum(~fa_resp_windows);
        end
        
        % write vistasoft-compatible parfile for each run
        function session = write_parfiles(session)
            session.parfiles = cell(1, session.num_runs/2);   % IBC change: 2 longer runs
            % list of conditions and plotting colors
            conds = ['Baseline' session.sequence.stim_conds];
            cols = {[1 1 1] [0 0 1] [0 0 0] [1 0 0] [.8 .8 0] [0 1 0]};
            % write information about each block on a separate line
            for rr = 1:session.num_runs/2   % IBC change: 2 longer runs
                block_onsets = session.sequence.block_onsets(:, rr);
                block_conds = session.sequence.block_conds(:, rr);
                cond_names = conds(block_conds + 1);
                cond_cols = cols(block_conds + 1);
                fname = [session.id '_fLoc_run' num2str(rr) '.par'];
                fpath = fullfile(session.exp_dir, 'data', session.id, fname);
                fid = fopen(fpath, 'w');
                for bb = 1:length(block_onsets)
                    fprintf(fid, '%d \t %d \t', block_onsets(bb), block_conds(bb));
                    fprintf(fid, '%s \t', cond_names{bb});
                    fprintf(fid, '%i %i %i \n', cond_cols{bb});
                end
                fclose(fid);
                session.parfiles{rr} = fpath;
            end
        end
        
    end
    
end

