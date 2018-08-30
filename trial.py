from exptools.core import Trial
from psychopy import event, visual
import itertools
import numpy as np
from stimuli import StimulusSet


class BRAnaglyphTrial(Trial):

    def __init__(self, 
                 ID=None,
                 session=None,
                 parameters={},
                 *args, 
                 **kwargs):

        phase_durations = [10]

        super(
            BRAnaglyphTrial,
            self).__init__(ID=ID,
                           phase_durations=phase_durations,
                           session=session,
                           parameters=parameters,
                           *args,
                           **kwargs)


        rot_per_second = self.session.config.get('stimuli', 'rotations_per_second')
        self.rotate_per_frame = 360 / self.session.framerate * rot_per_second


    def draw(self):


        self.session.red_grating.draw()
        self.session.green_grating.draw()

        self.session.red_grating.ori = self.session.red_grating.ori + self.rotate_per_frame
        self.session.green_grating.ori = self.session.green_grating.ori + self.rotate_per_frame

        self.session.rim.draw()

        super(BRAnaglyphTrial,
              self).draw()

        

    def event(self):
        for ev in event.getKeys():
            if ev in ['esc', 'escape', 'q']:
                self.events.append(
                    [-99, self.session.clock.getTime() - self.start_time])

                self.stopped = True
                self.session.stopped = True
                print 'run canceled by user'

            super(BRAnaglyphTrial, self).key_event(ev)

        super(BRAnaglyphTrial, self).event()


