from django.shortcuts import render

# Create your views here.
def test_view(request):
	# to start db: C:/PostgreSQL/10/bin/pg_ctl -D ^"C^:^\PostgreSQL^\data^" -l logfile start
	return render(request, 'stats_h.html', {'dict_item': 'test_item'})