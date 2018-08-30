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

        phase_durations = [session.config.get('stimuli', 'trial_duration')]

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

class IntroTrial(Trial):

    def __init__(self, 
                 ID='intro',
                 session=None,
                 parameters={},
                 *args, 
                 **kwargs):

        phase_durations = [1e9]

        super(
            IntroTrial,
            self).__init__(ID=ID,
                           phase_durations=phase_durations,
                           session=session,
                           parameters=parameters,
                           *args,
                           **kwargs)

        self.parameters.update({'green_key':self.session.config.get('keys', 'green'),
                           'red_key':self.session.config.get('keys', 'red'),
                           'mixed_key':self.session.config.get('keys', 'mixed'), })



        key_green = self.session.config.get('keys', 'green')
        key_red = self.session.config.get('keys', 'red')
        key_mixed = self.session.config.get('keys', 'mixed')

        text = 'Welcome! Please press {green_key} when you see a GREEN '\
            'stimulus and {red_key} when you see a RED stimulus '\
            'press {mixed_key} when you see a MIXED percept. '\
            'press SPACEBAR to start'.format(**self.parameters)

        self.text = visual.TextStim(self.session.screen,
                                    text)


    def draw(self):
        self.text.draw()

        super(IntroTrial,
              self).draw()

    def event(self):
        for ev in event.getKeys():
            if ev in ['esc', 'escape', 'q']:
                self.events.append(
                    [-99, self.session.clock.getTime() - self.start_time])

                self.stopped = True
                self.session.close()
                print 'run canceled by user'

            elif ev in ['space']:
                self.stopped = True

            super(IntroTrial, self).key_event(ev)

        super(IntroTrial, self).event()


class PauseTrial(Trial):
    
    def __init__(self, 
                 ID='pause',
                 session=None,
                 parameters={},
                 *args, 
                 **kwargs):
        
        phase_durations = [1e9]

        super(
            PauseTrial,
            self).__init__(ID=ID,
                           phase_durations=phase_durations,
                           session=session,
                           parameters=parameters,
                           *args,
                           **kwargs)
        
        text = 'Take a small break. Press SPACE to continue.'

        self.text = visual.TextStim(self.session.screen,
                                    text)

    def draw(self):
        self.text.draw()

        super(PauseTrial,
              self).draw()


    def event(self):
        for ev in event.getKeys():
            if ev in ['esc', 'escape', 'q']:
                self.events.append(
                    [-99, self.session.clock.getTime() - self.start_time])

                self.stopped = True
                self.session.close()
                print 'run canceled by user'

            elif ev in ['space']:
                self.stopped = True

            super(PauseTrial, self).key_event(ev)

        super(PauseTrial, self).event()
