'''
    Simple clock for MicroPython
    OS: MicroPython v1.20.0 on 2023-04-26
    Device: Raspberry Pi Pico W with RP2040
    Display: Waveshare Pico-LCD-1.14
'''


from color_setup import ssd # create display instance
from gui.widgets.label import Label # Label widget
from gui.widgets.meter import Meter # Meter widget
from gui.core.writer import CWriter # text Writer
from gui.core.colors import * # standard color definitions
from gui.core.nanogui import refresh
refresh(ssd, True)

import gui.fonts.arial35 as arial35
import gui.fonts.courier20 as courier20
import gui.fonts.arial10 as arial10

import sys
import time
import ntptime

ntptime.settime() # set time to gmt

month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
weekday = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

def pclock():
    
    ''' create time and date labels '''
    CWriter.set_textpos(ssd, 0, 0) # set insertion point
    
    wri = CWriter(ssd, arial35, GREEN, BLACK)
    width = wri.stringlen('XXXX')
    lbltim = Label(wri, 20, 120-int(width/2), width) # time Label
    
    wri4 = CWriter(ssd, courier20, CYAN, BLACK, verbose=False)
    lblsec = Label(wri4, 0, 210, 20) # seconds Label
    
    wri1 = CWriter(ssd, courier20, BLUE, BLACK, verbose=False)
    width1 = wri1.stringlen('XX XX XXXX')
    lbldate = Label(wri1, 70, 120-int(width1/2), width1) # date Label
    
    wri2 = CWriter(ssd, courier20, RED, BLACK, verbose=False)
    width2 = wri2.stringlen('XXXXXXX')
    lblday = Label(wri2, 100, 120-int(width2/2), width2) # day Label
    
    ''' create seconds meter '''
    wri3 = CWriter(ssd, arial10, GREY, BLACK, verbose=False)
    wri3.set_clip(True, True, False)
    mtr = Meter(wri3, 30, 210, width=20, height=100, divisions=0, style=Meter.BAR, bdcolor=False)
    
    try:
        while True:
            t = time.localtime()
            lbltim.value('{:02d}:{:02d}'.format(t[3], t[4]))
            lblsec.value('{:02d}'.format(t[5]))
            lbldate.value('{:02d} {} {:04d}'.format(t[2], month[int(t[1])-1], t[0]))
            lblday.value('{}'.format(weekday[int(t[6])]))
            mtr.value(t[5]/60)
            refresh(ssd)
            time.sleep(1)
    
    except Exception as error:
        print("\nException encountered, exiting")
        print(error)
        refresh(ssd, True)
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, exiting")
        refresh(ssd, True)
        sys.exit(0)
 
pclock()