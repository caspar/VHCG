!pip3 install sqlalchemy # ORM for databases
!pip3 install ipython-sql # SQL magic function
%load_ext sql
%sql postgresql://sa4129:Welcome201@w4111project1part2db.cisxo09blonu.us-east-1.rds.amazonaws.com/proj1part2
%%sql ALTER ROLE sa4129
WITH PASSWORD 'Welcome201';