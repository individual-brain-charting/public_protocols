from neurodesign import geneticalgorithm, generate, msequence 
import sys

design_i = sys.argv[1]

EXP = geneticalgorithm.experiment( 
    TR = 0.68, 
    P = [0.5, 0.5], 
    C = [[0.5, -0.5]], 
    rho = 0.3, 
    n_stimuli = 2, 
    n_trials = 48, 
    duration = 620, 
    resolution = 0.136, 
    stim_duration = 10, 
    t_pre = 0.0, 
    t_post = 2, 
    maxrep = 6, 
    hardprob = False, 
    confoundorder = 3, 
    ITImodel = 'exponential', 
    ITImin = 0.0, 
    ITImean = .9, 
    ITImax = 6.0, 
    restnum = 0, 
    restdur = 0.0) 


POP = geneticalgorithm.population( 
    experiment = EXP, 
    G = 20, 
    R = [0.4, 0.4, 0.2], 
    q = 0.01, 
    weights = [0.0, 0.1, 0.4, 0.5], 
    I = 4, 
    preruncycles = 1000, 
    cycles = 4000, 
    convergence = 1000, 
    outdes = 4, 
    folder = '../fmri_experiments/design_files/ward_and_allport/ward_and_allport_designs_'+design_i) 


POP.naturalselection()
POP.download()
