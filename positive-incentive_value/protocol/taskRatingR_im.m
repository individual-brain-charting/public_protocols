% function [] = taskRatingR_im(subid,nsession)
% MBB motivational battery (version 2.2).
% Task RatingR
%
% Written by Raphael Le Bouc - September 2013
% Triggers and eye_tracker added by Alizee Lopez - October 2015

% modified by Nicolas Clairis - mars 2016 and re-adapted in january 2017
% for NeuroSpin study

%%Uncomment the next line if you want to resize the images upon launching the protocol
%pkg load image

%% Identification of the task
taskName = 'ratingR_im';

%a voir comment on definit le run ??? Isa (run definition inside ratings_full_Nspin.m)
runname = num2str(nsession);
resultname = identification_batmotiv(taskName, subid, runname);


%% Directory Configuration
stimDir = [root filesep 'rewardim' filesep];

%% Generator reset
rand('state',sum(100*clock));

%% Load stimuli
if stimCateg == 1
  instruction = 'Évaluer les images de nourriture \n\n de "Pas du tout agréable" à "Énormément agréable" \n\n selon à quel point vous voudriez manger l''aliment.';
elseif stimCateg == 2
  instruction = 'Évaluer les images de tableaux \n\n de "Pas du tout agréable" à "Énormément agréable" \n\n selon à quel point vous voudriez posséder le tableau.';
elseif stimCateg == 3
  instruction = 'Évaluer les images de visages \n\n de "Pas du tout agréable" à "Énormément agréable" \n\n selon à quel point vous voudriez rencontrer la personne.';
elseif stimCateg == 4
  instruction = 'Évaluer les images de maisons \n\n de "Pas du tout agréable" à "Énormément agréable" \n\n selon à quel point vous voudriez habiter la maison.';
end

% extract folder where images are stored for this particular run
if nsession > 0
  group = {'A','B'};
  if stimCateg == 1
      categName = 'food_';
      categDir = [stimDir, categName,group{stimGroup},'_resized'];
  elseif stimCateg == 2
      categName = 'painting_';
      categDir = [stimDir, categName,group{stimGroup}];
  elseif stimCateg == 3
      categName = 'face_';
      categDir = [stimDir, categName,group{stimGroup}];
  elseif stimCateg == 4
      categName = 'house_';
      categDir = [stimDir, categName,group{stimGroup},'_resized'];
  end
end
% load images
for iItem = 1:total_items
    % training
    if nsession == 0
        categ = categName(1:end);
        if stimCateg == 1 || stimCateg == 4
          pic_stim{iItem} = Screen('MakeTexture',window,imread([stimDir, 'training_',categ, '_resized', filesep,'example_' num2str(iItem) '.bmp']));
        else
          pic_stim{iItem} = Screen('MakeTexture',window,imread([stimDir, 'training_',categ,filesep,'example_' num2str(iItem) '.bmp']));
        end
    else
        %% Resizing original images before main run
        %new_pic_stim = imread([categDir, filesep, categName, num2str(iItem) '.bmp']); % task
        %new_pic_stim_resized = imresize(new_pic_stim, 1.1);
        %pic_stim{iItem} = Screen('MakeTexture',window,new_pic_stim_resized); % task
        pic_stim{iItem} = Screen('MakeTexture',window,imread([categDir, filesep, categName, num2str(iItem) '.bmp'])); % task
    end
    [wrect{iItem},hrect{iItem}] = RectSize(Screen('Rect',pic_stim{iItem}));
    rect_stim{iItem} = CenterRectOnPoint(Screen('Rect',pic_stim{iItem}),x,y+hrect{iItem}/2-y_shift);
    %disp(rect_stim{iItem})
end

%% data to save
trials = 1:total_items;
totalTrials = length(trials);
if nsession == 0
    Perm = 1:length(trials); % keep the same training order for all the subjects
else
    Perm = randperm(total_items);
    save([subdir, filesep, 'Perm_Rim_ratings_sub-',subid,'_run',num2str(nsession),'.mat'],'Perm');
end
trialtime = nan(1,totalTrials);
rt_decision = nan(1,totalTrials);
rt_validate = nan(1,totalTrials);
rating = nan(1,totalTrials);
% fixation cross jitter between 1 to 4.5 seconds
if totalTrials == 60 && nsession > 0
    jitters = 0.5:0.067:4.5; % this is adapted for 60 trials, be careful this has to be changed if you change the number of trials
    jittersPerms = randperm(60);
elseif nsession == 0 && totalTrials == 4
    jitters = [0.5, 1.5, 3.5, 4.5]; % this is adapted for 4 trials, suitable for training session
    jittersPerms = randperm(totalTrials);
else
    warning('you have to fix the way the jitters are defined');
end
cross_ITI_T = jitters(jittersPerms);

%==========================================================================
% INSTRUCTIONS
%==========================================================================

