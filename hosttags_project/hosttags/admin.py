from hosttags.models import INCLUDE_HOST_OS_FIELDS,Host
from django.contrib import admin
import hostlists

class HostAdmin(admin.ModelAdmin):
  def save_model(self,request,obj,form,change):
    print 'Saving model',obj,request.REQUEST
    super(HostAdmin, self).save_model(request, obj, form, change)
    obj.save()
    tags=obj.tags.all()
    print 'tags',tags
    tag_names=[]
    tag_names=request.REQUEST['tags'].split(',')
    print 'tags2',tag_names
    hosts=hostlists.expand_item(hostlists.range_split(obj.name))
    if len(hosts) > 1:
      for hostname in hosts:
        host,created=Host.objects.get_or_create(name=hostname)
        host.save()
        if created:
          host.tags.set(*tag_names)
        else:
          for tag in tags_names:
            host.tags.add(tag)
        host.save()
      Host.objects.get(name=obj.name).delete()
    else:
      obj.save()
  list_display = ('name',)
  list_filter  = ('tags',)
  search_fields =['name']
  fieldsets    = [
                   (None,
                     {'fields': ('name','tags')}
                   )
                 ]
  if INCLUDE_HOST_OS_FIELDS:
    fieldsets.append(
                ('OS', {
                    'fields': ('os_kernel_name','os_kernel_release','os_kernel_version','os_machine','os_processor','os_hardware_platform','os_operating_system'),
                    'classes': ('collapse',),
                    'description':('Host OS sepecific parameters.  Currently these map to the varioius data returned by the Unix uname command.  These are frequently updated by external scripts and are not required fields'),
                }),)
admin.site.register(Host,HostAdmin)
