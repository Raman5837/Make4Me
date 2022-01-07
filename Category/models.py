from django.db import models
from PIL import Image
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
# Create your models here.

class Category(MPTTModel):
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    categoryName = models.CharField(max_length = 100, verbose_name='Category Name', unique = True)
    slug = models.SlugField(null = False, unique = True)
    description = models.TextField(blank = True)
    categoryImage = models.ImageField(upload_to = 'Images/CategoryImages/', blank = True)
    create_at = models.DateTimeField(auto_now_add = True, editable = False)
    update_at = models.DateTimeField(auto_now = True, editable = False)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
        
    class MPTTMeta:
        order_insertion_by = ['categoryName']
        
    def getUrl(self):
        return reverse('productByCategory', args = [self.slug])
    
    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.categoryName]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.categoryName)
            k = k.parent
        return ' / '.join(full_path[::-1])
    
    # def __str__(self):
    #     return self.categoryName
    
    def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)

	    img = Image.open(self.categoryImage.path)
	    if img.height > 600 or img.width > 600:
	    	output_size = (600, 600)
	    	img.thumbnail(output_size)
	    	img.save(self.categoryImage.path)