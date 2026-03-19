# AtOffice Shell

AtOffice Shell is a combination of multiple modules: `PyFunny`, `todocli`, `chronoterm`
Each of them have their distinct commands, which can be accessed together in `atoffice-shell`

`AtOffice Shell` is a command shell made specifically for employees/team members. It is designed to fullfill their needs, like:
 - `pyfunny commands` can be used by them to be happy, or to refresh their mood when they might be sad.
 - `todocli commands` are a bunch of different commands that they can use to manage their time effectively.
 - `chronoterm commands` are used to do with everything relating to time, and timezones. It also has capanility to add alarms, and stopwatches.

 todocli- dates use isoformat for easy storage

 project.py- 
  - is_valid_timezone() --> return True if timezone exists.
  - format_current_time() --> return current time in a timezone as HH:MM.
  - parse_alarm_time() --> parses a time string and return ISO formatted datetime string. Raises ValueError if invalid.

 shell.py-
  - now() --> Show current local time.
  - time() --> Show the current local time in ASCII clock format.
  - world() --> Show current time in your favorite time zones.

## Execution:
`$ python main.py`

> This is a CS50P Final Project. 
> Made through Python, by **Akshaj Singhal**
