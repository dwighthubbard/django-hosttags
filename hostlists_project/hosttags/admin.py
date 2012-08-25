from hosttags.models import Host
from django.contrib import admin
import hostlists

class HostAdmin(admin.ModelAdmin):
  def save_model(self,request,obj,form,change):
    print obj.name
    hosts=hostlists.expand_item(hostlists.range_split(obj.name))
    for hostname in hosts:
      host,created=Host.objects.get_or_create(name=hostname)
      super(HostAdmin, self).save_model(request, obj, form, change)
      tags=obj.tags.all()
      tag_names=[]
      for tag in tags:
        print dir(tag)
        #tag_names.append(tag.name)
        host.tags.add(tag)
      #host.tags.set(*tag_names)
      host.save()
    if len(hosts) > 1:
      obj.group=True
      obj.save()
  list_display = ('name', 'group')
  list_filter  = ('name','group','tags')
  readonly_fields = ('group',)
          
admin.site.register(Host,HostAdmin)
