function out = mdSpatialScramble(md, area, vertord);
% out = mdSpatialScramble(md,area);
% Spatial scrambling of md data. Area is a vector with
% three numbers that define the range within which the
% random trajectory locations are chosen
    
%vertord = 0 ->retain vert layout; vertord = 1 ->scramble vert layout too

    
nframes = size(md,1);
nmarkers = size(md,2);
meanpos = mean(md,1);
center = mean(squeeze(meanpos));
h = (rand(nmarkers,3)-0.5)*diag(area) + repmat(center,nmarkers,1);
newmeanpos(1,1:nmarkers,1:3) = h;

if vertord == 0 %quick hack for retaining z
    newmeanpos(:,:,3) = meanpos(:,:,3);
end

out = md - repmat(meanpos,[nframes,1,1]) + repmat(newmeanpos,[nframes,1,1]);