Screen('TextSize', window, 40);
DrawFormattedText(window, instruction, 'center', 'center', [255 255 255], 60, 0, 0, 1.5, 0, [])
% onset
[~,timenow1,~,~,~] = Screen(window,'Flip');
onset.instruction = [onset.instruction; timenow1];
WaitSecs(instruction_T);

%duration
timenow2 = GetSecs;
dur = timenow2 - timenow1;
duration.instruction = [duration.instruction; dur];

%==========================================================================
% RATING
%==========================================================================
stoptask = 0;
cursor = cell(1,totalTrials);
tooslowtrial = 0;

ntrial = 1;
while ntrial <= totalTrials && stoptask == 0
    
    %% ITI cross
    Screen('DrawTexture',window,pic_cross,[],rect_cross);
    % onset
    [~,timenow1,~,~,~] = Screen(window,'Flip');
    onset.cross_ITI = [onset.cross_ITI; timenow1];
    WaitSecs(cross_ITI_T(ntrial));
    % duration
    timenow2 = GetSecs;
    dur = timenow2 - timenow1;
    duration.cross_ITI = [duration.cross_ITI; dur];

    %% check if all keys are up before starting the trial
    keys_are_up = 0;
    [keyisdown, secs, keycode] = KbCheck;
    
    if keyisdown == 1 && (keycode(key.left) == 1 || keycode(key.right) == 1 || keycode(key.leftsmall) == 1 || keycode(key.rightsmall) == 1 || keycode(key.space) == 1)
        keys_are_up = 1;
        while keys_are_up == 1
            [keyisdown, secs, keycode] = KbCheck;
            DrawFormattedText(window,'Relachez les boutons svp','center','center', [255 255 255]);
            % onset
            [~,timenow1,~,~,~] = Screen(window,'Flip');
            onset.please_release = [onset.please_release; timenow1];
            if keyisdown == 0
                keys_are_up = 0;
            end
        end
        % duration
        timenow2 = GetSecs;
        dur = timenow2 - timenow1;
        duration.please_release = [duration.please_release; dur];
        Screen('DrawTexture',window,pic_cross,[],rect_cross);
        % onset
        [~,timenow1,~,~,~] = Screen(window,'Flip');
        onset.cross_release = [onset.cross_release; timenow1];
        WaitSecs(release_wait);
        % duration
        timenow2 = GetSecs;
        dur = timenow2 - timenow1;
        duration.cross_release = [duration.cross_release; dur];
    end
    
    
    if stoptask
        break
    end
    
    %% Show rating scale
    exit_cur = 0;
    iCursor = 1;
    %% cursor at random position between 25 and 75 at beginning of trial
    cursor{ntrial}(iCursor) = randi([1,50],1)+25;
