from psychopy import visual, gui, data, core, event, logging, info
from psychopy.constants import *
import numpy as np  # whole numpy lib is available, prepend 'np.'
import os
from scipy.io import savemat
from config import *

def runBandit(expInfo, dispInfo, taskInfo, taskObj, keyInfo):
    # Assign the instruction condition (between subject)
    taskInfo.subID = expInfo.SubNo
    taskInfo.instructCond = expInfo.BSCond
    # Loop through sessions
    for sI in np.arange(taskInfo.numSessions):
        # Wait for start confirmation
        if (expInfo.Modality == "behaviour"):
            while True:
                # Draw experimenter wait screen
                taskObj.readyExp.draw()
                taskObj.screen.flip()
                # Wait for starting confirmation response
                response = event.waitKeys(keyList=[keyInfo.instructDone, 'escape'])
                if keyInfo.instructDone in response:
                    # Initialize session clock
                    sessionClock = core.Clock()
                    break
                elif 'escape' in response:
                    print("Aborting program...")
                    core.wait(2)
                    core.quit()
        elif (expInfo.Modality == 'fMRI'):
            # Wait for scanner pulse if fMRI
            while True:
                # Draw pulse-wait screen
                taskObj.scanPulse.draw()
                taskObj.screen.flip()
                # Wait for starting confirmation response
                response = event.waitKeys(keyList=[keyInfo.pulseCode, 'escape'])
                if keyInfo.pulseCode in response:
                    print('Received scanner trigger..')
                    # Initialize session clock
                    sessionClock = core.Clock()
                    taskObj.startFix.setAutoDraw(True)
                    break
                elif 'escape' in response:
                    print("Aborting program...")
                    core.wait(2)
                    core.quit()
        # Intitialize session
        taskObj.screen.flip()
        taskObj.startFix.setAutoDraw(False)
        sessionInfo = taskInfo.sessionInfo[sI]
        # Record disdaq time
        sessionInfo.__dict__.update({'StartTime':sessionClock.getTime()})
        print('Start time: ' + str(sessionClock.getTime()))
        # Initialize the reverseStatus to False (need participant to get 4 continuous correct)
        reverseStatus = False
        # Proceed to trials
        for tI in range(taskInfo.trialInfo.trialsPerSess):
            # Print trial number
            print('Trial No: ' + str(tI))
            # show fixation while loading
            trialStart = sessionClock.getTime()
            # Set up trial structure
            taskObj.ITI.start(sessionInfo.jitter[tI])
            # Record onset for start fixation
            sessionInfo.sessionOnsets.tPreFix[tI] = sessionClock.getTime()
            # Show start fixation
            taskObj.startFix.setAutoDraw(True)
            taskObj.screen.flip()
            # Assign the current reward contingency
            taskObj.ITI.complete()
            initTrial(tI, dispInfo, taskInfo, taskObj, sessionInfo)
            # Run the trial
            runTrial(tI, taskObj, taskInfo, dispInfo, keyInfo, sessionInfo, sessionClock)
            # Compute reversal (for next trial)
            reverseStatus = computeReversal(tI, taskInfo, sessionInfo, reverseStatus)
            taskObj.ITI.complete()
            # Print trial timestamp
            print('Trial time ' + str(tI) + ': ' + str(sessionClock.getTime() - trialStart)+' sec')
        sessionInfo.__dict__.update({'EndTime':sessionClock.getTime()})
        # Show end ITI and save data
        taskObj.ITI.start(5)# Close screen
        toPay = np.sum(taskInfo.sessionInfo[sI].payOut)
        if toPay < 0: 
            toPay = "perdu {}".format(int(toPay*-1))
        else:
            toPay = "remporté {}".format(toPay)
        moneyWon = visual.TextStim(taskObj.screen,
                                text="Fini\nVous avez {} €".format(toPay),
                                font=dispInfo.textFont,
                                pos=taskObj.screen.pos,
                                height=0.1,
                                color='black',
                                wrapWidth=1.8)
        moneyWon.setAutoDraw(True)
        taskObj.screen.flip()
        # Print session time
        print('Session Time: {} min' .format(sessionClock.getTime()/60))
        # Saving the data
        if (expInfo.Version == 'pract'):
            expInfo.__dict__.update({'SubNo':str(expInfo.SubNo)+'pract'})
        saveData(sI, expInfo, dispInfo, taskInfo, taskObj, keyInfo)
        moneyWon.setAutoDraw(False)
        taskObj.ITI.complete()
    return


