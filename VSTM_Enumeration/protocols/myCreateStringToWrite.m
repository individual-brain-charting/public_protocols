function [sf] = myCreateStringToWrite(input);
sf ='';
for i= 1:length(input)    
    if (length(input{i})> 1) && (isa(input{i}, 'char')~=1)  
        for j=1:length(input{i})
            input{i}= input{i} * 1.000000001; % I do not know a clever way to have a uniform data format.
            sf = sprintf('%s %s\t',sf, num2str(input{i}(j)));
        end
    else
        sf = sprintf('%s %s\t',sf, num2str(input{i}));
    end
end
sf = sprintf('%s\t',sf);

