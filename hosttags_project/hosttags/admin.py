from hosttags.models import Host
from django.contrib import admin
import hostlists

class HostAdmin(admin.ModelAdmin):
  def save_model(self,request,obj,form,change):
    super(HostAdmin, self).save_model(request, obj, form, change)
    obj.save()
    tags=obj.tags.all()
    print tags
    hosts=hostlists.expand_item(hostlists.range_split(obj.name))
    if len(hosts) > 1:
      for hostname in hosts:
        host,created=Host.objects.get_or_create(name=hostname)
        #super(HostAdmin, self).save_model(request, obj, form, change)
        host.save()
        for tag in tags:
          dir(tag)
          host.tags.add(tag)
        #host.tags.set(*tag_names)
        host.save()
      #obj.save()
      Host.objects.get(name=obj.name).delete()
    else:
      obj.save()
    #  obj.delete()
  list_display = ('name',)
  list_filter  = ('name','tags')
admin.site.register(Host,HostAdmin)