def saveData(sI, expInfo, dispInfo, taskInfo, taskObj, keyInfo):
    # Save ancilliary data
    ancOutDir = expInfo.outDir + os.sep + 'ancillary'
    if not os.path.exists(ancOutDir):
        os.mkdir(ancOutDir)
    save_obj(expInfo, ancOutDir + os.sep + 'sub' + str(expInfo.SubNo) + '_sess' + str(expInfo.RunNo) + '_expInfo_' + str(expInfo.date))
    save_obj(dispInfo, ancOutDir + os.sep + 'sub' + str(expInfo.SubNo) + '_sess' + str(expInfo.RunNo) + '_dispInfo_' + str(expInfo.date))
    save_obj(keyInfo, ancOutDir + os.sep + 'sub' + str(expInfo.SubNo) + '_sess' + str(expInfo.RunNo) + '_keyInfo_' + str(expInfo.date))
    # Save data
    save_obj(taskInfo, expInfo.outDir + os.sep + 'sub' + str(expInfo.SubNo) + '_sess' + str(expInfo.RunNo) + '_data_' + str(expInfo.date))
    return


def computeReversal(tI, taskInfo, sessionInfo, reverseStatus):
    # No reversals in the first 5 trials of the task
    if (tI < 4):
        sessionInfo.reverseTrial[tI] = False
    # After the first 5 trials, reversals are possible
    if (tI >= 4):
        # Reversals are possible if 4 continuous correct responses
        if (np.all(sessionInfo.highChosen[tI-4:tI+1] == True)) and (np.all(np.diff(sessionInfo.selectedStim[tI-4:tI+1]) == 0)):
            reverseStatus = True
        # If 4 continuous incorrect responses, not sufficient learning. Reset reversalStatus
        if (np.all(sessionInfo.highChosen[tI-4:tI+1] == False)):
            reverseStatus = False
        # If reversals are possible
        sessionInfo.reverseStatus[tI] = reverseStatus
        # Store the reversal status of the trial
        if (reverseStatus):
            # Determine whether reversals occurs on this trials
            reverse = np.random.binomial(1, taskInfo.pReversal, 1).astype(bool)[0]
            if (reverse):
                # Execute high stim reversal
                sessionInfo.stim1_high = not sessionInfo.stim1_high
                sessionInfo.reverseTrial[tI] = True
                # Reset the reverseStatus
                reverseStatus = False
    return reverseStatus

def initTrial(tI, dispInfo, taskInfo, taskObj, sessionInfo):
    # Initialize trial display drawings
    # End start-trial fixation
    taskObj.startFix.setAutoDraw(False)
    # Define stimulus and responses images for this trial
    if (sessionInfo.stim1_left[tI]):
        taskObj.leftStim.image=taskObj.stim1.path
        taskObj.leftResp.image=taskObj.stim1.respPath
        taskObj.rightStim.image=taskObj.stim2.path
        taskObj.rightResp.image=taskObj.stim2.respPath
    else:
        taskObj.leftStim.image=taskObj.stim2.path
        taskObj.leftResp.image=taskObj.stim2.respPath
        taskObj.rightStim.image=taskObj.stim1.path
        taskObj.rightResp.image=taskObj.stim1.respPath
    # Rescale images
    taskObj.leftStim.rescaledSize = rescaleStim(taskObj.leftStim, dispInfo.imageSize, dispInfo)
    taskObj.leftStim.setSize(taskObj.leftStim.rescaledSize)
    taskObj.leftResp.rescaledSize = rescaleStim(taskObj.leftResp, dispInfo.imageSize, dispInfo)
    taskObj.leftResp.setSize(taskObj.leftResp.rescaledSize)
    taskObj.rightStim.rescaledSize = rescaleStim(taskObj.rightStim, dispInfo.imageSize, dispInfo)
    taskObj.rightStim.setSize(taskObj.rightStim.rescaledSize)
    taskObj.rightResp.rescaledSize = rescaleStim(taskObj.rightResp, dispInfo.imageSize, dispInfo)
    taskObj.rightResp.setSize(taskObj.rightResp.rescaledSize)
    # Draw the stims
    taskObj.leftStim.setAutoDraw(True)
    taskObj.rightStim.setAutoDraw(True)
    # Compute win probabilities for each stim
    if (sessionInfo.stim1_high):
        # Toggle which stim is high/low
        taskObj.stim1.pWin = sessionInfo.stimAttrib.pWin[0, tI] = taskInfo.pWinHigh
        sessionInfo.stimAttrib.isHigh[0, tI] = True
        taskObj.stim2.pWin = sessionInfo.stimAttrib.pWin[1, tI] = taskInfo.pWinLow
        sessionInfo.stimAttrib.isHigh[1, tI] = False
    else:
        # Toggle which stim is high/low
        taskObj.stim1.pWin = sessionInfo.stimAttrib.pWin[0, tI] = taskInfo.pWinLow
        sessionInfo.stimAttrib.isHigh[0, tI] = False
        taskObj.stim2.pWin = sessionInfo.stimAttrib.pWin[1, tI] = taskInfo.pWinHigh
        sessionInfo.stimAttrib.isHigh[1, tI] = True
    return

