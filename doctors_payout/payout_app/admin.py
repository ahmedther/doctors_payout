from django.contrib import admin
from .models import *


class DoctorProfileAdmin(admin.ModelAdmin):
    search_fields = ['doctors_pr_number', 'doctors_name']

class TransplantAdmin(admin.ModelAdmin):
    search_fields = ['doctors_share', 'doctors_department']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        try:
            doctors = DoctorProfile.objects.filter(doctors_name__icontains=search_term)
            doctor_transplants = Transplant.objects.filter(doctors_name__in=doctors)
            queryset |= doctor_transplants
        except ValueError:
            pass

        return queryset, use_distinct
    
class QueryAdmin(admin.ModelAdmin):
    search_fields = ['query_name']


admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(Transplant,TransplantAdmin)
admin.site.register(Query,QueryAdmin)


# CHnage admin Panel
admin.site.site_header = "Doctor's Payout Automation Panel"
admin.site.site_title = "Doctor's Payout Admin Panel"
admin.site.index_title = "Doctor's Payout Administration"



