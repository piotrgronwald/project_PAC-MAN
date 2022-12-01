from django.contrib import admin



class WebAppAdmin(admin.ModelAdmin):

   ordering = ['ranking']
   list_display = ['username', 'ranking']
   list_display_links = ['username', 'ranking']
   list_per_page = 20
   list_filter = ['username']
   search_fields = ['username']
   fieldsets = [
      (None, {'fields': ['username', 'ranking', 'created']}),
   ]
   readonly_fields = ['created']




