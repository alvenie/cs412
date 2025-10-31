# voter_analytics/views.py
# auther: Chonghao Chen (alvenie@bu.edu), 10/31/2025
# description: The views.py file specific to the voter analytics app

from django.views import generic
from .models import Voter
import datetime

class VoterListView(generic.ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """
        Overrides the default queryset to allow filtering.
        """
        # Start with all voters
        queryset = super().get_queryset().order_by('last_name', 'first_name')
        
        # Get filter parameters from the GET request
        party = self.request.GET.get('party', '')
        min_year = self.request.GET.get('min_dob_year', '')
        max_year = self.request.GET.get('max_dob_year', '')
        score = self.request.GET.get('score', '')
        
        # Apply filters if they exist
        if party:
            # Filter by the exact value, e.g., 'U '
            queryset = queryset.filter(party_affiliation=party)
        
        if min_year:
            queryset = queryset.filter(dob__year__gte=min_year)
            
        if max_year:
            queryset = queryset.filter(dob__year__lte=max_year)
            
        if score:
            queryset = queryset.filter(voter_score=score)
        
        # Handle election checkboxes
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Passes filter options and current filter values to the template.
        """
        context = super().get_context_data(**kwargs)
        
        # Get distinct party affiliations from the DB
        context['party_options'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        
        # Generate a range of scores (0-5)
        context['score_options'] = range(0, 6)
        
        # Generate a range of years for DOB filters (e.g., 18-100 years ago)
        current_year = datetime.date.today().year
        context['year_options'] = range(current_year - 17, current_year - 101, -1)
        
        # Pass the current GET parameters back to the template
        context['current_filters'] = self.request.GET
        
        return context

class VoterDetailView(generic.DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'