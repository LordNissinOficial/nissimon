import sys
from pstats import Stats

#0: calls
#1: tempo
my_stat = Stats('profile.prof', stream=sys.stdout)

my_stat.sort_stats(1)
my_stat.print_stats()
#print(help(my_stat.print_stats))