function pptwrite(data, fname, check)

%pptwrite(data, fname, check)
%
% writes the data created by runtrials_single, runtrials_double,
% or runtrials_ident (completed trials variable) into an ascii file.
% If check is set to 1, existing files will not be overwritten
% and a warning will be issued.
%
%INPUTS
%data       data to be written - the completed trials variable from runtrials
%fname      file name
%check      OPTIONAL flag: 1=do not overwrite existing file, 0 (DEFAULT) = overwrite


if nargin < 3
    check = 0;
end;

if check
    fid = fopen(fname);
    if fid>0
        fclose(fid);
        error('There exists a file for this name already. Please choose a different name.\n');
        return;
    end;
end;

if ~isempty(fname);
    fid=fopen(fname,'w');
    for i=1:size(data,1);
        switch size(data,2)                             %Detect which routine pptwrite was called from based on size
                                                        %of trials (data)
            case 38                                     %from runtrials_double
                fprintf(fid,'%2.0f %4.1f %2.1f %3.1f %2.0f %1.0f %2.1f %2.1f %3.0f %3.0f %1.0f %2.0f %4.1f %2.1f %3.1f %2.0f %1.0f %2.1f %2.1f %3.0f %3.0f %1.0f %2.0f %4.1f %2.1f %3.1f %2.0f %1.0f %2.1f %2.1f %4.0f %4.1f %4.1f %2.1f %1.0f %1.0f %2.0f %4.3f', data(i,1), data(i,2), data(i,3), data(i,4), data(i,5), data(i,6), data(i,7), data(i,8), data(i,9), data(i,10), data(i,11), data(i,12), data(i,13), data(i,14), data(i,15), data(i,16), data(i,17), data(i,18), data(i,19), data(i,20), data(i,21), data(i,22), data(i,23), data(i,24), data(i,25), data(i,26), data(i,27), data(i,28), data(i,29), data(i,30), data(i,31), data(i,32), data(i,33), data(i,34), data(i,35), data(i,36), data(i,37), data(i,38));
            case 24                                     %from runtrials_single
                fprintf(fid,'%2.0f %4.1f %2.1f %3.1f %2.0f %1.0f %2.1f %2.1f %3.0f %3.0f %1.0f %2.0f %4.1f %2.1f %3.1f %2.0f %1.0f %2.1f %2.1f %4.0f %4.1f %1.0f %2.0f %4.3f', data(i,1), data(i,2), data(i,3), data(i,4), data(i,5), data(i,6), data(i,7), data(i,8), data(i,9), data(i,10), data(i,11), data(i,12), data(i,13), data(i,14), data(i,15), data(i,16), data(i,17), data(i,18), data(i,19), data(i,20), data(i,21), data(i,22), data(i,23), data(i,24));
            case 26                                     %from runtrials_ident
                fprintf(fid,'%2.0f %4.1f %2.1f %3.1f %2.0f %1.0f %2.1f %2.1f %3.0f %3.0f %1.0f %2.0f %4.1f %2.1f %3.1f %2.0f %1.0f %2.1f %2.1f %4.0f %4.1f %2.0f %1.0f %2.0f %4.3f %1.0f', data(i,1), data(i,2), data(i,3), data(i,4), data(i,5), data(i,6), data(i,7), data(i,8), data(i,9), data(i,10), data(i,11), data(i,12), data(i,13), data(i,14), data(i,15), data(i,16), data(i,17), data(i,18), data(i,19), data(i,20), data(i,21), data(i,22), data(i,23), data(i,24), data(i,25), data(i,26));
        end;
        if i < size(data,1); fprintf(fid,'\n'); end;
    end;
end;
fclose('all');