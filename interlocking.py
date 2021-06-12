#----------------------------------------------------------------------
# This Module deals with the signal/point interlocking for the layout
# This ensures signals are locked (in their "ON" state- i.e. danger)
# if the points ahead are not switched correctly (with FPLs activated)
# for the route controlled by the signal. Similarly points are locked
# along the route controlled by the signal when the signal is "OFF"
#----------------------------------------------------------------------

from model_railway_signals import *

#----------------------------------------------------------------------
# External function to set the initial locking conditions at startup
#----------------------------------------------------------------------

def set_initial_interlocking_conditions():
    lock_signal (5,7,13,14)
    return()

#----------------------------------------------------------------------
# Internal function to interlock a signal with its subsidary aspect
#----------------------------------------------------------------------
def interlock_main_and_subsidary (sig_id):
    if subsidary_clear(sig_id): lock_signal(sig_id)
    else: unlock_signal(sig_id)
    if signal_clear(sig_id): lock_subsidary(sig_id)
    else: unlock_subsidary(sig_id)


#----------------------------------------------------------------------
# Refresh the interlocking (to be called following any changes)
# Station area is effectively split into East and West
# Which would equate to two signal boxes (just like the real thing)
#----------------------------------------------------------------------

def process_interlocking_west():

    # ----------------------------------------------------------------------
    # Signal 1 (West box)
    # Main Signal - Branch Line towards Signal 2
    # ----------------------------------------------------------------------

    # Interlock with signals controlling conflicting outbound movements
    if not point_switched(2) and not point_switched(4):
        # Route into Platform 3 - Interlock with Signal 6
        if signal_clear(6) or subsidary_clear(6): lock_signal(1)
        else: unlock_signal(1)
    elif not point_switched(2) and point_switched(4) and not point_switched(5):
        # Route into Goods Loop - Interlock with Signal 5
        if signal_clear(5) or subsidary_clear(6): lock_signal(1)
        else: unlock_signal(1)
    else:
        # no conflicting movements set up
        unlock_signal(1)
    
    # ----------------------------------------------------------------------
    # Signal 2 (West box)
    # Main & Subsidary Signals - Branch Line into Platform 3 or Goods loop
    # ----------------------------------------------------------------------

    if point_switched(2) or not fpl_active(2) or not fpl_active(4):
        # No Route
        lock_signal(2)
        lock_subsidary(2)
    elif not point_switched(4):
        # Route into Platform 3 - interlock with Signal 6
        if signal_clear(6) or subsidary_clear(6):
            lock_signal(2)
            lock_subsidary(2)
        else:
            # Finally interlock the main and subsidary signals
            interlock_main_and_subsidary(2)
    elif point_switched(5):
        # No route
        lock_signal(2)
        lock_subsidary(2)
    else:
        # Route into Goods Loop - interlock with Signal 5
        if signal_clear(6) or subsidary_clear(6):
            lock_signal(2)
            lock_subsidary(2)
        else:
            # Finally interlock the main and subsidary signals
            interlock_main_and_subsidary(2)

    # ----------------------------------------------------------------------
    # Signal 3 (West box)
    # Main Signal - Up Main into Platform 1, Platform 3 or Goods loop
    # ----------------------------------------------------------------------

    if not fpl_active(1) or point_switched(1) or not fpl_active(2):
        # No route
        lock_signal(3)
    elif not point_switched(2):
        # Route set for up main
        unlock_signal(3)
    elif not point_switched(4):
        # Route into Platform 3 - interlock with Signal 6
        if signal_clear(6) or subsidary_clear(6): lock_signal(3)
        else: unlock_signal(3)
    elif point_switched(5) or not fpl_active(4):
        # No route
        lock_signal(3)
    else:
        # Route into Goods Loop - interlock with Signal 5
        if signal_clear(6) or subsidary_clear(6): lock_signal(3)
        else: unlock_signal(3)
            
    # ----------------------------------------------------------------------
    # Signal 5 (West box)
    # Main Signal - Routes onto Branch or Down Maiin
    # Subsidary Signal - Route onto Branch or MPD or Goods Yard
    # ----------------------------------------------------------------------

    if point_switched(5):
        # Shunting move into Goods yard only
        lock_signal(5)
        if signal_clear(14): lock_subsidary(5)
        else: unlock_subsidary(5)
    elif not fpl_active(4):
        # No Route - Point 4 not locked
        lock_signal(5)
        lock_subsidary(5)
    elif not point_switched(4) and fpl_active(4):
        # Shunting move into MPD only
        lock_signal(5)
        if signal_clear(15): lock_subsidary(5)
        else: unlock_subsidary(5)
    elif not fpl_active(2):
        # No Route - Point 2 not locked
        lock_signal(5)
        lock_subsidary(5)
    elif not point_switched(2):
        # Route is set to Branch - Interlock with Signals 1 and 2
        if signal_clear(1) or signal_clear(2) or subsidary_clear(2):
            lock_signal(5)
            lock_subsidary(5)
        else:
            # Finally interlock the main/subsidary signals
            interlock_main_and_subsidary(5)
    elif not point_switched(1) or not fpl_active(1):
        # Outbound Route is not fully set (no route onto Down Main)
        lock_signal(5)
        lock_subsidary(5)
    else:
        # Route is set and locked to Down Main - shunting not allowed
        unlock_signal(5)
        lock_subsidary(5)

    # ----------------------------------------------------------------------
    # Signal 6 (West box)
    # Main Signal - Routes onto Branch or Down Maiin
    # Subsidary Signal - Route onto Branch only
    # ----------------------------------------------------------------------

    if point_switched(4) or not fpl_active(4) or not fpl_active(2):
        # No Route
        lock_signal(6)
        lock_subsidary(6)
    elif not point_switched(2):
        # Route is set to Branch - Interlock with Signals 1 and 2
        if signal_clear(1) or signal_clear(2) or subsidary_clear(2):
            lock_signal(6)
            lock_subsidary(6)
        else:
            # Finally interlock the main/subsidary signals
            interlock_main_and_subsidary(6)
    elif not point_switched(1) or not fpl_active(1):
        # Outbound Route is not fully set (no route onto Down Main)
        lock_signal(6)
        lock_subsidary(6)
    else:
        # Route is set and locked to Down Main - shunting not allowed
        unlock_signal(6)
        lock_subsidary(6)
        
    # ----------------------------------------------------------------------
    # Signal 12 (West box)
    # Main Signal - Route onto Down Main only
    # ----------------------------------------------------------------------

    if point_switched(3) or not fpl_active(3) or point_switched(1) or not fpl_active(1):
        # Route not set and locked
        lock_signal(12)
    else:
        unlock_signal(12)

    # ----------------------------------------------------------------------
    # Signal 13 (West box)
    # Main Signal - Route onto Down Main only
    # ----------------------------------------------------------------------

    if not point_switched(3) or not fpl_active(3) or point_switched(1) or not fpl_active(1):
        # Route not set and locked
        lock_signal(13)
    else:
        unlock_signal(13)

    # ----------------------------------------------------------------------
    # Signal 14 (West box) - Exit from Goods Yard
    # Subsidary Signal - Route to Goods Loop only
    # ----------------------------------------------------------------------
    
    if not point_switched(5):
        # No route
        lock_signal(14)
    else:
        # Route set to goods loop - Interlock with signal 5
        if signal_clear(5) or subsidary_clear(5):lock_signal(14)
        else: unlock_signal(14)

    # ----------------------------------------------------------------------
    # Signal 15 (West box) - Exit from MPD
    # Subsidary Signal - Route to Goods Loop only
    # ----------------------------------------------------------------------

    if point_switched(5) or point_switched(4) or not fpl_active(4):
        # No route
        lock_signal(15)
    else:
        # Route set to goods loop - Interlock with signal 5
        if signal_clear(5) or subsidary_clear(5): lock_signal(15)
        else: unlock_signal(15)

    # ----------------------------------------------------------------------
    # Point 1 (West box)
    # Routes from Goods Loop, Platform 3, Down Loop and Platform 1
    # ----------------------------------------------------------------------

    if signal_clear(3):
        # arrival from up main Set/Cleared
        lock_point(1)
    elif signal_clear(12) or signal_clear(13):
        # departure from Down main or Platform 3 Set/Cleared
        lock_point(1)
    elif point_switched(1) and point_switched(2) and (signal_clear(5) or signal_clear(6)) :
        # departute from goods loop or platform 3 onto Down main set/cleared (no shunting onto down main)
        lock_point(1)
    else:
        unlock_point(1)

    # ----------------------------------------------------------------------
    # Point 2 (West box)
    # Routes from Goods Loop, Platform 3, Down Loop and Platform 1
    # ----------------------------------------------------------------------

    if signal_clear(3) or signal_clear(2) or subsidary_clear(2):
        # movement from up main or from branch set/cleared
        lock_point(2)
    elif not point_switched(4) and (signal_clear(6) or subsidary_clear(6)):
        # movement from platform 3 set/cleared
        lock_point(2)
    elif point_switched(4) and not point_switched(5) and (signal_clear(5) or subsidary_clear(5)):
        # movement from goods loop set/cleared
        lock_point(2)
    else:
        unlock_point(2)

    # ----------------------------------------------------------------------
    # Point 3 (West box)
    # Routes from Down Loop and Platform 1
    # ----------------------------------------------------------------------

    if signal_clear(12) or signal_clear(13):
        # Departure from platform 3 or down main set/cleared
        lock_point(3)
    else:
        unlock_point(3)
        
    # ----------------------------------------------------------------------
    # Point 4 (West box)
    # ----------------------------------------------------------------------

    if signal_clear(15):
        # movement from MPD set/cleared
        lock_point(4)
    elif signal_clear(2) or subsidary_clear(2):
        # arrival from branch set/cleared
        lock_point(4)
    elif signal_clear(6) or subsidary_clear(6):
        # Departure from platform 3 set/cleared
        lock_point(4)
    elif not point_switched(5) and (signal_clear(5) or subsidary_clear(5)):
        # departure from goods loop set/cleared
        lock_point(4)
    elif point_switched(2) and signal_clear(3):
        # arrival from up main set/cleared
        lock_point(4)
    else:
        unlock_point(4)

    # ----------------------------------------------------------------------
    # Point 5 (West box) - No Facing Point Locks
    # ----------------------------------------------------------------------

    if signal_clear(14) or signal_clear(15):
        # movement from MPD or from goods yard set/cleared
        lock_point(5)
    elif signal_clear(5) or subsidary_clear(5):
        # movement from goods loop set/cleared
        lock_point(5)
    elif point_switched(4) and (signal_clear(2) or subsidary_clear(2)):
        # movement from branch set/cleared
        lock_point(5)
    elif point_switched(2) and point_switched(4) and signal_clear(3):
        # arrival from up main set/cleared
        lock_point(5)
    else:
        unlock_point(5)

