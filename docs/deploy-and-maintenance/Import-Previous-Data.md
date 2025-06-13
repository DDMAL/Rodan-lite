# Migrate

When you want to import old Rodan data, you will have to update the old databases to use the current models. Meaning, you will have to:

- Take down Rodan
- Run `git pull` to the same version you wish to import data into. 
- Run `python manage.py migrate` and fix all errors, hopefully without deleting anything.
- Once you Rodan working again, you can finally dump the database, and load it in the new rodan instance. 

# Backup and Restore

Bulk of Rodan data is held in a PostgreSQL database, meaning that backing up and restoring the container that houses this is quite important. While the exact details may change, the scripts that allow this to happen can be found in the `/postgres/maintenance` folder. 

Backups are saved on volumes specified by Dockerfiles and used for booting up and restoring the PostgreSQL containers. The `backup_db` and `restore_db` commands in the Makefile work and can be used as starting points for running more complex restoration operations.  
