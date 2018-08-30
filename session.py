from exptools.core.session import Session
from psychopy.visual import GratingStim
from psychopy import filters
from stimuli import StimulusSet
from trial import BRAnaglyphTrial, IntroTrial, PauseTrial
import numpy as np
import glob
import pandas as pd
import numpy as np

class BRAnaglyphSession(Session):

    def __init__(self, *args, **kwargs):
        super(BRAnaglyphSession, self).__init__(*args, **kwargs)

        self.n_cycles = 5
        self.framerate = self.config.get('screen', 'framerate')
        self.screen.setBlendMode('add')
        
        self.setup_stimuli()
        
        self.intro_trial = IntroTrial(session=self)

        self.trials = []

        for i in xrange(self.config.get('stimuli', 'n_trials')):
            self.trials.append(BRAnaglyphTrial(ID='trial%d' % i,
                                         session=self))

            if i != self.config.get('stimuli', 'n_trials') - 1:
                self.trials.append(PauseTrial(ID='pause%d' % i,
                                              session=self))

    
    def setup_stimuli(self):
        grating_res = 256
        

        size = self.deg2pix(self.config.get('stimuli', 'size'))

        n_cycles = 1./self.deg2pix(1./self.config.get('stimuli','cycles_per_degree')) * size

        grating = filters.makeGrating(res=grating_res,
                                      cycles=n_cycles) * -1
        green_grating = np.ones((grating_res, grating_res, 3)) * -1.0
        green_grating[..., 1] = grating
        
        self.green_grating = GratingStim(self.screen,
                                 size=self.deg2pix(self.config.get('stimuli', 'size')),
                                 tex=green_grating,
                                 mask='raisedCos',
                                 maskParams={'fringeWidth':0.1},)

        red_grating = np.ones((grating_res, grating_res, 3)) * -1.0
        red_grating[..., 0] = grating

        self.red_grating = GratingStim(self.screen,
                                 size=self.deg2pix(self.config.get('stimuli', 'size')),
                                 tex=red_grating,
                                 ori=90,
                                 mask='raisedCos',
                                 maskParams={'fringeWidth':0.1},)

        self.rim = StimulusSet(self.screen,
                               (0, 0),
                               self.config.get('stimuli', 'size'),
                               self)

    def run(self):
        """run the session"""

        self.intro_trial.run()

        for trial in self.trials:
            trial.run()

        self.stop()
        self.close()
