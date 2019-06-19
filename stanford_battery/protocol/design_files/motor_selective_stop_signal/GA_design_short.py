from neurodesign import geneticalgorithm, generate, msequence 
import sys

design_i = sys.argv[1]

EXP = geneticalgorithm.experiment( 
    TR = 0.68, 
    P = [.6,.2,.2], 
    C = [[0.5, 0, -0.5],[0, 0.5, -0.5]], 
    rho = 0.3, 
    n_stimuli = 3, 
    n_trials = 250, 
    duration = 619, 
    resolution = 0.136, 
    stim_duration = 1.85, 
    t_pre = 0.0, 
    t_post = 0.4, 
    maxrep = 9, 
    hardprob = False, 
    confoundorder = 3, 
    ITImodel = 'exponential', 
    ITImin = 0.0, 
    ITImean = 0.225, 
    ITImax = 6.0, 
    restnum = 0, 
    restdur = 0.0) 


POP = geneticalgorithm.population( 
    experiment = EXP, 
    G = 20, 
    R = [0, 1, 0], 
    q = 0.01, 
    weights = [0.0, 0.1, 0.4, 0.5], 
    I = 4, 
    preruncycles = 500, 
    cycles = 3000, 
    convergence = 100, 
    outdes = 4, 
    folder = '../fmri_experiments/design_files/motor_selective_stop_signal/motor_selective_stop_signal_designs_'+design_i) 


POP.naturalselection()
POP.download()