%     cursor{ntrial}(iCursor) = 50;
    
    % Get trialtime
    trialtime(ntrial) = GetSecs;
    cursortime{ntrial}(iCursor) = GetSecs;  % the time of first checking the cursor
    cursormove{ntrial}(iCursor) = 0;        % whether cursor is moved at this time point, if keyisdown, 1, if not, then 0
    
    % Write reward
    Screen('TextSize', window, 25);
    Screen('DrawTexture',window,pic_stim{Perm(ntrial)},[],rect_stim{Perm(ntrial)});
    % Write instructions
    [width,hight] = RectSize(Screen('TextBounds',window,'Ça me plaît :'));
    Screen('DrawText',window,'Ça me plaît :',x-width/2,y-hight/2-60+yscale,[255 255 255]);
    [width,hight] = RectSize(Screen('TextBounds',window,'Pas du tout'));
    Screen('DrawText',window,'Pas du tout',x-400-width/2,y+yscale-hight-25,[255 153 0]);
    [width,hight] = RectSize(Screen('TextBounds',window,'Énormément'));
    Screen('DrawText',window,'Énormément',x+400-width/2,y+yscale-hight-25,[255 153 0]);
    
    % Display cursor and scale
    display_Rating(window,x,y,yscale,cursor{ntrial}(iCursor));
    % onset
    [~,timenow1,~,~,~] = Screen(window,'Flip');
    if tooslowtrial == 0
        onset.display_ratingscaleRim = [onset.display_ratingscaleRim; timenow1];
    elseif tooslowtrial == 1
        onset.tooslowtrial_display_ratingscaleRim = [onset.tooslowtrial_display_ratingscaleRim; timenow1];
    end
    
    while exit_cur == 0
        
        check_time = GetSecs;
        tooslow = 0;
        
        % Write reward
        Screen('TextSize', window, 25);
        Screen('DrawTexture',window,pic_stim{Perm(ntrial)},[],rect_stim{Perm(ntrial)});
        % Write instructions
        [width,hight] = RectSize(Screen('TextBounds',window,'Ça me plaît :'));
        Screen('DrawText',window,'Ça me plaît :',x-width/2,y-hight/2-60+yscale,[255 255 255]);
        
        [width,hight] = RectSize(Screen('TextBounds',window,'Pas du tout'));
        Screen('DrawText',window,'Pas du tout',x-400-width/2,y+yscale-hight-25,[255 153 0]);
        [width,hight] = RectSize(Screen('TextBounds',window,'Énormément'));
        Screen('DrawText',window,'Énormément',x+400-width/2,y+yscale-hight-25,[255 153 0]);
        
        % Display cursor and scale
        display_Rating(window,x,y,yscale,cursor{ntrial}(iCursor));
        Screen(window,'Flip');
        iCursor = iCursor + 1;
        cursor{ntrial}(iCursor) = cursor{ntrial}(iCursor-1);
        
       % Check keys
        keyisdown = false;
        while ~keyisdown
          [keyisdown, secs, keycode] = KbCheck;
          if keyisdown == 1, break; end
        end
        
        if check_time - trialtime(ntrial) < WaitPressTime
            if keyisdown == 1
                
              % check time when subject starts rating (=took his
                % decisions and moves the cursor)
                if isnan(rt_decision(ntrial))
                    ratingtime = GetSecs;
                    rt_decision(ntrial) = ratingtime - trialtime(ntrial);
                end
                
                % monitor rating
                if  keycode(key.space) == 1
                    exit_cur = 1;
                    % duration when checks choice
                    timenow2 = GetSecs;
                    dur = timenow2 - timenow1;
                    if tooslowtrial == 0
                        duration.display_ratingscaleRim = [duration.display_ratingscaleRim; dur];
                        rt_validate(ntrial) = dur;
                    elseif tooslowtrial == 1
                        duration.tooslowtrial_display_ratingscaleRim = [duration.tooslowtrial_display_ratingscaleRim; dur];
                        tooslowtrial = 0;
                    end

                elseif  keycode(key.right) == 1
                    cursor{ntrial}(iCursor) = min([cursor{ntrial}(iCursor)+25 100]);
                elseif keycode(key.left) == 1
                    cursor{ntrial}(iCursor) = max([cursor{ntrial}(iCursor)-25 1]);
                elseif  keycode(key.rightsmall) == 1
                    cursor{ntrial}(iCursor) = min([cursor{ntrial}(iCursor)+2 100]);
                elseif keycode(key.leftsmall) == 1
                    cursor{ntrial}(iCursor) = max([cursor{ntrial}(iCursor)-2 1]);
                elseif keycode(key.escape) == 1
                    exit_cur = 1;
                    stoptask = 1;
                end
            end
        elseif check_time - trialtime(ntrial) >= WaitPressTime
            % duration
            dur = WaitPressTime;
            if tooslowtrial == 0 % writes time both in normal matrix as in tooslow matrix for the first too slow of a trial
                duration.display_ratingscaleRim = [duration.display_ratingscaleRim; dur];
                onset.tooslowtrial_display_ratingscaleRim = [onset.tooslowtrial_display_ratingscaleRim; timenow1];
                duration.tooslowtrial_display_ratingscaleRim = [duration.tooslowtrial_display_ratingscaleRim; dur];
            elseif tooslowtrial == 1
                duration.tooslowtrial_display_ratingscaleRim = [duration.tooslowtrial_display_ratingscaleRim; dur];
            end
            exit_cur = 1;
            Screen('TextSize', window, 60);
            DrawFormattedText(window, 'Trop lent!', 'center', 'center', [255 255 255], 60, 0, 0, 1.5, 0, [])
            % onset
            [~,timenow1,~,~,~] = Screen(window,'Flip');
            onset.tooslow = [onset.tooslow; timenow1];
            WaitSecs(tooslow_fdbk_T);
            % duration
            timenow2 = GetSecs;
            dur = timenow2 - timenow1;
            duration.tooslow = [duration.tooslow; dur];
            tooslow = 1;
            tooslowtrial = 1;
        end
        cursortime{ntrial}(iCursor) = GetSecs;
        cursormove{ntrial}(iCursor) = keyisdown;
    end
    
    % Update data to save
    rating(ntrial) = cursor{ntrial}(iCursor);
    ratingRimsummary(Perm(ntrial)) = cursor{ntrial}(iCursor);
    if tooslow == 0
        ntrial = ntrial + 1; % otherwise comes back to same trial
    end
    
    % display number of the trial so that the experimenter can keep track
    % on how much there is left at the end of each trial
    disp(['Trial ',num2str(ntrial),'/',num2str(totalTrials)]);
    
    % save all stuff at the end of each trial in the subject's results
    % directory (if fMRI crashes or any problem, we can still keep a record
    % of the data)
    save([behaviordir,filesep,'global_sub_',subid,'_run',runname,'_',taskName,'_',categName,'group',groupName,'.mat'])
end

%% Save data
data = [trials; rating; trialtime; rt_decision; rt_validate]';
cd(subdir);
save(resultname,'subid','nsession',...
    'data','rt_decision','rt_validate',...
    'rating','Perm','ratingRimsummary',...
    'cursor','cursortime','cursormove',...
    'onset','duration');
cd(root);
