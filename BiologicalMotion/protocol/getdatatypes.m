function datatypes=getdatatypes(data)

%datatypes=getdatatypes(data)
%
%Determines the type of each walker data set in 'data'
%Each type may be:
%'mm'           mm walker, either alone or in an mmw matrix
%'md'           md walker (alone)
%'cellmm'       mm walker in a cell array
%'cellmd'       md walker in a cell array
%'mmw'          mmw array - each page (dim 3) = mm
%
%INPUT
%data           data variable
%
%OUTPUTS
%datatypes      cell array indexed according to the data indeces
%               each element is a string: either 'mm', 'md', 'cellmm', 'cellmd'


%Determine data types ('mm', 'md', 'cellmm', 'cellmd', 'mmw')
if iscell(data)                                 %cell array
    for i=1:size(data,2)
        if ndims(data{i})==2                    %cell i is mm
            datatypes{i}='cellmm';
        else                                    %cell i is md
            datatypes{i}='cellmd';
        end
    end
elseif ndims(data)==3                           %3D matrix -> either md or mmw
    if size(data,3)==3                          %either an md matrix or a 3-walker mmw matrix
        beep
        datatypes{1}=input('Is your data variable an md matrix or an mmw matrix?\nType ''md'' (without quotation marks) or ''mmw'' and press ENTER: ', 's');
        if strcmp(datatypes{1},'mmw')           %3-walker mmw matrix
            for i=1:3
                datatypes{i}='mmw';
            end
        end
    else                                        %mmw
        for i=1:size(data,3)
            datatypes{i}='mmw';
        end
    end
else                                            %2D matrix -> only one walker, mm
    datatypes{1}='mm';
end