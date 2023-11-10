from psychopy import visual, gui, data, core, event, logging, info
from psychopy.constants import *
import numpy as np
import os
from config import *

def initTask(expInfo):
   ###### Task parameters properties ######
    # task properties
    numSessions = 1
    numTrials = 20
    # trial timing
    def trialParam(numSessions, numTrials):
        maxRT = 3
        isiTime = 1.75
        fbTime = 1.75
        disDaqTime = 0
        minJitter = 0.5
        maxJitter = 1.5
        endFixTime = 0.5
        trialsPerSess = numTrials // numSessions
        return dict(maxRT=maxRT,
                    isiTime=isiTime,
                    fbTime=fbTime,
                    disDaqTime=disDaqTime,
                    minJitter=minJitter,
                    maxJitter=maxJitter,
                    endFixTime=endFixTime,
                    trialsPerSess=trialsPerSess)
    trialInfo = dict2class(trialParam(numSessions, numTrials))
    # Win probabilities

    def taskParam():
        subID = int()
        instructCond = str()
        pWinHigh = 0.70
        pWinLow = 0.30
        outMag = np.array([10, 20])
        pReversal = 0.25
        return dict(subID=subID,
                    instructCond=instructCond,
                    pWinHigh=pWinHigh,
                    pWinLow=pWinLow,
                    outMag=outMag,
                    pReversal=pReversal)
    taskInfo = dict2class(taskParam())
    taskInfo.__dict__.update({'trialInfo': trialInfo,
                              'numSessions': numSessions,
                              'numTrials': numTrials})
    ###### Setting up the display structure #######

    def dispParam(expInfo):
        xRes = 1600
        yRes = 1200
        screenColor=[0.6, 0.6, 0.6]
        screenColSpace='rgb'
        screenPos=(0, 0)
        screenUnit='norm'
        screenWinType='pyglet'
        screenScaling = 1
        screen = visual.Window(color=screenColor,
                               colorSpace=screenColSpace,
                               size=(xRes * screenScaling, yRes * screenScaling),
                               pos=screenPos,
                               units=screenUnit,
                               winType=screenWinType,
                               fullscr=True,
                               screen=1,
                               allowGUI=False)
        monitorX = screen.size[0]
        monitorY = screen.size[1]
        fps = screen.getActualFrameRate(nIdentical=10,
                                        nMaxFrames=100,
                                        nWarmUpFrames=10,
                                        threshold=1)
        textFont = 'Helvetica'
        imageSize = 0.5
        imagePosL = [-0.5,0]
        imagePosR = [0.5,0]
        dispInfo = dict2class(dict(screenScaling=screenScaling,
                                monitorX=monitorX,
                                monitorY=monitorY,
                                fps=fps,
                                textFont=textFont,
                                imageSize=imageSize,
                                imagePosL=imagePosL,
                                imagePosR=imagePosR))
        return dispInfo, screen
    [dispInfo, screen] = dispParam(expInfo)

    # Set up python objects for all generic task objects

    # Start loading images
    loadScreen = visual.TextStim(screen,
                                 text="Loading...",
                                 font=dispInfo.textFont,
                                 pos=screen.pos,
                                 height=0.1,
                                 color='black')
    loadScreen.setAutoDraw(True)
    screen.flip()
    # display 'save' screen
    saveScreen = visual.TextStim(screen,
                                 text="Saving...",
                                 font=dispInfo.textFont,
                                 pos=screen.pos,
                                 height=0.1,
                                 color='black')
    # Keyboard info
    keyInfo = dict2class(trainingkeyConfig())

    # Stimuli
    stim1 = TrialObj(taskInfo, type="stim", pathToFile=expInfo.stimDir + os.sep + 'fract1')
    stim2 = TrialObj(taskInfo, type="stim", pathToFile=expInfo.stimDir + os.sep + 'fract2')

    # Outcome
    outGain = np.empty(len(taskInfo.outMag), dtype=object)
    outLoss = np.empty(len(taskInfo.outMag), dtype=object)
    for idx, mag in enumerate(taskInfo.outMag):
        outGain[idx] = TrialObj(taskInfo, type='out', pathToFile=expInfo.stimDir + os.sep +
                                'cb_' + str(expInfo.sub_cb) + os.sep + 'gain_' + str(mag))
        outLoss[idx] = TrialObj(taskInfo, type='out', pathToFile=expInfo.stimDir + os.sep +
                                'cb_' + str(expInfo.sub_cb) + os.sep + 'loss_' + str(mag))
    # Fixations
    startFix = visual.TextStim(screen,
                               text="+",
                               font=dispInfo.textFont,
                               pos=[0, 0],
                               height=0.15,
                               color='black',
                               wrapWidth=1.8)
    endFix = visual.TextStim(screen,
                             text="+",
                             font=dispInfo.textFont,
                             pos=screen.pos,
                             height=0.15,
                             color='black',
                             wrapWidth=1.8)

    expEndFix = visual.TextStim(screen,
                             text="+",
                             font=dispInfo.textFont,
                             pos=screen.pos,
                             height=0.15,
                             color='red',
                             wrapWidth=1.8)
    # Stimuli
    leftStim = visual.ImageStim(win=screen,
                                size=dispInfo.imageSize,
                                pos=dispInfo.imagePosL)
    rightStim = visual.ImageStim(win=screen,
                                size=dispInfo.imageSize,
                                pos=dispInfo.imagePosR)
    # Responses (ISI)
    leftResp = visual.ImageStim(win=screen,
                                size=dispInfo.imageSize,
                                pos=dispInfo.imagePosL)
    rightResp = visual.ImageStim(win=screen,
                                size=dispInfo.imageSize,
                                pos=dispInfo.imagePosR)
    # Outcomes
    leftOut = visual.ImageStim(win=screen,
                                size=dispInfo.imageSize,
                                pos=dispInfo.imagePosL)
    rightOut = visual.ImageStim(win=screen,
                                size=dispInfo.imageSize,
                                pos=dispInfo.imagePosR)
    # Initialize special messages
    readyExp = visual.TextStim(screen,
                               text= ("Appuyez sur la << flèche gauche >> pour sélectionner l'image de gauche"
                                      "\net sur la << flèche droite >> pour sélectionner celle de droite."
                                      "\nAppuyez sur << espace >> pour commencer."),
                               font=dispInfo.textFont,
                               pos=screen.pos,
                               height=0.1,
                               color='black',
                               wrapWidth=1.9)
    noRespErr = visual.TextStim(screen,
                                text="Veuillez répondre plus rapidement. Cet essai a été annulé.",
                                font=dispInfo.textFont,
                                pos=screen.pos,
                                height=0.07,
                                color='black',
                                wrapWidth=1.8)

    # ITI object
    ITI = core.StaticPeriod(screenHz=dispInfo.fps, win=screen, name='ITI')
    # Wrap objects into dictionary
    taskObj = dict2class(dict(screen=screen,
                           loadScreen=loadScreen,
                           saveScreen=saveScreen,
                           stim1=stim1,
                           stim2=stim2,
                           outGain=outGain,
                           outLoss=outLoss,
                           startFix=startFix,
                           endFix=endFix,
                           expEndFix=expEndFix,
                           leftStim=leftStim,
                           rightStim=rightStim,
                           leftResp=leftResp,
                           rightResp=rightResp,
                           leftOut=leftOut,
                           rightOut=rightOut,
                           readyExp=readyExp,
                           noRespErr=noRespErr,
                           ITI=ITI))

    # Initialize task variables
    taskInfo = initSessions(taskInfo, numSessions)
    # Close loading screen
    loadScreen.setAutoDraw(False)
    return screen, dispInfo, taskInfo, taskObj, keyInfo