def computeOutcome(tI, dispInfo, taskInfo, taskObj, keyInfo, sessionInfo, respKey):
     # Draw win and loss magnitudes
     outMag_idx = np.random.choice(np.arange(len(taskInfo.outMag)), 1, True)[0]
     outMag = taskInfo.outMag[outMag_idx]
     # Determine which stim was chosen
     if (respKey == keyInfo.respLeft):
         # Turn off the isi images
         taskObj.leftResp.setAutoDraw(False)
         if (sessionInfo.stim1_left[tI]):
             resp_stimIdx = 0
             sessionInfo.selectedStim[tI] = 1
             pWin = taskObj.stim1.pWin
             isWin = np.random.binomial(1,pWin,1).astype(bool)[0]

         else:
             resp_stimIdx = 1
             sessionInfo.selectedStim[tI] = 2
             pWin = taskObj.stim2.pWin
             isWin = np.random.binomial(1,pWin,1).astype(bool)[0]
         # Present the outcome screen
         if (isWin):
             taskObj.leftOut.image = taskObj.outGain[outMag_idx].path
         else:
             taskObj.leftOut.image = taskObj.outLoss[outMag_idx].path
         # Resize outcome image
         taskObj.leftOut.rescaledSize = rescaleStim(taskObj.leftOut, dispInfo.imageSize, dispInfo)
         taskObj.leftOut.setSize(taskObj.leftOut.rescaledSize)
         taskObj.leftOut.setAutoDraw(True)
     elif (respKey == keyInfo.respRight):
         # Turn off the isi images
         taskObj.rightResp.setAutoDraw(False)
         if (sessionInfo.stim1_left[tI]):
              resp_stimIdx = 1
              sessionInfo.selectedStim[tI] = 2
              pWin = taskObj.stim2.pWin
              isWin = np.random.binomial(1,pWin,1).astype(bool)[0]
         else:
              resp_stimIdx = 0
              sessionInfo.selectedStim[tI] = 1
              pWin = taskObj.stim1.pWin
              isWin = np.random.binomial(1,pWin,1).astype(bool)[0]
         # Present the outcome screen
         if (isWin):
             taskObj.rightOut.image = taskObj.outGain[outMag_idx].path
         else:
             taskObj.rightOut.image = taskObj.outLoss[outMag_idx].path
         # Resize outcome image
         taskObj.rightOut.rescaledSize = rescaleStim(taskObj.rightOut, dispInfo.imageSize, dispInfo)
         taskObj.rightOut.setSize(taskObj.rightOut.rescaledSize)
         taskObj.rightOut.setAutoDraw(True)

     # Record stim attributes
     sessionInfo.stimAttrib.isSelected[resp_stimIdx, tI] = 1
     sessionInfo.stimAttrib.isWin[resp_stimIdx, tI] = isWin
     sessionInfo.stimAttrib.outMag[resp_stimIdx, tI] = outMag
     sessionInfo.stimAttrib.isSelected[1-resp_stimIdx, tI] = 0
     sessionInfo.stimAttrib.isWin[1-resp_stimIdx, tI] = np.nan
     sessionInfo.stimAttrib.outMag[1-resp_stimIdx, tI] = np.nan
     # Record whether they chose the high value option
     sessionInfo.highChosen[tI] = True if (pWin == taskInfo.pWinHigh) else False
     # Record the observed payOut
     sessionInfo.payOut[tI] = outMag * 1 if isWin else outMag * -1
     return

