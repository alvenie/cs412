# voter_analytics/views.py
# auther: Chonghao Chen (alvenie@bu.edu), 10/31/2025
# description: The views.py file specific to the voter analytics app

from django.views import generic
from .models import Voter
import datetime

import plotly.express as px
import pandas as pd
from django.db.models import Count

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

class VoterGraphView(VoterListView): # Inherits from VoterListView
    """
    A view to display graphs based on filtered Voter data.
    Reuses all filtering and context logic from VoterListView.
    """
    template_name = 'voter_analytics/graphs.html'
    paginate_by = None # We don't paginate graphs

    def get_context_data(self, **kwargs):
        """
        Generates Plotly graphs from the filtered queryset.
        """
        # 1. Call the parent method
        # This runs get_queryset() and populates context with
        # filter options (party_options, etc.) and current_filters
        context = super().get_context_data(**kwargs)
        
        # 2. Get the filtered queryset
        # The parent ListView puts the filtered data in 'object_list'
        queryset = context['object_list'] 

        # --- Graph 1: Birth Year Histogram (Bar Chart) ---
        # Get a list of all birth years, excluding nulls
        dob_data = queryset.exclude(dob__isnull=True).values_list('dob__year', flat=True)
        
        # Use Pandas to easily count occurrences of each year
        df_dob = pd.DataFrame(dob_data, columns=['Year of Birth'])
        dob_counts = df_dob['Year of Birth'].value_counts().sort_index()

        fig1 = px.bar(
            x=dob_counts.index, 
            y=dob_counts.values,
            labels={'x': 'Year of Birth', 'y': 'Number of Voters'},
            title='Voters by Year of Birth'
        )
        # Convert graph to an HTML div
        context['graph1_div'] = fig1.to_html(full_html=False)

        # --- Graph 2: Party Affiliation Pie Chart ---
        # Use Django's .annotate() to count voters per party
        party_data = queryset.values('party_affiliation').annotate(count=Count('id')).order_by('party_affiliation')
        
        fig2 = px.pie(
            party_data, 
            names='party_affiliation', 
            values='count',
            title='Voters by Party Affiliation'
        )
        context['graph2_div'] = fig2.to_html(full_html=False)
        
        # --- Graph 3: Election Participation (Bar Chart) ---
        # We need to get 5 separate counts from the filtered queryset
        election_counts = {
            '2020 State': queryset.filter(v20state=True).count(),
            '2021 Town': queryset.filter(v21town=True).count(),
            '2021 Primary': queryset.filter(v21primary=True).count(),
            '2022 General': queryset.filter(v22general=True).count(),
            '2023 Town': queryset.filter(v23town=True).count(),
        }
        
        # Convert the dictionary to a DataFrame for Plotly
        df_elections = pd.DataFrame(list(election_counts.items()), columns=['Election', 'Voter Count'])
        
        fig3 = px.bar(
            df_elections, 
            x='Election', 
            y='Voter Count',
            title='Voter Participation by Election'
        )
        context['graph3_div'] = fig3.to_html(full_html=False)
        
        # 3. Return the final context
        return context    