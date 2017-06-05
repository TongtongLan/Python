#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Utils.Utils
import Operations
class Interaction:

    HINT = 'Please enter the operation number :'
    HINT_SONGNAME = 'Please enter the songname'
    def __init__(self):
        pass

    def exe(self):
        while 1:
            Utils.Utils.Utils().initialize_MainInterface()
            number = Utils.Utils.Utils().get_CommandLineInput(Interaction.HINT)

            if number == '0':
                # quit
                return
            elif number == '1':
                # select songs
                songname = Utils.Utils.Utils().get_CommandLineInput(self.HINT_SONGNAME)
                Operations.selectOperations().select_Songs(songname)
            elif number == '2':
                # select artlist
                pass
            elif number == '3':
                # select
                pass
            else:
                pass

Interaction().exe()