#----------------------------------------------------------------------
# Station East Interlocking
#----------------------------------------------------------------------

def process_interlocking_east():

    # ----------------------------------------------------------------------
    # Signal 4 (East box)
    # Main Signal - Route onto Up Maiin
    # ----------------------------------------------------------------------

    if point_switched(8) or not fpl_active(8) or point_switched(9) or not fpl_active(9):
        # No Route
        lock_signal(4)
    else:
        unlock_signal(4)
        
    # ----------------------------------------------------------------------
    # Signal 7 (East box)
    # Main Signal - Routes onto Branch or Up Maiin
    # Subsidary Signal - Route onto Branch only
    # ----------------------------------------------------------------------

    if not fpl_active(6):
        # No Route - Point 6 not locked
        lock_signal(7)
        lock_subsidary(7)
    elif not point_switched(6):
        # Route selected for goods yard - shunting only
        lock_signal(7)
        # interlock with signal 16 controlling output from the yard
        if signal_clear(16): lock_subsidary(7)
        else: unlock_subsidary(7)
    elif not fpl_active(8):
        # No Route - Point 8 not locked
        lock_signal(7)
        lock_subsidary(7)
    elif not point_switched(8):
        # Route selected for Branch line
        # Interlock with signals controling movements from branch line
        if signal_clear(9) or signal_clear(10) or subsidary_clear(10):
            lock_signal(7)
            lock_subsidary(7)
        else:
            # interlock the main/subsidary signals
            interlock_main_and_subsidary(7)
    elif point_switched(9) or not fpl_active(9):
        # No route (points are set for down main)
        lock_signal(7)
        lock_subsidary(7)
    else:
        # Route is set and locked to Up Main - No shunting
        unlock_signal(7)
        lock_subsidary(7)
        
    # ----------------------------------------------------------------------
    # Signal 8 (East box)
    # Main Signal - Routes onto Branch or Up Maiin
    # Subsidary Signal - Route onto Branch only
    # ----------------------------------------------------------------------

    if point_switched(6) or not fpl_active(6) or not fpl_active(8):
        # No Route
        lock_signal(8)
        lock_subsidary(8)
    elif not point_switched(8):
        # Route is set to Branch - Interlock with Signals 9 and 10
        if signal_clear(9) or signal_clear(10) or subsidary_clear(10):
            lock_signal(8)
            lock_subsidary(8)
        else:
            # Finally interlock the main/subsidary signals
            interlock_main_and_subsidary(8)
    elif point_switched(9) or not fpl_active(9):
        # Outbound Route is not fully set (no route onto Up Main)
        lock_signal(8)
        lock_subsidary(8)
    else:
        # Route is set and locked to Up Main - shunting not allowed
        unlock_signal(8)
        lock_subsidary(8)
        
    # ----------------------------------------------------------------------
    # Signal 9 (East box)
    # Main Signal - Routes into Platform 3 or Goods loop
    # ----------------------------------------------------------------------

    # Interlock with signals controlling conflicting outbound movements
    if not point_switched(8) and not point_switched(6):
        # Route into Platform 3 - Interlock with Signal 8
        if signal_clear(8) or subsidary_clear(8): lock_signal(9)
        else: unlock_signal(9)
    elif not point_switched(8) and point_switched(6):
        # Route into Goods Loop - Interlock with Signal 7
        if signal_clear(7) or subsidary_clear(7): lock_signal(9)
        else: unlock_signal(9)
    else:
        # no conflicting movements set up
        unlock_signal(9)

    # ----------------------------------------------------------------------
    # Signal 10 (East box)
    # Main Signal & Subsidary Signal - Routes into Platform 3 or Goods loop
    # ----------------------------------------------------------------------

    if point_switched(8) or not fpl_active(8) or not fpl_active(6):
        # No Route
        lock_signal(10)
        lock_subsidary(10)
    elif not point_switched(6):
        # Route into Platform 3 - interlock with Signal 8
        if signal_clear(8) or subsidary_clear(8):
            lock_signal(10)
            lock_subsidary(10)
        else:
            # Finally interlock the main and subsidary signals
            interlock_main_and_subsidary(10)
    else:
        # Route into Goods Loop - interlock with Signal 7
        if signal_clear(7) or subsidary_clear(7):
            lock_signal(10)
            lock_subsidary(10)
        else:
            # Finally interlock the main and subsidary signals
            interlock_main_and_subsidary(10)
            
    # ----------------------------------------------------------------------
    # Signal 11 (East box)
    # Main Signal - Routes into Plat 1, Down Loop, Plat 3 or Goods loop
    # ----------------------------------------------------------------------

    if not fpl_active(9):
        # No route
        lock_signal(11)
    elif not point_switched(9):
        # Route set for down main or platform 1
        if not fpl_active(7):
            # Route not fully set/locked
            lock_signal(11)
        else:
            unlock_signal(11)
    elif not point_switched(8) or not fpl_active(8) or not fpl_active(6):
        # Route not fully set/locked
        lock_signal(11)
    elif not point_switched(6):
        # Route into Platform 3 - interlock with Signal 8
        if signal_clear(8) or subsidary_clear(8): lock_signal(11)
        else: unlock_signal(11)
    else:
        # Route into Goods Loop - interlock with Signal 7
        if signal_clear(7) or subsidary_clear(7): lock_signal(11)
        else: unlock_signal(11)
        
    # ----------------------------------------------------------------------
    # Signal 16 (East box) - Exit from Goods Yard
    # ----------------------------------------------------------------------

    if point_switched(10) or point_switched(6) or not fpl_active(6):
        # Route not fully set/locked
        lock_signal(16)
    elif not point_switched(6) and (signal_clear(7) or subsidary_clear(7)):
        # Conflicting movement from goods loop already set/cleared
        lock_signal(16)
    else:
        unlock_signal(16)
        
    # ----------------------------------------------------------------------
    # Point 6 (East box)
    # ----------------------------------------------------------------------
    
    if signal_clear(16):
        # movement from Goods Yard set/cleared
        lock_point(6)
    elif signal_clear(10) or subsidary_clear(10):
        # arrival from branch set/cleared
        lock_point(6)
    elif signal_clear(8) or subsidary_clear(8):
        # Departure from platform 3 set/cleared
        lock_point(6)
    elif signal_clear(7) or subsidary_clear(7):
        # departure from goods loop set/cleared
        lock_point(6)
    elif point_switched(8) and point_switched(9) and signal_clear(11):
        # arrival from down main set/cleared
        lock_point(6)
    else:
        unlock_point(6)
        
    # ----------------------------------------------------------------------
    # Point 7 (East box)
    # ----------------------------------------------------------------------

    if not point_switched(9) and signal_clear(11):
        # arrival from down main into platform 1 or through loop set/cleared
        lock_point(7)
    else:
        unlock_point(7)
    
    # ----------------------------------------------------------------------
    # Point 8 (East box)
    # ----------------------------------------------------------------------

    if point_switched(9) and signal_clear(11):
        # arrival from down main set/cleared
        lock_point(8)
    elif signal_clear(10) or subsidary_clear(10):
        # movement from branch set/cleared
        lock_point(8)
    elif not point_switched(6) and (signal_clear(8) or subsidary_clear(8)):
        # movement from platform 3 set/cleared
        lock_point(8)
    elif point_switched(6) and (signal_clear(7) or subsidary_clear(7)):
        # movement from goods loop set/cleared
        lock_point(8)
    elif signal_clear(4):
        # departure from platform 2 set/cleared
        lock_point(8)
    else:
        unlock_point(8)
            
    # ----------------------------------------------------------------------
    # Point 9 (East box)
    # ----------------------------------------------------------------------

    if signal_clear(11) or signal_clear(4):
        # arrival from down main or departure from platform 2 Set/Cleared
        lock_point(9)
    elif point_switched(9) and point_switched(8) and (signal_clear(7) or signal_clear(8)) :
        # departute from goods loop or platform 3 onto Down main set/cleared (no shunting onto down main)
        lock_point(9)
    else:
        unlock_point(9)

    # ----------------------------------------------------------------------
    # Point 10 (East box) - To Goods yard
    # ----------------------------------------------------------------------

    if signal_clear(16):
        # movement from goods yard set/cleared
        lock_point(10)
    elif not point_switched(6) and subsidary_clear(7):
        # shunting movement to goods yard set/cleared (no main route)
        lock_point(10)
    else:
        unlock_point(10)
        

    return()

#######################################################################################

