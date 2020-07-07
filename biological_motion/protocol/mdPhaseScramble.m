function out = mdphasescramble(md);
    nframes = size(md,1);
    nmarkers = size(md,2);
    r = round(rand(1,nmarkers)*nframes);
    for i=1:nmarkers
        h = md(1:r(i),i,:);
        md(1:nframes-r(i),i,:) = md(end-nframes+r(i)+1:end,i,:);
        md(nframes-r(i)+1:end,i,:) = h;
    end;
    out=md;