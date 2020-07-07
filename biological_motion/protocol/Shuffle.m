function [Y,index] = shuffle(X)

% Randomly sorts the input array.
% function [Y,index] = shuffle(X)
%
% Randomly sorts X.
% If X is a vector, sorts all of X, so Y = X(index).
% If X is an m-by-n matrix, sorts each column of X, so
%   for j=1:n, Y(:,j)=X(index(:,j),j).
%
% Also see SORT, Sample, Randi, and RandSample.

% xx/xx/92  dhb  Wrote it.
% 10/25/93  dhb  Return index.
% 5/25/96   dgp  Made consistent with sort and "for i=Shuffle(1:10)"
% 6/29/96   dgp  Edited comments above.
%
%
% Last Update: "2013-11-22 23:53:31 ban (ban.hiroshi@gmail.com)"

[null,index] = sort(rand(size(X)));
Y = X(index);