def runTrial(tI, taskObj, taskInfo, dispInfo, keyInfo, sessionInfo, sessionClock):
    # Flip screen and wait for response
    taskObj.screen.flip()
    sessionInfo.sessionOnsets.tStim[tI] = stimOnset = sessionClock.getTime()
    response = event.clearEvents()
    while (sessionClock.getTime() - stimOnset) <= taskInfo.trialInfo.maxRT:
        # wait for response
        response = event.getKeys(keyList=[keyInfo.respLeft, keyInfo.respRight, 'escape'])
        # Process response
        if response:
            # Get response time to calculate RT below
            taskObj.ITI.start(taskInfo.trialInfo.isiTime)
            sessionInfo.sessionOnsets.tResp[tI] = respOnset = sessionClock.getTime()
            # which response was made
            if keyInfo.respLeft in response:
                # left key was pressed
                sessionInfo.sessionResponses.respKey[tI] = respKey = keyInfo.respLeft
                sessionInfo.sessionResponses.rt[tI] = waitTime = respOnset - stimOnset
                fbPosition = dispInfo.imagePosL
                # Show response-specific ISI screen
                taskObj.leftStim.setAutoDraw(False)
                taskObj.leftResp.setAutoDraw(True)
                taskObj.screen.flip()
                computeOutcome(tI, dispInfo, taskInfo, taskObj, keyInfo, sessionInfo, respKey)
                taskObj.ITI.complete()
                # Show outcome feedback
                taskObj.ITI.start(taskInfo.trialInfo.fbTime)
                taskObj.screen.flip()
                sessionInfo.sessionOnsets.tOut[tI] = fbOnset = sessionClock.getTime()
                # Clear objects after presenting
                taskObj.leftOut.setAutoDraw(False)
                taskObj.rightStim.setAutoDraw(False)
                taskObj.ITI.complete()
            elif keyInfo.respRight in response:
                # right key was pressed
                sessionInfo.sessionResponses.respKey[tI] = respKey = keyInfo.respRight
                sessionInfo.sessionResponses.rt[tI] = waitTime = respOnset - stimOnset
                fbPosition = dispInfo.imagePosR
                # Show response-specific ISI screen
                taskObj.rightStim.setAutoDraw(False)
                taskObj.rightResp.setAutoDraw(True)
                taskObj.screen.flip()
                computeOutcome(tI, dispInfo, taskInfo, taskObj, keyInfo, sessionInfo, respKey)
                taskObj.ITI.complete()
                # Show outcome feedback
                taskObj.ITI.start(taskInfo.trialInfo.fbTime)
                taskObj.screen.flip()
                sessionInfo.sessionOnsets.tOut[tI] = fbOnset = sessionClock.getTime()
                # Clear objects after presenting
                taskObj.rightOut.setAutoDraw(False)
                taskObj.leftStim.setAutoDraw(False)
                taskObj.ITI.complete()
            elif 'escape' in response:
                core.wait(1)
                core.quit()
            #  Present trial-end fixation
            taskObj.ITI.start(taskInfo.trialInfo.endFixTime +
                            (taskInfo.trialInfo.maxJitter - sessionInfo.jitter[tI]) +
                            (taskInfo.trialInfo.maxRT - waitTime))
            taskObj.endFix.setAutoDraw(True)
            taskObj.screen.flip()
            taskObj.endFix.setAutoDraw(False)
            sessionInfo.sessionOnsets.tPostFix[tI] = sessionClock.getTime()
            break
    if not response:
        taskObj.ITI.start(taskInfo.trialInfo.isiTime + taskInfo.trialInfo.fbTime)
        taskObj.leftStim.setAutoDraw(False)
        taskObj.rightStim.setAutoDraw(False)
        taskObj.noRespErr.setAutoDraw(True)
        taskObj.screen.flip()
        taskObj.noRespErr.setAutoDraw(False)
        # Set onsets to nan
        sessionInfo.sessionOnsets.tResp[tI] = np.nan
        sessionInfo.sessionResponses.respKey[tI] = np.nan
        sessionInfo.sessionResponses.rt[tI] = np.nan
        waitTime = taskInfo.trialInfo.maxRT
        sessionInfo.sessionOnsets.tOut[tI] = np.nan
        # Set stim attributes to nan
        sessionInfo.stimAttrib.isSelected[:, tI] = np.nan
        sessionInfo.stimAttrib.isWin[:, tI] = np.nan
        sessionInfo.stimAttrib.outMag[:, tI] = np.nan
        taskObj.ITI.complete()
        #  Present trial-end fixation
        taskObj.ITI.start(taskInfo.trialInfo.endFixTime +
                        (taskInfo.trialInfo.maxJitter - sessionInfo.jitter[tI]) +
                        (taskInfo.trialInfo.maxRT - waitTime))
        taskObj.endFix.setAutoDraw(True)
        taskObj.screen.flip()
        taskObj.endFix.setAutoDraw(False)
        sessionInfo.sessionOnsets.tPostFix[tI] = sessionClock.getTime()
    return
