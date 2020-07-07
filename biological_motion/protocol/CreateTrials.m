function trials = CreateTrials(walkerindex, walkerdir, walkerori, walkercoh, masktype, maskdir, maskori, maskcoh, rep)

%Randomization of trials
ran = 2; %in blocks
%rep = 4;

%Prepare trials
tr = 1;
for l=1:rep
    for m=1:size(walkerindex,2)
        for n = 1:size(walkerdir,2)
            for o = 1:size(walkerori, 2)
                for p = 1:size(walkercoh, 2);   
                    for q = 1:size(masktype, 2);
                        for r = 1:size(maskdir,2);
                            for s = 1:size(maskori, 2);
                                for t = 1:size(maskcoh, 2);
                                    trials(tr,1)= walkerindex(m);
                                    trials(tr,2)= walkerdir(n);
                                    trials(tr,3)= walkerori(o);
                                    trials(tr,4)= walkercoh(p);
                                    trials(tr,5)= masktype(q);
                                    trials(tr,6)= maskdir(r);
                                    trials(tr,7)= maskori(s);
                                    trials(tr,8)= maskcoh(t);
                                    
                                    tr = tr+1;
                                end
                            end
                        end
                    end
                end
            end
        end
    end
end

%RANDOMIZE TRIALS
%rand('state',sum(100*clock));

if ran == 1;                                % randomize trials in blocks
    blocksize=size(trials,1) / rep;         % size of a trial block
    for i=1:rep
        random=shuffle((i-1)*blocksize+1:(i-1)*blocksize+blocksize);
        j=(i-1)*blocksize+1;
        for k=random
            trials2(j,:)=trials(k,:);
            j=j+1;
        end
    end
    trials=trials2;
    clear trials2;
elseif ran == 2;                            % completely randomize order of trials
    random=randperm(size(trials,1));
    j=1;
    for i=random
        trials2(j,:)=trials(i,:);
        j=j+1;
    end
    trials=trials2;
    clear trials2;
end;




