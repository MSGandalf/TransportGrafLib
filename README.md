# TransportGrafLib
Project for lyceum

main file - script.py

command:: 'help' in script.py returns:


legend: (X) - parameter, [X] - optional parameter
valid commands:
    USER COMMANDS -----------------------------
    help -> this page.
    list -> generously information about city.
    route (from) (to) [time = 0:0] [weight time = 1] [weight money = 0.001]
        -> makes route from (from) to (to).
    load (filename) -> load info from file.
    
    
    EDITOR COMMANDS:
    to edit file you need get access.
    !!! edit [password] -> getting access, if there is no password,
            don't enter password at all.
    and after getting access, you can do:
    
    save (filename) -> save info to file.
    start_log (filename) -> start logging in filename. All logs making by SQLite3,
            DB1 - routes:
                date, request, sfrom, sto, res.
            DB2 - full_log:
                date, request.
    deploy -> placing all stations at map like it can be in real.
    add_station / as (name)
    add_route / ar (station1) (station2) (transport) (type of time) (time) (type of wait) (wait) ->
        add route from station1 to station2 and back, at transport,
        !!! wait need and time needed write in [] and doesn't include spaces!: like 3 [35,3:00,15:00] or 1 [15]
        with time and it's type:
            types of time:                      time needed
        1 - standard (constant)         (constant time)
        2 - time with pike hours        (basic time) [time at peak = basic time * 2]
        
        wait time:
            types of wait:                      wait needed
        1 - standard (constant)         (constant time)
        2 - time with pike hours        (basic time) [time at peak = basic time * 2]
        3 - route with schedule         (one transport once at time) [from time = 0:00] [to time = 23:59]
                                # train, starting at 6 and routes to 21, every hour will be
                                     (wait type) = 3, (and wait need) = [60 6:00 19:00]
        
    add_single_route / asr (station1) (station2) (transport) (type of time) (time) (type of wait) (wait) ->
        like add_route, but route will be only one side (from station1 to station2)
    set_password (password now, if no password, don't enter anything) [password2, if empty - no password.] ->
                                                                                                set password2 as main.
    set_pos (name_station) (xpos) (ypos) -> set station position.
            
