# Extraction of events files

The script 'paradigm_descriptors_extraction_formisano.py' allows to obtain
BIDS compliant tsv files from the default expyriment output files.

## Running the script

In order for the script to work properly, you will have to specify 4 different
arguments when calling it from the command line:

    $ python paradigm_descriptors_extraction_formisano [sub_type] [sub] 
      [ses-num] [logfile_id]

* sub_type: 0 for pilots ('MRI_pilot-') and 1 for regular participants ('sub-')

* sub: This is the number you want to appear in the output as the participant
number. It is automatically formatted to 2 digit format, so if you input '1',
the script will treat is as '01'. If you work with more than 99 participants,
you can cange the format to 3 digits in line 27 of the script

* ses-num: This is the number of the session, to appear in the events files. Both
the original experiment and this version was conceived to be run into two separated
sessions, so it should be 1 or 2, as with the previous argument, it will be formatted
to two digits

* logfile_id: This will be used to look for logfiles in your input folder.
This parameter will be used to look for files with a wildcard

  * For example, if your value for this parameter is '01', the script will
  look up to all files called 'formisano_protocol_01*'
  
An example of calling would be:

    $ python paradigm_descriptors_extraction_formisano 1 12 1 12
    
This would look up for all logfiles that start by 'formisano_protocol_12*' and 
generate output files named in the following fashion:

sub-01_ses-01_task-formisano_run[number of the run]_events.tsv

## Handling several logfiles

There are several scenarious where you will have more than one logfile from expyriment
for the same participant.

### Multiple sessions

This experiment was originally conceived to be run in two separated 
sessions, so even if you do not repeat any runs, maybe you will end up with
multiple logfiles for the same participant as well.

The third argument of the calling (logfile_id) will help here. Expyriment generates
logfile names using the participant number you provide, and also date information.
For example:

    formisano_protocol_01_201812011345.xpd
    
Would be for participant number 1, year 2018, month 12, day 1, hour 13, minute 45, so
December 1st 2018 at 13:45. This would allow us to be specific about which
logfiles we want.

The two sessions of the experiment were run on different days on the original
experiment, so assuming that is preserved, we can call our function this way:

    $ python paradigm_descriptors_extraction_formisano 1 12 1 12_20181201
    
Now it will look for all the logfiles generated for that participant in that particular
year, month and date. Supposing you scan the same participant again on the next
day for the second session, then:

    $ python paradigm_descriptors_extraction_formisano 1 12 2 12_20181202
    
We change the third argument so our files will be labeled for session 2, and
we also change the logfile_id to the next day. This way you can generate the
events files without worrying about mixing up information pertaining to different 
sessions
    
### Multiple logfiles for the same session

The protocol can start at any of the runs. In case the acquisition has to be
interrupted or repeated for whatever reason. If that is the case, you will have
several logfiles for the same participant. 

In this case, you do not need to change your command line call for the script.
The script will add '-[logfile_number]' for any files that come from additional
logfiles.

For example, let's say that you had to interrupt the acquisition in the middle
of the third run, and then restarted the protocol from that run until the end. In
that particular case, you will have two logfiles for the same day, one with runs
1, 2 and the interrupted run 3, and another one with runs 3, 4, 5 and 6.

We call the function normally, for example to pick all the logfiles for that day,
December 10th of 2018:

    $ python paradigm_descriptors_extraction_formisano 1 12 2 12_20181210

Your output folder then will look like this:

    sub-12_ses-02_task-formisano_run1_events.tsv
    sub-12_ses-02_task-formisano_run2_events.tsv
    sub-12_ses-02_task-formisano_run3_events.tsv
    sub-12_ses-02_task-formisano_run3-1_events.tsv
    sub-12_ses-02_task-formisano_run4-1_events.tsv
    sub-12_ses-02_task-formisano_run5-1_events.tsv
    sub-12_ses-02_task-formisano_run6-1_events.tsv
    
You can easily tell which event files come from which xpd file. In our example, we 
probably would want to delete the first event file for run 3, and manually remove the
extra '-1' for all the ones that come from the extra logfile.