class TrialObj(object):
    def __init__(self, taskInfo, type, pathToFile):
        # Static object parameters
        self.path = pathToFile + '.png'
        if (type == "stim"):
            self.respPath = pathToFile + '_resp.png'
            # Initialize design containers
            self.pWin = float()

class Onsets(object):
    def __init__(self,taskInfo):
        self.tPreFix = np.empty(taskInfo.trialInfo.trialsPerSess)
        self.tStim = np.empty(taskInfo.trialInfo.trialsPerSess)
        self.tResp = np.empty(taskInfo.trialInfo.trialsPerSess)
        self.tOut = np.empty(taskInfo.trialInfo.trialsPerSess)
        self.tPostFix = np.empty(taskInfo.trialInfo.trialsPerSess)

class Responses(object):
    def __init__(self,taskInfo):
        self.respKey = np.empty(taskInfo.trialInfo.trialsPerSess, dtype=object)
        self.rt = np.empty(taskInfo.trialInfo.trialsPerSess)

def initSessions(taskInfo, numSessions):
    # Set up the session-wise design
    sessionInfo = np.empty(taskInfo.numSessions, dtype=object)
    for sI in range(taskInfo.numSessions):
        # Specify which stim is on the left/right
        stim1_left = np.random.binomial(1, 0.5, taskInfo.trialInfo.trialsPerSess).astype(bool)
        # Initialize (before first reversal) which stim is p(high)
        stim1_high = np.random.binomial(1, 0.5, 1).astype(bool)[0]
        # Trial design randomisations
        jitter = np.random.uniform(taskInfo.trialInfo.minJitter,
                                     taskInfo.trialInfo.maxJitter,
                                     taskInfo.trialInfo.trialsPerSess)
        # Store whether the good (pWinHigh) option was chosen
        highChosen = np.zeros(taskInfo.trialInfo.trialsPerSess,dtype=bool)
        # Store which stim is the selected stim
        selectedStim = np.zeros(taskInfo.trialInfo.trialsPerSess,dtype=int)
        # Store whether reversals are possible on trial tI
        reverseStatus = np.zeros(taskInfo.trialInfo.trialsPerSess,dtype=bool)
        # Store whether a reversal occurred on trial tI
        reverseTrial = np.zeros(taskInfo.trialInfo.trialsPerSess,dtype=bool)
        # Initialize timing containers
        sessionOnsets = Onsets(taskInfo)
        sessionResponses = Responses(taskInfo)
        # Initialize stim attribute containers
        def stimParam(taskInfo):
            # For the first axis, indices of 0 = stim1 and 1 = stim2
            pWin = np.empty((2,taskInfo.trialInfo.trialsPerSess), dtype=float)
            isHigh = np.empty((2,taskInfo.trialInfo.trialsPerSess), dtype=bool)
            isSelected = np.empty((2,taskInfo.trialInfo.trialsPerSess), dtype=float)
            isWin = np.empty((2,taskInfo.trialInfo.trialsPerSess), dtype=float)
            outMag = np.empty((2,taskInfo.trialInfo.trialsPerSess), dtype=float)
            return dict(pWin=pWin,
                        isHigh=isHigh,
                        isSelected=isSelected,
                        isWin=isWin,
                        outMag=outMag)
        stimAttrib = dict2class(stimParam(taskInfo))
        # Initialize payout container
        payOut = np.zeros(taskInfo.trialInfo.trialsPerSess,dtype=float)
        # Flatten into class object
        sessionInfo[sI] = dict2class(dict(stim1_left=stim1_left,
                                       stim1_high=stim1_high,
                                       jitter=jitter,
                                       highChosen=highChosen,
                                       selectedStim=selectedStim,
                                       reverseStatus=reverseStatus,
                                       reverseTrial=reverseTrial,
                                       sessionOnsets=sessionOnsets,
                                       sessionResponses=sessionResponses,
                                       stimAttrib=stimAttrib,
                                       payOut=payOut))
    taskInfo.__dict__.update({'sessionInfo': sessionInfo})
    return(taskInfo)
