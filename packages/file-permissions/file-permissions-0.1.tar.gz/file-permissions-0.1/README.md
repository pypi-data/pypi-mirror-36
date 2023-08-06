# Permissions
`Permissions` provides a tiny wrapper on top of built-in Python's libraries 
to get information about file permissions in Unix systems.  

## Installation
```
pip install file-permissions
```

## Example
```python
from permissions import get_permissions_from

p = get_permissions_from('test.txt')  # returns PermissionsContainer object
p.executable()
# False
p.readable()
# True
```

## Reference
Available fields in PermissionsContainer:
1. executable - boolean, indicates whether file could be executed by current user or not; 
2. group - object(pwd.struct_group), contains information about group the file belongs to. Available fields there are:
   - gr_name
   - gr_passwd
   - gr_gid
   - gr_mem
3. is_sticky - boolean, inficates whether file has sticky bit or not.
4. owner - object(pwd.struct_passwd), contains information about user the file belongs to. Available fields there are: 
   - pw_name
   - pw_passwd
   - pw_uid
   - pw_gid
   - pw_gecos
   - pw_dir
   - pw_shell
5. readable - boolean, indicates whether file could be read by current user or not; 
6. sgid - returns SGID if set or 0;
7. suid - returns SUID if set or 0;
8. umask - str, file permissions as umask, e. g. 0755, 0400;
9. writable - boolean, indicates whether file could be written by current user or not;
