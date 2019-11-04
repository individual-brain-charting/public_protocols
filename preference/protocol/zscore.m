function [y] = zscore(x)

    y = (x-mean(x))./(std(x));

end