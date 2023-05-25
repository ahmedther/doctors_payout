from django.contrib import admin
from .models import *


admin.site.register(DoctorProfile)
admin.site.register(Transplant)
admin.site.register(Query)


# CHnage admin Panel
admin.site.site_header = "Doctor's Payout Automation Panel"
admin.site.site_title = "Doctor's Payout Admin Panel"
admin.site.index_title = "Doctor's Payout Administration"
