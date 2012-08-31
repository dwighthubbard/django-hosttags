from django.db import models
from taggit.managers import TaggableManager
import hostlists
from django.contrib.admin.filterspecs import FilterSpec, RelatedFilterSpec
from django.contrib.admin.util import get_model_from_relation
from django.db.models import Count

# PRESETS, these allow specifying fields for the host objects
INCLUDE_HOST_OS_FIELDS=True

class Host(models.Model):
  """ 
  Basic host class
  This class can be extended to container a wide variety of host information
  """
  def __unicode__(self):
    return self.name
  # The host name, this should match the nodename from the uname -n command, 
  # the admin module runs the entered info through the hostlists
  # module and generates one or more host objects from the results.
  name= models.CharField(max_length=256,unique=True,help_text='This can be a single host or any host grouping supported by hostlists, example www[01-09].foo.com')
  # Tags, these are any tags assigned to the host.  These allow creating groups of hosts
  tags= TaggableManager(blank=True)
  if INCLUDE_HOST_OS_FIELDS:
      # Kernel name, this should match the output of uname -s
      os_kernel_name=models.CharField(max_length=256,blank=True)
      # this should match the output of uname -r
      os_kernel_release=models.CharField(max_length=128,blank=True)
      # this should match the output of uname -v
      os_kernel_version=models.CharField(max_length=128,blank=True)
      # this should match the output of uname -m
      os_machine=models.CharField(max_length=64,blank=True)
      # this should match the output of uname -p
      os_processor=models.CharField(max_length=64,blank=True)
      os_hardware_platform=models.CharField(max_length=64,blank=True)
      os_operating_system=models.CharField(max_length=64,blank=True)

class TaggitFilterSpec(RelatedFilterSpec):
    """
    A FilterSpec that can be used to filter by taggit tags in the admin.

    To use, simply import this module (for example in `models.py`), and add the
    name of your :class:`taggit.managers.TaggableManager` field in the
    :attr:`list_filter` attribute of your :class:`django.contrib.ModelAdmin`
    class.
    """

    def __init__(self, f, request, params, model, model_admin,
                 field_path=None):
        super(RelatedFilterSpec, self).__init__(
            f, request, params, model, model_admin, field_path=field_path)

        other_model = get_model_from_relation(f)
        if isinstance(f, (models.ManyToManyField,
                          models.related.RelatedObject)):
            # no direct field on this model, get name from other model
            self.lookup_title = other_model._meta.verbose_name
        else:
            self.lookup_title = f.verbose_name # use field name
        rel_name = other_model._meta.pk.name
        self.lookup_kwarg = '%s__%s__exact' % (self.field_path, rel_name)
        self.lookup_kwarg_isnull = '%s__isnull' % (self.field_path)
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        self.lookup_val_isnull = request.GET.get(
                                      self.lookup_kwarg_isnull, None)
        # Get tags and their count
        through_opts = f.through._meta
        count_field = ("%s_%s_items" % (through_opts.app_label,
                through_opts.object_name)).lower()
        queryset = getattr(f.model, f.name).all()
        queryset = queryset.annotate(num_times=Count(count_field))
        queryset = queryset.order_by("-num_times")
        self.lookup_choices = [(t.pk, "%s (%s)" % (t.name, t.num_times)) 
                for t in queryset]


# HACK: we insert the filter at the beginning of the list to avoid the manager
# to be associated with a RelatedFilterSpec
FilterSpec.filter_specs.insert(0, (lambda f: isinstance(f, TaggableManager),
    TaggitFilterSpec))
  